"""JSON-backed session learner for Ghost-Eye inference.

The learner stores consent-based labeled fingerprints as local JSON session
records and compares incoming fingerprints with a small weighted k-nearest-
neighbor pass. It intentionally avoids ML dependencies while the prototype
session format is still stabilizing.
"""

from __future__ import annotations

import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
from uuid import uuid4


Number = float
FingerprintVector = Dict[str, Number]


class GhostEyeSessionLearner:
    """Learn and infer labeled Ghost-Eye session fingerprints."""

    SUPPORTED_SESSION_LABELS = frozenset(
        {
            "empty_room",
            "one_person_zone_a",
            "one_person_zone_b",
            "walking_path",
            "door_open",
            "door_closed",
            "router_near",
            "router_far",
        }
    )

    DEFAULT_SESSION_LOG_DIR = (
        Path(__file__).resolve().parents[1] / "sessions" / "logs"
    )

    def __init__(
        self,
        session_log_dir: Optional[Path | str] = None,
        k_neighbors: int = 3,
    ) -> None:
        if k_neighbors < 1:
            raise ValueError("k_neighbors must be at least 1")

        self.session_log_dir = Path(
            session_log_dir if session_log_dir is not None else self.DEFAULT_SESSION_LOG_DIR
        )
        self.k_neighbors = k_neighbors
        self.session_log_dir.mkdir(parents=True, exist_ok=True)

    def save_labeled_fingerprint(
        self,
        label: str,
        fingerprint: Any,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Persist a labeled session fingerprint as a JSON record."""

        self._validate_label(label)
        vector = self._fingerprint_to_vector(fingerprint)
        if not vector:
            raise ValueError("fingerprint must contain at least one numeric value")

        created_at = timestamp if timestamp is not None else time.time()
        safe_session_id = session_id or self._new_session_id(label, created_at)
        record = {
            "session_id": safe_session_id,
            "label": label,
            "fingerprint": fingerprint,
            "created_at": created_at,
            "metadata": dict(metadata or {}),
        }

        destination = self.session_log_dir / f"{safe_session_id}.json"
        with destination.open("w", encoding="utf-8") as session_file:
            json.dump(record, session_file, indent=2, sort_keys=True)
            session_file.write("\n")

        return record

    def record_session(
        self,
        label: str,
        fingerprint: Any,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Alias for callers that think in terms of session records."""

        return self.save_labeled_fingerprint(
            label,
            fingerprint,
            metadata=metadata,
            session_id=session_id,
            timestamp=timestamp,
        )

    def load_labeled_sessions(self) -> List[Dict[str, Any]]:
        """Load valid labeled session records from the JSON session log."""

        sessions: List[Dict[str, Any]] = []
        for session_path in sorted(self.session_log_dir.glob("*.json")):
            try:
                with session_path.open("r", encoding="utf-8") as session_file:
                    record = json.load(session_file)
            except (OSError, json.JSONDecodeError):
                continue

            if not self._is_valid_session_record(record):
                continue

            sessions.append(record)

        return sessions

    def infer_session(self, fingerprint: Any, *, k_neighbors: Optional[int] = None) -> Dict[str, Any]:
        """Return nearest session matches and a learned label/confidence hint."""

        query_vector = self._fingerprint_to_vector(fingerprint)
        if not query_vector:
            return self._empty_inference_result()

        matches = self._nearest_matches(query_vector, k_neighbors or self.k_neighbors)
        if not matches:
            return self._empty_inference_result()

        label_scores: Dict[str, float] = defaultdict(float)
        total_score = 0.0
        for match in matches:
            score = float(match["similarity"])
            label_scores[str(match["label"])] += score
            total_score += score

        learned_label, learned_score = max(
            label_scores.items(),
            key=lambda label_score: (label_score[1], label_score[0]),
        )
        vote_confidence = learned_score / total_score if total_score else 0.0
        nearest_similarity = float(matches[0]["similarity"])

        return {
            "nearest_session_matches": matches,
            "learned_zone_hint": learned_label,
            "confidence_hint": round(vote_confidence * nearest_similarity, 4),
        }

    def learn_from_fingerprint(
        self, fingerprint: Any, *, k_neighbors: Optional[int] = None
    ) -> Dict[str, Any]:
        """Alias for callers that describe inference as learning from a scan."""

        return self.infer_session(fingerprint, k_neighbors=k_neighbors)

    def _nearest_matches(
        self, query_vector: FingerprintVector, k_neighbors: int
    ) -> List[Dict[str, Any]]:
        if k_neighbors < 1:
            raise ValueError("k_neighbors must be at least 1")

        matches: List[Dict[str, Any]] = []
        for session in self.load_labeled_sessions():
            session_vector = self._fingerprint_to_vector(session["fingerprint"])
            if not session_vector:
                continue

            distance = self._euclidean_distance(query_vector, session_vector)
            similarity = 1.0 / (1.0 + distance)
            matches.append(
                {
                    "session_id": session["session_id"],
                    "label": session["label"],
                    "distance": round(distance, 6),
                    "similarity": round(similarity, 6),
                    "created_at": session.get("created_at"),
                    "metadata": session.get("metadata", {}),
                }
            )

        matches.sort(
            key=lambda match: (
                float(match["distance"]),
                str(match["label"]),
                str(match["session_id"]),
            )
        )
        return matches[:k_neighbors]

    @classmethod
    def _fingerprint_to_vector(cls, fingerprint: Any) -> FingerprintVector:
        vector: FingerprintVector = {}
        for key, value in cls._iter_numeric_values(fingerprint):
            vector[key] = value
        return vector

    @classmethod
    def _iter_numeric_values(
        cls, value: Any, prefix: str = "fingerprint"
    ) -> Iterable[Tuple[str, Number]]:
        if cls._is_number(value):
            yield prefix, float(value)
            return

        if isinstance(value, Mapping):
            for key in sorted(value.keys(), key=str):
                child_prefix = f"{prefix}.{key}"
                yield from cls._iter_numeric_values(value[key], child_prefix)
            return

        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            for index, item in enumerate(value):
                child_prefix = f"{prefix}[{index}]"
                yield from cls._iter_numeric_values(item, child_prefix)

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    @staticmethod
    def _euclidean_distance(
        left_vector: FingerprintVector, right_vector: FingerprintVector
    ) -> float:
        keys = set(left_vector) | set(right_vector)
        if not keys:
            return math.inf

        squared_distance = 0.0
        for key in keys:
            delta = left_vector.get(key, 0.0) - right_vector.get(key, 0.0)
            squared_distance += delta * delta

        return math.sqrt(squared_distance)

    def _is_valid_session_record(self, record: Any) -> bool:
        if not isinstance(record, Mapping):
            return False

        label = record.get("label")
        if not isinstance(label, str) or label not in self.SUPPORTED_SESSION_LABELS:
            return False

        session_id = record.get("session_id")
        if not isinstance(session_id, str) or not session_id:
            return False

        return bool(self._fingerprint_to_vector(record.get("fingerprint")))

    @classmethod
    def _validate_label(cls, label: str) -> None:
        if label not in cls.SUPPORTED_SESSION_LABELS:
            supported = ", ".join(sorted(cls.SUPPORTED_SESSION_LABELS))
            raise ValueError(f"unsupported session label {label!r}; expected one of: {supported}")

    @staticmethod
    def _new_session_id(label: str, created_at: float) -> str:
        timestamp_ms = int(created_at * 1000)
        return f"{timestamp_ms}-{label}-{uuid4().hex[:8]}"

    @staticmethod
    def _empty_inference_result() -> Dict[str, Any]:
        return {
            "nearest_session_matches": [],
            "learned_zone_hint": None,
            "confidence_hint": 0.0,
        }
"""Session-level learning for baselines and room fingerprints."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Iterable, Mapping

from .adaptive_baseline import AdaptiveBaseline, BaselineSnapshot
from .room_fingerprint_mapper import RoomFingerprint
from ghost_eye.wifi.wifi_scan import WifiScan


@dataclass(frozen=True)
class LearnedSessionState:
    """Learned signal state accumulated during a sensing session."""

    baseline: BaselineSnapshot
    fingerprints: tuple[RoomFingerprint, ...]
    updated_at: float = field(default_factory=time)


class SessionLearner:
    """Learns baselines and optional labeled room fingerprints from scans."""

    def __init__(self, baseline: AdaptiveBaseline | None = None) -> None:
        self._baseline = baseline or AdaptiveBaseline()
        self._fingerprints: list[RoomFingerprint] = []

    def observe(self, scan: WifiScan) -> BaselineSnapshot:
        return self._baseline.update(
            {network.bssid.lower(): network.rssi_dbm for network in scan.networks}
        )

    def learn_fingerprint(
        self,
        label: str,
        scans: Iterable[WifiScan],
    ) -> RoomFingerprint:
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}
        for scan in scans:
            for network in scan.networks:
                key = network.bssid.lower()
                totals[key] = totals.get(key, 0.0) + network.rssi_dbm
                counts[key] = counts.get(key, 0) + 1

        fingerprint = RoomFingerprint(
            label=label,
            signals={key: totals[key] / counts[key] for key in totals},
        )
        self._fingerprints.append(fingerprint)
        return fingerprint

    def state(self) -> LearnedSessionState:
        return LearnedSessionState(
            baseline=self._baseline.snapshot(),
            fingerprints=tuple(self._fingerprints),
        )

    def load_fingerprints(self, fingerprints: Iterable[RoomFingerprint]) -> None:
        self._fingerprints = list(fingerprints)

    def load_baseline(self, values: Mapping[str, float]) -> None:
        self._baseline = AdaptiveBaseline()
        self._baseline.update(values)

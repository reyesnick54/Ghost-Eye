"""JSON-backed room fingerprint mapping for coarse WiFi-only zones."""

from __future__ import annotations

import json
import math
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional


NumberMap = Dict[str, float]


@dataclass(frozen=True)
class RoomFingerprint:
    """A saved RSSI fingerprint for a calibrated zone."""

    label: str
    signals: Mapping[str, float]


@dataclass(frozen=True)
class FingerprintMatch:
    """Best-match result for an observed RSSI vector."""

    label: str
    distance: float
    confidence: float


class RoomFingerprintMapper:
    """Create, load, and compare small JSON zone fingerprints."""

    DEFAULT_FINGERPRINT_DIR = Path(__file__).resolve().parents[1] / "sessions" / "fingerprints"

    def __init__(self, fingerprint_dir: Optional[Path | str] = None) -> None:
        self.fingerprint_dir = Path(fingerprint_dir or self.DEFAULT_FINGERPRINT_DIR)
        self.fingerprint_dir.mkdir(parents=True, exist_ok=True)

    def create_fingerprint(self, zone_name: str, observation: Mapping[str, Any]) -> Dict[str, Any]:
        zone = str(zone_name).strip()
        if not zone:
            raise ValueError("zone_name must not be empty")

        signals = _rssi_map(observation)
        fingerprint = {
            "zone": zone,
            "created_at": time.time(),
            "updated_at": time.time(),
            "sample_count": 1,
            "rssi_by_bssid": signals,
            "gateway_latency_ms": _read_float(observation, "gateway_latency_ms", 0.0),
            "jitter_ms": _read_float(observation, "jitter_ms", 0.0),
        }
        self._write_fingerprint(fingerprint)
        return fingerprint

    def estimate_zone(
        self,
        observation: Mapping[str, Any],
        saved_fingerprints: Optional[Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]] | str | Path] = None,
    ) -> Dict[str, Any]:
        fingerprints = self._load_fingerprints(saved_fingerprints)
        if not fingerprints:
            return {"zone": "unknown", "zone_scores": {}, "confidence_hint": "low"}

        current = _rssi_map(observation)
        zone_scores: Dict[str, float] = {}
        best_zone = "unknown"
        best_score = 0.0

        for fingerprint in fingerprints:
            zone = str(fingerprint.get("zone", "unknown"))
            score = self._weighted_similarity(observation, fingerprint, current)
            zone_scores[zone] = round(score, 2)
            if score > best_score:
                best_zone = zone
                best_score = score

        sorted_scores = sorted(zone_scores.values(), reverse=True)
        runner_up = sorted_scores[1] if len(sorted_scores) > 1 else 0.0
        margin = best_score - runner_up
        if best_score >= 0.78 and margin >= 0.10:
            hint = "high"
        elif best_score >= 0.55:
            hint = "medium"
        else:
            hint = "low"

        return {"zone": best_zone, "zone_scores": zone_scores, "confidence_hint": hint}

    def match(self, signals: Mapping[str, float]) -> FingerprintMatch | None:
        result = self.estimate_zone({"rssi_by_bssid": signals})
        scores = result["zone_scores"]
        if not scores:
            return None
        zone = str(result["zone"])
        confidence = float(scores.get(zone, 0.0))
        return FingerprintMatch(label=zone, distance=1.0 - confidence, confidence=confidence)

    def fingerprint_count(self) -> int:
        return len(list(self.fingerprint_dir.glob("*.json")))

    def _write_fingerprint(self, fingerprint: Mapping[str, Any]) -> Path:
        path = self.fingerprint_dir / f"{self._slug(str(fingerprint['zone']))}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(dict(fingerprint), handle, indent=2, sort_keys=True)
            handle.write("\n")
        return path

    def _load_fingerprints(
        self,
        source: Optional[Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]] | str | Path],
    ) -> list[Mapping[str, Any]]:
        if source is None:
            return [self._read_json(path) for path in sorted(self.fingerprint_dir.glob("*.json")) if path.is_file()]
        if isinstance(source, (str, Path)):
            path = Path(source)
            if path.is_dir():
                return [self._read_json(item) for item in sorted(path.glob("*.json")) if item.is_file()]
            if path.is_file():
                payload = self._read_json(path)
                if isinstance(payload, list):
                    return [item for item in payload if isinstance(item, Mapping)]
                if isinstance(payload, Mapping):
                    return self._fingerprints_from_mapping(payload)
            return []
        if isinstance(source, Mapping):
            return self._fingerprints_from_mapping(source)
        return [item for item in source if isinstance(item, Mapping)]

    def _fingerprints_from_mapping(self, value: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        if "zone" in value:
            return [value]
        fingerprints = []
        for zone, fingerprint in value.items():
            if isinstance(fingerprint, Mapping):
                copy = dict(fingerprint)
                copy.setdefault("zone", str(zone))
                fingerprints.append(copy)
        return fingerprints

    def _read_json(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @classmethod
    def _weighted_similarity(
        cls,
        observation: Mapping[str, Any],
        fingerprint: Mapping[str, Any],
        current: Mapping[str, float],
    ) -> float:
        rssi_similarity = cls._similarity(current, _rssi_map(fingerprint))
        latency_similarity = cls._metric_similarity(
            _read_float(observation, "gateway_latency_ms", 0.0),
            _read_float(fingerprint, "gateway_latency_ms", 0.0),
            scale=35.0,
        )
        jitter_similarity = cls._metric_similarity(
            _read_float(observation, "jitter_ms", 0.0),
            _read_float(fingerprint, "jitter_ms", 0.0),
            scale=12.0,
        )
        ap_visibility_similarity = cls._metric_similarity(
            float(len(current)),
            float(len(_rssi_map(fingerprint))),
            scale=5.0,
        )
        return (
            (rssi_similarity * 0.72)
            + (latency_similarity * 0.10)
            + (jitter_similarity * 0.08)
            + (ap_visibility_similarity * 0.10)
        )

    @staticmethod
    def _similarity(current: Mapping[str, float], fingerprint: Mapping[str, float]) -> float:
        keys = set(current) | set(fingerprint)
        if not keys:
            return 0.0
        squared = 0.0
        for key in keys:
            squared += (current.get(key, -100.0) - fingerprint.get(key, -100.0)) ** 2
        rms = math.sqrt(squared / len(keys))
        return max(0.0, min(1.0, 1.0 - rms / 28.0))

    @staticmethod
    def _metric_similarity(current: float, reference: float, scale: float) -> float:
        if scale <= 0.0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - abs(current - reference) / scale))

    @staticmethod
    def _slug(zone_name: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9_.-]+", "_", zone_name.strip()).strip("._-")
        return slug or "unknown"


def _rssi_map(observation: Mapping[str, Any]) -> NumberMap:
    if "rssi_by_bssid" in observation and isinstance(observation["rssi_by_bssid"], Mapping):
        return {str(key).lower(): float(value) for key, value in observation["rssi_by_bssid"].items()}
    if "rssi" in observation and isinstance(observation["rssi"], Mapping):
        return {str(key).lower(): float(value) for key, value in observation["rssi"].items()}
    aps = observation.get("visible_access_points") or observation.get("access_points") or []
    signals: NumberMap = {}
    if isinstance(aps, list):
        for ap in aps:
            if not isinstance(ap, Mapping):
                continue
            bssid = ap.get("bssid") or ap.get("id") or ap.get("ssid")
            rssi = ap.get("rssi", ap.get("rssi_dbm"))
            if bssid is not None and rssi is not None:
                signals[str(bssid).lower()] = float(rssi)
    return signals


def _read_float(source: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(source.get(key, default))
    except (TypeError, ValueError):
        return default


_DEFAULT_MAPPER = RoomFingerprintMapper()


def create_fingerprint(zone_name: str, observation: Mapping[str, Any]) -> Dict[str, Any]:
    return _DEFAULT_MAPPER.create_fingerprint(zone_name, observation)


def estimate_zone(
    observation: Mapping[str, Any],
    saved_fingerprints: Optional[Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]] | str | Path] = None,
) -> Dict[str, Any]:
    return _DEFAULT_MAPPER.estimate_zone(observation, saved_fingerprints)

"""Adaptive baseline management for Ghost-Eye inference.

The engine keeps a fixed static baseline and a separately persisted adaptive
baseline. The adaptive baseline is only refreshed from scans that are stable
enough to be useful as environmental reference data.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
from threading import RLock
from typing import Any


DEFAULT_BASELINE_DIR = Path(__file__).resolve().parents[1] / "sessions" / "baselines"
MOTION_SCORE_THRESHOLD = 0.15
SCAN_STABILITY_THRESHOLD = 0.70
PACKET_LOSS_THRESHOLD = 0.05


class AdaptiveBaselineEngine:
    """Maintain static and adaptive inference baselines.

    Parameters
    ----------
    session_id:
        Identifier used to choose the persisted baseline file.
    baseline_dir:
        Directory where baseline snapshots are stored. Defaults to
        ``ghost_eye/sessions/baselines/``.
    adaptation_rate:
        Blend factor used when an adaptive baseline already exists. The default
        of ``1.0`` replaces the adaptive baseline with the latest stable scan.
        Lower values apply an exponential moving average to numeric fields.
    """

    def __init__(
        self,
        session_id: str = "default",
        baseline_dir: str | Path | None = None,
        adaptation_rate: float = 1.0,
    ) -> None:
        if not 0.0 < adaptation_rate <= 1.0:
            raise ValueError("adaptation_rate must be greater than 0.0 and at most 1.0")

        self.session_id = self._safe_session_id(session_id)
        self.baseline_dir = Path(baseline_dir) if baseline_dir is not None else DEFAULT_BASELINE_DIR
        self.baseline_path = self.baseline_dir / f"{self.session_id}.json"
        self.adaptation_rate = float(adaptation_rate)
        self.static_baseline: dict[str, Any] | None = None
        self.adaptive_baseline: dict[str, Any] | None = None
        self.last_updated: str | None = None
        self._lock = RLock()

        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self._load()

    def update(
        self,
        scan: dict[str, Any],
        *,
        motion_score: float,
        scan_stability: float,
        packet_loss: float,
    ) -> dict[str, Any]:
        """Process a scan and return baseline metadata.

        The adaptive baseline changes only when all quality gates pass:
        ``motion_score < 0.15``, ``scan_stability > 0.70``, and
        ``packet_loss < 0.05``.
        """

        scan_payload = self._coerce_scan(scan)
        motion_score = self._coerce_metric("motion_score", motion_score)
        scan_stability = self._coerce_metric("scan_stability", scan_stability)
        packet_loss = self._coerce_metric("packet_loss", packet_loss)

        with self._lock:
            changed = False
            if self.static_baseline is None:
                self.static_baseline = deepcopy(scan_payload)
                changed = True

            if self._can_update(motion_score, scan_stability, packet_loss):
                if self.adaptive_baseline is None or self.adaptation_rate == 1.0:
                    self.adaptive_baseline = deepcopy(scan_payload)
                else:
                    self.adaptive_baseline = self._blend_baselines(
                        self.adaptive_baseline,
                        scan_payload,
                        self.adaptation_rate,
                    )
                self.last_updated = self._utc_now()
                baseline_status = "updated"
                changed = True
            else:
                baseline_status = "held"

            if changed:
                self._save()

            return {
                "baseline_status": baseline_status,
                "drift_score": self.drift_score(),
                "last_updated": self.last_updated,
            }

    def update_baseline(
        self,
        scan: dict[str, Any],
        *,
        motion_score: float,
        scan_stability: float,
        packet_loss: float,
    ) -> dict[str, Any]:
        """Alias for callers that use an explicit baseline verb."""

        return self.update(
            scan,
            motion_score=motion_score,
            scan_stability=scan_stability,
            packet_loss=packet_loss,
        )

    def process_scan(
        self,
        scan: dict[str, Any],
        *,
        motion_score: float,
        scan_stability: float,
        packet_loss: float,
    ) -> dict[str, Any]:
        """Alias for scan-oriented inference pipelines."""

        return self.update(
            scan,
            motion_score=motion_score,
            scan_stability=scan_stability,
            packet_loss=packet_loss,
        )

    def drift_score(self) -> float:
        """Return normalized drift between static and adaptive baselines."""

        if self.static_baseline is None or self.adaptive_baseline is None:
            return 0.0
        return self._calculate_drift(self.static_baseline, self.adaptive_baseline)

    @classmethod
    def _can_update(cls, motion_score: float, scan_stability: float, packet_loss: float) -> bool:
        return (
            motion_score < MOTION_SCORE_THRESHOLD
            and scan_stability > SCAN_STABILITY_THRESHOLD
            and packet_loss < PACKET_LOSS_THRESHOLD
        )

    @staticmethod
    def _safe_session_id(session_id: str) -> str:
        safe_id = re.sub(r"[^a-zA-Z0-9_.-]+", "_", str(session_id)).strip("._")
        return safe_id or "default"

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _coerce_metric(name: str, value: float) -> float:
        try:
            metric = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} must be numeric") from exc
        if not math.isfinite(metric):
            raise ValueError(f"{name} must be finite")
        return metric

    @classmethod
    def _coerce_scan(cls, scan: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(scan, dict):
            raise ValueError("scan must be a dictionary")
        return cls._json_safe(scan)

    @classmethod
    def _json_safe(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): cls._json_safe(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [cls._json_safe(item) for item in value]
        if hasattr(value, "tolist"):
            return cls._json_safe(value.tolist())
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    def _load(self) -> None:
        if not self.baseline_path.exists():
            return

        with self.baseline_path.open("r", encoding="utf-8") as baseline_file:
            payload = json.load(baseline_file)

        static_baseline = payload.get("static_baseline")
        adaptive_baseline = payload.get("adaptive_baseline")
        self.static_baseline = deepcopy(static_baseline) if isinstance(static_baseline, dict) else None
        self.adaptive_baseline = deepcopy(adaptive_baseline) if isinstance(adaptive_baseline, dict) else None
        self.last_updated = payload.get("last_updated")

    def _save(self) -> None:
        payload = {
            "session_id": self.session_id,
            "static_baseline": self.static_baseline,
            "adaptive_baseline": self.adaptive_baseline,
            "last_updated": self.last_updated,
        }

        temporary_path = self.baseline_path.with_suffix(f"{self.baseline_path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8") as baseline_file:
            json.dump(payload, baseline_file, indent=2, sort_keys=True)
            baseline_file.write("\n")
        temporary_path.replace(self.baseline_path)

    @classmethod
    def _calculate_drift(cls, left: dict[str, Any], right: dict[str, Any]) -> float:
        left_values = cls._numeric_features(left)
        right_values = cls._numeric_features(right)
        shared_keys = sorted(set(left_values) & set(right_values))
        if not shared_keys:
            return 0.0

        squared_delta_total = 0.0
        squared_reference_total = 0.0
        for key in shared_keys:
            left_value = left_values[key]
            right_value = right_values[key]
            squared_delta_total += (right_value - left_value) ** 2
            squared_reference_total += left_value**2

        rms_delta = math.sqrt(squared_delta_total / len(shared_keys))
        rms_reference = math.sqrt(squared_reference_total / len(shared_keys))
        if rms_reference == 0.0:
            drift = rms_delta
        else:
            drift = rms_delta / rms_reference
        return round(max(0.0, min(drift, 1.0)), 6)

    @classmethod
    def _numeric_features(cls, value: Any, prefix: str = "") -> dict[str, float]:
        features: dict[str, float] = {}
        if isinstance(value, dict):
            for key in sorted(value):
                child_prefix = f"{prefix}.{key}" if prefix else str(key)
                features.update(cls._numeric_features(value[key], child_prefix))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                child_prefix = f"{prefix}[{index}]"
                features.update(cls._numeric_features(item, child_prefix))
        elif isinstance(value, bool):
            return features
        elif isinstance(value, (int, float)) and math.isfinite(float(value)):
            features[prefix] = float(value)
        return features

    @classmethod
    def _blend_baselines(
        cls,
        current: dict[str, Any],
        incoming: dict[str, Any],
        adaptation_rate: float,
    ) -> dict[str, Any]:
        return cls._blend_value(current, incoming, adaptation_rate)

    @classmethod
    def _blend_value(cls, current: Any, incoming: Any, adaptation_rate: float) -> Any:
        if isinstance(current, dict) and isinstance(incoming, dict):
            merged: dict[str, Any] = {}
            for key in sorted(set(current) | set(incoming)):
                if key in current and key in incoming:
                    merged[key] = cls._blend_value(current[key], incoming[key], adaptation_rate)
                elif key in incoming:
                    merged[key] = deepcopy(incoming[key])
                else:
                    merged[key] = deepcopy(current[key])
            return merged

        if isinstance(current, list) and isinstance(incoming, list) and len(current) == len(incoming):
            return [
                cls._blend_value(current_item, incoming_item, adaptation_rate)
                for current_item, incoming_item in zip(current, incoming)
            ]

        if (
            isinstance(current, (int, float))
            and not isinstance(current, bool)
            and isinstance(incoming, (int, float))
            and not isinstance(incoming, bool)
        ):
            return (1.0 - adaptation_rate) * float(current) + adaptation_rate * float(incoming)

        return deepcopy(incoming)

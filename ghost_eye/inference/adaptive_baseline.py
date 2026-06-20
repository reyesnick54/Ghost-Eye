"""Adaptive baseline management for GhostEye WiFi-only sensing."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
from time import time
from typing import Any, Mapping


DEFAULT_BASELINE_DIR = Path(__file__).resolve().parents[1] / "sessions" / "baselines"
MOTION_SCORE_THRESHOLD = 0.15
SCAN_STABILITY_THRESHOLD = 0.70
PACKET_LOSS_THRESHOLD = 0.05


@dataclass(frozen=True)
class BaselineSnapshot:
    """Current expected RSSI values for known access points."""

    values: Mapping[str, float]
    observations: Mapping[str, int]
    timestamp: float = field(default_factory=time)


class AdaptiveBaseline:
    """In-memory exponential moving average baseline per BSSID."""

    def __init__(self, alpha: float = 0.15) -> None:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be within (0.0, 1.0]")
        self.alpha = alpha
        self._values: dict[str, float] = {}
        self._observations: dict[str, int] = {}

    def update(self, signals: Mapping[str, float]) -> BaselineSnapshot:
        for bssid, rssi_dbm in signals.items():
            key = bssid.lower()
            if key in self._values:
                self._values[key] = (self.alpha * rssi_dbm) + ((1.0 - self.alpha) * self._values[key])
            else:
                self._values[key] = rssi_dbm
            self._observations[key] = self._observations.get(key, 0) + 1
        return self.snapshot()

    def residuals(self, signals: Mapping[str, float]) -> dict[str, float]:
        return {bssid.lower(): rssi_dbm - self._values.get(bssid.lower(), rssi_dbm) for bssid, rssi_dbm in signals.items()}

    def snapshot(self) -> BaselineSnapshot:
        return BaselineSnapshot(values=dict(self._values), observations=dict(self._observations))


class AdaptiveBaselineEngine:
    """Persist static and adaptive JSON baselines for one session."""

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
        scan_payload = self._json_safe(scan)
        changed = False
        if self.static_baseline is None:
            self.static_baseline = deepcopy(scan_payload)
            changed = True

        if self._can_update(float(motion_score), float(scan_stability), float(packet_loss)):
            if self.adaptive_baseline is None or self.adaptation_rate == 1.0:
                self.adaptive_baseline = deepcopy(scan_payload)
            else:
                self.adaptive_baseline = self._blend_value(self.adaptive_baseline, scan_payload, self.adaptation_rate)
            self.last_updated = self._utc_now()
            status = "updated"
            changed = True
        else:
            status = "held"

        if changed:
            self._save()

        return {
            "baseline_status": status,
            "drift_score": self.drift_score(),
            "last_updated": self.last_updated,
        }

    def update_baseline(self, scan: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return self.update(scan, **kwargs)

    def process_scan(self, scan: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return self.update(scan, **kwargs)

    def drift_score(self) -> float:
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

    @classmethod
    def _json_safe(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): cls._json_safe(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [cls._json_safe(item) for item in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    def _load(self) -> None:
        if not self.baseline_path.exists():
            return
        with self.baseline_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.static_baseline = deepcopy(payload.get("static_baseline")) if isinstance(payload.get("static_baseline"), dict) else None
        self.adaptive_baseline = deepcopy(payload.get("adaptive_baseline")) if isinstance(payload.get("adaptive_baseline"), dict) else None
        self.last_updated = payload.get("last_updated")

    def _save(self) -> None:
        payload = {
            "session_id": self.session_id,
            "static_baseline": self.static_baseline,
            "adaptive_baseline": self.adaptive_baseline,
            "last_updated": self.last_updated,
        }
        temporary_path = self.baseline_path.with_suffix(f"{self.baseline_path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
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
        drift = rms_delta if rms_reference == 0.0 else rms_delta / rms_reference
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
                features.update(cls._numeric_features(item, f"{prefix}[{index}]"))
        elif isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)):
            features[prefix] = float(value)
        return features

    @classmethod
    def _blend_value(cls, current: Any, incoming: Any, rate: float) -> Any:
        if isinstance(current, dict) and isinstance(incoming, dict):
            return {
                key: cls._blend_value(current.get(key), incoming.get(key), rate)
                for key in sorted(set(current) | set(incoming))
            }
        if isinstance(current, list) and isinstance(incoming, list) and len(current) == len(incoming):
            return [cls._blend_value(left, right, rate) for left, right in zip(current, incoming)]
        if isinstance(current, (int, float)) and isinstance(incoming, (int, float)) and not isinstance(current, bool) and not isinstance(incoming, bool):
            return (1.0 - rate) * float(current) + rate * float(incoming)
        return deepcopy(incoming if incoming is not None else current)

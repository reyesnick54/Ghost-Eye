"""Coarse WiFi-only disturbance estimation."""

from __future__ import annotations

import statistics
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class DisturbanceFieldResult:
    """Presence and motion estimate from RSSI/latency disturbance."""

    motion_score: float
    presence: str
    mean_rssi_delta_db: float
    max_rssi_delta_db: float
    changed_access_points: list[str]
    explanation_features: Dict[str, Any]

    @property
    def presence_state(self) -> str:
        return self.presence

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DisturbanceFieldDetector:
    """Compare the current observation with an optional empty-room baseline."""

    def detect(
        self,
        current_observation: Any,
        empty_room_baseline: Optional[Mapping[str, Any]] = None,
        adaptive_baseline: Optional[Mapping[str, Any]] = None,
    ) -> DisturbanceFieldResult:
        current_rssi = _rssi_map(current_observation)
        baseline = adaptive_baseline or empty_room_baseline or {}
        baseline_rssi = _rssi_map(baseline) or _rssi_map(baseline.get("observation")) if isinstance(baseline, Mapping) else {}
        if isinstance(baseline, Mapping) and not baseline_rssi:
            baseline_rssi = {
                str(key).lower(): float(value)
                for key, value in dict(baseline.get("rssi_by_bssid", {})).items()
            }

        deltas = []
        changed = []
        for bssid, rssi in current_rssi.items():
            if bssid not in baseline_rssi:
                continue
            delta = abs(rssi - baseline_rssi[bssid])
            deltas.append(delta)
            if delta >= 3.5:
                changed.append(bssid)

        if deltas:
            mean_delta = statistics.fmean(deltas)
            max_delta = max(deltas)
            rssi_score = min(1.0, (mean_delta / 10.0) * 0.72 + (max_delta / 18.0) * 0.28)
        else:
            rssi_std = _read_float(current_observation, "rssi_std", 0.0)
            mean_delta = 0.0
            max_delta = 0.0
            rssi_score = min(0.75, 0.18 + rssi_std / 24.0)

        latency_score = min(1.0, max(_read_float(current_observation, "gateway_latency_ms", 0.0) - 8.0, 0.0) / 35.0)
        jitter_score = min(1.0, _read_float(current_observation, "jitter_ms", 0.0) / 12.0)
        loss_score = min(1.0, _read_float(current_observation, "packet_loss", 0.0) * 12.0)
        motion_score = round(
            min(1.0, (rssi_score * 0.64) + (latency_score * 0.16) + (jitter_score * 0.14) + (loss_score * 0.06)),
            2,
        )

        if motion_score >= 0.70:
            presence = "presence_detected"
        elif motion_score >= 0.35:
            presence = "possible_presence"
        else:
            presence = "clear"

        return DisturbanceFieldResult(
            motion_score=motion_score,
            presence=presence,
            mean_rssi_delta_db=round(mean_delta, 2),
            max_rssi_delta_db=round(max_delta, 2),
            changed_access_points=changed,
            explanation_features={
                "baseline_available": bool(baseline_rssi),
                "rssi_score": round(rssi_score, 3),
                "latency_score": round(latency_score, 3),
                "jitter_score": round(jitter_score, 3),
                "packet_loss_score": round(loss_score, 3),
            },
        )

    __call__ = detect


def _rssi_map(observation: Any) -> Dict[str, float]:
    if observation is None:
        return {}
    if hasattr(observation, "rssi_by_bssid"):
        return dict(observation.rssi_by_bssid)
    if isinstance(observation, Mapping):
        if "rssi_by_bssid" in observation and isinstance(observation["rssi_by_bssid"], Mapping):
            return {str(key).lower(): float(value) for key, value in observation["rssi_by_bssid"].items()}
        for ap_key in ("visible_access_points", "access_points", "aps", "networks"):
            aps = observation.get(ap_key)
            if isinstance(aps, list):
                return _rssi_from_ap_list(aps)
        if "rssi" in observation and isinstance(observation["rssi"], Mapping):
            return {str(key).lower(): float(value) for key, value in observation["rssi"].items()}
    return {}


def _rssi_from_ap_list(aps: list[Any]) -> Dict[str, float]:
    rssi: Dict[str, float] = {}
    for ap in aps:
        if not isinstance(ap, Mapping):
            continue
        bssid = ap.get("bssid") or ap.get("id") or ap.get("ssid")
        value = ap.get("rssi", ap.get("rssi_dbm"))
        if bssid is None or value is None:
            continue
        rssi[str(bssid).lower()] = float(value)
    return rssi


def _read_float(source: Any, name: str, default: float) -> float:
    if isinstance(source, Mapping):
        value = source.get(name, default)
    else:
        value = getattr(source, name, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

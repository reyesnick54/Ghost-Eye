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


@dataclass(frozen=True)
class DisturbanceField:
    """Compatibility field used by the higher-level presence helpers."""

    magnitude: float
    affected_access_points: int
    features: Dict[str, Any]


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

        baseline_available = bool(baseline_rssi) or bool(baseline)
        latency_delta = _metric_delta(current_observation, baseline, "gateway_latency_ms")
        jitter_delta = _metric_delta(current_observation, baseline, "jitter_ms")
        loss_delta = _metric_delta(current_observation, baseline, "packet_loss")
        ap_visibility_delta = _metric_delta(current_observation, baseline, "bssid_count", "visible_access_points")

        if baseline_available:
            latency_score = min(1.0, abs(latency_delta) / 28.0)
            jitter_score = min(1.0, abs(jitter_delta) / 9.0)
            loss_score = min(1.0, abs(loss_delta) / 0.06)
            ap_visibility_score = min(
                1.0,
                abs(ap_visibility_delta)
                / max(
                    _read_float(current_observation, "bssid_count", 1.0),
                    _metric_value(baseline, "bssid_count", "visible_access_points", default=1.0),
                    1.0,
                ),
            )
        else:
            latency_score = min(1.0, max(_read_float(current_observation, "gateway_latency_ms", 0.0) - 8.0, 0.0) / 35.0)
            jitter_score = min(1.0, _read_float(current_observation, "jitter_ms", 0.0) / 12.0)
            loss_score = min(1.0, _read_float(current_observation, "packet_loss", 0.0) * 12.0)
            ap_visibility_score = 0.0

        motion_score = round(
            min(
                1.0,
                (rssi_score * 0.58)
                + (latency_score * 0.15)
                + (jitter_score * 0.13)
                + (loss_score * 0.07)
                + (ap_visibility_score * 0.07),
            ),
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
                "baseline_available": baseline_available,
                "rssi_score": round(rssi_score, 3),
                "latency_score": round(latency_score, 3),
                "jitter_score": round(jitter_score, 3),
                "packet_loss_score": round(loss_score, 3),
                "ap_visibility_score": round(ap_visibility_score, 3),
                "latency_delta_ms": round(latency_delta, 2),
                "jitter_delta_ms": round(jitter_delta, 2),
                "packet_loss_delta": round(loss_delta, 4),
                "ap_visibility_delta": round(ap_visibility_delta, 2),
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


def _metric_delta(current: Any, baseline: Any, current_name: str, baseline_name: str | None = None) -> float:
    baseline_name = baseline_name or current_name
    current_value = _read_float(current, current_name, 0.0)
    baseline_value = _metric_value(baseline, current_name, baseline_name, default=current_value)
    return current_value - baseline_value


def _metric_value(source: Any, current_name: str, baseline_name: str, default: float) -> float:
    if not isinstance(source, Mapping):
        return _read_float(source, baseline_name, default)

    for container_name in ("observation", "signal_quality", "quality"):
        nested = source.get(container_name)
        if isinstance(nested, Mapping):
            value = _first_float(nested, (current_name, baseline_name))
            if value is not None:
                return value

    value = _first_float(source, (current_name, baseline_name))
    return default if value is None else value


def _first_float(source: Mapping[str, Any], names: tuple[str, str]) -> Optional[float]:
    for name in names:
        if name in source:
            try:
                return float(source[name])
            except (TypeError, ValueError):
                continue
    return None

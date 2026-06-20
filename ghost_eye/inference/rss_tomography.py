"""Coarse RSSI heatmap projection for WiFi-only non-CSI mode."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


DEFAULT_ZONES = ("zone_a", "zone_b", "zone_c")


@dataclass(frozen=True)
class RSSITomographyResult:
    """Coarse probabilistic zone map."""

    most_likely_zone: Optional[str]
    heatmap: Dict[str, float]
    confidence_hint: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "most_likely_zone": self.most_likely_zone,
            "heatmap": dict(self.heatmap),
            "confidence_hint": self.confidence_hint,
        }


class OpportunisticRSSITomography:
    """Produce a simple per-zone map from RSSI disturbance and fingerprints."""

    def project(
        self,
        observation: Mapping[str, Any],
        baseline: Optional[Mapping[str, Any]],
        fingerprint_scores: Optional[Mapping[str, float]],
        motion_score: float,
    ) -> Dict[str, float]:
        base_map = self._default_map(observation, motion_score)
        for zone, score in (fingerprint_scores or {}).items():
            if zone in base_map:
                base_map[zone] = max(base_map[zone], float(score))
        return self._normalizeish(base_map)

    def infer(
        self,
        current_observation: Mapping[str, Any],
        baseline_observation: Optional[Mapping[str, Any]],
        saved_zone_fingerprints: Mapping[str, Mapping[str, Any]],
    ) -> RSSITomographyResult:
        motion_score = _motion_hint(current_observation, baseline_observation)
        heatmap = self.project(current_observation, baseline_observation, {}, motion_score)
        zone = max(heatmap, key=heatmap.get) if heatmap else None
        return RSSITomographyResult(zone, heatmap, "low" if not saved_zone_fingerprints else "medium")

    def infer_dict(
        self,
        current_observation: Mapping[str, Any],
        baseline_observation: Optional[Mapping[str, Any]],
        saved_zone_fingerprints: Mapping[str, Mapping[str, Any]],
    ) -> Dict[str, Any]:
        return self.infer(current_observation, baseline_observation, saved_zone_fingerprints).as_dict()

    __call__ = infer

    def _default_map(self, observation: Mapping[str, Any], motion_score: float) -> Dict[str, float]:
        mean_rssi = _read_float(observation, "mean_rssi", -60.0)
        jitter_ms = _read_float(observation, "jitter_ms", 0.0)
        latency_ms = _read_float(observation, "gateway_latency_ms", 0.0)

        wave = (math.sin(abs(mean_rssi) / 8.0) + 1.0) / 2.0
        return {
            "zone_a": round(max(0.05, (motion_score * 0.45) + (1.0 - wave) * 0.22), 2),
            "zone_b": round(max(0.05, motion_score + min(jitter_ms / 18.0, 0.18)), 2),
            "zone_c": round(max(0.05, (motion_score * 0.55) + min(latency_ms / 90.0, 0.22) + wave * 0.10), 2),
        }

    @staticmethod
    def _normalizeish(zone_map: Mapping[str, float]) -> Dict[str, float]:
        normalized = {zone: round(max(0.0, min(1.0, float(zone_map.get(zone, 0.0)))), 2) for zone in DEFAULT_ZONES}
        if all(value == 0.0 for value in normalized.values()):
            return {"zone_a": 0.05, "zone_b": 0.05, "zone_c": 0.05}
        return normalized


RssTomography = OpportunisticRSSITomography


def _motion_hint(current: Mapping[str, Any], baseline: Optional[Mapping[str, Any]]) -> float:
    if not baseline:
        return 0.35
    current_rssi = _rssi_map(current)
    baseline_rssi = _rssi_map(baseline)
    common = current_rssi.keys() & baseline_rssi.keys()
    if not common:
        return 0.35
    delta = sum(abs(current_rssi[key] - baseline_rssi[key]) for key in common) / len(common)
    return max(0.0, min(1.0, delta / 12.0))


def _rssi_map(observation: Mapping[str, Any]) -> Dict[str, float]:
    if "rssi_by_bssid" in observation and isinstance(observation["rssi_by_bssid"], Mapping):
        return {str(key).lower(): float(value) for key, value in observation["rssi_by_bssid"].items()}
    aps = observation.get("visible_access_points") or observation.get("access_points") or []
    result: Dict[str, float] = {}
    if isinstance(aps, list):
        for ap in aps:
            if isinstance(ap, Mapping) and ap.get("bssid") is not None and ap.get("rssi") is not None:
                result[str(ap["bssid"]).lower()] = float(ap["rssi"])
    return result


def _read_float(source: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(source.get(key, default))
    except (TypeError, ValueError):
        return default

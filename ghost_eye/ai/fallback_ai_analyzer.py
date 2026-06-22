"""Deterministic fallback analyzer used when optional S3M runtime is unavailable."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ghost_eye.ai.ai_analysis_schema import (
    AIAnalysisResult,
    SAFE_LIMITATION_NOTICE,
    clamp_confidence,
)
from ghost_eye.ai.telemetry_prompt_builder import build_telemetry_prompt


class FallbackAIAnalyzer:
    """Local rules-based analyzer for GhostEye telemetry summaries."""

    provider_name = "fallback"
    model_name = "ghosteye-live-wifi-rules-v03"

    def analyze(
        self,
        telemetry: Mapping[str, Any],
        prompt: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> AIAnalysisResult:
        """Return an advisory analysis result without external model calls."""

        prompt = prompt or build_telemetry_prompt(telemetry)
        presence = str(telemetry.get("presence") or "unknown")
        zone = str(telemetry.get("zone") or "unknown")
        motion_score = _as_float(telemetry.get("motion_score"), default=0.0)
        confidence = clamp_confidence(telemetry.get("confidence"), default=0.0)
        confidence_ceiling = min(0.65, clamp_confidence(telemetry.get("confidence_ceiling"), default=0.65))
        source_type = self._source_type(telemetry)
        signal_quality = telemetry.get("signal_quality") if isinstance(telemetry.get("signal_quality"), Mapping) else {}
        zone_map = telemetry.get("map") if isinstance(telemetry.get("map"), Mapping) else {}
        baseline = telemetry.get("baseline") if isinstance(telemetry.get("baseline"), Mapping) else {}
        fingerprint_count = _as_int(_read_path(telemetry, ("fingerprints", "count")), default=0)

        risks = self._false_positive_risks(signal_quality, baseline, fingerprint_count)
        if source_type == "simulated":
            risks.append("simulated_source_not_live_wifi")
        observations = [
            self._source_observation(source_type, telemetry),
            f"Motion score {motion_score:.2f} maps to {presence}.",
            self._zone_observation(zone, zone_map),
            f"Confidence is capped at {confidence_ceiling:.2f} for WiFi-only non-CSI telemetry.",
        ]
        if self._quality_is_weak(signal_quality):
            observations.append("Signal quality is weak or degraded; interpretation should be conservative.")

        next_action = self._recommend_next_action(baseline, fingerprint_count, signal_quality)
        summary = self._summary(presence, motion_score, zone, confidence, source_type)
        explanation = (
            f"Analyzer confidence remains {confidence:.2f}, no higher than telemetry confidence "
            f"and the {confidence_ceiling:.2f} non-CSI ceiling. The result is probabilistic and "
            "does not identify an exact person, object, or location."
        )

        result_metadata: dict[str, Any] = {
            "prompt_chars": len(prompt),
            "confidence_capped_to_telemetry": True,
            "baseline_available": self._baseline_available(baseline),
            "fingerprint_count": fingerprint_count,
        }
        if metadata:
            result_metadata.update(dict(metadata))

        return AIAnalysisResult(
            available=True,
            provider=self.provider_name,
            model=self.model_name,
            summary=summary,
            confidence=confidence,
            confidence_explanation=explanation,
            false_positive_risks=tuple(risks),
            recommended_next_action=next_action,
            observations=tuple(observations),
            recommendations=(next_action,),
            limitations=(
                SAFE_LIMITATION_NOTICE,
                "WiFi-only non-CSI mode provides coarse probabilistic estimates only.",
                "No exact person/object location or validated through-wall tracking is claimed.",
            ),
            metadata=result_metadata,
        )

    __call__ = analyze

    @staticmethod
    def _summary(presence: str, motion_score: float, zone: str, confidence: float, source_type: str) -> str:
        if source_type == "live":
            source_prefix = "Live WiFi telemetry"
        elif source_type == "simulated":
            source_prefix = "Simulated WiFi telemetry"
        else:
            source_prefix = "Telemetry"
        zone_text = "an unknown zone" if zone == "unknown" else f"coarse {zone}"
        if presence == "clear":
            return f"{source_prefix} is currently consistent with a clear environment at confidence {confidence:.2f}."
        if presence == "unstable_scan":
            return f"{source_prefix} is unstable; signal quality should be improved before interpreting movement."
        return (
            f"{source_prefix} shows {presence.replace('_', ' ')} with motion score {motion_score:.2f}; "
            f"the strongest coarse map response is {zone_text}."
        )

    @staticmethod
    def _source_type(telemetry: Mapping[str, Any]) -> str:
        source = str(telemetry.get("source") or "").lower()
        if source.endswith("_live") or "live" in source:
            return "live"
        return "simulated" if "simulated" in source else "unknown"

    @staticmethod
    def _source_observation(source_type: str, telemetry: Mapping[str, Any]) -> str:
        source = str(telemetry.get("source") or "unknown")
        if source_type == "live":
            return f"Source is live local WiFi RSSI plus gateway latency ({source})."
        if source_type == "simulated":
            live_error = telemetry.get("live_error")
            if live_error:
                return f"Source is simulated fallback because live WiFi was unavailable: {live_error}."
            return f"Source is simulated WiFi RSSI plus gateway latency ({source})."
        return f"Source is {source}; interpretation remains bounded to WiFi-only non-CSI telemetry."

    @staticmethod
    def _zone_observation(zone: str, zone_map: Mapping[str, Any]) -> str:
        if zone == "unknown" or not zone_map:
            return "No calibrated zone is strong enough for a reliable coarse zone estimate."
        score = _as_float(zone_map.get(zone), default=0.0)
        return f"Likely coarse zone is {zone} with map score {score:.2f}; this is not an exact location."

    @classmethod
    def _false_positive_risks(
        cls,
        signal_quality: Mapping[str, Any],
        baseline: Mapping[str, Any],
        fingerprint_count: int,
    ) -> list[str]:
        risks: list[str] = []
        if not cls._baseline_available(baseline):
            risks.append("missing_empty_room_baseline")
        if fingerprint_count <= 0:
            risks.append("missing_zone_fingerprints")
        if _as_float(signal_quality.get("packet_loss"), default=0.0) > 0.05:
            risks.append("gateway_packet_loss")
        if _as_float(signal_quality.get("jitter_ms"), default=0.0) > 25.0:
            risks.append("high_gateway_jitter")
        if _as_float(signal_quality.get("rssi_stability"), default=1.0) < 0.45:
            risks.append("unstable_rssi")
        if _as_int(signal_quality.get("visible_access_points"), default=0) < 1:
            risks.append("no_visible_wifi_observation")
        return risks

    @classmethod
    def _recommend_next_action(
        cls,
        baseline: Mapping[str, Any],
        fingerprint_count: int,
        signal_quality: Mapping[str, Any],
    ) -> str:
        if not cls._baseline_available(baseline):
            return "Run empty-room calibration before interpreting live scans."
        if fingerprint_count <= 0:
            return "Run zone calibration for zone_a, zone_b, and zone_c."
        if cls._quality_is_weak(signal_quality):
            return "Improve signal quality, keep the backend device stationary, then rescan."
        return "Continue controlled scanning and compare changes against the saved baseline."

    @staticmethod
    def _baseline_available(baseline: Mapping[str, Any]) -> bool:
        status = str(baseline.get("baseline_status") or baseline.get("status") or "").lower()
        return status not in {"", "unavailable"} and "not_calibrated" not in str(baseline.get("reason") or "")

    @staticmethod
    def _quality_is_weak(signal_quality: Mapping[str, Any]) -> bool:
        if not signal_quality:
            return True
        return (
            _as_float(signal_quality.get("rssi_stability"), default=0.0) < 0.45
            or _as_float(signal_quality.get("packet_loss"), default=1.0) > 0.10
            or _as_int(signal_quality.get("visible_access_points"), default=0) <= 0
        )


def _read_path(source: Mapping[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = source
    for key in path:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

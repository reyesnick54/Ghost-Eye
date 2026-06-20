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
    model_name = "ghosteye-rules-fallback"

    def analyze(
        self,
        telemetry: Mapping[str, Any],
        prompt: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> AIAnalysisResult:
        """Return an advisory analysis result without external model calls."""

        prompt = prompt or build_telemetry_prompt(telemetry)
        presence = str(telemetry.get("presence", "unknown"))
        zone = str(telemetry.get("zone", "unknown"))
        motion_score = _as_float(telemetry.get("motion_score"), default=0.0)
        confidence = clamp_confidence(telemetry.get("confidence"), default=0.0)

        observations = [
            f"Presence state: {presence}.",
            f"Motion score: {motion_score:.2f}.",
            f"Reported confidence: {confidence:.2f}.",
        ]
        if zone and zone != "unknown":
            observations.append(f"Coarse zone estimate: {zone}.")
        else:
            observations.append("No reliable zone estimate is available.")

        recommendations = []
        if confidence < 0.35:
            recommendations.append("Collect more calibration samples before acting on this estimate.")
        if motion_score >= 0.7:
            recommendations.append("Verify that environmental movement is expected for this session.")
        if presence in {"possible_presence", "presence_detected"}:
            recommendations.append("Treat the result as probabilistic and confirm with authorized sensors.")
        if not recommendations:
            recommendations.append("Continue monitoring for drift or signal-quality changes.")

        summary = (
            "Fallback advisory analysis generated from GhostEye telemetry. "
            f"The current result reports {presence} with confidence {confidence:.2f}."
        )

        result_metadata: dict[str, Any] = {
            "prompt_chars": len(prompt),
            "external_runtime": False,
        }
        if metadata:
            result_metadata.update(dict(metadata))

        return AIAnalysisResult(
            available=True,
            provider=self.provider_name,
            model=self.model_name,
            summary=summary,
            confidence=confidence,
            observations=tuple(observations),
            recommendations=tuple(recommendations),
            limitations=(SAFE_LIMITATION_NOTICE,),
            metadata=result_metadata,
        )


def _as_float(value: Any, default: float = 0.0) -> float:
"""Deterministic fallback analysis for Ghost-Eye telemetry."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from math import isclose
from typing import Any

from pydantic import BaseModel

from ghost_eye.api.schemas import AIAnalysisResult, GhostEyeTelemetry


REQUIRED_LIMITATIONS = [
    "wifi_only_non_csi",
    "confidence_capped",
    "authorized_environment_required",
]


class FallbackAIAnalyzer:
    """Analyze telemetry with deterministic rules when AI inference is absent."""

    MODEL_NAME = "deterministic_fallback_rules_v1"
    LOW_CONFIDENCE_THRESHOLD = 0.35
    ELEVATED_MOTION_THRESHOLD = 0.65
    HIGH_JITTER_SCORE_THRESHOLD = 0.65
    HIGH_JITTER_MS_THRESHOLD = 30.0

    def analyze(self, telemetry: GhostEyeTelemetry | Mapping[str, Any]) -> AIAnalysisResult:
        """Return a deterministic AIAnalysisResult for telemetry-like input."""

        telemetry_data = _to_mapping(telemetry)
        telemetry_confidence = _number_at(telemetry_data, ("confidence",), default=0.0) or 0.0
        confidence = _clamp01(telemetry_confidence)
        motion_score = _number_at(telemetry_data, ("motion_score",), default=0.0) or 0.0
        zone_match = self._highest_confidence_zone(telemetry_data)
        jitter = _first_number(
            telemetry_data,
            (
                ("jitter",),
                ("jitter_ms",),
                ("network_jitter",),
                ("network_jitter_ms",),
                ("observation", "jitter"),
                ("observation", "jitter_ms"),
                ("observation", "network_jitter"),
                ("observation", "network_jitter_ms"),
                ("disturbance", "explanation_features", "current_jitter_avg"),
                ("metadata", "jitter"),
                ("metadata", "jitter_ms"),
            ),
        )
        visible_access_points = _visible_access_point_count(telemetry_data)

        summary_parts: list[str] = []
        triggered_rules: list[str] = []
        risk_flags: list[str] = []

        if confidence < self.LOW_CONFIDENCE_THRESHOLD:
            summary_parts.append("low confidence / scan quality weak")
            triggered_rules.append("low_confidence")

        if motion_score > self.ELEVATED_MOTION_THRESHOLD:
            summary_parts.append("elevated disturbance")
            triggered_rules.append("elevated_disturbance")

        if zone_match is not None:
            summary_parts.append(f"likely zone: {zone_match['zone']}")
            triggered_rules.append("likely_zone")

        if jitter is not None and self._is_high_jitter(jitter):
            risk_flags.append("network_jitter_possible")
            triggered_rules.append("network_jitter_possible")

        if visible_access_points is not None and visible_access_points < 2:
            risk_flags.append("weak_ap_geometry")
            triggered_rules.append("weak_ap_geometry")

        if not summary_parts:
            summary_parts.append("fallback analysis: no elevated disturbance detected")

        metadata: dict[str, Any] = {
            "risk_flags": risk_flags,
            "flags": list(REQUIRED_LIMITATIONS),
            "required_flags": list(REQUIRED_LIMITATIONS),
            "rules_triggered": triggered_rules,
            "telemetry_confidence": confidence,
            "confidence_capped_to_telemetry": True,
        }
        if jitter is not None:
            metadata["jitter"] = jitter
        if visible_access_points is not None:
            metadata["visible_access_points"] = visible_access_points
        if zone_match is not None:
            metadata["likely_zone"] = zone_match["zone"]
            metadata["likely_zone_score"] = zone_match["score"]

        return AIAnalysisResult(
            available=True,
            model=self.MODEL_NAME,
            summary="; ".join(summary_parts),
            confidence=confidence,
            limitations=list(REQUIRED_LIMITATIONS),
            metadata=metadata,
        )

    __call__ = analyze

    def _highest_confidence_zone(self, telemetry: Mapping[str, Any]) -> dict[str, Any] | None:
        zone = _text_at(telemetry, ("zone",))
        if zone is None or zone == "unknown":
            return None

        zone_scores = _zone_scores(telemetry)
        if zone not in zone_scores:
            return None

        score = zone_scores[zone]
        highest_score = max(zone_scores.values())
        if score == highest_score or isclose(score, highest_score):
            return {"zone": zone, "score": score}
        return None

    def _is_high_jitter(self, jitter: float) -> bool:
        normalized = abs(jitter)
        if normalized <= 1.0:
            return normalized > self.HIGH_JITTER_SCORE_THRESHOLD
        return normalized > self.HIGH_JITTER_MS_THRESHOLD


def _to_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if isinstance(value, BaseModel):
        if hasattr(value, "model_dump"):
            return value.model_dump()
        return value.dict()
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "to_dict") and callable(value.to_dict):
        converted = value.to_dict()
        if isinstance(converted, Mapping):
            return converted
    if hasattr(value, "to_response") and callable(value.to_response):
        converted = value.to_response()
        if isinstance(converted, Mapping):
            return converted
    return vars(value)


def _read(value: Any, key: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(key)
    if isinstance(value, BaseModel):
        return getattr(value, key, None)
    if is_dataclass(value):
        return getattr(value, key, None)
    return getattr(value, key, None)


def _at(source: Any, path: Sequence[str]) -> Any:
    current = source
    for key in path:
        if current is None:
            return None
        current = _read(current, key)
    return current


def _first_number(source: Any, paths: Sequence[Sequence[str]]) -> float | None:
    for path in paths:
        value = _number_at(source, path)
        if value is not None:
            return value
    return None


def _number_at(source: Any, path: Sequence[str], default: float | None = None) -> float | None:
    value = _at(source, path)
    if value is None:
        return default
    if isinstance(value, bool):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _text_at(source: Any, path: Sequence[str]) -> str | None:
    value = _at(source, path)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clamp01(value: float) -> float:
    return min(max(float(value), 0.0), 1.0)


def _zone_scores(telemetry: Mapping[str, Any]) -> dict[str, float]:
    candidates = (
        _at(telemetry, ("map", "confidence_by_zone")),
        _at(telemetry, ("zone_map", "confidence_by_zone")),
        _at(telemetry, ("confidence_by_zone",)),
        _at(telemetry, ("map",)),
        _at(telemetry, ("zone_map",)),
    )

    for candidate in candidates:
        scores = _numeric_mapping(candidate)
        if scores:
            return scores
    return {}


def _numeric_mapping(value: Any) -> dict[str, float]:
    if value is None:
        return {}
    if isinstance(value, BaseModel):
        if hasattr(value, "model_dump"):
            value = value.model_dump()
        else:
            value = value.dict()
    elif is_dataclass(value):
        value = asdict(value)
    if not isinstance(value, Mapping):
        return {}

    scores: dict[str, float] = {}
    for key, raw_score in value.items():
        if isinstance(raw_score, bool):
            continue
        try:
            scores[str(key)] = float(raw_score)
        except (TypeError, ValueError):
            continue
    return scores


def _visible_access_point_count(telemetry: Mapping[str, Any]) -> int | None:
    direct_count = _first_number(
        telemetry,
        (
            ("visible_access_point_count",),
            ("visible_ap_count",),
            ("bssid_count",),
            ("observation", "visible_access_point_count"),
            ("observation", "visible_ap_count"),
            ("observation", "bssid_count"),
            ("capabilities", "access_point_count"),
        ),
    )
    if direct_count is not None:
        return int(direct_count)

    for path in (
        ("visible_access_points",),
        ("visible_aps",),
        ("access_points",),
        ("observation", "visible_access_points"),
        ("observation", "visible_aps"),
        ("observation", "access_points"),
        ("observation", "rssi_vector"),
    ):
        value = _at(telemetry, path)
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            return len(value)

    return None

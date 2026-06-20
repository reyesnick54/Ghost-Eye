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
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

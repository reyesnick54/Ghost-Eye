"""Optional AI analysis helpers for GhostEye telemetry."""

from ghost_eye.ai.ai_analysis_schema import (
    AIAnalysisConfig,
    AIAnalysisResult,
    SAFE_LIMITATION_NOTICE,
    clamp_confidence,
)
from ghost_eye.ai.fallback_ai_analyzer import FallbackAIAnalyzer
from ghost_eye.ai.telemetry_prompt_builder import build_scan_analysis_prompt, build_telemetry_prompt, sanitize_telemetry

__all__ = [
    "AIAnalysisConfig",
    "AIAnalysisResult",
    "FallbackAIAnalyzer",
    "SAFE_LIMITATION_NOTICE",
    "build_scan_analysis_prompt",
    "build_telemetry_prompt",
    "clamp_confidence",
    "sanitize_telemetry",
]

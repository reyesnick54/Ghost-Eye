"""Optional AI analysis helpers for GhostEye telemetry."""

from ghost_eye.ai.ai_analysis_schema import AIAnalysisConfig, AIAnalysisResult
from ghost_eye.ai.fallback_ai_analyzer import FallbackAIAnalyzer
from ghost_eye.ai.s3m_bridge import S3MBridge, S3M_AVAILABLE, create_ai_analyzer
from ghost_eye.ai.telemetry_prompt_builder import build_telemetry_prompt, sanitize_telemetry

__all__ = [
    "AIAnalysisConfig",
    "AIAnalysisResult",
    "FallbackAIAnalyzer",
    "S3MBridge",
    "S3M_AVAILABLE",
    "build_telemetry_prompt",
    "create_ai_analyzer",
    "sanitize_telemetry",
]
"""AI analysis helpers for Ghost-Eye telemetry."""

from .fallback_ai_analyzer import FallbackAIAnalyzer

__all__ = ["FallbackAIAnalyzer"]
"""Optional AI integrations for Ghost-Eye telemetry analysis."""

from .s3m_bridge import S3MBridge, telemetry_prompt_builder

__all__ = ["S3MBridge", "telemetry_prompt_builder"]
"""AI-assisted analysis schemas for GhostEye telemetry."""

from .ai_analysis_schema import AIAnalysisRequest, AIAnalysisResult, AIStatus

__all__ = ["AIAnalysisRequest", "AIAnalysisResult", "AIStatus"]
"""AI prompt helpers for GhostEye telemetry analysis."""

from ghost_eye.ai.telemetry_prompt_builder import build_scan_analysis_prompt

__all__ = ["build_scan_analysis_prompt"]

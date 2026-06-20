"""Shared schemas and configuration for optional GhostEye AI analysis."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


DEFAULT_AI_ANALYSIS = "false"
DEFAULT_AI_PROVIDER = "fallback"
DEFAULT_S3M_PATH = ""
SAFE_LIMITATION_NOTICE = (
    "Optional AI analysis is advisory only and is limited to GhostEye telemetry "
    "from authorized controlled environments."
)
ALLOWED_AI_PROVIDERS = ("fallback", "s3m")


def parse_bool(value: str | None, default: bool = False) -> bool:
    """Parse common environment-style boolean values."""

    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on", "enabled"}:
        return True
    if normalized in {"0", "false", "no", "off", "disabled", ""}:
        return False
    return default


@dataclass(frozen=True)
class AIAnalysisConfig:
    """Runtime configuration for optional AI analysis."""

    enabled: bool = False
    provider: str = DEFAULT_AI_PROVIDER
    s3m_path: str = DEFAULT_S3M_PATH

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "AIAnalysisConfig":
        """Create configuration from GhostEye AI environment variables."""

        source = env if env is not None else os.environ
        provider = source.get("GHOSTEYE_AI_PROVIDER", DEFAULT_AI_PROVIDER).strip().lower()
        if provider not in ALLOWED_AI_PROVIDERS:
            provider = DEFAULT_AI_PROVIDER

        return cls(
            enabled=parse_bool(source.get("GHOSTEYE_AI_ANALYSIS", DEFAULT_AI_ANALYSIS)),
            provider=provider,
            s3m_path=source.get("GHOSTEYE_S3M_PATH", DEFAULT_S3M_PATH).strip(),
        )


@dataclass(frozen=True)
class AIAnalysisResult:
    """Serializable result returned by both S3M and fallback analyzers."""

    available: bool = False
    provider: str = DEFAULT_AI_PROVIDER
    model: str | None = None
    summary: str = ""
    confidence: float = 0.0
    observations: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    limitations: tuple[str, ...] = (SAFE_LIMITATION_NOTICE,)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary suitable for JSON responses."""

        return asdict(self)


def clamp_confidence(value: Any, default: float = 0.0) -> float:
    """Normalize confidence values to the inclusive 0..1 range."""

    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = default

    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence

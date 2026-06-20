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
"""Pydantic schemas for AI-assisted GhostEye telemetry analysis."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator


SAFE_LIMITATION_NOTICE = (
    "AI analysis is advisory and bounded by GhostEye telemetry confidence. "
    "Use only in authorized, consent-based, controlled environments."
)


def _utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for schema defaults."""

    return datetime.now(timezone.utc)


def _coerce_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None

    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = default

    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence
        return None

    return max(0.0, min(confidence, 1.0))


class AIStatus(BaseModel):
    """Runtime status for the AI provider and its telemetry consensus."""

    enabled: bool = Field(default=False)
    provider: Optional[str] = Field(default=None)
    status: str = Field(default="disabled")
    telemetry_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    message: Optional[str] = Field(default=None)


class AIAnalysisRequest(BaseModel):
    """Request payload for generating advisory AI analysis from telemetry."""

    enabled: bool = Field(default=True)
    provider: Optional[str] = Field(default=None)
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    telemetry_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    prompt: Optional[str] = Field(default=None)

    @root_validator(pre=True)
    def derive_telemetry_confidence(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Allow callers to pass the full GhostEye telemetry object."""

        if not isinstance(values, dict) or values.get("telemetry_confidence") is not None:
            return values

        telemetry = values.get("telemetry")
        if isinstance(telemetry, dict):
            confidence = _coerce_confidence(telemetry.get("confidence"))
            if confidence is not None:
                values = dict(values)
                values["telemetry_confidence"] = confidence

        return values


class AIAnalysisResult(BaseModel):
    """Advisory AI analysis result bounded by GhostEye telemetry confidence."""

    enabled: bool = Field(default=False)
    provider: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    likely_explanation: Optional[str] = Field(default=None)
    recommended_action: Optional[str] = Field(default=None)
    risk_flags: List[str] = Field(default_factory=list)
    operator_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    consensus_status: AIStatus = Field(default_factory=AIStatus)
    limitations: List[str] = Field(default_factory=lambda: [SAFE_LIMITATION_NOTICE])
    created_at: datetime = Field(default_factory=_utc_now)

    @root_validator(pre=True)
    def cap_operator_confidence(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Keep operator confidence no higher than GhostEye telemetry confidence."""

        if not isinstance(values, dict):
            return values

        capped_values = dict(values)
        telemetry_confidence = cls._extract_telemetry_confidence(capped_values)
        operator_confidence = _coerce_confidence(capped_values.get("operator_confidence"))

        if operator_confidence is None:
            return capped_values

        operator_confidence = min(operator_confidence, telemetry_confidence or 0.0)

        capped_values["operator_confidence"] = operator_confidence
        return capped_values

    @staticmethod
    def _extract_telemetry_confidence(values: Dict[str, Any]) -> Optional[float]:
        for key in (
            "telemetry_confidence",
            "ghost_eye_telemetry_confidence",
            "ghosteye_telemetry_confidence",
        ):
            confidence = _coerce_confidence(values.get(key))
            if confidence is not None:
                return confidence

        telemetry = values.get("telemetry")
        if isinstance(telemetry, dict):
            confidence = _coerce_confidence(telemetry.get("confidence"))
            if confidence is not None:
                return confidence

        consensus_status = values.get("consensus_status")
        if isinstance(consensus_status, AIStatus):
            return consensus_status.telemetry_confidence

        if isinstance(consensus_status, dict):
            for key in (
                "telemetry_confidence",
                "ghost_eye_telemetry_confidence",
                "ghosteye_telemetry_confidence",
                "confidence",
            ):
                confidence = _coerce_confidence(consensus_status.get(key))
                if confidence is not None:
                    return confidence

        return None

    class Config:
        extra = "ignore"

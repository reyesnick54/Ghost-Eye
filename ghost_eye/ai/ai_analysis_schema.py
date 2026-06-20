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

        if telemetry_confidence is not None:
            operator_confidence = min(operator_confidence, telemetry_confidence)

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

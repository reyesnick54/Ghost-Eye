"""AI analysis schemas shared by GhostEye Cloud API routes."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.telemetry import ANALYSIS_MODE, TelemetryScan


class AIAnalysis(BaseModel):
    summary: str
    confidence_explanation: str
    false_positive_risks: list[str] = Field(default_factory=list)
    calibration_recommendations: list[str] = Field(default_factory=list)
    operator_notes: list[str] = Field(default_factory=list)
    recommended_next_action: str
    provider: str
    mode: Literal["analysis_only_no_autonomy"] = ANALYSIS_MODE
    confidence: float = Field(ge=0, le=1)
    created_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class AIAnalyzeScanRequest(BaseModel):
    scan: TelemetryScan
    metadata: dict[str, Any] = Field(default_factory=dict)


class AIAnalyzeSessionRequest(BaseModel):
    session_id: str
    team_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)

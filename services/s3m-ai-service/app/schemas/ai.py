"""Schemas for the hosted S3M AI service."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class AIAnalysis(BaseModel):
    summary: str
    confidence_explanation: str
    false_positive_risks: list[str] = Field(default_factory=list)
    calibration_recommendations: list[str] = Field(default_factory=list)
    operator_notes: list[str] = Field(default_factory=list)
    recommended_next_action: str
    provider: str
    mode: Literal["analysis_only_no_autonomy"] = "analysis_only_no_autonomy"
    confidence: float = Field(ge=0, le=1)
    created_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class AnalyzeScanRequest(BaseModel):
    scan: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)


class AnalyzeSessionRequest(BaseModel):
    session: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)


class CalibrationRecommendationRequest(BaseModel):
    team_id: str
    room_id: str | None = None
    latest_scan: dict[str, Any] | None = None
    existing_baseline: dict[str, Any] | None = None
    zone_fingerprints: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

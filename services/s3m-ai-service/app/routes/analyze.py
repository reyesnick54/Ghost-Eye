"""AI analysis routes for the hosted S3M service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Request

from app.schemas.ai import (
    AIAnalysis,
    AnalyzeScanRequest,
    AnalyzeSessionRequest,
    CalibrationRecommendationRequest,
)

router = APIRouter()


@router.get("/ai/status")
def ai_status(request: Request) -> dict[str, Any]:
    return request.app.state.s3m_bridge.status()


@router.post("/ai/analyze-scan", response_model=AIAnalysis)
def analyze_scan(payload: AnalyzeScanRequest, request: Request) -> AIAnalysis:
    return _run_or_fallback(request, "scan", payload.scan, payload.metadata)


@router.post("/ai/analyze-session", response_model=AIAnalysis)
def analyze_session(payload: AnalyzeSessionRequest, request: Request) -> AIAnalysis:
    return _run_or_fallback(request, "session", payload.session, payload.metadata)


@router.post("/ai/recommend-calibration", response_model=AIAnalysis)
def recommend_calibration(payload: CalibrationRecommendationRequest, request: Request) -> AIAnalysis:
    fallback = request.app.state.fallback_ai_analyzer
    return fallback.recommend_calibration(payload.model_dump(mode="json"))


def _run_or_fallback(
    request: Request,
    analysis_type: str,
    subject: dict[str, Any],
    metadata: dict[str, Any],
) -> AIAnalysis:
    bridge = request.app.state.s3m_bridge
    fallback = request.app.state.fallback_ai_analyzer
    if bridge.available:
        try:
            output = bridge.analyze({"type": analysis_type, "payload": subject, "metadata": metadata})
            return _analysis_from_output(output, fallback, analysis_type, subject, metadata)
        except Exception:
            pass

    if analysis_type == "session":
        return fallback.analyze_session(subject, metadata)
    return fallback.analyze_scan(subject, metadata)


def _analysis_from_output(
    output: dict[str, Any],
    fallback: Any,
    analysis_type: str,
    subject: dict[str, Any],
    metadata: dict[str, Any],
) -> AIAnalysis:
    base = fallback.analyze_session(subject, metadata) if analysis_type == "session" else fallback.analyze_scan(subject, metadata)
    confidence = min(base.confidence, _float_or(output.get("confidence"), base.confidence))
    return base.model_copy(
        update={
            "summary": str(output.get("summary") or base.summary)[:2000],
            "confidence_explanation": str(
                output.get("confidence_explanation")
                or "S3M-Core analysis confidence is capped to GhostEye telemetry confidence."
            ),
            "false_positive_risks": _list_or(output.get("false_positive_risks"), base.false_positive_risks),
            "calibration_recommendations": _list_or(
                output.get("calibration_recommendations"),
                base.calibration_recommendations,
            ),
            "operator_notes": _list_or(output.get("operator_notes"), base.operator_notes),
            "recommended_next_action": str(output.get("recommended_next_action") or base.recommended_next_action),
            "provider": "s3m_core",
            "confidence": confidence,
            "created_at": datetime.now(timezone.utc),
            "metadata": {**base.metadata, "s3m_core_available": True},
        }
    )


def _float_or(value: Any, default: float) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def _list_or(value: Any, default: list[str]) -> list[str]:
    if value is None:
        return list(default)
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]

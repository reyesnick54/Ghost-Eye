"""AI analysis routes for GhostEye Cloud API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth.jwt_auth import get_current_principal
from app.schemas.ai import AIAnalysis, AIAnalyzeScanRequest, AIAnalyzeSessionRequest

router = APIRouter(dependencies=[Depends(get_current_principal)])


@router.get("/ai/status")
def ai_status(request: Request) -> dict[str, object]:
    return request.app.state.s3m_client.status()


@router.post("/ai/analyze-scan", response_model=AIAnalysis)
def analyze_scan(payload: AIAnalyzeScanRequest, request: Request) -> AIAnalysis:
    try:
        return request.app.state.s3m_client.analyze_scan(payload.scan, payload.metadata)
    except Exception:
        return request.app.state.fallback_ai_analyzer.analyze_scan(payload.scan, payload.metadata)


@router.post("/ai/analyze-session", response_model=AIAnalysis)
def analyze_session(payload: AIAnalyzeSessionRequest, request: Request) -> AIAnalysis:
    session = request.app.state.session_store.get_session(payload.session_id)
    if session is None or session.team_id != payload.team_id:
        raise HTTPException(status_code=404, detail=f"Unknown session_id: {payload.session_id}")
    try:
        return request.app.state.s3m_client.analyze_session(session, payload.metadata)
    except Exception:
        return request.app.state.fallback_ai_analyzer.analyze_session(session, payload.metadata)

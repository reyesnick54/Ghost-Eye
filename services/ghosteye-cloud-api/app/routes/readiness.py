"""Readiness endpoint for hosted deployments."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.config import get_settings
from app.schemas.readiness import ReadinessStatus

router = APIRouter()


@router.get("/system/readiness", response_model=ReadinessStatus)
def readiness(request: Request) -> ReadinessStatus:
    settings = get_settings()
    ai_status = request.app.state.s3m_client.status()
    return ReadinessStatus(
        status="ready",
        timestamp=datetime.now(timezone.utc),
        environment=settings.ghosteye_env,
        storage={
            **request.app.state.session_store.readiness(),
            "calibration_status": request.app.state.calibration_store.readiness()["status"],
        },
        ai_service={
            "configured": ai_status.get("configured", False),
            "available": ai_status.get("available", False),
            "provider": ai_status.get("provider"),
            "url_configured": bool(settings.s3m_ai_service_url),
        },
        dependencies={
            "supabase_url_configured": bool(settings.supabase_url),
            "supabase_jwt_secret_configured": bool(settings.supabase_jwt_secret),
            "cors_allowed_origins": ",".join(settings.cors_allowed_origins),
        },
    )

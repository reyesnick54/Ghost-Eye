"""Hosted GhostEye Cloud API.

The cloud API is intentionally mobile-observation driven: it cannot directly
observe local NetGear, TP-Link, or other WiFi RF conditions from a hosted
environment. Mobile clients collect allowed RSSI/network observations and send
them here for storage, calibration, coarse telemetry, and advisory AI analysis.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.fallback_ai_analyzer import FallbackAIAnalyzer
from app.ai.s3m_client import S3MAIClient
from app.config import get_settings
from app.inference.cloud_pipeline import CloudInferencePipeline
from app.routes import ai, calibration, devices, health, readiness, sessions, telemetry
from app.schemas.telemetry import LIMITATIONS, NOTICE
from app.storage.calibration_store import CalibrationStore
from app.storage.session_store import SessionStore


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="GhostEye Cloud API",
        version="0.4.0",
        description="Hosted mobile-first GhostEye API for WiFi-only non-CSI telemetry.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=settings.cors_allowed_origins != ("*",),
        allow_methods=["*"],
        allow_headers=["*"],
    )

    session_store = SessionStore(settings.storage_dir / "sessions")
    calibration_store = CalibrationStore(settings.storage_dir / "calibrations")
    app.state.session_store = session_store
    app.state.calibration_store = calibration_store
    app.state.pipeline = CloudInferencePipeline(session_store, calibration_store)
    app.state.s3m_client = S3MAIClient(settings)
    app.state.fallback_ai_analyzer = FallbackAIAnalyzer()

    app.include_router(health.router)
    app.include_router(readiness.router)
    app.include_router(devices.router)
    app.include_router(telemetry.router)
    app.include_router(calibration.router)
    app.include_router(sessions.router)
    app.include_router(ai.router)

    return app


app = create_app()


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "ghosteye-cloud-api",
        "version": "0.4.0",
        "status": "online",
        "architecture": "mobile_app_to_hosted_cloud_api_to_hosted_s3m_ai_service",
        "mode": "wifi_only_non_csi",
        "analysis_mode": "analysis_only_no_autonomy",
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }

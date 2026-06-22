"""Hosted S3M AI service for GhostEye analysis-only workflows."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.fallback_ai_analyzer import FallbackAIAnalyzer
from app.adapters.s3m_bridge import S3MBridge
from app.config import get_settings
from app.routes import analyze, health


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="S3M AI Service",
        version="0.4.0",
        description="Hosted analysis-only AI service for GhostEye telemetry.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=settings.cors_allowed_origins != ("*",),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.s3m_bridge = S3MBridge()
    app.state.fallback_ai_analyzer = FallbackAIAnalyzer()
    app.include_router(health.router)
    app.include_router(analyze.router)
    return app


app = create_app()


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "s3m-ai-service",
        "version": "0.4.0",
        "status": "online",
        "mode": "analysis_only_no_autonomy",
        "provider": app.state.s3m_bridge.status()["provider"],
    }

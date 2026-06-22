"""Health routes for S3M AI service."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "service": "s3m-ai-service",
        "timestamp": datetime.now(timezone.utc),
        "mode": "analysis_only_no_autonomy",
    }

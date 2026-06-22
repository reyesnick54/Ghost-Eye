"""Health endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "ghosteye-cloud-api",
        "timestamp": datetime.now(timezone.utc),
        "mode": "wifi_only_non_csi",
        "analysis_mode": "analysis_only_no_autonomy",
    }

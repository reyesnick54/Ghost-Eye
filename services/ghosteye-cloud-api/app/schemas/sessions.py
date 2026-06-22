"""Session schemas for rolling cloud telemetry state."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.telemetry import TelemetryScan


class SessionSummary(BaseModel):
    session_id: str
    team_id: str
    device_id: str | None = None
    room_id: str | None = None
    active: bool = True
    started_at: datetime
    updated_at: datetime
    scan_count: int = Field(default=0, ge=0)
    latest_scan: TelemetryScan | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

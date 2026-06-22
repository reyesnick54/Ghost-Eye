"""Device registration schemas for GhostEye mobile clients."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.telemetry import Platform


class DeviceRegistration(BaseModel):
    device_id: str | None = None
    team_id: str = Field(min_length=1)
    platform: Platform
    app_version: str | None = None
    device_model: str | None = None
    capability_mode: str = "wifi_only_non_csi"
    metadata: dict[str, Any] = Field(default_factory=dict)


class DeviceRegistrationResponse(BaseModel):
    device_id: str
    team_id: str
    platform: Platform
    status: Literal["registered"] = "registered"
    registered_at: datetime
    auth_mode: str = "jwt_placeholder"
    token_type: str = "bearer"
    access_token: str
    expires_in_seconds: int
    metadata: dict[str, Any] = Field(default_factory=dict)

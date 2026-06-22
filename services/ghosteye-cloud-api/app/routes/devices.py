"""Mobile device registration routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Request

from app.auth.jwt_auth import create_device_token
from app.config import get_settings
from app.schemas.devices import DeviceRegistration, DeviceRegistrationResponse

router = APIRouter()


@router.post("/auth/device/register", response_model=DeviceRegistrationResponse)
def register_device(payload: DeviceRegistration, request: Request) -> DeviceRegistrationResponse:
    device_id = payload.device_id or f"dev_{uuid.uuid4().hex[:12]}"
    normalized = payload.model_copy(update={"device_id": device_id})
    token, ttl = create_device_token(device_id=device_id, team_id=payload.team_id, settings=get_settings())
    return request.app.state.session_store.register_device(normalized, token, ttl)

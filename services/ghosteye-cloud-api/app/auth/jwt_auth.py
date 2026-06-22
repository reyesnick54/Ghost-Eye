"""Small JWT-compatible auth placeholder for mobile clients.

This module intentionally avoids a hard dependency on a specific identity
provider. Hosted deployments can replace it with Supabase JWT verification or
another OIDC verifier while keeping the route dependency shape stable.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings


bearer_scheme = HTTPBearer(auto_error=False)


def create_device_token(device_id: str, team_id: str, settings: Settings | None = None) -> tuple[str, int]:
    """Issue a signed placeholder bearer token for mobile development."""

    settings = settings or get_settings()
    ttl_seconds = 60 * 60 * 24
    now = datetime.now(timezone.utc)
    payload = {
        "sub": device_id,
        "team_id": team_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp()),
        "iss": "ghosteye-cloud-api",
        "aud": "ghosteye-mobile",
    }
    token = _encode_jwt(payload, settings.ghosteye_api_secret)
    return token, ttl_seconds


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> dict[str, Any]:
    """Validate bearer tokens when provided or required by environment."""

    if credentials is None:
        if settings.ghosteye_env.lower() in {"development", "test", "local"}:
            return {"sub": "anonymous-dev-device", "team_id": "dev-team", "auth": "development"}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
        )

    try:
        return verify_token(credentials.credentials, settings.ghosteye_api_secret)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


def verify_token(token: str, secret: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid bearer token")

    signing_input = ".".join(parts[:2]).encode("utf-8")
    expected = _sign(signing_input, secret)
    if not hmac.compare_digest(expected, parts[2]):
        raise ValueError("Invalid bearer token signature")

    payload = json.loads(_b64decode(parts[1]))
    exp = int(payload.get("exp", 0))
    if exp < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Bearer token expired")
    return payload


def _encode_jwt(payload: dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_text = _b64encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_text = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = _sign(f"{header_text}.{payload_text}".encode("utf-8"), secret)
    return f"{header_text}.{payload_text}.{signature}"


def _sign(signing_input: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return _b64encode(digest)


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)

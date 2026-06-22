"""Runtime configuration for the hosted GhostEye Cloud API."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Environment-backed settings for hosted deployments."""

    ghosteye_env: str = Field(default="development", alias="GHOSTEYE_ENV")
    ghosteye_api_secret: str = Field(default="dev-only-change-me", alias="GHOSTEYE_API_SECRET")
    supabase_url: str | None = Field(default=None, alias="SUPABASE_URL")
    supabase_jwt_secret: str | None = Field(default=None, alias="SUPABASE_JWT_SECRET")
    s3m_ai_service_url: str | None = Field(default=None, alias="S3M_AI_SERVICE_URL")
    cors_allowed_origins: tuple[str, ...] = Field(default=("*",), alias="CORS_ALLOWED_ORIGINS")
    storage_dir: Path = Field(default=Path("/tmp/ghosteye-cloud-api"), alias="GHOSTEYE_STORAGE_DIR")

    @classmethod
    def from_env(cls) -> "Settings":
        origins = tuple(
            origin.strip()
            for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
            if origin.strip()
        )
        return cls(
            GHOSTEYE_ENV=os.getenv("GHOSTEYE_ENV", "development"),
            GHOSTEYE_API_SECRET=os.getenv("GHOSTEYE_API_SECRET", "dev-only-change-me"),
            SUPABASE_URL=os.getenv("SUPABASE_URL") or None,
            SUPABASE_JWT_SECRET=os.getenv("SUPABASE_JWT_SECRET") or None,
            S3M_AI_SERVICE_URL=os.getenv("S3M_AI_SERVICE_URL") or None,
            CORS_ALLOWED_ORIGINS=origins or ("*",),
            GHOSTEYE_STORAGE_DIR=Path(os.getenv("GHOSTEYE_STORAGE_DIR", "/tmp/ghosteye-cloud-api")),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings for route dependencies."""

    return Settings.from_env()

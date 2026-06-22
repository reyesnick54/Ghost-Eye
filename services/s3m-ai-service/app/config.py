"""Runtime configuration for the hosted S3M AI service."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    ghosteye_env: str = Field(default="development", alias="GHOSTEYE_ENV")
    cors_allowed_origins: tuple[str, ...] = Field(default=("*",), alias="CORS_ALLOWED_ORIGINS")
    s3m_core_path: Path | None = Field(default=None, alias="S3M_CORE_PATH")

    @classmethod
    def from_env(cls) -> "Settings":
        origins = tuple(
            origin.strip()
            for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
            if origin.strip()
        )
        core_path = os.getenv("S3M_CORE_PATH")
        return cls(
            GHOSTEYE_ENV=os.getenv("GHOSTEYE_ENV", "development"),
            CORS_ALLOWED_ORIGINS=origins or ("*",),
            S3M_CORE_PATH=Path(core_path) if core_path else None,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()

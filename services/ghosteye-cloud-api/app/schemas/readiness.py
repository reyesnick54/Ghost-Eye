"""Readiness schema for cloud deployments."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ReadinessStatus(BaseModel):
    status: str
    timestamp: datetime
    environment: str
    storage: dict[str, str] = Field(default_factory=dict)
    ai_service: dict[str, str | bool | None] = Field(default_factory=dict)
    dependencies: dict[str, str | bool | None] = Field(default_factory=dict)

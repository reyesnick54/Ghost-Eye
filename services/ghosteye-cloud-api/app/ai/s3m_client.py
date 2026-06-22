"""HTTP client for the hosted S3M AI service."""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings, get_settings
from app.schemas.ai import AIAnalysis
from app.schemas.sessions import SessionSummary
from app.schemas.telemetry import TelemetryScan


class S3MAIClient:
    """Small sync client for internal hosted S3M service calls."""

    def __init__(self, settings: Settings | None = None, timeout_seconds: float = 4.0) -> None:
        self.settings = settings or get_settings()
        self.timeout_seconds = timeout_seconds

    @property
    def configured(self) -> bool:
        return bool(self.settings.s3m_ai_service_url)

    def status(self) -> dict[str, Any]:
        if not self.configured:
            return {"configured": False, "available": False, "provider": "fallback"}
        try:
            response = httpx.get(self._url("/ai/status"), timeout=self.timeout_seconds)
            response.raise_for_status()
            payload = response.json()
            payload["configured"] = True
            payload["available"] = True
            return payload
        except Exception as exc:
            return {
                "configured": True,
                "available": False,
                "provider": "fallback",
                "error": exc.__class__.__name__,
            }

    def analyze_scan(self, scan: TelemetryScan, metadata: dict[str, Any] | None = None) -> AIAnalysis:
        payload = {"scan": scan.model_dump(mode="json"), "metadata": metadata or {}}
        return self._post_analysis("/ai/analyze-scan", payload)

    def analyze_session(self, session: SessionSummary, metadata: dict[str, Any] | None = None) -> AIAnalysis:
        payload = {"session": session.model_dump(mode="json"), "metadata": metadata or {}}
        return self._post_analysis("/ai/analyze-session", payload)

    def _post_analysis(self, path: str, payload: dict[str, Any]) -> AIAnalysis:
        if not self.configured:
            raise RuntimeError("S3M_AI_SERVICE_URL is not configured")
        response = httpx.post(self._url(path), json=payload, timeout=self.timeout_seconds)
        response.raise_for_status()
        return AIAnalysis.model_validate(response.json())

    def _url(self, path: str) -> str:
        base_url = str(self.settings.s3m_ai_service_url).rstrip("/")
        return f"{base_url}{path}"

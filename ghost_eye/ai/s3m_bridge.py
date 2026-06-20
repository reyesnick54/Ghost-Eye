"""Optional S3M runtime bridge for GhostEye AI analysis."""

from __future__ import annotations

import inspect
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ghost_eye.ai.ai_analysis_schema import (
    AIAnalysisConfig,
    AIAnalysisResult,
    SAFE_LIMITATION_NOTICE,
    clamp_confidence,
)
from ghost_eye.ai.fallback_ai_analyzer import FallbackAIAnalyzer
from ghost_eye.ai.telemetry_prompt_builder import build_telemetry_prompt


def _prepend_configured_s3m_path() -> None:
    config = AIAnalysisConfig.from_env()
    if not config.s3m_path:
        return

    s3m_path = Path(config.s3m_path).expanduser()
    if s3m_path.exists():
        path_text = str(s3m_path)
        if path_text not in sys.path:
            sys.path.insert(0, path_text)


_prepend_configured_s3m_path()

try:
    from llm_core.unified_runtime import UnifiedRuntime, MissionRequest
    S3M_AVAILABLE = True
except Exception:
    S3M_AVAILABLE = False


class S3MBridge:
    """Adapter that prefers S3M only when explicitly enabled and available."""

    def __init__(
        self,
        config: AIAnalysisConfig | None = None,
        runtime: Any | None = None,
        fallback: FallbackAIAnalyzer | None = None,
    ) -> None:
        self.config = config or AIAnalysisConfig.from_env()
        self._runtime = runtime
        self._fallback = fallback or FallbackAIAnalyzer()

    @property
    def enabled(self) -> bool:
        return self.config.enabled

    @property
    def provider(self) -> str:
        return self.config.provider

    @property
    def s3m_available(self) -> bool:
        return bool(S3M_AVAILABLE or self._runtime is not None)

    def analyze(self, telemetry: Mapping[str, Any]) -> AIAnalysisResult:
        """Analyze telemetry with S3M when configured, otherwise use fallback."""

        prompt = build_telemetry_prompt(telemetry)
        if not self.config.enabled:
            return AIAnalysisResult(
                available=False,
                provider=self.config.provider,
                summary="GhostEye AI analysis is disabled.",
                limitations=(SAFE_LIMITATION_NOTICE,),
                metadata={
                    "enabled": False,
                    "s3m_available": self.s3m_available,
                },
            )

        if self.config.provider != "s3m":
            return self._fallback.analyze(
                telemetry,
                prompt=prompt,
                metadata={"fallback_reason": "provider_configured_as_fallback"},
            )

        if not self.s3m_available:
            return self._fallback.analyze(
                telemetry,
                prompt=prompt,
                metadata={"fallback_reason": "s3m_unavailable", "s3m_available": False},
            )

        try:
            output = self._run_s3m(prompt, telemetry)
        except Exception as exc:
            return self._fallback.analyze(
                telemetry,
                prompt=prompt,
                metadata={
                    "fallback_reason": "s3m_runtime_error",
                    "error": exc.__class__.__name__,
                },
            )

        return self._coerce_s3m_result(output, telemetry)

    def _run_s3m(self, prompt: str, telemetry: Mapping[str, Any]) -> Any:
        runtime = self._runtime or self._create_runtime()
        request = self._create_mission_request(prompt, telemetry)

        for method_name in ("analyze", "generate", "complete", "run", "invoke"):
            method = getattr(runtime, method_name, None)
            if not callable(method):
                continue

            output = method(request)
            if inspect.isawaitable(output):
                raise RuntimeError("S3M runtime returned an awaitable to the sync bridge")
            return output

        raise AttributeError("S3M UnifiedRuntime has no supported analysis method")

    def _create_runtime(self) -> Any:
        runtime_type = globals().get("UnifiedRuntime")
        if runtime_type is None:
            raise RuntimeError("S3M UnifiedRuntime is unavailable")
        return runtime_type()

    def _create_mission_request(self, prompt: str, telemetry: Mapping[str, Any]) -> Any:
        request_type = globals().get("MissionRequest")
        if request_type is None:
            return prompt

        request_kwargs = (
            {
                "prompt": prompt,
                "context": {"telemetry": dict(telemetry)},
                "metadata": {"source": "ghost_eye"},
            },
            {"prompt": prompt, "metadata": {"source": "ghost_eye"}},
            {"prompt": prompt},
        )
        for kwargs in request_kwargs:
            try:
                return request_type(**kwargs)
            except TypeError:
                continue

        try:
            return request_type(prompt)
        except TypeError:
            return prompt

    def _coerce_s3m_result(
        self,
        output: Any,
        telemetry: Mapping[str, Any],
    ) -> AIAnalysisResult:
        if isinstance(output, Mapping):
            summary = _first_text(output, ("summary", "response", "text", "result", "content"))
            confidence = clamp_confidence(output.get("confidence"), telemetry.get("confidence", 0.0))
            observations = _as_tuple(output.get("observations"))
            recommendations = _as_tuple(output.get("recommendations"))
            metadata = {
                "s3m_available": True,
                "raw_keys": tuple(str(key) for key in output.keys()),
            }
        else:
            summary = str(output)
            confidence = clamp_confidence(telemetry.get("confidence"), default=0.0)
            observations = ()
            recommendations = ()
            metadata = {"s3m_available": True}

        return AIAnalysisResult(
            available=True,
            provider="s3m",
            model="llm_core.unified_runtime.UnifiedRuntime",
            summary=summary[:2000],
            confidence=confidence,
            observations=observations,
            recommendations=recommendations,
            limitations=(SAFE_LIMITATION_NOTICE,),
            metadata=metadata,
        )


def create_ai_analyzer(config: AIAnalysisConfig | None = None) -> S3MBridge:
    """Factory used by backend code to keep S3M optional."""

    return S3MBridge(config=config)


def _first_text(output: Mapping[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = output.get(key)
        if value is not None:
            return str(value)
    return ""


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    try:
        return tuple(str(item) for item in value)
    except TypeError:
        return (str(value),)


__all__ = [
    "S3MBridge",
    "S3M_AVAILABLE",
    "create_ai_analyzer",
]

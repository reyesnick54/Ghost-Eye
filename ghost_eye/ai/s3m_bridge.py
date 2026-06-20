"""Bridge Ghost-Eye WiFi telemetry into the optional S3M runtime."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
import json
import os
from pathlib import Path
import queue
import sys
import threading
from typing import Any, Callable, Mapping

from ghost_eye.api.schemas import AIAnalysisResult, SAFE_LIMITATION_NOTICE


MISSION_TYPE = "ghosteye_wifi_analysis"
RULES_OF_ENGAGEMENT = "authorized_controlled_research_only"
DEFAULT_TIMEOUT_SECONDS = 15.0


def telemetry_prompt_builder(telemetry: Any) -> str:
    """Build a bounded analysis prompt from Ghost-Eye scan telemetry."""

    telemetry_payload = _to_plain_data(telemetry)
    telemetry_json = json.dumps(telemetry_payload, indent=2, sort_keys=True, default=str)
    return (
        "Analyze the following Ghost-Eye WiFi sensing telemetry for an authorized, "
        "controlled research environment only.\n\n"
        "Focus on coarse presence, motion, zone confidence, signal quality, "
        "limitations, and safe next calibration or measurement steps. "
        "Do not infer identity, sensitive traits, or private activity.\n\n"
        f"Telemetry:\n{telemetry_json}\n\n"
        "Return a concise summary, confidence from 0.0 to 1.0 when supported, "
        "limitations, and any metadata useful for auditability."
    )


class S3MBridge:
    """Optional adapter from Ghost-Eye scan telemetry to S3M UnifiedRuntime."""

    def __init__(self, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS, consensus_mode: bool = False) -> None:
        self.timeout_seconds = timeout_seconds
        self.consensus_mode = consensus_mode

    def status(self) -> dict[str, Any]:
        """Return runtime availability and environment configuration details."""

        env = self._environment()
        runtime_available = False
        error: str | None = None
        try:
            self._load_runtime()
            runtime_available = True
        except Exception as exc:  # pragma: no cover - exact import errors vary by environment.
            error = f"{type(exc).__name__}: {exc}"

        status: dict[str, Any] = {
            "available": runtime_available,
            "mode": "runtime" if runtime_available else "fallback",
            "provider": env["provider"],
            "provider_configured": bool(env["provider"]),
            "s3m_path": env["s3m_path"],
            "s3m_path_exists": env["s3m_path_exists"],
            "s3m_path_added": env["s3m_path_added"],
            "mission_type": MISSION_TYPE,
            "rules_of_engagement": RULES_OF_ENGAGEMENT,
            "consensus_mode": self.consensus_mode,
        }
        if error:
            status["error"] = error
        return status

    def analyze_scan(self, telemetry: Any) -> AIAnalysisResult:
        """Analyze scan telemetry through UnifiedRuntime, falling back safely."""

        env = self._environment()
        try:
            UnifiedRuntime, MissionRequest = self._load_runtime()
        except Exception as exc:
            return self._fallback_analysis(
                telemetry,
                reason="runtime_import_failed",
                detail=f"{type(exc).__name__}: {exc}",
                env=env,
            )

        prompt = telemetry_prompt_builder(telemetry)
        try:
            request = MissionRequest(
                mission_type=MISSION_TYPE,
                prompt=prompt,
                rules_of_engagement=RULES_OF_ENGAGEMENT,
                consensus_mode=self.consensus_mode,
            )
            runtime = self._build_runtime(UnifiedRuntime, env["provider"])
            result = _call_with_timeout(
                lambda: runtime.execute(request),
                timeout_seconds=self.timeout_seconds,
            )
        except TimeoutError as exc:
            return self._fallback_analysis(
                telemetry,
                reason="runtime_timeout",
                detail=str(exc),
                env=env,
            )
        except Exception as exc:
            return self._fallback_analysis(
                telemetry,
                reason="runtime_failed",
                detail=f"{type(exc).__name__}: {exc}",
                env=env,
            )

        return self._to_ai_analysis_result(result, telemetry=telemetry, env=env)

    def _environment(self) -> dict[str, Any]:
        provider = os.getenv("GHOSTEYE_AI_PROVIDER")
        s3m_path = os.getenv("GHOSTEYE_S3M_PATH")
        path_exists = False
        path_added = False

        if s3m_path:
            candidate = Path(s3m_path).expanduser()
            path_exists = candidate.exists()
            if path_exists:
                resolved = str(candidate.resolve())
                if resolved not in sys.path:
                    sys.path.append(resolved)
                    path_added = True

        return {
            "provider": provider,
            "s3m_path": s3m_path,
            "s3m_path_exists": path_exists,
            "s3m_path_added": path_added,
        }

    def _load_runtime(self) -> tuple[type[Any], type[Any]]:
        self._environment()
        from llm_core.unified_runtime import MissionRequest, UnifiedRuntime

        return UnifiedRuntime, MissionRequest

    def _build_runtime(self, unified_runtime_cls: type[Any], provider: str | None) -> Any:
        if provider:
            try:
                return unified_runtime_cls(provider=provider)
            except TypeError:
                pass
        return unified_runtime_cls()

    def _fallback_analysis(
        self,
        telemetry: Any,
        *,
        reason: str,
        detail: str,
        env: Mapping[str, Any],
    ) -> AIAnalysisResult:
        metadata = {
            "mode": "fallback",
            "reason": reason,
            "detail": detail,
            "provider": env.get("provider"),
            "s3m_path": env.get("s3m_path"),
            "s3m_path_exists": env.get("s3m_path_exists"),
            "mission_type": MISSION_TYPE,
            "rules_of_engagement": RULES_OF_ENGAGEMENT,
        }
        return AIAnalysisResult(
            available=False,
            model=None,
            summary=(
                "AI runtime unavailable; using Ghost-Eye's coarse WiFi telemetry "
                "without external analysis."
            ),
            confidence=_telemetry_confidence(telemetry),
            limitations=[
                SAFE_LIMITATION_NOTICE,
                "External AI analysis unavailable; interpret results as coarse telemetry only.",
            ],
            metadata=metadata,
        )

    def _to_ai_analysis_result(
        self,
        result: Any,
        *,
        telemetry: Any,
        env: Mapping[str, Any],
    ) -> AIAnalysisResult:
        if isinstance(result, AIAnalysisResult):
            result.metadata.setdefault("mode", "runtime")
            result.metadata.setdefault("provider", env.get("provider"))
            result.metadata.setdefault("mission_type", MISSION_TYPE)
            result.metadata.setdefault("rules_of_engagement", RULES_OF_ENGAGEMENT)
            return result

        result_data = _to_mapping(result)
        metadata = _metadata_from_result(result_data)
        metadata.update(
            {
                "mode": "runtime",
                "provider": env.get("provider"),
                "mission_type": MISSION_TYPE,
                "rules_of_engagement": RULES_OF_ENGAGEMENT,
                "runtime_result_type": type(result).__name__,
            }
        )

        summary = _first_present(
            result_data,
            "summary",
            "analysis",
            "response",
            "text",
            "content",
            default=str(result) if result is not None else None,
        )
        confidence = _coerce_confidence(
            _first_present(result_data, "confidence", "score", default=None)
        )
        limitations = _coerce_limitations(result_data.get("limitations"))

        return AIAnalysisResult(
            available=True,
            model=_first_present(result_data, "model", "model_name", default=env.get("provider")),
            summary=summary,
            confidence=confidence if confidence is not None else _telemetry_confidence(telemetry),
            limitations=limitations,
            metadata=metadata,
        )


def _call_with_timeout(call: Callable[[], Any], *, timeout_seconds: float) -> Any:
    if timeout_seconds <= 0:
        return call()

    results: queue.Queue[tuple[bool, Any]] = queue.Queue(maxsize=1)

    def run() -> None:
        try:
            results.put((True, call()))
        except BaseException as exc:  # Propagate runtime exceptions to the caller.
            results.put((False, exc))

    thread = threading.Thread(target=run, name="ghosteye-s3m-runtime", daemon=True)
    thread.start()
    thread.join(timeout_seconds)
    if thread.is_alive():
        raise TimeoutError(f"UnifiedRuntime did not complete within {timeout_seconds:.2f}s")

    ok, value = results.get_nowait()
    if ok:
        return value
    raise value


def _to_plain_data(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if is_dataclass(value):
        return _to_plain_data(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _to_plain_data(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_plain_data(item) for item in value]
    if hasattr(value, "model_dump"):
        return _to_plain_data(value.model_dump())
    if hasattr(value, "dict") and callable(value.dict):
        return _to_plain_data(value.dict())
    if hasattr(value, "__dict__"):
        return _to_plain_data(vars(value))
    return str(value)


def _to_mapping(result: Any) -> dict[str, Any]:
    data = _to_plain_data(result)
    if isinstance(data, Mapping):
        return dict(data)
    return {"summary": str(data)}


def _metadata_from_result(result_data: Mapping[str, Any]) -> dict[str, Any]:
    metadata = result_data.get("metadata")
    if isinstance(metadata, Mapping):
        return {str(key): _to_plain_data(value) for key, value in metadata.items()}
    return {}


def _first_present(data: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return value
    return default


def _coerce_confidence(value: Any) -> float | None:
    if value is None:
        return None
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return None
    return min(max(confidence, 0.0), 1.0)


def _telemetry_confidence(telemetry: Any) -> float | None:
    data = _to_plain_data(telemetry)
    if isinstance(data, Mapping):
        return _coerce_confidence(data.get("confidence"))
    return None


def _coerce_limitations(value: Any) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        limitations = [str(item) for item in value if item]
        if limitations:
            return limitations
    return [SAFE_LIMITATION_NOTICE]


__all__ = ["S3MBridge", "telemetry_prompt_builder"]

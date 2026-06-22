"""Optional import-safe bridge to S3M-Core."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

from app.config import get_settings


class S3MBridge:
    """Adapter that calls S3M-Core only when a compatible module is available."""

    def __init__(self) -> None:
        self._module: Any | None = None
        self._runtime: Any | None = None
        self._load_optional_runtime()

    @property
    def available(self) -> bool:
        return self._runtime is not None or self._module is not None

    def status(self) -> dict[str, Any]:
        return {
            "provider": "s3m_core" if self.available else "fallback",
            "s3m_core_available": self.available,
            "mode": "analysis_only_no_autonomy",
        }

    def analyze(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._runtime is None and self._module is None:
            raise RuntimeError("S3M-Core runtime is unavailable")

        target = self._runtime or self._module
        for method_name in ("analyze_telemetry", "analyze", "generate", "run"):
            method = getattr(target, method_name, None)
            if callable(method):
                output = method(payload)
                return _coerce_output(output)
        raise RuntimeError("S3M-Core module has no supported analysis method")

    def _load_optional_runtime(self) -> None:
        settings = get_settings()
        if settings.s3m_core_path:
            path = Path(settings.s3m_core_path).expanduser()
            if path.exists() and str(path) not in sys.path:
                sys.path.insert(0, str(path))

        for module_name in ("s3m_core", "s3m"):
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            self._module = module
            for factory_name in ("create_runtime", "Runtime", "Analyzer"):
                factory = getattr(module, factory_name, None)
                if callable(factory):
                    try:
                        self._runtime = factory()
                    except Exception:
                        self._runtime = None
                    break
            return


def _coerce_output(output: Any) -> dict[str, Any]:
    if isinstance(output, dict):
        return output
    if hasattr(output, "model_dump"):
        return output.model_dump(mode="json")
    if hasattr(output, "to_dict"):
        return output.to_dict()
    return {"summary": str(output)}

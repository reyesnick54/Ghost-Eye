"""Build bounded prompts from GhostEye telemetry for optional AI analysis."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from typing import Any


DEFAULT_MAX_PROMPT_TELEMETRY_CHARS = 4000
ALLOWED_TELEMETRY_KEYS = {
    "timestamp",
    "mode",
    "source",
    "selected_network",
    "presence",
    "motion_score",
    "zone",
    "confidence",
    "confidence_ceiling",
    "signal_quality",
    "map",
    "baseline",
    "fingerprints",
    "limitations",
    "notice",
}
SENSITIVE_KEY_PARTS = ("bssid", "mac")


def build_telemetry_prompt(
    telemetry: Mapping[str, Any],
    max_telemetry_chars: int = DEFAULT_MAX_PROMPT_TELEMETRY_CHARS,
) -> str:
    """Create a compact advisory-analysis prompt from GhostEye telemetry."""

    sanitized = sanitize_telemetry(telemetry)
    telemetry_json = json.dumps(sanitized, sort_keys=True, separators=(",", ":"), default=str)
    if len(telemetry_json) > max_telemetry_chars:
        telemetry_json = telemetry_json[:max_telemetry_chars] + "...[truncated]"

    return (
        "Analyze GhostEye WiFi-only non-CSI telemetry for signal quality and "
        "uncertainty. Provide advisory observations only for authorized controlled "
        "environments. Do not infer identity, exact person/object location, true RF "
        "imaging, or unprovided sensor data.\n\n"
        f"Telemetry JSON:\n{telemetry_json}"
    )


def build_scan_analysis_prompt(telemetry: Any) -> str:
    """Compatibility prompt helper used by older S3M bridge code."""

    return build_telemetry_prompt(_to_json_compatible(telemetry))


def sanitize_telemetry(telemetry: Mapping[str, Any]) -> dict[str, Any]:
    """Keep prompt input scoped to telemetry fields and redact local identifiers."""

    return {
        key: _sanitize_value(value, key)
        for key, value in telemetry.items()
        if key in ALLOWED_TELEMETRY_KEYS
    }


def _sanitize_value(value: Any, key: str = "") -> Any:
    lowered_key = key.lower()
    if any(part in lowered_key for part in SENSITIVE_KEY_PARTS):
        return "[redacted]"

    if isinstance(value, Mapping):
        return {
            str(child_key): _sanitize_value(child_value, str(child_key))
            for child_key, child_value in value.items()
        }

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_sanitize_value(item, key) for item in value]

    return value


def _to_json_compatible(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _to_json_compatible(asdict(value))
    if hasattr(value, "model_dump") and callable(value.model_dump):
        return _to_json_compatible(value.model_dump())
    if hasattr(value, "dict") and callable(value.dict):
        return _to_json_compatible(value.dict())
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return _to_json_compatible(value.to_dict())
    if isinstance(value, Mapping):
        return {str(key): _to_json_compatible(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_to_json_compatible(item) for item in value]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_to_json_compatible(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)

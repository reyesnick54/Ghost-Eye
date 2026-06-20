"""Build bounded prompts from GhostEye telemetry for optional AI analysis."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any


DEFAULT_MAX_PROMPT_TELEMETRY_CHARS = 4000
ALLOWED_TELEMETRY_KEYS = {
    "timestamp",
    "mode",
    "presence",
    "motion_score",
    "zone",
    "confidence",
    "notice",
    "source",
    "observation",
    "capabilities",
    "baseline",
    "disturbance",
    "fingerprint",
    "tomography",
    "adaptive_baseline",
    "confidence_ceiling",
    "session",
    "signal_quality",
    "map",
    "limitations",
}
SENSITIVE_KEY_PARTS = ("bssid", "mac", "ssid")


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
        "Analyze the following GhostEye WiFi sensing telemetry for operational "
        "health, signal quality, and uncertainty. Provide advisory observations "
        "only for authorized controlled environments. Do not infer personal "
        "identity or protected attributes.\n\n"
        f"Telemetry JSON:\n{telemetry_json}"
    )


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

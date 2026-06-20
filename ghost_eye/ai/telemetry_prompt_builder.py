"""Build bounded prompts from GhostEye telemetry for optional AI analysis."""
"""Prompt construction for S3M analysis of GhostEye telemetry."""

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
from dataclasses import asdict, is_dataclass
from typing import Any


def build_scan_analysis_prompt(telemetry: Any) -> str:
    """Build an S3M prompt for structured GhostEye scan telemetry analysis.

    The prompt deliberately anchors S3M to the serialized telemetry payload and
    repeats GhostEye's WiFi-only, authorized-use, and confidence-ceiling limits.
    """

    telemetry_json = json.dumps(
        _to_json_compatible(telemetry),
        indent=2,
        sort_keys=True,
    )

    return f"""You are S3M analyzing GhostEye scan telemetry.

Analyze only the provided GhostEye telemetry below. Do not use outside context,
assumptions, memories, hidden sensor feeds, or prior scans unless they are
explicitly present in this telemetry payload. Do not invent sensor data,
observations, CSI values, RF measurements, rooms, people, devices, coordinates,
or calibration history.

Safety and confidence requirements:
- Preserve GhostEye's authorized controlled-use language. Treat this as analysis
  for authorized controlled environments only.
- State that WiFi-only non-CSI mode is coarse and probabilistic.
- Do not increase confidence beyond the provided confidence.
- Preserve the confidence ceiling exactly as provided by the telemetry. If both
  confidence and confidence_ceiling are present, any analysis confidence must be
  less than or equal to both values. If a confidence value is missing, use null
  rather than estimating one.
- Clearly distinguish observed telemetry fields from interpretation.

Analysis requirements:
- Explain likely causes of signal disturbance using only the provided telemetry.
- Identify false-positive risks for presence, motion, zone, tomography, or
  disturbance interpretations.
- Recommend calibration or scan-quality improvements appropriate to the supplied
  mode, source, signal quality, baseline, and observations.
- Preserve limitations and notices already present in the telemetry.

Return structured JSON-compatible analysis only. Do not wrap the response in
Markdown. Use this object shape:
{{
  "summary": "string",
  "observed_fields_used": ["string"],
  "likely_signal_disturbance_causes": ["string"],
  "false_positive_risks": ["string"],
  "calibration_recommendations": ["string"],
  "scan_quality_improvements": ["string"],
  "confidence": {{
    "provided_confidence": 0.0,
    "confidence_ceiling": 0.0,
    "analysis_confidence": 0.0,
    "ceiling_preserved": true,
    "notes": ["string"]
  }},
  "limitations": ["string"],
  "authorized_use_notice": "string",
  "wifi_only_non_csi_notice": "string"
}}

Provided GhostEye telemetry:
{telemetry_json}
"""


def _to_json_compatible(value: Any) -> Any:
    """Convert common Python schema objects into JSON-compatible values."""

    if is_dataclass(value) and not isinstance(value, type):
        return _to_json_compatible(asdict(value))

    if hasattr(value, "model_dump") and callable(value.model_dump):
        return _to_json_compatible(value.model_dump())

    if hasattr(value, "dict") and callable(value.dict):
        return _to_json_compatible(value.dict())

    if hasattr(value, "to_response") and callable(value.to_response):
        return _to_json_compatible(value.to_response())

    if isinstance(value, Mapping):
        return {str(key): _to_json_compatible(item) for key, item in value.items()}

    if isinstance(value, tuple):
        return [_to_json_compatible(item) for item in value]

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_to_json_compatible(item) for item in value]

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    return str(value)

"""Classify available WiFi sensing signal capabilities.

The profiler intentionally describes *capability ceilings* instead of live
signal quality. Downstream inference should use these ceilings to avoid
overstating confidence when the source only exposes coarse RF signals.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import re
from typing import Any


@dataclass(frozen=True)
class _ModeDefinition:
    supports_rssi_scan: bool
    supports_latency_probe: bool
    supports_rtt: bool
    supports_csi: bool
    confidence_ceiling: float
    recommended_scan_mode: str
    limitations: tuple[str, ...]


class SignalCapabilityProfiler:
    """Infer sensing capabilities from a source description or capability hints."""

    SIMULATOR = "simulator"
    WIFI_ONLY_RSSI = "wifi_only_rssi"
    WIFI_ONLY_RSSI_LATENCY = "wifi_only_rssi_latency"
    WIFI_ONLY_RTT_IF_AVAILABLE = "wifi_only_rtt_if_available"
    SINGLE_ROUTER_WIFI_ONLY = "single_router_wifi_only"
    ESP32_CSI_PLACEHOLDER = "esp32_csi_placeholder"
    ROUTER_ADAPTER_PLACEHOLDER = "router_adapter_placeholder"

    CONFIDENCE_CEILINGS: dict[str, float] = {
        SIMULATOR: 0.90,
        WIFI_ONLY_RSSI_LATENCY: 0.65,
        WIFI_ONLY_RSSI: 0.50,
        SINGLE_ROUTER_WIFI_ONLY: 0.40,
        WIFI_ONLY_RTT_IF_AVAILABLE: 0.80,
        ESP32_CSI_PLACEHOLDER: 0.95,
        ROUTER_ADAPTER_PLACEHOLDER: 0.55,
    }

    _MODE_DEFINITIONS: dict[str, _ModeDefinition] = {
        SIMULATOR: _ModeDefinition(
            supports_rssi_scan=False,
            supports_latency_probe=False,
            supports_rtt=False,
            supports_csi=False,
            confidence_ceiling=CONFIDENCE_CEILINGS[SIMULATOR],
            recommended_scan_mode="simulated_scan",
            limitations=(
                "Synthetic readings only; no live RF channel is observed.",
                "Hardware noise, multipath, and device-specific behavior are not represented.",
            ),
        ),
        WIFI_ONLY_RSSI: _ModeDefinition(
            supports_rssi_scan=True,
            supports_latency_probe=False,
            supports_rtt=False,
            supports_csi=False,
            confidence_ceiling=CONFIDENCE_CEILINGS[WIFI_ONLY_RSSI],
            recommended_scan_mode="rssi_scan",
            limitations=(
                "RSSI is coarse and highly sensitive to orientation and interference.",
                "No latency, RTT, or CSI features are available for distance refinement.",
            ),
        ),
        WIFI_ONLY_RSSI_LATENCY: _ModeDefinition(
            supports_rssi_scan=True,
            supports_latency_probe=True,
            supports_rtt=False,
            supports_csi=False,
            confidence_ceiling=CONFIDENCE_CEILINGS[WIFI_ONLY_RSSI_LATENCY],
            recommended_scan_mode="rssi_latency_scan",
            limitations=(
                "Latency probes are noisy and can reflect network load instead of motion.",
                "No fine-grained RTT or CSI features are available.",
            ),
        ),
        WIFI_ONLY_RTT_IF_AVAILABLE: _ModeDefinition(
            supports_rssi_scan=True,
            supports_latency_probe=True,
            supports_rtt=True,
            supports_csi=False,
            confidence_ceiling=CONFIDENCE_CEILINGS[WIFI_ONLY_RTT_IF_AVAILABLE],
            recommended_scan_mode="rtt_augmented_wifi_scan",
            limitations=(
                "RTT depends on device and access point support for FTM/802.11mc.",
                "No CSI features are available for subcarrier-level inference.",
            ),
        ),
        SINGLE_ROUTER_WIFI_ONLY: _ModeDefinition(
            supports_rssi_scan=True,
            supports_latency_probe=False,
            supports_rtt=False,
            supports_csi=False,
            confidence_ceiling=CONFIDENCE_CEILINGS[SINGLE_ROUTER_WIFI_ONLY],
            recommended_scan_mode="single_router_rssi_scan",
            limitations=(
                "Single-router visibility limits spatial discrimination.",
                "No latency, RTT, CSI, or multi-access-point corroboration is available.",
            ),
        ),
        ESP32_CSI_PLACEHOLDER: _ModeDefinition(
            supports_rssi_scan=False,
            supports_latency_probe=False,
            supports_rtt=False,
            supports_csi=True,
            confidence_ceiling=CONFIDENCE_CEILINGS[ESP32_CSI_PLACEHOLDER],
            recommended_scan_mode="csi_capture_placeholder",
            limitations=(
                "ESP32 CSI support is a placeholder until a live capture adapter is wired in.",
                "Capability indicates expected CSI availability, not validated sample quality.",
            ),
        ),
        ROUTER_ADAPTER_PLACEHOLDER: _ModeDefinition(
            supports_rssi_scan=True,
            supports_latency_probe=False,
            supports_rtt=False,
            supports_csi=False,
            confidence_ceiling=CONFIDENCE_CEILINGS[ROUTER_ADAPTER_PLACEHOLDER],
            recommended_scan_mode="router_adapter_scan_placeholder",
            limitations=(
                "Router adapter support is a placeholder until router telemetry is integrated.",
                "Available metrics depend on router firmware and client association state.",
            ),
        ),
    }

    SUPPORTED_MODES: tuple[str, ...] = tuple(_MODE_DEFINITIONS)

    _MODE_ALIASES: dict[str, str] = {
        SIMULATOR: SIMULATOR,
        "demo": SIMULATOR,
        "simulated": SIMULATOR,
        "simulated_demo": SIMULATOR,
        "simulation": SIMULATOR,
        WIFI_ONLY_RSSI: WIFI_ONLY_RSSI,
        "rssi": WIFI_ONLY_RSSI,
        "rssi_only": WIFI_ONLY_RSSI,
        "wifi": WIFI_ONLY_RSSI,
        "wifi_only": WIFI_ONLY_RSSI,
        "wifi_rssi": WIFI_ONLY_RSSI,
        "wifi_rssi_only": WIFI_ONLY_RSSI,
        WIFI_ONLY_RSSI_LATENCY: WIFI_ONLY_RSSI_LATENCY,
        "latency": WIFI_ONLY_RSSI_LATENCY,
        "rssi_latency": WIFI_ONLY_RSSI_LATENCY,
        "wifi_latency": WIFI_ONLY_RSSI_LATENCY,
        "wifi_only_latency": WIFI_ONLY_RSSI_LATENCY,
        "wifi_rssi_latency": WIFI_ONLY_RSSI_LATENCY,
        WIFI_ONLY_RTT_IF_AVAILABLE: WIFI_ONLY_RTT_IF_AVAILABLE,
        "ftm": WIFI_ONLY_RTT_IF_AVAILABLE,
        "rtt": WIFI_ONLY_RTT_IF_AVAILABLE,
        "wifi_ftm": WIFI_ONLY_RTT_IF_AVAILABLE,
        "wifi_only_rtt": WIFI_ONLY_RTT_IF_AVAILABLE,
        "wifi_rtt": WIFI_ONLY_RTT_IF_AVAILABLE,
        SINGLE_ROUTER_WIFI_ONLY: SINGLE_ROUTER_WIFI_ONLY,
        "one_router": SINGLE_ROUTER_WIFI_ONLY,
        "single_ap": SINGLE_ROUTER_WIFI_ONLY,
        "single_access_point": SINGLE_ROUTER_WIFI_ONLY,
        "single_router": SINGLE_ROUTER_WIFI_ONLY,
        "single_router_wifi": SINGLE_ROUTER_WIFI_ONLY,
        ESP32_CSI_PLACEHOLDER: ESP32_CSI_PLACEHOLDER,
        "csi": ESP32_CSI_PLACEHOLDER,
        "esp32": ESP32_CSI_PLACEHOLDER,
        "esp32_csi": ESP32_CSI_PLACEHOLDER,
        "esp_csi": ESP32_CSI_PLACEHOLDER,
        ROUTER_ADAPTER_PLACEHOLDER: ROUTER_ADAPTER_PLACEHOLDER,
        "openwrt": ROUTER_ADAPTER_PLACEHOLDER,
        "router": ROUTER_ADAPTER_PLACEHOLDER,
        "router_adapter": ROUTER_ADAPTER_PLACEHOLDER,
        "router_integration": ROUTER_ADAPTER_PLACEHOLDER,
    }

    _EXPLICIT_MODE_KEYS = (
        "mode",
        "scan_mode",
        "source_mode",
        "capability_mode",
        "recommended_mode",
    )

    _TEXT_KEYS = (
        "adapter",
        "adapter_type",
        "device",
        "device_type",
        "driver",
        "kind",
        "name",
        "provider",
        "source",
        "source_type",
        "type",
    )

    def profile(self, source: Any = None, **hints: Any) -> dict[str, Any]:
        """Return a capability profile for ``source``.

        ``source`` may be a mode string, a descriptive string, a mapping of
        capability hints, or an object exposing common source attributes. Keyword
        hints are merged on top of the source description.
        """

        source_info = self._coerce_source(source)
        source_info.update(hints)
        mode = self._classify_mode(source_info)
        return self.profile_for_mode(mode)

    def classify(self, source: Any = None, **hints: Any) -> dict[str, Any]:
        """Alias for :meth:`profile` for call sites that use classification terms."""

        return self.profile(source, **hints)

    def profile_source(self, source: Any = None, **hints: Any) -> dict[str, Any]:
        """Alias for :meth:`profile` for call sites that use source terms."""

        return self.profile(source, **hints)

    def profile_for_mode(self, mode: str) -> dict[str, Any]:
        """Return the canonical profile for a supported mode."""

        canonical_mode = self._canonical_mode(mode)
        if canonical_mode is None or canonical_mode not in self._MODE_DEFINITIONS:
            supported = ", ".join(self.SUPPORTED_MODES)
            raise ValueError(f"Unsupported signal capability mode {mode!r}; expected one of: {supported}")

        definition = self._MODE_DEFINITIONS[canonical_mode]
        return {
            "mode": canonical_mode,
            "supports_rssi_scan": definition.supports_rssi_scan,
            "supports_latency_probe": definition.supports_latency_probe,
            "supports_rtt": definition.supports_rtt,
            "supports_csi": definition.supports_csi,
            "confidence_ceiling": definition.confidence_ceiling,
            "recommended_scan_mode": definition.recommended_scan_mode,
            "limitations": list(definition.limitations),
        }

    def _classify_mode(self, source_info: Mapping[str, Any]) -> str:
        for key in self._EXPLICIT_MODE_KEYS:
            canonical_mode = self._canonical_mode(source_info.get(key))
            if canonical_mode is not None:
                return canonical_mode

        if self._flag(source_info, "is_simulator", "simulator", "simulated"):
            return self.SIMULATOR

        text = self._normalized_source_text(source_info)
        if self._text_matches(text, "simulator", "simulated", "simulation", "simulated_demo"):
            return self.SIMULATOR

        if self._flag(source_info, "supports_csi", "has_csi", "csi_available"):
            return self.ESP32_CSI_PLACEHOLDER
        if self._text_matches(text, "esp32_csi", "esp32", "esp_csi", "csi"):
            return self.ESP32_CSI_PLACEHOLDER

        if self._flag(source_info, "router_adapter", "has_router_adapter"):
            return self.ROUTER_ADAPTER_PLACEHOLDER
        if self._text_matches(text, "router_adapter", "router_integration", "openwrt"):
            return self.ROUTER_ADAPTER_PLACEHOLDER

        if self._flag(source_info, "supports_rtt", "has_rtt", "rtt_available", "ftm_available"):
            return self.WIFI_ONLY_RTT_IF_AVAILABLE
        if self._text_matches(text, "wifi_only_rtt_if_available", "wifi_only_rtt", "wifi_rtt", "rtt", "ftm"):
            return self.WIFI_ONLY_RTT_IF_AVAILABLE

        if self._single_router(source_info):
            return self.SINGLE_ROUTER_WIFI_ONLY
        if self._text_matches(text, "single_router_wifi_only", "single_router", "single_ap", "one_router"):
            return self.SINGLE_ROUTER_WIFI_ONLY

        if self._flag(source_info, "supports_latency_probe", "has_latency_probe", "latency_probe_available"):
            return self.WIFI_ONLY_RSSI_LATENCY
        if self._text_matches(text, "wifi_only_rssi_latency", "wifi_rssi_latency", "rssi_latency", "wifi_latency", "latency"):
            return self.WIFI_ONLY_RSSI_LATENCY

        if self._flag(source_info, "supports_rssi_scan", "has_rssi", "rssi_available"):
            return self.WIFI_ONLY_RSSI
        if self._text_matches(text, "wifi_only_rssi", "wifi_rssi", "rssi_only", "rssi", "wifi_only", "wifi"):
            return self.WIFI_ONLY_RSSI

        return self.SIMULATOR

    def _coerce_source(self, source: Any) -> dict[str, Any]:
        if source is None:
            return {}
        if isinstance(source, str):
            return {"source": source}
        if isinstance(source, Mapping):
            return dict(source)

        source_info: dict[str, Any] = {}
        for key in (*self._EXPLICIT_MODE_KEYS, *self._TEXT_KEYS):
            if hasattr(source, key):
                source_info[key] = getattr(source, key)

        for key in (
            "access_point_count",
            "ap_count",
            "router_count",
            "supports_csi",
            "supports_latency_probe",
            "supports_rssi_scan",
            "supports_rtt",
        ):
            if hasattr(source, key):
                source_info[key] = getattr(source, key)

        if not source_info:
            source_info["source"] = str(source)
        return source_info

    def _canonical_mode(self, value: Any) -> str | None:
        if value is None:
            return None
        token = self._normalize(value)
        return self._MODE_ALIASES.get(token)

    def _normalized_source_text(self, source_info: Mapping[str, Any]) -> str:
        parts: list[str] = []
        for key in self._TEXT_KEYS:
            value = source_info.get(key)
            if value is not None:
                parts.append(str(value))

        for key, value in source_info.items():
            if key in self._EXPLICIT_MODE_KEYS or key in self._TEXT_KEYS:
                continue
            if self._truthy(value):
                parts.append(str(key))
                if not isinstance(value, bool):
                    parts.append(str(value))

        return " ".join(self._normalize(part) for part in parts if str(part).strip())

    def _text_matches(self, normalized_text: str, *aliases: str) -> bool:
        if not normalized_text:
            return False
        text_tokens = set(normalized_text.split())
        for alias in aliases:
            token = self._normalize(alias)
            if token in text_tokens or token in normalized_text:
                return True
        return False

    def _flag(self, source_info: Mapping[str, Any], *keys: str) -> bool:
        return any(self._truthy(source_info.get(key)) for key in keys)

    def _single_router(self, source_info: Mapping[str, Any]) -> bool:
        for key in ("router_count", "ap_count", "access_point_count"):
            count = self._int_or_none(source_info.get(key))
            if count == 1:
                return True
        return False

    def _truthy(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on", "available", "supported"}
        return bool(value)

    def _int_or_none(self, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, bool):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _normalize(self, value: Any) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower())
        return normalized.strip("_")

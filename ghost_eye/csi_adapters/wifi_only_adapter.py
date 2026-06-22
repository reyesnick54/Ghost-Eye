"""WiFi-only adapter facade for GhostEye live RSSI/latency sensing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Protocol, Union

from ghost_eye.api.schemas import (
    LIMITATIONS,
    MODE_WIFI_ONLY_NON_CSI,
    SOURCE_LOCAL_WIFI_LIVE,
    SOURCE_LOCAL_WIFI_SIMULATED,
)
from ghost_eye.wifi.live_observation import LiveObservationCollector

from .simulator_adapter import (
    WIFI_ONLY_NON_CSI_MODE,
    WiFiSignalObservation,
    WiFiSignalSimulatorAdapter,
)


ObservationSource = Callable[[], Union[WiFiSignalObservation, Dict[str, Any]]]


@dataclass(frozen=True)
class WifiObservationBatch:
    """Compatibility wrapper for older batch-oriented imports."""

    observation: WiFiSignalObservation


class WifiObservationProvider(Protocol):
    """Protocol implemented by WiFi observation providers."""

    def get_observation(self) -> WiFiSignalObservation:
        """Collect one WiFi-only observation."""


class WiFiOnlyAdapter:
    """Produce WiFi RSSI observations while explicitly avoiding CSI capture."""

    adapter_name = "wifi_only_non_csi"
    mode = WIFI_ONLY_NON_CSI_MODE
    is_csi_adapter = False
    confidence_ceiling = 0.65

    def __init__(
        self,
        simulated: bool = True,
        simulator: Optional[WiFiSignalSimulatorAdapter] = None,
        scanner: Optional[ObservationSource] = None,
        live_collector: Optional[LiveObservationCollector] = None,
        prefer_live: bool = True,
        **simulator_kwargs: Any,
    ) -> None:
        self.simulated = simulated
        self._scanner = scanner
        self._simulator = simulator or WiFiSignalSimulatorAdapter(**simulator_kwargs)
        self._live_collector = live_collector or LiveObservationCollector()
        self._selected_source_id = SOURCE_LOCAL_WIFI_LIVE if prefer_live else SOURCE_LOCAL_WIFI_SIMULATED
        self._last_source_id = SOURCE_LOCAL_WIFI_SIMULATED
        self._selected_wifi_ssid = getattr(self._simulator, "ssid", "GhostEye-Simulated")
        self._last_live_normalized: dict[str, Any] | None = None
        self._last_live_error: str | None = None

    def get_live_observation(self) -> WiFiSignalObservation | None:
        """Return one live WiFi observation, or ``None`` when unavailable."""

        try:
            snapshot = self._live_collector.collect()
        except Exception as exc:
            self._last_live_error = f"live_collector:{exc.__class__.__name__}"
            self._last_live_normalized = {
                "available": False,
                "ssid": "unknown",
                "vendor_hint": "unknown",
                "live_error": self._last_live_error,
            }
            return None

        self._last_live_normalized = dict(snapshot.normalized)
        if not snapshot.normalized.get("available"):
            self._last_live_error = str(snapshot.normalized.get("live_error") or "live_wifi_unavailable")
            return None
        self._last_live_error = None
        self._selected_wifi_ssid = str(snapshot.normalized.get("ssid") or self._selected_wifi_ssid)
        return snapshot.observation

    def get_sources(self) -> list[dict[str, Any]]:
        """Return available sources for the API."""

        live_available = self.live_available()
        live_status = self._last_live_normalized or {}
        current_ssid = live_status.get("ssid") if live_status.get("ssid") != "unknown" else None
        vendor_hint = live_status.get("vendor_hint") or "unknown"

        return [
            {
                "id": SOURCE_LOCAL_WIFI_LIVE,
                "name": "Local live WiFi RSSI + gateway latency",
                "mode": self.mode,
                "type": "wifi_rssi_latency",
                "simulated": False,
                "live": True,
                "available": live_available,
                "selected": self._selected_source_id == SOURCE_LOCAL_WIFI_LIVE,
                "current_ssid": current_ssid,
                "vendor_hint": vendor_hint,
                "confidence_ceiling": self.confidence_ceiling,
                "capabilities": ["current_ssid", "rssi", "noise", "channel", "tx_rate", "gateway_latency", "jitter", "packet_loss"],
                "csi": False,
                "can_use_as_csi_sensor": False,
                "limitations": LIMITATIONS,
                "status": "available" if live_available else "unavailable",
            },
            {
                "id": SOURCE_LOCAL_WIFI_SIMULATED,
                "name": "Local WiFi RSSI + gateway latency simulator",
                "mode": self.mode,
                "type": "wifi_rssi_latency",
                "simulated": True,
                "live": False,
                "available": True,
                "selected": self._selected_source_id == SOURCE_LOCAL_WIFI_SIMULATED,
                "selected_wifi_ssid": self._selected_wifi_ssid,
                "confidence_ceiling": self.confidence_ceiling,
                "capabilities": ["rssi_scan", "gateway_latency", "jitter", "packet_loss"],
                "csi": False,
                "can_use_as_csi_sensor": False,
                "limitations": "Ordinary WiFi APIs do not provide raw CSI in this mode.",
                "status": "available",
            },
        ]

    def sources(self) -> list[dict[str, Any]]:
        """Compatibility alias for the API."""

        return self.get_sources()

    def get_selected_source(self) -> dict[str, Any]:
        """Return the currently selected source descriptor."""

        selected = next((source for source in self.get_sources() if source["id"] == self._selected_source_id), None)
        if selected is None:
            return self.get_sources()[0]
        return selected

    def get_selected_source_id(self) -> str:
        """Return the source used for the most recent observation."""

        return self._last_source_id

    def get_preferred_source_id(self) -> str:
        """Return the configured source preference before live fallback."""

        return self._selected_source_id

    def select_source(self, source_id: str) -> dict[str, Any]:
        """Select a configured source by ID."""

        source_id = str(source_id).strip()
        valid = {SOURCE_LOCAL_WIFI_LIVE, SOURCE_LOCAL_WIFI_SIMULATED}
        if source_id not in valid:
            raise ValueError(f"Unknown source: {source_id}")
        self._selected_source_id = source_id
        return {**self.get_selected_source(), "selected": True}

    def select_wifi_environment(self, ssid: str) -> dict[str, Any]:
        """Set the selected WiFi environment label without enabling CSI capture."""

        selected_ssid = str(ssid).strip()
        if not selected_ssid:
            raise ValueError("ssid must not be empty")
        self._selected_wifi_ssid = selected_ssid
        if hasattr(self._simulator, "select_environment"):
            self._simulator.select_environment(selected_ssid)
        return {
            "ssid": selected_ssid,
            "mode": self.mode,
            "csi": False,
            "can_use_as_csi_sensor": False,
        }

    def get_capability_profile(self) -> dict[str, Any]:
        """Return source capabilities and the non-CSI confidence ceiling."""

        return {
            "mode": MODE_WIFI_ONLY_NON_CSI,
            "selected_source": self._selected_source_id,
            "last_source": self._last_source_id,
            "live_available": self.live_available(),
            "supports_rssi_scan": True,
            "supports_gateway_latency": True,
            "supports_csi": False,
            "confidence_ceiling": self.confidence_ceiling,
            "limitations": LIMITATIONS,
        }

    def live_available(self) -> bool:
        """Return whether the live source currently has usable WiFi data."""

        if self._last_live_normalized and self._last_live_normalized.get("available"):
            return True
        try:
            snapshot = self._live_collector.collect()
        except Exception as exc:
            self._last_live_error = f"live_collector:{exc.__class__.__name__}"
            self._last_live_normalized = {
                "available": False,
                "ssid": "unknown",
                "vendor_hint": "unknown",
                "live_error": self._last_live_error,
            }
            return False
        self._last_live_normalized = dict(snapshot.normalized)
        if self._last_live_normalized.get("available"):
            self._last_live_error = None
            return True
        self._last_live_error = str(self._last_live_normalized.get("live_error") or "live_wifi_unavailable")
        return False

    def get_live_status(self) -> dict[str, Any]:
        """Return the latest live normalized measurement if available."""

        status = dict(self._last_live_normalized or {})
        if self._last_live_error and not status.get("live_error"):
            status["live_error"] = self._last_live_error
        return status

    def get_live_error(self) -> str | None:
        """Return the latest live-source failure reason, if any."""

        return self._last_live_error

    def get_observation(self) -> WiFiSignalObservation:
        """Return one WiFi-only, non-CSI signal observation."""

        if self._selected_source_id == SOURCE_LOCAL_WIFI_LIVE:
            live_observation = self.get_live_observation()
            if live_observation is not None:
                self._validate_mode(live_observation)
                self._last_source_id = SOURCE_LOCAL_WIFI_LIVE
                return live_observation

        if not self.simulated and self._scanner is not None:
            observation = self._scanner()
            normalized = observation if isinstance(observation, WiFiSignalObservation) else WiFiSignalObservation(**observation)
            self._validate_mode(normalized)
            self._last_source_id = self._selected_source_id
            return normalized

        simulated_observation = self._simulator.get_observation()
        self._validate_mode(simulated_observation)
        self._last_source_id = SOURCE_LOCAL_WIFI_SIMULATED
        return simulated_observation

    def observe(self) -> WiFiSignalObservation:
        """Compatibility alias for older backend code."""

        return self.get_observation()

    def collect(self) -> WifiObservationBatch:
        """Compatibility batch wrapper."""

        return WifiObservationBatch(observation=self.get_observation())

    @staticmethod
    def _validate_mode(observation: WiFiSignalObservation) -> None:
        if observation.mode != WIFI_ONLY_NON_CSI_MODE:
            raise ValueError("WiFiOnlyAdapter only supports wifi_only_non_csi observations")


WifiOnlyAdapter = WiFiOnlyAdapter

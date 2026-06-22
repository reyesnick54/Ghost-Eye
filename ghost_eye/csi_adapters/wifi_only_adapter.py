"""WiFi-only adapter facade for GhostEye v0.2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Protocol, Union

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

    def __init__(
        self,
        simulated: bool = True,
        simulator: Optional[WiFiSignalSimulatorAdapter] = None,
        scanner: Optional[ObservationSource] = None,
        **simulator_kwargs: Any,
    ) -> None:
        if not simulated and scanner is None:
            raise ValueError("A scanner callback is required when simulated is False")

        self.simulated = simulated
        self._scanner = scanner
        self._simulator = simulator or WiFiSignalSimulatorAdapter(**simulator_kwargs)
        self._selected_source_id = "local_wifi_rssi_latency_simulated"
        self._selected_wifi_ssid = getattr(self._simulator, "ssid", "GhostEye-Simulated")

    def sources(self) -> list[dict[str, Any]]:
        """Return available sources for the API."""

        return [
            {
                "id": "local_wifi_rssi_latency_simulated",
                "name": "Local WiFi RSSI + gateway latency simulator",
                "mode": self.mode,
                "type": "wifi_rssi_latency",
                "simulated": self.simulated,
                "selected": self._selected_source_id == "local_wifi_rssi_latency_simulated",
                "capabilities": ["rssi_scan", "gateway_latency", "jitter", "packet_loss"],
                "csi": False,
                "can_use_as_csi_sensor": False,
                "selected_wifi_ssid": self._selected_wifi_ssid,
                "limitations": "Ordinary WiFi APIs do not provide raw CSI in this mode.",
                "status": "available",
            }
        ]

    def select_source(self, source_id: str) -> dict[str, Any]:
        """Select a configured source by ID."""

        for source in self.sources():
            if source["id"] == source_id:
                self._selected_source_id = source_id
                return {**source, "selected": True}
        raise ValueError(f"Unknown source: {source_id}")

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

    def get_observation(self) -> WiFiSignalObservation:
        """Return one WiFi-only, non-CSI signal observation."""

        if self.simulated:
            return self._simulator.get_observation()

        assert self._scanner is not None
        observation = self._scanner()
        if isinstance(observation, WiFiSignalObservation):
            self._validate_mode(observation)
            return observation

        normalized = WiFiSignalObservation(**observation)
        self._validate_mode(normalized)
        return normalized

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

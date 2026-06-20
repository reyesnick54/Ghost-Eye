"""Adapter interfaces for GhostEye WiFi-only sensing inputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Protocol

from ghost_eye.wifi.gateway_probe import GatewayProbeResult
from ghost_eye.wifi.wifi_scan import WifiNetwork, WifiScan, parse_wifi_networks


@dataclass(frozen=True)
class WifiObservationBatch:
    """Collected WiFi observations and optional gateway probe summary."""

    scan: WifiScan
    gateway_probe: GatewayProbeResult | None = None


class WifiObservationProvider(Protocol):
    """Protocol implemented by concrete WiFi observation adapters."""

    def collect(self) -> WifiObservationBatch:
        """Collect a batch of WiFi-only observations."""


class WifiOnlyAdapter:
    """Base adapter for sources that provide RSSI observations."""

    source = "wifi_only"

    def from_rows(
        self,
        rows: Iterable[WifiNetwork | Mapping[str, object]],
        gateway_probe: GatewayProbeResult | None = None,
    ) -> WifiObservationBatch:
        return WifiObservationBatch(
            scan=WifiScan(
                networks=tuple(parse_wifi_networks(rows)),
                source=self.source,
            ),
            gateway_probe=gateway_probe,
        )

    def collect(self) -> WifiObservationBatch:
        return self.from_rows(())
"""Compatibility adapter for WiFi-only, non-CSI signal observations."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Union

from .simulator_adapter import (
    WIFI_ONLY_NON_CSI_MODE,
    WiFiSignalObservation,
    WiFiSignalSimulatorAdapter,
)


ObservationSource = Callable[[], Union[WiFiSignalObservation, Dict[str, Any]]]


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

    @staticmethod
    def _validate_mode(observation: WiFiSignalObservation) -> None:
        if observation.mode != WIFI_ONLY_NON_CSI_MODE:
            raise ValueError("WiFiOnlyAdapter only supports wifi_only_non_csi observations")

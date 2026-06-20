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

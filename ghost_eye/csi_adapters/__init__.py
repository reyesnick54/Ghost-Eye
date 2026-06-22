"""Adapters for GhostEye signal sources."""

try:  # Optional placeholders kept for compatibility with earlier imports.
    from .esp32_csi_adapter import Esp32CsiAdapter
except Exception:  # pragma: no cover
    Esp32CsiAdapter = None  # type: ignore[assignment]

try:
    from .router_adapter import RouterAdapter
except Exception:  # pragma: no cover
    RouterAdapter = None  # type: ignore[assignment]

from .simulator_adapter import (
    WIFI_ONLY_NON_CSI_MODE,
    SimulatedAccessPoint,
    SimulatorAdapter,
    WiFiSignalObservation,
    WiFiSignalSimulatorAdapter,
)
from .wifi_only_adapter import (
    SOURCE_LOCAL_WIFI_LIVE,
    SOURCE_LOCAL_WIFI_SIMULATED,
    WiFiOnlyAdapter,
    WifiObservationBatch,
    WifiObservationProvider,
)

__all__ = [
    "Esp32CsiAdapter",
    "RouterAdapter",
    "WIFI_ONLY_NON_CSI_MODE",
    "SimulatedAccessPoint",
    "SimulatorAdapter",
    "SOURCE_LOCAL_WIFI_LIVE",
    "SOURCE_LOCAL_WIFI_SIMULATED",
    "WiFiOnlyAdapter",
    "WiFiSignalObservation",
    "WiFiSignalSimulatorAdapter",
    "WifiObservationBatch",
    "WifiObservationProvider",
]

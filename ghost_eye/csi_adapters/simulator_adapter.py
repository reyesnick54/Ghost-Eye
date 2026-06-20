"""Deterministic simulator adapter for WiFi-only GhostEye demos."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from ghost_eye.wifi.wifi_scan import WifiNetwork

from .wifi_only_adapter import WifiObservationBatch, WifiOnlyAdapter


@dataclass(frozen=True)
class SimulatedAccessPoint:
    """Configured access point for simulated RSSI scans."""

    ssid: str
    bssid: str
    baseline_rssi_dbm: float
    channel: int


class SimulatorAdapter(WifiOnlyAdapter):
    """Produces repeatable RSSI scans for local development and tests."""

    source = "simulator"

    def __init__(
        self,
        access_points: tuple[SimulatedAccessPoint, ...] | None = None,
        seed: int = 7,
    ) -> None:
        self._random = Random(seed)
        self._access_points = access_points or (
            SimulatedAccessPoint("ghosteye-a", "02:00:00:00:00:01", -48.0, 1),
            SimulatedAccessPoint("ghosteye-b", "02:00:00:00:00:02", -61.0, 6),
            SimulatedAccessPoint("ghosteye-c", "02:00:00:00:00:03", -72.0, 11),
        )

    def collect(self) -> WifiObservationBatch:
        networks = []
        for ap in self._access_points:
            jitter = self._random.uniform(-2.5, 2.5)
            networks.append(
                WifiNetwork(
                    ssid=ap.ssid,
                    bssid=ap.bssid,
                    rssi_dbm=ap.baseline_rssi_dbm + jitter,
                    channel=ap.channel,
                    metadata={"simulated": True},
                )
            )
        return self.from_rows(networks)

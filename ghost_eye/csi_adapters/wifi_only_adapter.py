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

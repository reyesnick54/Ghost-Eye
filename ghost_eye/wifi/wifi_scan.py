"""WiFi scan data structures for GhostEye-owned sensing pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any, Callable, Iterable, Mapping


@dataclass(frozen=True)
class WifiNetwork:
    """A single access point observation from a WiFi scan."""

    ssid: str
    bssid: str
    rssi_dbm: float
    channel: int | None = None
    frequency_mhz: int | None = None
    security: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WifiScan:
    """A timestamped collection of nearby WiFi network observations."""

    networks: tuple[WifiNetwork, ...]
    timestamp: float = field(default_factory=time)
    source: str = "wifi_scan"

    def strongest(self, limit: int = 5) -> tuple[WifiNetwork, ...]:
        """Return the strongest access-point observations in this scan."""

        return tuple(
            sorted(self.networks, key=lambda network: network.rssi_dbm, reverse=True)[
                :limit
            ]
        )

    def by_bssid(self) -> dict[str, WifiNetwork]:
        """Index observations by normalized BSSID."""

        return {network.bssid.lower(): network for network in self.networks}


class WifiScanner:
    """Wraps a platform-specific scan provider without owning OS integration."""

    def __init__(
        self,
        scan_provider: Callable[[], Iterable[WifiNetwork | Mapping[str, Any]]] | None = None,
    ) -> None:
        self._scan_provider = scan_provider

    def scan(self, source: str = "wifi_scan") -> WifiScan:
        """Run the configured scan provider and return normalized scan rows."""

        if self._scan_provider is None:
            return WifiScan(networks=(), source=source)

        return WifiScan(
            networks=tuple(parse_wifi_networks(self._scan_provider())),
            source=source,
        )


def parse_wifi_networks(
    rows: Iterable[WifiNetwork | Mapping[str, Any]],
) -> list[WifiNetwork]:
    """Convert provider rows into ``WifiNetwork`` objects."""

    networks: list[WifiNetwork] = []
    for row in rows:
        if isinstance(row, WifiNetwork):
            networks.append(row)
            continue

        networks.append(
            WifiNetwork(
                ssid=str(row.get("ssid", "")),
                bssid=str(row.get("bssid", "")).lower(),
                rssi_dbm=float(row.get("rssi_dbm", row.get("rssi", -100.0))),
                channel=_optional_int(row.get("channel")),
                frequency_mhz=_optional_int(row.get("frequency_mhz")),
                security=_optional_str(row.get("security")),
                metadata=dict(row.get("metadata", {})),
            )
        )
    return networks


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)

"""Router telemetry adapter for WiFi-only GhostEye observations."""

from __future__ import annotations

from typing import Iterable, Mapping

from .wifi_only_adapter import WifiObservationBatch, WifiOnlyAdapter


class RouterAdapter(WifiOnlyAdapter):
    """Normalizes router scan or station telemetry into GhostEye scan rows."""

    source = "router"

    def __init__(self, telemetry_rows: Iterable[Mapping[str, object]] = ()) -> None:
        self._telemetry_rows = list(telemetry_rows)

    def collect(self) -> WifiObservationBatch:
        rows = []
        for row in self._telemetry_rows:
            rows.append(
                {
                    "ssid": row.get("ssid", row.get("network", "")),
                    "bssid": row.get("bssid", row.get("ap_mac", "")),
                    "rssi_dbm": row.get("rssi_dbm", row.get("signal_dbm", -100.0)),
                    "channel": row.get("channel"),
                    "frequency_mhz": row.get("frequency_mhz"),
                    "security": row.get("security"),
                    "metadata": {
                        "adapter": self.source,
                        "client_count": row.get("client_count"),
                    },
                }
            )
        return self.from_rows(rows)

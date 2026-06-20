"""ESP32 telemetry adapter for GhostEye WiFi-only RSSI observations."""

from __future__ import annotations

from typing import Iterable, Mapping

from .wifi_only_adapter import WifiObservationBatch, WifiOnlyAdapter


class Esp32CsiAdapter(WifiOnlyAdapter):
    """Converts ESP32 CSI-node telemetry into WiFi-only RSSI observations.

    The adapter intentionally keeps only WiFi RSSI metadata. Raw CSI processing
    remains outside this GhostEye-owned integration layer.
    """

    source = "esp32_csi"

    def __init__(self, telemetry_rows: Iterable[Mapping[str, object]] = ()) -> None:
        self._telemetry_rows = list(telemetry_rows)

    def collect(self) -> WifiObservationBatch:
        rows = []
        for row in self._telemetry_rows:
            rows.append(
                {
                    "ssid": row.get("ssid", ""),
                    "bssid": row.get("bssid", row.get("mac", "")),
                    "rssi_dbm": row.get("rssi_dbm", row.get("rssi", -100.0)),
                    "channel": row.get("channel"),
                    "metadata": {
                        "adapter": self.source,
                        "device_id": row.get("device_id"),
                    },
                }
            )
        return self.from_rows(rows)

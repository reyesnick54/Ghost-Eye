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
"""Simulation source for WiFi-only, non-CSI observations.

This module intentionally models RSSI/scan metadata only. It does not expose
channel state information (CSI), raw frames, monitor mode capture, or hardware
specific access.
"""

from __future__ import annotations

import math
import platform as platform_module
import random
import statistics
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Literal, Optional


WIFI_ONLY_NON_CSI_MODE = "wifi_only_non_csi"


@dataclass(frozen=True)
class WiFiSignalObservation:
    """A single WiFi-only signal observation without CSI data."""

    timestamp: float
    ssid: str
    bssid_count: int
    visible_access_points: List[Dict[str, Any]]
    rssi_vector: List[float]
    mean_rssi: float
    rssi_std: float
    gateway_latency_ms: float
    jitter_ms: float
    packet_loss: float
    scan_stability: float
    platform: str
    mode: Literal["wifi_only_non_csi"] = WIFI_ONLY_NON_CSI_MODE

    def __post_init__(self) -> None:
        if self.mode != WIFI_ONLY_NON_CSI_MODE:
            raise ValueError("WiFiSignalObservation mode must be wifi_only_non_csi")

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


class WiFiSignalSimulatorAdapter:
    """Generate realistic-enough WiFi RSSI observations for v0.1 backends."""

    mode = WIFI_ONLY_NON_CSI_MODE

    def __init__(
        self,
        ssid: str = "GhostEye-Simulated",
        bssid_count: int = 6,
        seed: Optional[int] = None,
        platform_name: Optional[str] = None,
    ) -> None:
        if bssid_count <= 0:
            raise ValueError("bssid_count must be greater than zero")

        self.ssid = ssid
        self.bssid_count = bssid_count
        self.platform_name = platform_name or platform_module.system().lower() or "unknown"
        self._rng = random.Random(seed)
        self._step = 0
        self._access_points = self._build_access_points()

    def get_observation(self) -> WiFiSignalObservation:
        """Return one simulated WiFi-only observation."""

        self._step += 1
        drift = math.sin(self._step / 5.0) * 2.5
        rssi_vector: List[float] = []
        visible_access_points: List[Dict[str, Any]] = []

        for index, ap in enumerate(self._access_points):
            base_rssi = -45.0 - (index * 4.5)
            rssi = round(base_rssi + drift + self._rng.gauss(0.0, 2.2), 2)
            rssi_vector.append(rssi)
            visible_access_points.append(
                {
                    "ssid": ap["ssid"],
                    "bssid": ap["bssid"],
                    "channel": ap["channel"],
                    "rssi": rssi,
                }
            )

        mean_rssi = round(statistics.fmean(rssi_vector), 2)
        rssi_std = round(statistics.pstdev(rssi_vector), 2) if len(rssi_vector) > 1 else 0.0
        gateway_latency_ms = round(max(1.0, self._rng.gauss(18.0, 4.0)), 2)
        jitter_ms = round(max(0.0, self._rng.gauss(3.5, 1.2)), 2)
        packet_loss = round(min(max(self._rng.gauss(0.01, 0.008), 0.0), 0.08), 4)
        scan_stability = round(min(max(1.0 - (rssi_std / 35.0) - packet_loss, 0.0), 1.0), 4)

        return WiFiSignalObservation(
            timestamp=time.time(),
            ssid=self.ssid,
            bssid_count=len(visible_access_points),
            visible_access_points=visible_access_points,
            rssi_vector=rssi_vector,
            mean_rssi=mean_rssi,
            rssi_std=rssi_std,
            gateway_latency_ms=gateway_latency_ms,
            jitter_ms=jitter_ms,
            packet_loss=packet_loss,
            scan_stability=scan_stability,
            platform=self.platform_name,
            mode=self.mode,
        )

    def _build_access_points(self) -> List[Dict[str, Any]]:
        access_points: List[Dict[str, Any]] = []
        for index in range(self.bssid_count):
            ssid = self.ssid if index == 0 else "{}-neighbor-{}".format(self.ssid, index)
            access_points.append(
                {
                    "ssid": ssid,
                    "bssid": self._generate_bssid(index),
                    "channel": self._rng.choice([1, 6, 11, 36, 40, 44, 149, 153]),
                }
            )
        return access_points

    def _generate_bssid(self, index: int) -> str:
        octets = [0x02, 0x00, 0x00, self._rng.randrange(0, 256), self._rng.randrange(0, 256), index]
        return ":".join("{:02x}".format(octet) for octet in octets)

"""Simulated WiFi-only signal source for GhostEye v0.2.

The simulator models RSSI scan metadata plus gateway latency/jitter only. It
does not expose CSI, raw frames, monitor-mode capture, or device identifiers
beyond synthetic BSSIDs used for local testing.
"""

from __future__ import annotations

import math
import platform as platform_module
import random
import statistics
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple


WIFI_ONLY_NON_CSI_MODE = "wifi_only_non_csi"


@dataclass(frozen=True)
class SimulatedAccessPoint:
    """Configured synthetic access point."""

    ssid: str
    bssid: str
    baseline_rssi_dbm: float
    channel: int
    frequency_mhz: int


@dataclass(frozen=True)
class WiFiSignalObservation:
    """One WiFi-only, non-CSI observation."""

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

    @property
    def rssi_by_bssid(self) -> Dict[str, float]:
        return {
            str(ap["bssid"]).lower(): float(ap["rssi"])
            for ap in self.visible_access_points
            if "bssid" in ap and "rssi" in ap
        }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WiFiSignalSimulatorAdapter:
    """Generate realistic-enough WiFi RSSI and latency observations."""

    mode = WIFI_ONLY_NON_CSI_MODE

    def __init__(
        self,
        ssid: str = "GhostEye-Simulated",
        bssid_count: int = 5,
        seed: Optional[int] = None,
        platform_name: Optional[str] = None,
        access_points: Optional[Tuple[SimulatedAccessPoint, ...]] = None,
    ) -> None:
        if bssid_count <= 0:
            raise ValueError("bssid_count must be greater than zero")

        self.ssid = ssid
        self.platform_name = platform_name or platform_module.system().lower() or "unknown"
        self._rng = random.Random(seed)
        self._step = 0
        self._access_points = access_points or self._build_access_points(bssid_count)

    def get_observation(self) -> WiFiSignalObservation:
        """Return one simulated WiFi-only observation."""

        self._step += 1
        slow_wave = math.sin(self._step / 4.0) * 2.4
        motion_burst = self._rng.uniform(0.0, 4.5) if self._rng.random() > 0.55 else 0.0
        rssi_vector: List[float] = []
        visible_access_points: List[Dict[str, Any]] = []

        for index, ap in enumerate(self._access_points):
            multipath = slow_wave * (1.0 - min(index, 4) * 0.08)
            burst = motion_burst * math.sin((self._step + index) / 2.0)
            noise = self._rng.gauss(0.0, 1.6)
            rssi = round(ap.baseline_rssi_dbm + multipath + burst + noise, 2)
            rssi_vector.append(rssi)
            visible_access_points.append(
                {
                    "ssid": ap.ssid,
                    "bssid": ap.bssid,
                    "channel": ap.channel,
                    "frequency_mhz": ap.frequency_mhz,
                    "rssi": rssi,
                }
            )

        mean_rssi = round(statistics.fmean(rssi_vector), 2)
        rssi_std = round(statistics.pstdev(rssi_vector), 2) if len(rssi_vector) > 1 else 0.0
        gateway_latency_ms = round(max(1.0, self._rng.gauss(12.0 + motion_burst, 2.8)), 2)
        jitter_ms = round(max(0.0, self._rng.gauss(2.7 + motion_burst / 4.0, 0.9)), 2)
        packet_loss = round(min(max(self._rng.gauss(0.004, 0.004), 0.0), 0.05), 4)
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

    def select_environment(self, ssid: str) -> None:
        """Label subsequent simulated observations with the selected WiFi SSID."""

        selected_ssid = str(ssid).strip()
        if selected_ssid:
            self.ssid = selected_ssid

    def _build_access_points(self, bssid_count: int) -> Tuple[SimulatedAccessPoint, ...]:
        channels = ((1, 2412), (6, 2437), (11, 2462), (36, 5180), (149, 5745), (153, 5765))
        access_points = []
        for index in range(bssid_count):
            channel, frequency = channels[index % len(channels)]
            ssid = self.ssid if index == 0 else f"{self.ssid}-neighbor-{index}"
            access_points.append(
                SimulatedAccessPoint(
                    ssid=ssid,
                    bssid=self._generate_bssid(index),
                    baseline_rssi_dbm=-45.0 - (index * 4.8),
                    channel=channel,
                    frequency_mhz=frequency,
                )
            )
        return tuple(access_points)

    def _generate_bssid(self, index: int) -> str:
        octets = [0x02, 0x00, 0x00, self._rng.randrange(0, 256), self._rng.randrange(0, 256), index]
        return ":".join(f"{octet:02x}" for octet in octets)


class SimulatorAdapter(WiFiSignalSimulatorAdapter):
    """Compatibility alias for older imports."""

    def collect(self) -> WiFiSignalObservation:
        return self.get_observation()

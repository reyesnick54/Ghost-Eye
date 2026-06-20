"""Estimate what WiFi-only signals can support in the current environment."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev
from typing import Iterable, Literal

from ghost_eye.wifi.wifi_scan import WifiScan


CapabilityTier = Literal["insufficient", "basic", "stable", "rich"]


@dataclass(frozen=True)
class SignalCapabilityProfile:
    """Summary of WiFi signal quality for downstream sensing."""

    tier: CapabilityTier
    access_point_count: int
    average_rssi_dbm: float | None
    rssi_stability: float
    supports_presence: bool
    supports_motion: bool
    supports_zone_mapping: bool


class SignalCapabilityProfiler:
    """Profiles scan density and RSSI stability for non-CSI algorithms."""

    def profile(self, scans: Iterable[WifiScan]) -> SignalCapabilityProfile:
        scan_tuple = tuple(scans)
        latest = scan_tuple[-1] if scan_tuple else WifiScan(networks=())
        rssis = [network.rssi_dbm for scan in scan_tuple for network in scan.networks]
        access_point_count = len(latest.networks)
        average_rssi = fmean(rssis) if rssis else None
        stability = self._stability_score(rssis)

        if access_point_count >= 6 and stability >= 0.7:
            tier: CapabilityTier = "rich"
        elif access_point_count >= 4 and stability >= 0.45:
            tier = "stable"
        elif access_point_count >= 2:
            tier = "basic"
        else:
            tier = "insufficient"

        return SignalCapabilityProfile(
            tier=tier,
            access_point_count=access_point_count,
            average_rssi_dbm=average_rssi,
            rssi_stability=stability,
            supports_presence=tier in {"basic", "stable", "rich"},
            supports_motion=tier in {"stable", "rich"},
            supports_zone_mapping=tier == "rich",
        )

    @staticmethod
    def _stability_score(rssis: list[float]) -> float:
        if len(rssis) < 2:
            return 0.0
        spread = pstdev(rssis)
        return max(0.0, min(1.0, 1.0 - (spread / 35.0)))

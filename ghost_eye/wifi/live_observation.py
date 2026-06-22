"""Rolling live WiFi observation collection for GhostEye v0.3."""

from __future__ import annotations

import math
import statistics
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, Mapping

from ghost_eye.csi_adapters.simulator_adapter import WIFI_ONLY_NON_CSI_MODE, WiFiSignalObservation
from ghost_eye.wifi.gateway_probe import GatewayProbeResult, probe_gateway
from ghost_eye.wifi.signal_normalizer import normalize_live_measurement
from ghost_eye.wifi.wifi_scan import LiveWifiScan, collect_live_wifi_scan


@dataclass(frozen=True)
class LiveObservationSnapshot:
    """One normalized live WiFi measurement plus derived adapter observation."""

    normalized: Mapping[str, Any]
    observation: WiFiSignalObservation
    wifi_scan: LiveWifiScan
    gateway_probe: GatewayProbeResult
    rolling_metrics: Mapping[str, Any]


@dataclass
class RollingObservationWindow:
    """Maintain recent observations and compute bounded stability metrics."""

    maxlen: int = 12
    observations: Deque[dict[str, Any]] = field(default_factory=lambda: deque(maxlen=12))

    def __post_init__(self) -> None:
        self.observations = deque(self.observations, maxlen=self.maxlen)

    def add(self, observation: Mapping[str, Any]) -> dict[str, Any]:
        self.observations.append(dict(observation))
        return self.metrics()

    def metrics(self) -> dict[str, Any]:
        values = list(self.observations)
        rssis = [_number(item.get("rssi_dbm")) for item in values if _number(item.get("rssi_dbm")) is not None]
        latencies = [
            _number(item.get("gateway_latency_ms"))
            for item in values
            if _number(item.get("gateway_latency_ms")) is not None
        ]
        jitters = [_number(item.get("jitter_ms")) for item in values if _number(item.get("jitter_ms")) is not None]
        losses = [_number(item.get("packet_loss")) for item in values if _number(item.get("packet_loss")) is not None]
        ap_counts = [int(_number(item.get("visible_access_points")) or 0) for item in values]

        return {
            "sample_count": len(values),
            "rssi_stability": _stability(rssis, scale=10.0, default=0.65),
            "latency_stability": _stability(latencies, scale=35.0, default=0.55),
            "jitter_trend": _trend(jitters),
            "packet_loss_trend": _trend(losses),
            "ap_visibility_changes": _change_count(ap_counts),
            "observation_quality": _quality_hint(rssis, latencies, losses, ap_counts),
        }


class LiveObservationCollector:
    """Collect live WiFi and gateway data and expose simulator-compatible rows."""

    def __init__(
        self,
        wifi_scan_provider: Callable[[], LiveWifiScan] = collect_live_wifi_scan,
        gateway_probe_provider: Callable[[], GatewayProbeResult] = probe_gateway,
        window: RollingObservationWindow | None = None,
    ) -> None:
        self._wifi_scan_provider = wifi_scan_provider
        self._gateway_probe_provider = gateway_probe_provider
        self.window = window or RollingObservationWindow()
        self.last_snapshot: LiveObservationSnapshot | None = None

    def collect(self) -> LiveObservationSnapshot:
        """Collect one live measurement and convert it to an observation."""

        wifi_scan = self._wifi_scan_provider()
        gateway_probe = self._gateway_probe_provider()
        pre_metrics = self.window.metrics()
        normalized = normalize_live_measurement(wifi_scan, gateway_probe, pre_metrics)
        rolling_metrics = self.window.add(normalized)
        normalized = normalize_live_measurement(wifi_scan, gateway_probe, rolling_metrics)
        observation = self._to_signal_observation(normalized)
        snapshot = LiveObservationSnapshot(
            normalized=normalized,
            observation=observation,
            wifi_scan=wifi_scan,
            gateway_probe=gateway_probe,
            rolling_metrics=rolling_metrics,
        )
        self.last_snapshot = snapshot
        return snapshot

    def available(self) -> bool:
        """Return whether a recent or lightweight live scan has usable data."""

        if self.last_snapshot is not None and bool(self.last_snapshot.normalized.get("available")):
            return True
        try:
            scan = self._wifi_scan_provider()
        except Exception:
            return False
        return bool(scan.available)

    @staticmethod
    def _to_signal_observation(normalized: Mapping[str, Any]) -> WiFiSignalObservation:
        rssi = _number(normalized.get("rssi_dbm"))
        if rssi is None:
            rssi = -90.0

        bssid = str(normalized.get("bssid_masked") or "unknown_ap")
        visible_ap_count = int(_number(normalized.get("visible_access_points")) or 0)
        if visible_ap_count <= 0 and normalized.get("available"):
            visible_ap_count = 1

        visible_access_points = []
        if visible_ap_count:
            visible_access_points.append(
                {
                    "ssid": normalized.get("ssid") or "unknown",
                    "bssid": bssid,
                    "bssid_masked": normalized.get("bssid_masked"),
                    "channel": normalized.get("channel"),
                    "rssi": round(rssi, 2),
                    "noise": normalized.get("noise_dbm"),
                    "vendor_hint": normalized.get("vendor_hint") or "unknown",
                    "observation_source": normalized.get("observation_source"),
                }
            )

        rssi_vector = [round(rssi, 2)] if visible_access_points else []
        mean_rssi = round(statistics.fmean(rssi_vector), 2) if rssi_vector else -90.0
        rssi_std = statistics.pstdev(rssi_vector) if len(rssi_vector) > 1 else 0.0

        return WiFiSignalObservation(
            timestamp=time.time(),
            ssid=str(normalized.get("ssid") or "unknown"),
            bssid_count=len(visible_access_points),
            visible_access_points=visible_access_points,
            rssi_vector=rssi_vector,
            mean_rssi=mean_rssi,
            rssi_std=round(rssi_std, 2),
            gateway_latency_ms=round(_number(normalized.get("gateway_latency_ms")) or 0.0, 2),
            jitter_ms=round(_number(normalized.get("jitter_ms")) or 0.0, 2),
            packet_loss=round(_number(normalized.get("packet_loss")) or 1.0, 4),
            scan_stability=round(_number(normalized.get("rssi_stability")) or 0.0, 4),
            platform=str(normalized.get("observation_source") or "live_wifi"),
            mode=WIFI_ONLY_NON_CSI_MODE,
        )


def _stability(values: list[float], *, scale: float, default: float) -> float:
    if not values:
        return 0.0
    if len(values) < 2:
        return default
    spread = statistics.pstdev(values)
    return round(max(0.0, min(1.0, 1.0 - spread / scale)), 3)


def _trend(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return round(max(-1.0, min(1.0, values[-1] - values[0])), 4)


def _change_count(values: list[int]) -> int:
    if len(values) < 2:
        return 0
    return sum(1 for left, right in zip(values, values[1:]) if left != right)


def _quality_hint(
    rssis: list[float],
    latencies: list[float],
    losses: list[float],
    ap_counts: list[int],
) -> float:
    if not rssis and not latencies:
        return 0.0
    rssi_score = _stability(rssis, scale=12.0, default=0.55)
    latency_score = _stability(latencies, scale=40.0, default=0.5)
    loss_score = 1.0 - min(1.0, (losses[-1] if losses else 1.0) * 4.0)
    ap_score = min(1.0, (ap_counts[-1] if ap_counts else 0) / 3.0)
    return round(max(0.0, min(1.0, rssi_score * 0.38 + latency_score * 0.28 + loss_score * 0.20 + ap_score * 0.14)), 3)


def _number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number

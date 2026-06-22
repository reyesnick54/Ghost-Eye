"""Normalize WiFi RSSI and gateway observations into inference features."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev
from typing import Any, Iterable, Mapping

from ghost_eye.wifi.gateway_probe import GatewayProbeResult
from ghost_eye.wifi.wifi_scan import LiveWifiScan


@dataclass(frozen=True)
class NormalizedSignal:
    """Normalized signal state for one access point."""

    bssid: str
    rssi_dbm: float
    strength: float
    delta_db: float = 0.0
    z_score: float = 0.0


class SignalNormalizer:
    """Converts RSSI dBm values into bounded and baseline-relative features."""

    def __init__(self, floor_dbm: float = -95.0, ceiling_dbm: float = -35.0) -> None:
        if floor_dbm >= ceiling_dbm:
            raise ValueError("floor_dbm must be lower than ceiling_dbm")
        self.floor_dbm = floor_dbm
        self.ceiling_dbm = ceiling_dbm

    def strength(self, rssi_dbm: float) -> float:
        """Scale an RSSI value into the ``0.0`` to ``1.0`` range."""

        bounded = min(max(rssi_dbm, self.floor_dbm), self.ceiling_dbm)
        return (bounded - self.floor_dbm) / (self.ceiling_dbm - self.floor_dbm)

    def normalize(
        self,
        signals: Mapping[str, float],
        baseline: Mapping[str, float] | None = None,
    ) -> dict[str, NormalizedSignal]:
        """Normalize current RSSI values against an optional baseline."""

        baseline = baseline or {}
        values = list(signals.values())
        spread = pstdev(values) if len(values) > 1 else 0.0
        center = fmean(values) if values else 0.0

        normalized: dict[str, NormalizedSignal] = {}
        for bssid, rssi_dbm in signals.items():
            delta_db = rssi_dbm - baseline.get(bssid, rssi_dbm)
            normalized[bssid.lower()] = NormalizedSignal(
                bssid=bssid.lower(),
                rssi_dbm=rssi_dbm,
                strength=self.strength(rssi_dbm),
                delta_db=delta_db,
                z_score=((rssi_dbm - center) / spread) if spread else 0.0,
            )
        return normalized

    def mean_rssi(self, samples: Iterable[float]) -> float | None:
        values = list(samples)
        return fmean(values) if values else None


def normalize_live_measurement(
    wifi_scan: LiveWifiScan | Mapping[str, Any],
    gateway_probe: GatewayProbeResult | Mapping[str, Any],
    rolling_metrics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Combine WiFi scan and gateway probe data into v0.3 inference fields."""

    wifi = wifi_scan.to_dict() if isinstance(wifi_scan, LiveWifiScan) else dict(wifi_scan)
    probe = gateway_probe.to_dict() if isinstance(gateway_probe, GatewayProbeResult) else dict(gateway_probe)
    rolling = dict(rolling_metrics or {})

    packet_loss = _float_or(probe.get("packet_loss"), 1.0)
    gateway_latency_ms = _float_or(probe.get("gateway_latency_ms"), 0.0)
    jitter_ms = _float_or(probe.get("jitter_ms"), 0.0)
    rssi_stability = _float_or(rolling.get("rssi_stability"), 0.0 if wifi.get("rssi_dbm") is None else 0.65)
    visible_access_points = int(_float_or(wifi.get("visible_access_points"), 0.0))

    observation_quality = _observation_quality(
        visible_access_points=visible_access_points,
        rssi_stability=rssi_stability,
        latency_stability=_float_or(rolling.get("latency_stability"), 0.5),
        packet_loss=packet_loss,
        scan_available=bool(wifi.get("available")),
        probe_status=str(probe.get("probe_status") or "unknown"),
    )

    return {
        "ssid": wifi.get("ssid") or "unknown",
        "bssid_masked": wifi.get("bssid_masked"),
        "vendor_hint": wifi.get("vendor_hint") or "unknown",
        "rssi_dbm": _optional_float(wifi.get("rssi_dbm")),
        "noise_dbm": _optional_float(wifi.get("noise_dbm")),
        "channel": wifi.get("channel"),
        "tx_rate_mbps": _optional_float(wifi.get("tx_rate_mbps")),
        "phy_mode": wifi.get("phy_mode"),
        "interface_name": wifi.get("interface_name"),
        "visible_access_points": visible_access_points,
        "gateway_ip": probe.get("gateway_ip"),
        "gateway_latency_ms": round(gateway_latency_ms, 2),
        "jitter_ms": round(jitter_ms, 2),
        "packet_loss": round(max(0.0, min(1.0, packet_loss)), 4),
        "rssi_stability": round(max(0.0, min(1.0, rssi_stability)), 3),
        "latency_stability": round(_float_or(rolling.get("latency_stability"), 0.5), 3),
        "jitter_trend": round(_float_or(rolling.get("jitter_trend"), 0.0), 3),
        "packet_loss_trend": round(_float_or(rolling.get("packet_loss_trend"), 0.0), 4),
        "ap_visibility_changes": int(_float_or(rolling.get("ap_visibility_changes"), 0.0)),
        "observation_quality": round(observation_quality, 3),
        "observation_source": "macos_live_wifi" if wifi.get("platform") == "macos" else "live_wifi",
        "probe_status": probe.get("probe_status") or "unknown",
        "scan_status": wifi.get("status") or "unknown",
        "available": bool(wifi.get("available")),
    }


def _observation_quality(
    *,
    visible_access_points: int,
    rssi_stability: float,
    latency_stability: float,
    packet_loss: float,
    scan_available: bool,
    probe_status: str,
) -> float:
    ap_score = min(1.0, visible_access_points / 3.0)
    loss_score = max(0.0, 1.0 - packet_loss * 4.0)
    probe_score = 1.0 if probe_status == "ok" else 0.45
    availability_score = 1.0 if scan_available else 0.25
    return (
        rssi_stability * 0.32
        + latency_stability * 0.20
        + ap_score * 0.16
        + loss_score * 0.12
        + probe_score * 0.10
        + availability_score * 0.10
    )


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), 3)
    except (TypeError, ValueError):
        return None


def _float_or(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

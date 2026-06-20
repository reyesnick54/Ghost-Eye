"""Capability and signal-quality profiling for WiFi-only observations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from ghost_eye.api.schemas import MODE_WIFI_ONLY_NON_CSI


@dataclass(frozen=True)
class SignalCapabilityProfile:
    """Summary of what the current source can support."""

    mode: str
    has_csi: bool
    has_rssi: bool
    supports_latency_probe: bool
    confidence_ceiling: float
    visible_access_points: int
    gateway_latency_ms: float
    jitter_ms: float
    packet_loss: float
    rssi_stability: float
    quality_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SignalCapabilityProfiler:
    """Profile WiFi-only non-CSI scan quality without overstating fidelity."""

    WIFI_ONLY_RSSI_LATENCY = "wifi_only_rssi_latency"
    WIFI_ONLY_NON_CSI = MODE_WIFI_ONLY_NON_CSI
    CONFIDENCE_CEILING = 0.65

    def profile(self, observation: Any = None, **_: Any) -> SignalCapabilityProfile:
        visible_ap_count = _read_int(observation, "bssid_count", default=0)
        latency_ms = _read_float(observation, "gateway_latency_ms", default=0.0)
        jitter_ms = _read_float(observation, "jitter_ms", default=0.0)
        packet_loss = _read_float(observation, "packet_loss", default=0.0)
        rssi_stability = _read_float(observation, "scan_stability", default=0.0)

        ap_score = min(1.0, visible_ap_count / 5.0)
        latency_score = max(0.0, min(1.0, 1.0 - max(latency_ms - 5.0, 0.0) / 80.0))
        jitter_score = max(0.0, min(1.0, 1.0 - jitter_ms / 25.0))
        loss_score = max(0.0, min(1.0, 1.0 - packet_loss * 10.0))
        quality_score = round(
            (ap_score * 0.35)
            + (rssi_stability * 0.35)
            + (latency_score * 0.12)
            + (jitter_score * 0.10)
            + (loss_score * 0.08),
            3,
        )

        return SignalCapabilityProfile(
            mode=MODE_WIFI_ONLY_NON_CSI,
            has_csi=False,
            has_rssi=True,
            supports_latency_probe=True,
            confidence_ceiling=self.CONFIDENCE_CEILING,
            visible_access_points=visible_ap_count,
            gateway_latency_ms=round(latency_ms, 2),
            jitter_ms=round(jitter_ms, 2),
            packet_loss=round(packet_loss, 4),
            rssi_stability=round(rssi_stability, 3),
            quality_score=quality_score,
        )

    def classify(self, source: Any = None, **hints: Any) -> dict[str, Any]:
        return self.profile(source, **hints).to_dict()

    def profile_source(self, source: Any = None, **hints: Any) -> dict[str, Any]:
        return self.classify(source, **hints)

    def profile_for_mode(self, mode: str) -> dict[str, Any]:
        if str(mode) not in {MODE_WIFI_ONLY_NON_CSI, self.WIFI_ONLY_RSSI_LATENCY, "simulated"}:
            raise ValueError(f"Unsupported signal capability mode {mode!r}")
        return {
            "mode": MODE_WIFI_ONLY_NON_CSI,
            "supports_rssi_scan": True,
            "supports_latency_probe": True,
            "supports_rtt": False,
            "supports_csi": False,
            "confidence_ceiling": self.CONFIDENCE_CEILING,
            "recommended_scan_mode": "rssi_latency_scan",
            "limitations": ["WiFi-only non-CSI mode provides coarse probabilistic estimates only."],
        }


def _read_float(source: Any, name: str, default: float) -> float:
    value = _read(source, name, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_int(source: Any, name: str, default: int) -> int:
    value = _read(source, name, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _read(source: Any, name: str, default: Any) -> Any:
    if source is None:
        return default
    if isinstance(source, Mapping):
        return source.get(name, default)
    return getattr(source, name, default)

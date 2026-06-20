"""Small API-facing schemas for GhostEye WiFi-only v0.2 telemetry."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Mapping, Optional, Tuple


MODE_WIFI_ONLY_NON_CSI = "wifi_only_non_csi"
SOURCE_LOCAL_WIFI_SIMULATED = "local_wifi_rssi_latency_simulated"
LIMITATIONS = "WiFi-only non-CSI mode provides coarse probabilistic estimates only."
NOTICE = (
    "Authorized controlled environments only. Not for covert surveillance or "
    "unauthorized monitoring."
)


def utc_now_iso() -> str:
    """Return an API timestamp in compact UTC form."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class ApiWifiNetwork:
    """Compatibility schema for raw WiFi scans."""

    ssid: str
    bssid: str
    rssi_dbm: float
    channel: Optional[int] = None
    frequency_mhz: Optional[int] = None


@dataclass(frozen=True)
class ApiScanResponse:
    """Compatibility schema for simple WiFi scan responses."""

    networks: Tuple[ApiWifiNetwork, ...]
    timestamp: str = field(default_factory=utc_now_iso)
    source: str = "wifi_scan"


@dataclass(frozen=True)
class ApiInferenceResponse:
    """Compatibility schema for presence, motion, and zone inference."""

    presence: Literal["clear", "possible_presence", "presence_detected"]
    motion_score: float
    zone: str
    confidence: float
    timestamp: str = field(default_factory=utc_now_iso)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SignalQuality:
    """Quality summary included in every v0.2 scan response."""

    visible_access_points: int
    gateway_latency_ms: float
    jitter_ms: float
    packet_loss: float
    rssi_stability: float


@dataclass(frozen=True)
class GhostEyeScanResponse:
    """Top-level GhostEye WiFi-only non-CSI v0.2 telemetry schema."""

    timestamp: str
    mode: str
    source: str
    presence: str
    motion_score: float
    zone: str
    confidence: float
    confidence_ceiling: float
    signal_quality: SignalQuality
    map: Dict[str, float]
    limitations: str = LIMITATIONS
    notice: str = NOTICE

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)


@dataclass(frozen=True)
class CalibrationSummary:
    """Response helper for calibration endpoints."""

    status: str
    notice: str = NOTICE
    metadata: Dict[str, Any] = field(default_factory=dict)


def to_dict(schema: object) -> Dict[str, Any]:
    """Convert dataclass schemas into plain JSON-ready dictionaries."""

    return asdict(schema)

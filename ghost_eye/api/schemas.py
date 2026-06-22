"""Small API-facing schemas for GhostEye WiFi-only telemetry."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Mapping, Optional, Tuple


MODE_WIFI_ONLY_NON_CSI = "wifi_only_non_csi"
SOURCE_LOCAL_WIFI_SIMULATED = "local_wifi_rssi_latency_simulated"
SOURCE_SELECTED_WIFI_ENVIRONMENT = "selected_wifi_environment"
LIMITATIONS = (
    "WiFi-only non-CSI mode provides coarse probabilistic estimates only. "
    "It does not provide validated through-wall imaging."
)
NOTICE = (
    "Authorized controlled environments only. Not for covert surveillance or "
    "unauthorized monitoring."
)
WIFI_NETWORK_LIMITATIONS = (
    "Ordinary WiFi network selection does not provide raw CSI or reliable "
    "through-wall imaging."
)
ROOM_SETUP_LIMITATIONS = (
    "Room shape is user-configured. WiFi-only mode estimates probabilistic "
    "disturbance zones, not true RF imaging."
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
class WifiNetworkEnvironment:
    """Safe WiFi environment descriptor exposed to the mobile selector."""

    ssid: str
    bssid_masked: str
    vendor_hint: str
    signal_dbm: int
    channel: int
    capability: str
    can_use_as_csi_sensor: bool
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)


@dataclass(frozen=True)
class WifiNetworksResponse:
    """Response schema for simulated/local WiFi environment discovery."""

    networks: Tuple[WifiNetworkEnvironment, ...]
    limitations: str = WIFI_NETWORK_LIMITATIONS

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)


@dataclass(frozen=True)
class WifiSelectionResponse:
    """Selected WiFi environment response."""

    selected_ssid: str
    adapter_mode: str
    status: str = "selected"
    confidence_ceiling: float = 0.65
    notice: str = "Authorized controlled environments only."

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)


@dataclass(frozen=True)
class SelectedNetwork:
    """Selected WiFi environment included in telemetry."""

    ssid: str
    vendor_hint: str


@dataclass(frozen=True)
class RouterLocation:
    """Manual room coordinate for the router or access point."""

    x_m: float
    y_m: float


@dataclass(frozen=True)
class RoomSetupResponse:
    """Response schema for manual room setup."""

    room_id: str
    status: str
    map_mode: str
    limitations: str = ROOM_SETUP_LIMITATIONS

    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self)


@dataclass(frozen=True)
class RoomMap:
    """Current user-configured room map plus probabilistic zone scores."""

    room_name: str
    shape: str
    width_m: float
    length_m: float
    zones: Dict[str, float]


@dataclass(frozen=True)
class GhostEyeScanResponse:
    """Top-level GhostEye WiFi-only non-CSI telemetry schema."""

    timestamp: str
    mode: str
    source: str
    selected_network: SelectedNetwork
    presence: str
    motion_score: float
    zone: str
    confidence: float
    confidence_ceiling: float
    signal_quality: SignalQuality
    room_map: RoomMap
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

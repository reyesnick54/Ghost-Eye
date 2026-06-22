"""Mobile telemetry contracts for hosted GhostEye scans."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


Platform = Literal["ios", "android"]
CapabilityMode = Literal["wifi_only_non_csi", "wifi_rssi_latency_only", "limited_mobile_wifi"]

LIMITATIONS = (
    "Cloud analysis uses mobile-provided WiFi/network observations only. "
    "WiFi-only non-CSI mode returns coarse probabilistic telemetry and does not "
    "claim exact through-wall object detection."
)
NOTICE = "Authorized, consent-based, controlled environments only."
ANALYSIS_MODE = "analysis_only_no_autonomy"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ErrorResponse(BaseModel):
    error: str
    detail: str
    request_id: str | None = None


class SignalQuality(BaseModel):
    visible_access_points: int = Field(ge=0)
    gateway_latency_ms: float | None = Field(default=None, ge=0)
    jitter_ms: float | None = Field(default=None, ge=0)
    packet_loss: float | None = Field(default=None, ge=0, le=1)
    rssi_dbm: float | None = None
    rssi_stability: float = Field(ge=0, le=1)
    quality_score: float = Field(ge=0, le=1)


class SelectedNetwork(BaseModel):
    ssid: str | None = None
    bssid_masked: str | None = None
    vendor_hint: str | None = None


class RoomMap(BaseModel):
    room_id: str | None = None
    room_name: str | None = None
    shape: str = "unknown"
    width_m: float | None = Field(default=None, gt=0)
    length_m: float | None = Field(default=None, gt=0)
    zones: dict[str, float] = Field(default_factory=dict)
    map_mode: str = "mobile_observation_plus_calibration"


class MobileWifiObservation(BaseModel):
    device_id: str = Field(min_length=1)
    team_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    timestamp: datetime = Field(default_factory=utc_now)
    platform: Platform
    capability_mode: str = "wifi_only_non_csi"
    ssid: str | None = None
    bssid_masked: str | None = None
    vendor_hint: str | None = None
    rssi_dbm: float | None = None
    gateway_latency_ms: float | None = Field(default=None, ge=0)
    jitter_ms: float | None = Field(default=None, ge=0)
    packet_loss: float | None = Field(default=None, ge=0, le=1)
    visible_access_points: int | None = Field(default=None, ge=0)
    device_motion_state: str = "unknown"
    room_id: str | None = None
    zone_label: str | None = None
    calibration_phase: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("capability_mode")
    @classmethod
    def normalize_capability_mode(cls, value: str) -> str:
        normalized = (value or "wifi_only_non_csi").strip().lower()
        if normalized in {"wifi_only", "rssi", "wifi_rssi"}:
            return "wifi_only_non_csi"
        return normalized


class ObservationBatch(BaseModel):
    observations: list[MobileWifiObservation] = Field(min_length=1, max_length=500)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TelemetryScan(BaseModel):
    scan_id: str
    device_id: str
    team_id: str
    session_id: str
    timestamp: datetime
    mode: str = "wifi_only_non_csi"
    source: str = "mobile_wifi_observation"
    selected_network: SelectedNetwork
    signal_quality: SignalQuality
    presence: Literal["clear", "possible_motion", "possible_presence", "unstable_scan"]
    motion_score: float = Field(ge=0, le=1)
    zone: str = "unknown"
    confidence: float = Field(ge=0, le=1)
    confidence_ceiling: float = Field(ge=0, le=1)
    confidence_explanation: str
    room_map: RoomMap
    map: dict[str, float] = Field(default_factory=dict)
    limitations: str = LIMITATIONS
    notice: str = NOTICE
    metadata: dict[str, Any] = Field(default_factory=dict)

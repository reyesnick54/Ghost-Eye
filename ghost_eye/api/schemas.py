"""API-facing schemas for GhostEye WiFi-only sensing results."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Mapping, Optional

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class ApiWifiNetwork:
    """Serializable WiFi network observation."""

    ssid: str
    bssid: str
    rssi_dbm: float
    channel: int | None = None
    frequency_mhz: int | None = None


@dataclass(frozen=True)
class ApiScanResponse:
    """Serializable WiFi scan response."""

    networks: tuple[ApiWifiNetwork, ...]
    timestamp: float = field(default_factory=time.time)
    source: str = "wifi_scan"


@dataclass(frozen=True)
class ApiInferenceResponse:
    """Serializable inference result for presence, motion, and zone."""

    presence: Literal["clear", "possible_presence", "presence_detected"]
    motion_score: float
    zone: str
    confidence: float
    timestamp: float = field(default_factory=time.time)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def to_dict(schema: object) -> dict[str, Any]:
    """Convert dataclass schemas into plain dictionaries."""

    return asdict(schema)


SAFE_LIMITATION_NOTICE = (
    "WiFi-only non-CSI mode provides coarse probabilistic estimates only. "
    "Authorized controlled environments only."
)


class WiFiSignalObservation(BaseModel):
    """A single WiFi scan observation used for coarse non-CSI sensing."""

    timestamp: float = Field(default_factory=time.time)
    bssid: Optional[str] = Field(default=None, description="Access point BSSID, if available.")
    ssid: Optional[str] = Field(default=None, description="Network SSID, if available.")
    rssi_dbm: Optional[float] = Field(default=None, description="Observed RSSI in dBm.")
    channel: Optional[int] = Field(default=None, ge=1, description="WiFi channel number.")
    frequency_mhz: Optional[int] = Field(default=None, ge=0, description="Center frequency in MHz.")
    noise_dbm: Optional[float] = Field(default=None, description="Estimated noise floor in dBm.")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SignalQuality(BaseModel):
    """Signal quality summary for the observations behind a telemetry result."""

    score: float = Field(default=0.0, ge=0.0, le=1.0)
    label: str = Field(default="unknown")
    rssi_dbm: Optional[float] = Field(default=None)
    snr_db: Optional[float] = Field(default=None)
    sample_count: int = Field(default=0, ge=0)
    observations: List[WiFiSignalObservation] = Field(default_factory=list)


class ZoneMap(BaseModel):
    """Coarse zone map and per-zone confidence estimates."""

    active_zone: str = Field(default="unknown")
    zones: List[str] = Field(default_factory=lambda: ["zone_a", "zone_b", "zone_c", "unknown"])
    confidence_by_zone: Dict[str, float] = Field(default_factory=dict)
    calibrated: bool = Field(default=False)
    coordinate_system: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SourceInfo(BaseModel):
    """Information about the telemetry source."""

    kind: str = Field(default="wifi_non_csi")
    name: str = Field(default="WiFi-only non-CSI scanner")
    interface: Optional[str] = Field(default=None)
    simulated: bool = Field(default=True)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AIAnalysisResult(BaseModel):
    """Placeholder for optional AI-assisted analysis details."""

    available: bool = Field(default=False)
    model: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    limitations: List[str] = Field(default_factory=lambda: [SAFE_LIMITATION_NOTICE])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GhostEyeTelemetry(BaseModel):
    """Response schema for /scan telemetry."""

    timestamp: float = Field(default_factory=time.time)
    mode: str = Field(default="simulated")
    source: SourceInfo = Field(default_factory=SourceInfo)
    presence: str = Field(default="clear")
    motion_score: float = Field(default=0.0, ge=0.0, le=1.0)
    zone: str = Field(default="unknown")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    notice: str = Field(default=SAFE_LIMITATION_NOTICE)
    confidence_ceiling: float = Field(default=0.65, ge=0.0, le=1.0)
    signal_quality: SignalQuality = Field(default_factory=SignalQuality)
    map: ZoneMap = Field(default_factory=ZoneMap)
    limitations: List[str] = Field(default_factory=lambda: [SAFE_LIMITATION_NOTICE])
    ai_analysis: Optional[AIAnalysisResult] = Field(default=None)


class CalibrationRequest(BaseModel):
    """Request payload for collecting calibration samples."""

    source: SourceInfo = Field(default_factory=SourceInfo)
    environment_label: Optional[str] = Field(default=None)
    duration_seconds: int = Field(default=30, ge=1)
    observations: List[WiFiSignalObservation] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None)
    limitations: List[str] = Field(default_factory=lambda: [SAFE_LIMITATION_NOTICE])


class ZoneCalibrationRequest(CalibrationRequest):
    """Request payload for calibrating a specific zone."""

    zone: str = Field(default="unknown")
    zone_map: Optional[ZoneMap] = Field(default=None)

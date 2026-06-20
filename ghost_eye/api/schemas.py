"""API-facing schemas for GhostEye WiFi-only sensing results."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import time
from typing import Any, Literal, Mapping


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
    timestamp: float = field(default_factory=time)
    source: str = "wifi_scan"


@dataclass(frozen=True)
class ApiInferenceResponse:
    """Serializable inference result for presence, motion, and zone."""

    presence: Literal["clear", "possible_presence", "presence_detected"]
    motion_score: float
    zone: str
    confidence: float
    timestamp: float = field(default_factory=time)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def to_dict(schema: object) -> dict[str, Any]:
    """Convert dataclass schemas into plain dictionaries."""

    return asdict(schema)

"""Calibration schemas for server-side GhostEye baselines and fingerprints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.telemetry import MobileWifiObservation, SignalQuality


CalibrationKind = Literal["empty_room", "zone"]
CalibrationStatus = Literal["started", "sampling", "completed"]


class CalibrationStartRequest(BaseModel):
    device_id: str
    team_id: str
    session_id: str | None = None
    room_id: str | None = None
    zone_label: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CalibrationSampleRequest(BaseModel):
    calibration_id: str
    observation: MobileWifiObservation


class CalibrationCompleteRequest(BaseModel):
    calibration_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class CalibrationSession(BaseModel):
    calibration_id: str
    team_id: str
    device_id: str
    session_id: str | None = None
    room_id: str | None = None
    zone_label: str | None = None
    kind: CalibrationKind
    status: CalibrationStatus
    started_at: datetime
    completed_at: datetime | None = None
    sample_count: int = Field(default=0, ge=0)
    baseline: dict[str, Any] | None = None
    fingerprint: dict[str, Any] | None = None
    signal_quality: SignalQuality | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ZoneFingerprint(BaseModel):
    fingerprint_id: str
    team_id: str
    room_id: str | None = None
    zone_label: str
    created_at: datetime
    sample_count: int = Field(ge=0)
    rssi_dbm_mean: float | None = None
    gateway_latency_ms_mean: float | None = None
    jitter_ms_mean: float | None = None
    packet_loss_mean: float | None = None
    signal_quality: SignalQuality | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

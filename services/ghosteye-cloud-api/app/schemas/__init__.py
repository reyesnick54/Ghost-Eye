"""Stable Pydantic schemas exposed by the GhostEye Cloud API."""

from app.schemas.ai import AIAnalysis, AIAnalyzeScanRequest, AIAnalyzeSessionRequest
from app.schemas.calibration import (
    CalibrationCompleteRequest,
    CalibrationSampleRequest,
    CalibrationSession,
    CalibrationStartRequest,
    ZoneFingerprint,
)
from app.schemas.devices import DeviceRegistration, DeviceRegistrationResponse
from app.schemas.readiness import ReadinessStatus
from app.schemas.sessions import SessionSummary
from app.schemas.telemetry import (
    ErrorResponse,
    MobileWifiObservation,
    ObservationBatch,
    RoomMap,
    SelectedNetwork,
    SignalQuality,
    TelemetryScan,
)

__all__ = [
    "AIAnalysis",
    "AIAnalyzeScanRequest",
    "AIAnalyzeSessionRequest",
    "CalibrationCompleteRequest",
    "CalibrationSampleRequest",
    "CalibrationSession",
    "CalibrationStartRequest",
    "DeviceRegistration",
    "DeviceRegistrationResponse",
    "ErrorResponse",
    "MobileWifiObservation",
    "ObservationBatch",
    "ReadinessStatus",
    "RoomMap",
    "SelectedNetwork",
    "SessionSummary",
    "SignalQuality",
    "TelemetryScan",
    "ZoneFingerprint",
]

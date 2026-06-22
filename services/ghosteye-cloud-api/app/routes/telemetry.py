"""Telemetry routes for mobile WiFi observations."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request

from app.auth.jwt_auth import get_current_principal
from app.schemas.telemetry import MobileWifiObservation, ObservationBatch, TelemetryScan

router = APIRouter(dependencies=[Depends(get_current_principal)])


@router.post("/telemetry/observation", response_model=TelemetryScan)
def submit_observation(payload: MobileWifiObservation, request: Request) -> TelemetryScan:
    return request.app.state.pipeline.process_observation(payload)


@router.post("/telemetry/batch", response_model=TelemetryScan)
def submit_batch(payload: ObservationBatch, request: Request) -> TelemetryScan:
    return request.app.state.pipeline.process_batch(payload)


@router.post("/scan/analyze", response_model=TelemetryScan)
def analyze_scan(payload: MobileWifiObservation, request: Request) -> TelemetryScan:
    return request.app.state.pipeline.process_observation(payload)

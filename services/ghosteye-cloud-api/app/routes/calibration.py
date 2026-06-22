"""Calibration routes for empty-room baselines and zone fingerprints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth.jwt_auth import get_current_principal
from app.schemas.calibration import (
    CalibrationCompleteRequest,
    CalibrationSampleRequest,
    CalibrationSession,
    CalibrationStartRequest,
)

router = APIRouter(dependencies=[Depends(get_current_principal)])


@router.post("/calibration/empty-room/start", response_model=CalibrationSession)
def start_empty_room(payload: CalibrationStartRequest, request: Request) -> CalibrationSession:
    return request.app.state.calibration_store.start(
        kind="empty_room",
        team_id=payload.team_id,
        device_id=payload.device_id,
        session_id=payload.session_id,
        room_id=payload.room_id,
        metadata=payload.metadata,
    )


@router.post("/calibration/empty-room/sample", response_model=CalibrationSession)
def sample_empty_room(payload: CalibrationSampleRequest, request: Request) -> CalibrationSession:
    return _add_sample(payload, request)


@router.post("/calibration/empty-room/complete", response_model=CalibrationSession)
def complete_empty_room(payload: CalibrationCompleteRequest, request: Request) -> CalibrationSession:
    return _complete(payload, request)


@router.post("/calibration/zone/start", response_model=CalibrationSession)
def start_zone(payload: CalibrationStartRequest, request: Request) -> CalibrationSession:
    if not payload.zone_label:
        raise HTTPException(status_code=400, detail="zone_label is required for zone calibration")
    return request.app.state.calibration_store.start(
        kind="zone",
        team_id=payload.team_id,
        device_id=payload.device_id,
        session_id=payload.session_id,
        room_id=payload.room_id,
        zone_label=payload.zone_label,
        metadata=payload.metadata,
    )


@router.post("/calibration/zone/sample", response_model=CalibrationSession)
def sample_zone(payload: CalibrationSampleRequest, request: Request) -> CalibrationSession:
    return _add_sample(payload, request)


@router.post("/calibration/zone/complete", response_model=CalibrationSession)
def complete_zone(payload: CalibrationCompleteRequest, request: Request) -> CalibrationSession:
    return _complete(payload, request)


def _add_sample(payload: CalibrationSampleRequest, request: Request) -> CalibrationSession:
    try:
        return request.app.state.calibration_store.add_sample(payload.calibration_id, payload.observation)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


def _complete(payload: CalibrationCompleteRequest, request: Request) -> CalibrationSession:
    try:
        return request.app.state.calibration_store.complete(payload.calibration_id, payload.metadata)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

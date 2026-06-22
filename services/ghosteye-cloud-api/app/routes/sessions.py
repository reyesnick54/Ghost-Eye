"""Session routes and WebSocket telemetry streaming."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect

from app.auth.jwt_auth import get_current_principal, verify_token
from app.config import get_settings
from app.schemas.sessions import SessionSummary

router = APIRouter()


@router.get("/sessions/latest", response_model=SessionSummary, dependencies=[Depends(get_current_principal)])
def latest_session(request: Request) -> SessionSummary:
    session = request.app.state.session_store.get_latest_session()
    if session is None:
        raise HTTPException(status_code=404, detail="No sessions available")
    return session


@router.get("/sessions/{session_id}", response_model=SessionSummary, dependencies=[Depends(get_current_principal)])
def get_session(session_id: str, request: Request) -> SessionSummary:
    session = request.app.state.session_store.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Unknown session_id: {session_id}")
    return session


@router.websocket("/ws/session/{session_id}")
async def session_websocket(websocket: WebSocket, session_id: str) -> None:
    settings = get_settings()
    token = websocket.query_params.get("token")
    if settings.ghosteye_env.lower() not in {"development", "test", "local"}:
        if not token:
            await websocket.close(code=1008)
            return
        try:
            verify_token(token, settings.ghosteye_api_secret)
        except ValueError:
            await websocket.close(code=1008)
            return

    await websocket.accept()
    try:
        while True:
            session = websocket.app.state.session_store.get_session(session_id)
            payload: dict[str, Any]
            if session is None:
                payload = {
                    "type": "session_heartbeat",
                    "session_id": session_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "waiting_for_mobile_observations",
                }
            else:
                payload = {"type": "session_update", "session": session.model_dump(mode="json")}
            await websocket.send_json(payload)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        return

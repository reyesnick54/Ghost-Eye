"""WebSocket helpers for streaming GhostEye telemetry."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect


async def stream_telemetry(
    websocket: WebSocket,
    telemetry_provider: Callable[[], Mapping[str, Any]],
    *,
    interval_seconds: float = 1.0,
) -> None:
    """Accept a client and stream JSON telemetry at a bounded demo cadence."""

    await websocket.accept()
    sleep_seconds = max(1.0, min(2.0, float(interval_seconds)))
    try:
        while True:
            await websocket.send_json(dict(telemetry_provider()))
            await asyncio.sleep(sleep_seconds)
    except WebSocketDisconnect:
        return

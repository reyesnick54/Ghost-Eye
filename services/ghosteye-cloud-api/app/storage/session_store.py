"""Thread-safe JSON-compatible session and device storage."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from app.schemas.devices import DeviceRegistration, DeviceRegistrationResponse
from app.schemas.sessions import SessionSummary
from app.schemas.telemetry import MobileWifiObservation, TelemetryScan


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SessionStore:
    """Minimal storage adapter for hosted session state."""

    def __init__(self, storage_dir: Path) -> None:
        self._lock = Lock()
        self._storage_dir = storage_dir
        self._sessions: dict[str, SessionSummary] = {}
        self._devices: dict[str, dict[str, Any]] = {}
        self._scans: dict[str, list[TelemetryScan]] = {}
        self._load()

    def register_device(
        self,
        registration: DeviceRegistration,
        access_token: str,
        expires_in_seconds: int,
    ) -> DeviceRegistrationResponse:
        device_id = registration.device_id or f"dev_{uuid.uuid4().hex[:12]}"
        response = DeviceRegistrationResponse(
            device_id=device_id,
            team_id=registration.team_id,
            platform=registration.platform,
            registered_at=utc_now(),
            access_token=access_token,
            expires_in_seconds=expires_in_seconds,
            metadata={
                "app_version": registration.app_version,
                "device_model": registration.device_model,
                "capability_mode": registration.capability_mode,
                **registration.metadata,
            },
        )
        with self._lock:
            self._devices[device_id] = response.model_dump(mode="json")
            self._persist()
        return response

    def add_scan(self, observation: MobileWifiObservation, scan: TelemetryScan) -> SessionSummary:
        with self._lock:
            existing = self._sessions.get(observation.session_id)
            if existing is None:
                existing = SessionSummary(
                    session_id=observation.session_id,
                    team_id=observation.team_id,
                    device_id=observation.device_id,
                    room_id=observation.room_id,
                    started_at=scan.timestamp,
                    updated_at=scan.timestamp,
                    scan_count=0,
                    metadata={"source": "mobile_wifi_observation"},
                )

            scans = self._scans.setdefault(observation.session_id, [])
            scans.append(scan)
            summary = existing.model_copy(
                update={
                    "updated_at": scan.timestamp,
                    "scan_count": existing.scan_count + 1,
                    "latest_scan": scan,
                    "room_id": observation.room_id or existing.room_id,
                    "device_id": observation.device_id,
                }
            )
            self._sessions[observation.session_id] = summary
            self._persist()
            return summary

    def get_session(self, session_id: str) -> SessionSummary | None:
        with self._lock:
            return self._sessions.get(session_id)

    def get_latest_session(self) -> SessionSummary | None:
        with self._lock:
            if not self._sessions:
                return None
            return max(self._sessions.values(), key=lambda session: session.updated_at)

    def get_session_scans(self, session_id: str) -> list[TelemetryScan]:
        with self._lock:
            return list(self._scans.get(session_id, []))

    def recent_observations(self, session_id: str, limit: int = 20) -> list[TelemetryScan]:
        with self._lock:
            return list(self._scans.get(session_id, [])[-limit:])

    def readiness(self) -> dict[str, str]:
        return {
            "type": "json_compatible_session_store",
            "path": str(self._storage_dir),
            "status": "ready",
        }

    def _load(self) -> None:
        path = self._storage_dir / "sessions.json"
        if not path.exists():
            return
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        self._devices = payload.get("devices", {}) if isinstance(payload.get("devices"), dict) else {}
        for raw in payload.get("sessions", []):
            try:
                session = SessionSummary.model_validate(raw)
            except Exception:
                continue
            self._sessions[session.session_id] = session
        for session_id, scans in payload.get("scans", {}).items():
            parsed: list[TelemetryScan] = []
            for raw_scan in scans:
                try:
                    parsed.append(TelemetryScan.model_validate(raw_scan))
                except Exception:
                    continue
            self._scans[session_id] = parsed

    def _persist(self) -> None:
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._storage_dir / "sessions.json"
        payload = {
            "devices": self._devices,
            "sessions": [session.model_dump(mode="json") for session in self._sessions.values()],
            "scans": {
                session_id: [scan.model_dump(mode="json") for scan in scans]
                for session_id, scans in self._scans.items()
            },
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

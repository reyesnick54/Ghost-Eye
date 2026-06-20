"""JSON-backed session logging for GhostEye v0.2."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Dict, Optional
from uuid import uuid4


DEFAULT_SESSION_LOG_DIR = Path(__file__).resolve().parents[1] / "sessions" / "logs"


class SessionLearner:
    """Persist lightweight session records and scan summaries as JSON."""

    def __init__(self, session_log_dir: str | Path | None = None) -> None:
        self.session_log_dir = Path(session_log_dir or DEFAULT_SESSION_LOG_DIR)
        self.session_log_dir.mkdir(parents=True, exist_ok=True)
        self.active_session_id: Optional[str] = None

    def start_session(self, session_id: Optional[str] = None, metadata: Optional[dict[str, Any]] = None) -> Dict[str, Any]:
        safe_id = self._safe_id(session_id or uuid4().hex)
        record = {
            "session_id": safe_id,
            "active": True,
            "started_at": self._utc_now(),
            "stopped_at": None,
            "metadata": dict(metadata or {}),
            "scan_count": 0,
            "latest_scan": None,
        }
        self.active_session_id = safe_id
        self._write(record)
        return record

    def stop_session(self) -> Dict[str, Any]:
        record = self.latest_session() or self.start_session()
        record["active"] = False
        record["stopped_at"] = self._utc_now()
        self.active_session_id = None
        self._write(record)
        return record

    def append_scan(self, telemetry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.active_session_id:
            return None
        record = self._read(self._path(self.active_session_id)) or self.start_session(self.active_session_id)
        record["scan_count"] = int(record.get("scan_count") or 0) + 1
        record["latest_scan"] = deepcopy(telemetry)
        record["updated_at"] = self._utc_now()
        self._write(record)
        return record

    def latest_session(self) -> Optional[Dict[str, Any]]:
        if self.active_session_id:
            active = self._read(self._path(self.active_session_id))
            if active:
                return active
        records = [self._read(path) for path in sorted(self.session_log_dir.glob("*.json"), key=lambda item: item.stat().st_mtime)]
        records = [record for record in records if isinstance(record, dict)]
        return records[-1] if records else None

    def _path(self, session_id: str) -> Path:
        return self.session_log_dir / f"{self._safe_id(session_id)}.json"

    def _write(self, record: Dict[str, Any]) -> None:
        path = self._path(str(record["session_id"]))
        with path.open("w", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2, sort_keys=True)
            handle.write("\n")

    def _read(self, path: Path) -> Optional[Dict[str, Any]]:
        if not path.exists():
            return None
        try:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    @staticmethod
    def _safe_id(value: str) -> str:
        safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", str(value)).strip("._-")
        return safe or uuid4().hex

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


GhostEyeSessionLearner = SessionLearner

"""JSON-compatible calibration storage for baselines and zone fingerprints."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean
from threading import Lock
from typing import Any

from app.schemas.calibration import CalibrationSession, ZoneFingerprint
from app.schemas.telemetry import MobileWifiObservation, SignalQuality


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CalibrationStore:
    """Store server-side calibration sessions and derived artifacts."""

    def __init__(self, storage_dir: Path) -> None:
        self._lock = Lock()
        self._storage_dir = storage_dir
        self._sessions: dict[str, CalibrationSession] = {}
        self._samples: dict[str, list[MobileWifiObservation]] = {}
        self._empty_room_baselines: dict[str, dict[str, Any]] = {}
        self._fingerprints: dict[str, ZoneFingerprint] = {}
        self._load()

    def start(
        self,
        *,
        kind: str,
        team_id: str,
        device_id: str,
        session_id: str | None,
        room_id: str | None,
        zone_label: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CalibrationSession:
        calibration_id = f"cal_{kind}_{uuid.uuid4().hex[:12]}"
        session = CalibrationSession(
            calibration_id=calibration_id,
            team_id=team_id,
            device_id=device_id,
            session_id=session_id,
            room_id=room_id,
            zone_label=zone_label,
            kind=kind,  # type: ignore[arg-type]
            status="started",
            started_at=utc_now(),
            metadata=metadata or {},
        )
        with self._lock:
            self._sessions[calibration_id] = session
            self._samples[calibration_id] = []
            self._persist()
        return session

    def add_sample(self, calibration_id: str, observation: MobileWifiObservation) -> CalibrationSession:
        with self._lock:
            session = self._require_session(calibration_id)
            samples = self._samples.setdefault(calibration_id, [])
            samples.append(observation)
            updated = session.model_copy(update={"status": "sampling", "sample_count": len(samples)})
            self._sessions[calibration_id] = updated
            self._persist()
            return updated

    def complete(self, calibration_id: str, metadata: dict[str, Any] | None = None) -> CalibrationSession:
        with self._lock:
            session = self._require_session(calibration_id)
            samples = self._samples.get(calibration_id, [])
            if not samples:
                raise ValueError("Calibration requires at least one sample")

            quality = _average_signal_quality(samples)
            update: dict[str, Any] = {
                "status": "completed",
                "completed_at": utc_now(),
                "sample_count": len(samples),
                "signal_quality": quality,
                "metadata": {**session.metadata, **(metadata or {})},
            }
            if session.kind == "empty_room":
                baseline = _average_observations(samples)
                baseline.update(
                    {
                        "baseline_id": calibration_id,
                        "team_id": session.team_id,
                        "room_id": session.room_id,
                        "created_at": utc_now().isoformat(),
                        "sample_count": len(samples),
                    }
                )
                self._empty_room_baselines[_baseline_key(session.team_id, session.room_id)] = baseline
                update["baseline"] = baseline
            else:
                zone_label = session.zone_label or samples[-1].zone_label or "unknown"
                fingerprint = ZoneFingerprint(
                    fingerprint_id=calibration_id,
                    team_id=session.team_id,
                    room_id=session.room_id,
                    zone_label=zone_label,
                    created_at=utc_now(),
                    sample_count=len(samples),
                    rssi_dbm_mean=_mean_optional(sample.rssi_dbm for sample in samples),
                    gateway_latency_ms_mean=_mean_optional(sample.gateway_latency_ms for sample in samples),
                    jitter_ms_mean=_mean_optional(sample.jitter_ms for sample in samples),
                    packet_loss_mean=_mean_optional(sample.packet_loss for sample in samples),
                    signal_quality=quality,
                    metadata={"calibration_id": calibration_id},
                )
                self._fingerprints[calibration_id] = fingerprint
                update["fingerprint"] = fingerprint.model_dump(mode="json")

            completed = session.model_copy(update=update)
            self._sessions[calibration_id] = completed
            self._persist()
            return completed

    def get_baseline(self, team_id: str, room_id: str | None) -> dict[str, Any] | None:
        with self._lock:
            return self._empty_room_baselines.get(_baseline_key(team_id, room_id))

    def list_fingerprints(self, team_id: str, room_id: str | None) -> list[ZoneFingerprint]:
        with self._lock:
            return [
                fingerprint
                for fingerprint in self._fingerprints.values()
                if fingerprint.team_id == team_id and fingerprint.room_id == room_id
            ]

    def readiness(self) -> dict[str, str]:
        return {
            "type": "json_compatible_calibration_store",
            "path": str(self._storage_dir),
            "status": "ready",
        }

    def _require_session(self, calibration_id: str) -> CalibrationSession:
        session = self._sessions.get(calibration_id)
        if session is None:
            raise KeyError(f"Unknown calibration_id: {calibration_id}")
        return session

    def _load(self) -> None:
        path = self._storage_dir / "calibrations.json"
        if not path.exists():
            return
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        self._empty_room_baselines = payload.get("empty_room_baselines", {})
        for raw in payload.get("sessions", []):
            try:
                session = CalibrationSession.model_validate(raw)
            except Exception:
                continue
            self._sessions[session.calibration_id] = session
        for calibration_id, raw_samples in payload.get("samples", {}).items():
            parsed: list[MobileWifiObservation] = []
            for raw_sample in raw_samples:
                try:
                    parsed.append(MobileWifiObservation.model_validate(raw_sample))
                except Exception:
                    continue
            self._samples[calibration_id] = parsed
        for raw in payload.get("fingerprints", []):
            try:
                fingerprint = ZoneFingerprint.model_validate(raw)
            except Exception:
                continue
            self._fingerprints[fingerprint.fingerprint_id] = fingerprint

    def _persist(self) -> None:
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._storage_dir / "calibrations.json"
        payload = {
            "sessions": [session.model_dump(mode="json") for session in self._sessions.values()],
            "samples": {
                calibration_id: [sample.model_dump(mode="json") for sample in samples]
                for calibration_id, samples in self._samples.items()
            },
            "empty_room_baselines": self._empty_room_baselines,
            "fingerprints": [
                fingerprint.model_dump(mode="json") for fingerprint in self._fingerprints.values()
            ],
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _baseline_key(team_id: str, room_id: str | None) -> str:
    return f"{team_id}:{room_id or 'default'}"


def _average_observations(samples: list[MobileWifiObservation]) -> dict[str, Any]:
    return {
        "rssi_dbm_mean": _mean_optional(sample.rssi_dbm for sample in samples),
        "gateway_latency_ms_mean": _mean_optional(sample.gateway_latency_ms for sample in samples),
        "jitter_ms_mean": _mean_optional(sample.jitter_ms for sample in samples),
        "packet_loss_mean": _mean_optional(sample.packet_loss for sample in samples),
        "visible_access_points_mean": _mean_optional(sample.visible_access_points for sample in samples),
        "ssid": samples[-1].ssid,
        "bssid_masked": samples[-1].bssid_masked,
        "vendor_hint": samples[-1].vendor_hint,
    }


def _average_signal_quality(samples: list[MobileWifiObservation]) -> SignalQuality:
    visible = int(round(_mean_optional(sample.visible_access_points for sample in samples) or 0))
    latency = _mean_optional(sample.gateway_latency_ms for sample in samples)
    jitter = _mean_optional(sample.jitter_ms for sample in samples)
    packet_loss = _mean_optional(sample.packet_loss for sample in samples)
    rssi = _mean_optional(sample.rssi_dbm for sample in samples)
    rssi_values = [float(sample.rssi_dbm) for sample in samples if sample.rssi_dbm is not None]
    stability = max(0.0, min(1.0, 1.0 - ((max(rssi_values) - min(rssi_values)) / 18.0))) if rssi_values else 0.35
    quality = _quality_score(visible, latency, jitter, packet_loss, stability)
    return SignalQuality(
        visible_access_points=visible,
        gateway_latency_ms=latency,
        jitter_ms=jitter,
        packet_loss=packet_loss,
        rssi_dbm=rssi,
        rssi_stability=round(stability, 3),
        quality_score=round(quality, 3),
    )


def _quality_score(
    visible_access_points: int,
    latency: float | None,
    jitter: float | None,
    packet_loss: float | None,
    rssi_stability: float,
) -> float:
    ap_score = min(1.0, visible_access_points / 3.0)
    latency_score = 1.0 if latency is None else max(0.0, 1.0 - (latency / 350.0))
    jitter_score = 1.0 if jitter is None else max(0.0, 1.0 - (jitter / 120.0))
    loss_score = 1.0 if packet_loss is None else max(0.0, 1.0 - (packet_loss * 4.0))
    return (ap_score * 0.20) + (latency_score * 0.20) + (jitter_score * 0.15) + (loss_score * 0.20) + (rssi_stability * 0.25)


def _mean_optional(values: Any) -> float | None:
    numbers = [float(value) for value in values if value is not None]
    if not numbers:
        return None
    return round(fmean(numbers), 4)

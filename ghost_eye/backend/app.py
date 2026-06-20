from __future__ import annotations

import asyncio
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random
import statistics
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional

from fastapi import Body, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ghost_eye.inference import DeviceMotionCompensator, DeviceMotionState

app = FastAPI(title="Ghost-Eye Demo API")
device_motion_compensator = DeviceMotionCompensator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


NOTICE = "Demo simulation only. Authorized test environments only."
DATA_DIR = Path(__file__).resolve().parent / "data"
EMPTY_ROOM_BASELINE_FILE = DATA_DIR / "empty_room_baseline.json"
ZONE_FINGERPRINTS_FILE = DATA_DIR / "zone_fingerprints.json"
AI_ANALYSIS_ENV = "GHOSTEYE_AI_ANALYSIS"
AI_MODE = "analysis_only_no_autonomy"
AI_EXCLUDED_LAYERS = [
    "c4isr",
    "autonomy",
    "robotics_control",
    "targeting",
    "weapons",
    "mission_command",
]


@dataclass
class AccessPointReading:
    bssid: str
    ssid: str
    rssi: float
    channel: int
    frequency_mhz: int


@dataclass
class WiFiObservation:
    timestamp: float
    source_id: str
    source_name: str
    mode: str
    access_points: List[AccessPointReading]
    sample_count: int


@dataclass
class SignalCapabilities:
    input_type: str
    adapter: str
    has_csi: bool
    has_rssi: bool
    access_point_count: int
    sample_count: int
    quality_score: float
    limitations: List[str]


@dataclass
class DisturbanceField:
    motion_score: float
    presence: str
    baseline_available: bool
    mean_delta_db: float
    max_delta_db: float
    changed_bssids: List[str]
    grid: List[List[float]]


@dataclass
class FingerprintMatch:
    available: bool
    zone: str
    confidence: float
    matched_zone: Optional[str] = None
    distance: Optional[float] = None


@dataclass
class TomographyMap:
    available: bool
    grid: List[List[float]]
    hotspots: List[Dict[str, Any]]
    method: str = "opportunistic_rssi"


@dataclass
class AdaptiveBaselineState:
    baseline_available: bool
    updated: bool
    drift_score: float
    sample_count: int


@dataclass
class ConfidenceCeiling:
    ceiling: float
    raw_confidence: float
    confidence: float
    factors: Dict[str, bool]


@dataclass
class SessionState:
    active: bool = False
    session_id: Optional[str] = None
    started_at: Optional[float] = None
    stopped_at: Optional[float] = None


@dataclass
class GhostEyeTelemetry:
    timestamp: float
    mode: str
    presence: str
    motion_score: float
    zone: str
    confidence: float
    notice: str
    telemetry_type: str = "GhostEyeTelemetry"
    source: Dict[str, Any] = field(default_factory=dict)
    observation: Dict[str, Any] = field(default_factory=dict)
    capabilities: Dict[str, Any] = field(default_factory=dict)
    baseline: Dict[str, Any] = field(default_factory=dict)
    disturbance: Dict[str, Any] = field(default_factory=dict)
    fingerprint: Dict[str, Any] = field(default_factory=dict)
    tomography: Dict[str, Any] = field(default_factory=dict)
    adaptive_baseline: Dict[str, Any] = field(default_factory=dict)
    confidence_ceiling: Dict[str, Any] = field(default_factory=dict)
    session: Dict[str, Any] = field(default_factory=dict)
    ai_analysis: Optional[Dict[str, Any]] = None

    def to_response(self) -> Dict[str, Any]:
        """Return JSON that keeps the original mobile demo fields at top level."""
        response = asdict(self)
        if response.get("ai_analysis") is None:
            response.pop("ai_analysis", None)
        return response


class WiFiOnlyAdapter:
    """WiFi RSSI-only observation source used until CSI hardware is attached."""

    def __init__(self) -> None:
        self._sources = [
            {
                "id": "simulated_wifi",
                "name": "Simulated WiFi RSSI",
                "type": "wifi_rssi",
                "selected": True,
                "status": "available",
                "capabilities": ["rssi_scan"],
            }
        ]
        self._selected_source_id = "simulated_wifi"
        self._ap_templates = [
            ("02:00:00:00:00:01", "ghost-eye-lab-a", 1, 2412, -48),
            ("02:00:00:00:00:02", "ghost-eye-lab-b", 6, 2437, -57),
            ("02:00:00:00:00:03", "ghost-eye-lab-c", 11, 2462, -64),
            ("02:00:00:00:00:04", "ghost-eye-lab-d", 36, 5180, -71),
        ]

    def sources(self) -> List[Dict[str, Any]]:
        return [
            {**source, "selected": source["id"] == self._selected_source_id}
            for source in self._sources
        ]

    def select_source(self, source_id: str) -> Dict[str, Any]:
        for source in self._sources:
            if source["id"] == source_id:
                self._selected_source_id = source_id
                return {**source, "selected": True}
        raise ValueError(f"Unknown source: {source_id}")

    def observe(self) -> WiFiObservation:
        now = time.time()
        wave = math.sin(now / 6.0)
        burst = 1.0 if random.random() > 0.72 else 0.0
        readings = []

        for index, (bssid, ssid, channel, frequency, base_rssi) in enumerate(self._ap_templates):
            multipath_shift = wave * (index + 1) * 1.4
            transient_shift = burst * random.uniform(-8.0, 8.0) / (index + 1)
            noise = random.gauss(0.0, 1.8)
            readings.append(
                AccessPointReading(
                    bssid=bssid,
                    ssid=ssid,
                    rssi=round(base_rssi + multipath_shift + transient_shift + noise, 2),
                    channel=channel,
                    frequency_mhz=frequency,
                )
            )

        return WiFiObservation(
            timestamp=now,
            source_id=self._selected_source_id,
            source_name="Simulated WiFi RSSI",
            mode="simulated",
            access_points=readings,
            sample_count=len(readings),
        )


class SignalCapabilityProfiler:
    def run(self, observation: WiFiObservation) -> SignalCapabilities:
        rssis = [reading.rssi for reading in observation.access_points]
        spread = statistics.pstdev(rssis) if len(rssis) > 1 else 0.0
        ap_score = min(1.0, len(rssis) / 4.0)
        stability_score = max(0.0, 1.0 - spread / 30.0)
        quality_score = round((ap_score * 0.7) + (stability_score * 0.3), 3)

        return SignalCapabilities(
            input_type="wifi_rssi",
            adapter="WiFiOnlyAdapter",
            has_csi=False,
            has_rssi=True,
            access_point_count=len(rssis),
            sample_count=observation.sample_count,
            quality_score=quality_score,
            limitations=[
                "RSSI-only observations provide coarse disturbance estimates.",
                "CSI hardware is not attached in this demo backend.",
            ],
        )


class DisturbanceFieldDetector:
    def run(
        self,
        observation: WiFiObservation,
        baseline: Optional[Dict[str, Any]],
    ) -> DisturbanceField:
        readings_by_bssid = {
            reading.bssid: reading.rssi for reading in observation.access_points
        }
        baseline_readings = (baseline or {}).get("rssi_by_bssid", {})
        deltas = []
        changed_bssids = []

        for bssid, rssi in readings_by_bssid.items():
            if bssid in baseline_readings:
                delta = abs(rssi - float(baseline_readings[bssid]))
                deltas.append(delta)
                if delta >= 4.0:
                    changed_bssids.append(bssid)

        if deltas:
            mean_delta = statistics.mean(deltas)
            max_delta = max(deltas)
            motion_score = min(0.98, (mean_delta / 11.0) + (max_delta / 24.0))
        else:
            rssis = list(readings_by_bssid.values())
            spread = statistics.pstdev(rssis) if len(rssis) > 1 else 0.0
            mean_delta = 0.0
            max_delta = 0.0
            motion_score = min(0.95, 0.12 + (spread / 32.0) + random.uniform(0.0, 0.18))

        motion_score = round(motion_score, 2)
        if motion_score > 0.7:
            presence = "presence_detected"
        elif motion_score > 0.4:
            presence = "possible_presence"
        else:
            presence = "clear"

        return DisturbanceField(
            motion_score=motion_score,
            presence=presence,
            baseline_available=baseline is not None,
            mean_delta_db=round(mean_delta, 2),
            max_delta_db=round(max_delta, 2),
            changed_bssids=changed_bssids,
            grid=self._grid_from_deltas(deltas, motion_score),
        )

    @staticmethod
    def _grid_from_deltas(deltas: List[float], motion_score: float) -> List[List[float]]:
        if not deltas:
            deltas = [motion_score * 8.0, motion_score * 5.0, motion_score * 3.0]

        grid = []
        for row in range(3):
            values = []
            for col in range(3):
                index = (row + col) % len(deltas)
                value = min(1.0, (deltas[index] / 12.0) * (0.75 + (row + col) / 8.0))
                values.append(round(value, 2))
            grid.append(values)
        return grid


class RoomFingerprintMapper:
    def run(
        self,
        observation: WiFiObservation,
        fingerprints: Dict[str, Any],
    ) -> FingerprintMatch:
        if not fingerprints:
            return FingerprintMatch(available=False, zone="unknown", confidence=0.0)

        current = {reading.bssid: reading.rssi for reading in observation.access_points}
        best_zone = None
        best_distance = None

        for zone, fingerprint in fingerprints.items():
            stored = fingerprint.get("rssi_by_bssid", {})
            common = set(current).intersection(stored)
            if not common:
                continue
            distance = statistics.mean(
                abs(current[bssid] - float(stored[bssid])) for bssid in common
            )
            if best_distance is None or distance < best_distance:
                best_zone = zone
                best_distance = distance

        if best_zone is None or best_distance is None:
            return FingerprintMatch(available=True, zone="unknown", confidence=0.0)

        confidence = round(max(0.1, min(0.96, 1.0 - best_distance / 18.0)), 2)
        return FingerprintMatch(
            available=True,
            zone=best_zone,
            confidence=confidence,
            matched_zone=best_zone,
            distance=round(best_distance, 2),
        )


class OpportunisticRSSITomography:
    def run(
        self,
        observation: WiFiObservation,
        disturbance: DisturbanceField,
    ) -> TomographyMap:
        hotspots = []
        for row_index, row in enumerate(disturbance.grid):
            for col_index, value in enumerate(row):
                if value >= 0.55:
                    hotspots.append(
                        {
                            "x": col_index,
                            "y": row_index,
                            "intensity": value,
                        }
                    )

        return TomographyMap(
            available=bool(observation.access_points),
            grid=disturbance.grid,
            hotspots=hotspots,
        )


class AdaptiveBaselineEngine:
    def run(
        self,
        observation: WiFiObservation,
        baseline: Optional[Dict[str, Any]],
        disturbance: DisturbanceField,
    ) -> AdaptiveBaselineState:
        if baseline is None:
            return AdaptiveBaselineState(
                baseline_available=False,
                updated=False,
                drift_score=0.0,
                sample_count=0,
            )

        drift_score = disturbance.mean_delta_db
        updated = False
        sample_count = int(baseline.get("sample_count", 1))

        if disturbance.presence == "clear" and drift_score <= 2.5:
            existing = baseline.get("rssi_by_bssid", {})
            for reading in observation.access_points:
                previous = float(existing.get(reading.bssid, reading.rssi))
                existing[reading.bssid] = round((previous * 0.95) + (reading.rssi * 0.05), 2)
            baseline["rssi_by_bssid"] = existing
            baseline["updated_at"] = observation.timestamp
            baseline["sample_count"] = sample_count + 1
            save_json(EMPTY_ROOM_BASELINE_FILE, baseline)
            updated = True
            sample_count += 1

        return AdaptiveBaselineState(
            baseline_available=True,
            updated=updated,
            drift_score=round(drift_score, 2),
            sample_count=sample_count,
        )


class ConfidenceCeilingEngine:
    def run(
        self,
        raw_confidence: float,
        capabilities: SignalCapabilities,
        baseline: Optional[Dict[str, Any]],
        fingerprint: FingerprintMatch,
    ) -> ConfidenceCeiling:
        factors = {
            "has_csi": capabilities.has_csi,
            "has_baseline": baseline is not None,
            "has_fingerprint": fingerprint.available,
            "rssi_only": capabilities.has_rssi and not capabilities.has_csi,
        }
        ceiling = 0.97
        if not capabilities.has_csi:
            ceiling = min(ceiling, 0.86)
        if baseline is None:
            ceiling = min(ceiling, 0.74)
        if not fingerprint.available:
            ceiling = min(ceiling, 0.78)
        ceiling = round(max(0.35, ceiling * capabilities.quality_score), 2)

        return ConfidenceCeiling(
            ceiling=ceiling,
            raw_confidence=round(raw_confidence, 2),
            confidence=round(min(raw_confidence, ceiling), 2),
            factors=factors,
        )


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: Path, payload: Any) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)


def observation_rssi_map(observation: WiFiObservation) -> Dict[str, float]:
    return {reading.bssid: reading.rssi for reading in observation.access_points}


def env_flag_enabled(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def s3m_core_available() -> bool:
    return importlib.util.find_spec("s3m_core") is not None


def ai_status_payload() -> Dict[str, Any]:
    s3m_available = s3m_core_available()
    return {
        "enabled": env_flag_enabled(AI_ANALYSIS_ENV),
        "provider": "s3m_core" if s3m_available else "fallback",
        "s3m_available": s3m_available,
        "mode": AI_MODE,
        "excluded_layers": AI_EXCLUDED_LAYERS,
    }


def build_ai_analysis(scan_payload: Dict[str, Any]) -> Dict[str, Any]:
    status = ai_status_payload()
    motion_score = float(scan_payload.get("motion_score") or 0.0)
    confidence = float(scan_payload.get("confidence") or 0.0)
    presence = str(scan_payload.get("presence") or "unknown")
    zone = str(scan_payload.get("zone") or "unknown")

    if presence == "presence_detected":
        summary = "Presence-like signal disturbance detected in the scan."
    elif presence == "possible_presence":
        summary = "Scan shows possible presence-like signal disturbance."
    elif presence == "clear":
        summary = "Scan is currently consistent with a clear environment."
    else:
        summary = "Scan analysis completed with an unknown presence state."

    return {
        "available": True,
        "provider": status["provider"],
        "mode": status["mode"],
        "summary": summary,
        "confidence": round(min(1.0, max(0.0, confidence)), 2),
        "signals": {
            "presence": presence,
            "motion_score": round(min(1.0, max(0.0, motion_score)), 2),
            "zone": zone,
        },
        "excluded_layers": status["excluded_layers"],
        "limitations": [
            "Analysis is limited to coarse WiFi RSSI telemetry.",
            "No autonomy, targeting, weapons, mission command, robotics control, or C4ISR layers are used.",
        ],
    }


adapter = WiFiOnlyAdapter()
capability_profiler = SignalCapabilityProfiler()
disturbance_detector = DisturbanceFieldDetector()
fingerprint_mapper = RoomFingerprintMapper()
tomography_engine = OpportunisticRSSITomography()
adaptive_baseline_engine = AdaptiveBaselineEngine()
confidence_ceiling_engine = ConfidenceCeilingEngine()
state_lock = Lock()
session_state = SessionState()
latest_telemetry: Optional[GhostEyeTelemetry] = None


def build_telemetry() -> GhostEyeTelemetry:
    global latest_telemetry

    observation = adapter.observe()
    capabilities = capability_profiler.run(observation)
    baseline = load_json(EMPTY_ROOM_BASELINE_FILE, None)
    disturbance = disturbance_detector.run(observation, baseline)
    fingerprints = load_json(ZONE_FINGERPRINTS_FILE, {})
    fingerprint = fingerprint_mapper.run(observation, fingerprints)
    tomography = tomography_engine.run(observation, disturbance)
    adaptive_baseline = adaptive_baseline_engine.run(observation, baseline, disturbance)

    fallback_zone = random.choice(["zone_a", "zone_b", "zone_c", "unknown"])
    zone = fingerprint.zone if fingerprint.available and fingerprint.zone != "unknown" else fallback_zone
    baseline_bonus = 0.12 if baseline is not None else 0.0
    fingerprint_bonus = fingerprint.confidence * 0.22 if fingerprint.available else 0.0
    raw_confidence = min(
        0.96,
        0.52
        + (capabilities.quality_score * 0.18)
        + (disturbance.motion_score * 0.14)
        + baseline_bonus
        + fingerprint_bonus,
    )
    confidence_ceiling = confidence_ceiling_engine.run(
        raw_confidence=raw_confidence,
        capabilities=capabilities,
        baseline=baseline,
        fingerprint=fingerprint,
    )

    telemetry = GhostEyeTelemetry(
        timestamp=observation.timestamp,
        mode=observation.mode,
        presence=disturbance.presence,
        motion_score=disturbance.motion_score,
        zone=zone,
        confidence=confidence_ceiling.confidence,
        notice=NOTICE,
        source={
            "id": observation.source_id,
            "name": observation.source_name,
            "type": "wifi_rssi",
        },
        observation=asdict(observation),
        capabilities=asdict(capabilities),
        baseline={
            "available": baseline is not None,
            "created_at": (baseline or {}).get("created_at"),
            "updated_at": (baseline or {}).get("updated_at"),
            "sample_count": (baseline or {}).get("sample_count", 0),
        },
        disturbance=asdict(disturbance),
        fingerprint=asdict(fingerprint),
        tomography=asdict(tomography),
        adaptive_baseline=asdict(adaptive_baseline),
        confidence_ceiling=asdict(confidence_ceiling),
        session=asdict(session_state),
    )

    if env_flag_enabled(AI_ANALYSIS_ENV):
        telemetry.ai_analysis = build_ai_analysis(telemetry.to_response())

    with state_lock:
        latest_telemetry = telemetry

    return telemetry


@app.get("/")
def root():
    return {
        "name": "Ghost-Eye",
        "status": "online",
        "mode": "simulated-demo",
        "notice": NOTICE,
        "endpoints": [
            "/health",
            "/scan",
            "/ai/status",
            "/ai/analyze-scan",
            "/sources",
            "/source/select",
            "/calibrate/empty-room",
            "/calibrate/zone",
            "/session/start",
            "/session/stop",
            "/session/latest",
            "/map/current",
            "/ws/telemetry",
        ],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "source": next((source for source in adapter.sources() if source["selected"]), None),
        "session": asdict(session_state),
    }


@app.get("/scan")
def scan():
    return build_telemetry().to_response()


@app.get("/ai/status")
def ai_status():
    return ai_status_payload()


@app.post("/ai/analyze-scan")
def analyze_scan(payload: Optional[Dict[str, Any]] = Body(default=None)):
    scan_payload = payload or build_telemetry().to_response()
    return {
        "status": ai_status_payload(),
        "ai_analysis": build_ai_analysis(scan_payload),
    }


@app.get("/sources")
def sources():
    return {"sources": adapter.sources()}
def scan(
    device_motion_state: Optional[DeviceMotionState] = Query(
        default=None,
        description="Optional device motion state: stable, moving, or unknown.",
    ),
):
    motion_score = round(random.uniform(0.05, 0.95), 2)
    device_motion = device_motion_compensator.compensate(device_motion_state)
    base_confidence = round(random.uniform(0.55, 0.96), 2)
    confidence = round(base_confidence * device_motion.confidence_multiplier, 2)


@app.post("/source/select")
def select_source(payload: Dict[str, Any] = Body(...)):
    source_id = payload.get("source_id") or payload.get("id")
    if not source_id:
        raise HTTPException(status_code=400, detail="source_id is required")

    try:
        selected = adapter.select_source(str(source_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {"selected": selected, "sources": adapter.sources()}


@app.post("/calibrate/empty-room")
def calibrate_empty_room():
    observation = adapter.observe()
    baseline = {
        "created_at": time.time(),
        "updated_at": time.time(),
        "source_id": observation.source_id,
        "sample_count": 1,
        "rssi_by_bssid": observation_rssi_map(observation),
        "access_points": [asdict(reading) for reading in observation.access_points],
    }
    save_json(EMPTY_ROOM_BASELINE_FILE, baseline)
    return {
        "status": "calibrated",
        "baseline": {
            "available": True,
            "sample_count": baseline["sample_count"],
            "access_point_count": len(observation.access_points),
            "updated_at": baseline["updated_at"],
        },
        "notice": NOTICE,
    }


@app.post("/calibrate/zone")
def calibrate_zone(payload: Dict[str, Any] = Body(...)):
    zone = str(payload.get("zone") or payload.get("zone_id") or "").strip()
    if not zone:
        raise HTTPException(status_code=400, detail="zone is required")

    observation = adapter.observe()
    fingerprints = load_json(ZONE_FINGERPRINTS_FILE, {})
    fingerprints[zone] = {
        "zone": zone,
        "created_at": time.time(),
        "updated_at": time.time(),
        "source_id": observation.source_id,
        "sample_count": int(fingerprints.get(zone, {}).get("sample_count", 0)) + 1,
        "rssi_by_bssid": observation_rssi_map(observation),
        "access_points": [asdict(reading) for reading in observation.access_points],
    }
    save_json(ZONE_FINGERPRINTS_FILE, fingerprints)
    return {
        "status": "calibrated",
        "zone": zone,
        "fingerprint_count": len(fingerprints),
        "notice": NOTICE,
    }


@app.post("/session/start")
def start_session(payload: Optional[Dict[str, Any]] = Body(default=None)):
    now = time.time()
    session_id = str((payload or {}).get("session_id") or uuid.uuid4())
    session_state.active = True
    session_state.session_id = session_id
    session_state.started_at = now
    session_state.stopped_at = None
    return {"session": asdict(session_state)}


@app.post("/session/stop")
def stop_session():
    session_state.active = False
    session_state.stopped_at = time.time()
    return {"session": asdict(session_state)}


@app.get("/session/latest")
def session_latest():
    with state_lock:
        telemetry = latest_telemetry
    return {
        "session": asdict(session_state),
        "telemetry": telemetry.to_response() if telemetry else None,
    }


@app.get("/map/current")
def current_map():
    with state_lock:
        telemetry = latest_telemetry

    if telemetry is None:
        telemetry = build_telemetry()

    return {
        "timestamp": telemetry.timestamp,
        "zone": telemetry.zone,
        "tomography": telemetry.tomography,
        "disturbance": telemetry.disturbance,
        "fingerprint": telemetry.fingerprint,
        "timestamp": time.time(),
        "mode": "simulated",
        "presence": presence,
        "motion_score": motion_score,
        "zone": random.choice(["zone_a", "zone_b", "zone_c", "unknown"]),
        "confidence": confidence,
        "device_stability": device_motion.device_stability,
        "confidence_multiplier": device_motion.confidence_multiplier,
        "scan_valid": device_motion.scan_valid,
        "reason": device_motion.reason,
        "notice": "Demo simulation only. Authorized test environments only."
    }


@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            telemetry = build_telemetry().to_response()
            await websocket.send_json(telemetry)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        return

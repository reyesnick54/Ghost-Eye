from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

from fastapi import Body, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ghost_eye.api.schemas import (  # noqa: E402
    LIMITATIONS,
    MODE_WIFI_ONLY_NON_CSI,
    NOTICE,
    SOURCE_LOCAL_WIFI_SIMULATED,
    GhostEyeScanResponse,
    SignalQuality,
    utc_now_iso,
)
from ghost_eye.csi_adapters import WiFiOnlyAdapter  # noqa: E402
from ghost_eye.inference import (  # noqa: E402
    ConfidenceCeilingEngine,
    DisturbanceFieldDetector,
    RoomFingerprintMapper,
    SessionLearner,
    SignalCapabilityProfiler,
)
from ghost_eye.inference.rss_tomography import OpportunisticRSSITomography  # noqa: E402


app = FastAPI(title="Ghost-Eye Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


SESSION_DIR = Path(__file__).resolve().parents[1] / "sessions"
LOG_DIR = SESSION_DIR / "logs"
BASELINE_DIR = SESSION_DIR / "baselines"
FINGERPRINT_DIR = SESSION_DIR / "fingerprints"
EMPTY_ROOM_BASELINE_FILE = BASELINE_DIR / "empty_room.json"
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

for directory in (LOG_DIR, BASELINE_DIR, FINGERPRINT_DIR):
    directory.mkdir(parents=True, exist_ok=True)


adapter = WiFiOnlyAdapter(seed=42, bssid_count=5)
capability_profiler = SignalCapabilityProfiler()
disturbance_detector = DisturbanceFieldDetector()
fingerprint_mapper = RoomFingerprintMapper(FINGERPRINT_DIR)
tomography_engine = OpportunisticRSSITomography()
confidence_engine = ConfidenceCeilingEngine()
session_learner = SessionLearner(LOG_DIR)
state_lock = Lock()
latest_telemetry: Optional[Dict[str, Any]] = None


def build_telemetry() -> Dict[str, Any]:
    """Build one GhostEye WiFi-only non-CSI v0.2 scan payload."""

    global latest_telemetry

    observation = adapter.get_observation()
    observation_payload = observation.to_dict()
    capabilities = capability_profiler.profile(observation)
    baseline = load_json(EMPTY_ROOM_BASELINE_FILE, None)
    disturbance = disturbance_detector.detect(observation, baseline)
    zone_estimate = fingerprint_mapper.estimate_zone(observation_payload)
    zone_map = tomography_engine.project(
        observation_payload,
        baseline,
        zone_estimate.get("zone_scores", {}),
        disturbance.motion_score,
    )
    zone = _selected_zone(zone_estimate.get("zone"), zone_map)
    raw_confidence = _raw_confidence(
        motion_score=disturbance.motion_score,
        quality_score=capabilities.quality_score,
        zone_score=zone_map.get(zone, 0.0),
    )
    confidence = confidence_engine.evaluate(
        raw_confidence=raw_confidence,
        mode=MODE_WIFI_ONLY_NON_CSI,
        signal_quality=capabilities.quality_score,
        map_ambiguity=_map_ambiguity(zone_map),
    )

    response = GhostEyeScanResponse(
        timestamp=utc_now_iso(),
        mode=MODE_WIFI_ONLY_NON_CSI,
        source=SOURCE_LOCAL_WIFI_SIMULATED,
        presence=disturbance.presence,
        motion_score=disturbance.motion_score,
        zone=zone,
        confidence=float(confidence["final_confidence"]),
        confidence_ceiling=float(confidence["confidence_ceiling"]),
        signal_quality=SignalQuality(
            visible_access_points=capabilities.visible_access_points,
            gateway_latency_ms=capabilities.gateway_latency_ms,
            jitter_ms=capabilities.jitter_ms,
            packet_loss=capabilities.packet_loss,
            rssi_stability=capabilities.rssi_stability,
        ),
        map=zone_map,
    ).to_dict()

    if env_flag_enabled(AI_ANALYSIS_ENV):
        response["ai_analysis"] = build_ai_analysis(response)

    with state_lock:
        latest_telemetry = response
    session_learner.append_scan(response)
    return response


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "name": "Ghost-Eye",
        "status": "online",
        "mode": MODE_WIFI_ONLY_NON_CSI,
        "notice": NOTICE,
        "endpoints": [
            "/health",
            "/scan",
            "/sources",
            "/source/select",
            "/map/current",
            "/calibrate/empty-room",
            "/calibrate/zone",
            "/session/start",
            "/session/stop",
            "/session/latest",
            "/ai/status",
            "/ai/analyze-scan",
            "/ws/telemetry",
        ],
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "timestamp": utc_now_iso(),
        "mode": MODE_WIFI_ONLY_NON_CSI,
        "source": _selected_source(),
        "session": session_learner.latest_session(),
    }


@app.get("/scan")
def scan() -> Dict[str, Any]:
    return build_telemetry()


@app.get("/sources")
def sources() -> Dict[str, Any]:
    return {"sources": adapter.sources()}


@app.post("/source/select")
def select_source(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    source_id = payload.get("source_id") or payload.get("id")
    if not source_id:
        raise HTTPException(status_code=400, detail="source_id is required")
    try:
        selected = adapter.select_source(str(source_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"selected": selected, "sources": adapter.sources()}


@app.get("/map/current")
def current_map() -> Dict[str, Any]:
    with state_lock:
        telemetry = latest_telemetry
    if telemetry is None:
        telemetry = build_telemetry()
    return {
        "timestamp": telemetry["timestamp"],
        "zone": telemetry["zone"],
        "map": telemetry["map"],
        "signal_quality": telemetry["signal_quality"],
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }


@app.post("/calibrate/empty-room")
def calibrate_empty_room() -> Dict[str, Any]:
    observation = adapter.get_observation()
    payload = observation.to_dict()
    baseline = {
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "mode": MODE_WIFI_ONLY_NON_CSI,
        "source": SOURCE_LOCAL_WIFI_SIMULATED,
        "sample_count": 1,
        "rssi_by_bssid": observation.rssi_by_bssid,
        "observation": payload,
        "signal_quality": {
            "visible_access_points": observation.bssid_count,
            "gateway_latency_ms": observation.gateway_latency_ms,
            "jitter_ms": observation.jitter_ms,
            "packet_loss": observation.packet_loss,
            "rssi_stability": observation.scan_stability,
        },
    }
    save_json(EMPTY_ROOM_BASELINE_FILE, baseline)
    return {
        "status": "calibrated",
        "baseline": {
            "available": True,
            "sample_count": baseline["sample_count"],
            "visible_access_points": observation.bssid_count,
            "updated_at": baseline["updated_at"],
        },
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }


@app.post("/calibrate/zone")
def calibrate_zone(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    zone = str(payload.get("zone") or payload.get("zone_id") or "").strip()
    if not zone:
        raise HTTPException(status_code=400, detail="zone is required")
    observation = adapter.get_observation()
    fingerprint = fingerprint_mapper.create_fingerprint(zone, observation.to_dict())
    return {
        "status": "calibrated",
        "zone": zone,
        "fingerprint": {
            "sample_count": fingerprint["sample_count"],
            "visible_access_points": len(fingerprint["rssi_by_bssid"]),
            "updated_at": fingerprint["updated_at"],
        },
        "fingerprint_count": fingerprint_mapper.fingerprint_count(),
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }


@app.post("/session/start")
def start_session(payload: Optional[Dict[str, Any]] = Body(default=None)) -> Dict[str, Any]:
    payload = payload or {}
    session = session_learner.start_session(
        session_id=payload.get("session_id"),
        metadata=payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
    )
    return {"session": session, "notice": NOTICE}


@app.post("/session/stop")
def stop_session() -> Dict[str, Any]:
    return {"session": session_learner.stop_session(), "notice": NOTICE}


@app.get("/session/latest")
def session_latest() -> Dict[str, Any]:
    with state_lock:
        telemetry = latest_telemetry
    return {
        "session": session_learner.latest_session(),
        "telemetry": telemetry,
        "notice": NOTICE,
    }


@app.get("/ai/status")
def ai_status() -> Dict[str, Any]:
    return ai_status_payload()


@app.post("/ai/analyze-scan")
def analyze_scan(payload: Optional[Dict[str, Any]] = Body(default=None)) -> Dict[str, Any]:
    scan_payload = payload or build_telemetry()
    return {
        "status": ai_status_payload(),
        "ai_analysis": build_ai_analysis(scan_payload),
    }


@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(build_telemetry())
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        return


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    temporary_path.replace(path)


def _selected_source() -> Optional[Dict[str, Any]]:
    return next((source for source in adapter.sources() if source.get("selected")), None)


def _selected_zone(zone_hint: Any, zone_map: Dict[str, float]) -> str:
    if isinstance(zone_hint, str) and zone_hint in zone_map and zone_hint != "unknown":
        return zone_hint
    return max(zone_map, key=zone_map.get) if zone_map else "unknown"


def _raw_confidence(motion_score: float, quality_score: float, zone_score: float) -> float:
    return round(min(0.95, 0.25 + (quality_score * 0.32) + (motion_score * 0.28) + (zone_score * 0.18)), 2)


def _map_ambiguity(zone_map: Dict[str, float]) -> float:
    if not zone_map:
        return 1.0
    scores = sorted(zone_map.values(), reverse=True)
    if len(scores) < 2 or scores[0] <= 0:
        return 0.0
    return round(max(0.0, min(1.0, 1.0 - (scores[0] - scores[1]))), 3)


def env_flag_enabled(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def ai_status_payload() -> Dict[str, Any]:
    return {
        "enabled": env_flag_enabled(AI_ANALYSIS_ENV),
        "provider": "fallback",
        "mode": AI_MODE,
        "excluded_layers": AI_EXCLUDED_LAYERS,
    }


def build_ai_analysis(scan_payload: Dict[str, Any]) -> Dict[str, Any]:
    presence = str(scan_payload.get("presence") or "unknown")
    if presence == "presence_detected":
        summary = "Presence-like WiFi signal disturbance detected in the scan."
    elif presence == "possible_presence":
        summary = "Scan shows possible presence-like WiFi signal disturbance."
    elif presence == "clear":
        summary = "Scan is currently consistent with a clear environment."
    else:
        summary = "Scan analysis completed with an unknown presence state."

    return {
        "available": True,
        "provider": "fallback",
        "mode": AI_MODE,
        "summary": summary,
        "confidence": scan_payload.get("confidence", 0.0),
        "signals": {
            "presence": presence,
            "motion_score": scan_payload.get("motion_score", 0.0),
            "zone": scan_payload.get("zone", "unknown"),
        },
        "excluded_layers": AI_EXCLUDED_LAYERS,
        "limitations": [
            LIMITATIONS,
            "No autonomy, targeting, weapons, mission command, robotics control, or C4ISR layers are used.",
        ],
    }

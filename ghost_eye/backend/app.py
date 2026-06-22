from __future__ import annotations

import asyncio
import json
import os
import re
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
    ROOM_SETUP_LIMITATIONS,
    SOURCE_LOCAL_WIFI_LIVE,
    SOURCE_LOCAL_WIFI_SIMULATED,
    SOURCE_SELECTED_WIFI_ENVIRONMENT,
    GhostEyeScanResponse,
    RoomMap,
    RoomSetupResponse,
    SelectedNetwork,
    SignalQuality,
    WIFI_NETWORK_LIMITATIONS,
    WifiNetworkEnvironment,
    WifiNetworksResponse,
    WifiSelectionResponse,
    utc_now_iso,
)
from ghost_eye.ai import FallbackAIAnalyzer  # noqa: E402
from ghost_eye.csi_adapters import WiFiOnlyAdapter  # noqa: E402
from ghost_eye.inference import (  # noqa: E402
    AdaptiveBaselineEngine,
    ConfidenceCeilingEngine,
    DeviceMotionCompensator,
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
ROOM_SETUP_FILE = FINGERPRINT_DIR / "room_setup.json"
AI_ANALYSIS_ENV = "GHOSTEYE_AI_ANALYSIS"
DEVICE_MOTION_STATE_ENV = "GHOSTEYE_DEVICE_MOTION_STATE"
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


DEMO_WIFI_NETWORKS = (
    WifiNetworkEnvironment(
        ssid="TP-Link_Demo",
        bssid_masked="aa:bb:**:**:**:11",
        vendor_hint="tp_link",
        signal_dbm=-48,
        channel=6,
        capability="wifi_only_environment",
        can_use_as_csi_sensor=False,
        notes="Usable as controlled access point/environment. Raw CSI not verified.",
    ),
    WifiNetworkEnvironment(
        ssid="NetGear_Demo",
        bssid_masked="cc:dd:**:**:**:22",
        vendor_hint="netgear",
        signal_dbm=-55,
        channel=11,
        capability="wifi_only_environment",
        can_use_as_csi_sensor=False,
        notes="Usable as controlled access point/environment. Raw CSI not verified.",
    ),
    WifiNetworkEnvironment(
        ssid="GhostEye_Lab",
        bssid_masked="02:00:**:**:**:33",
        vendor_hint="unknown",
        signal_dbm=-62,
        channel=1,
        capability="wifi_only_environment",
        can_use_as_csi_sensor=False,
        notes="Demo environment only. Ordinary phone WiFi APIs do not expose raw CSI.",
    ),
)

DEFAULT_ROOM_SETUP = {
    "room_id": "demo_room",
    "room_name": "Demo Room",
    "width_m": 5.2,
    "length_m": 4.1,
    "shape": "rectangle",
    "zones": ["zone_a", "zone_b", "zone_c"],
    "router_location": {"x_m": 0.5, "y_m": 2.0},
    "map_mode": "manual_dimensions_plus_wifi_fingerprint",
    "updated_at": None,
}


adapter = WiFiOnlyAdapter(seed=42, bssid_count=5)
ai_analyzer = FallbackAIAnalyzer()
capability_profiler = SignalCapabilityProfiler()
disturbance_detector = DisturbanceFieldDetector()
adaptive_baseline_engine = AdaptiveBaselineEngine(
    session_id="adaptive_empty_room",
    baseline_dir=BASELINE_DIR,
    adaptation_rate=0.2,
)
fingerprint_mapper = RoomFingerprintMapper(FINGERPRINT_DIR)
tomography_engine = OpportunisticRSSITomography()
confidence_engine = ConfidenceCeilingEngine()
device_motion_compensator = DeviceMotionCompensator()
session_learner = SessionLearner(LOG_DIR)
state_lock = Lock()
latest_telemetry: Optional[Dict[str, Any]] = None
selected_wifi_environment: Dict[str, Any] = DEMO_WIFI_NETWORKS[0].to_dict()


def build_telemetry() -> Dict[str, Any]:
    """Build one GhostEye WiFi-only non-CSI scan payload."""

    global latest_telemetry

    observation = adapter.get_observation()
    observation_payload = observation.to_dict()
    live_status = adapter.get_live_status()
    selected_network = _selected_wifi_network(observation_payload, live_status)
    actual_source = adapter.get_selected_source_id()
    capabilities = capability_profiler.profile(observation)
    baseline = load_json(EMPTY_ROOM_BASELINE_FILE, None)
    device_motion = device_motion_compensator.compensate(_device_motion_state())
    disturbance = disturbance_detector.detect(
        observation,
        baseline,
        adaptive_baseline=adaptive_baseline_engine.adaptive_baseline,
    )
    baseline_update = _update_adaptive_baseline(
        observation_payload,
        disturbance.motion_score,
        observation,
        baseline,
        device_motion,
    )
    zone_estimate = fingerprint_mapper.estimate_zone(observation_payload)
    zone_map = tomography_engine.project(
        observation_payload,
        baseline,
        zone_estimate.get("zone_scores", {}),
        disturbance.motion_score,
    )
    room_map = _room_map(zone_map)
    zone = _selected_zone(zone_estimate.get("zone"), zone_map)
    raw_confidence = _raw_confidence(
        motion_score=disturbance.motion_score,
        quality_score=capabilities.quality_score,
        zone_score=zone_map.get(zone, 0.0),
    )
    adjusted_confidence = raw_confidence * device_motion.confidence_multiplier
    confidence = confidence_engine.evaluate(
        raw_confidence=adjusted_confidence,
        mode=MODE_WIFI_ONLY_NON_CSI,
        signal_quality=capabilities.quality_score,
        device_motion_status=device_motion.device_stability,
        map_ambiguity=_map_ambiguity(zone_map),
    )
    presence = _bounded_presence(disturbance.presence, capabilities.quality_score, observation.packet_loss)

    response = GhostEyeScanResponse(
        timestamp=utc_now_iso(),
        mode=MODE_WIFI_ONLY_NON_CSI,
        source=actual_source,
        selected_network=SelectedNetwork(
            ssid=str(selected_network["ssid"]),
            vendor_hint=str(selected_network["vendor_hint"]),
            bssid_masked=selected_network.get("bssid_masked"),
        ),
        presence=presence,
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
            rssi_dbm=_optional_signal_float(live_status.get("rssi_dbm"), observation.mean_rssi),
            noise_dbm=_optional_signal_float(live_status.get("noise_dbm"), None),
        ),
        room_map=RoomMap(
            room_name=str(room_map["room_name"]),
            shape=str(room_map["shape"]),
            width_m=float(room_map["width_m"]),
            length_m=float(room_map["length_m"]),
            zones=room_map["zones"],
        ),
        map=zone_map,
    ).to_dict()
    response["device_motion"] = {
        "state": device_motion.device_stability,
        "confidence_multiplier": device_motion.confidence_multiplier,
        "scan_valid": device_motion.scan_valid,
        "reason": device_motion.reason,
    }
    response["baseline"] = baseline_update
    response["selected_adapter"] = adapter.get_selected_source()
    response["live_observation"] = live_status
    response["fingerprints"] = {"count": fingerprint_mapper.fingerprint_count()}
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
            "/wifi/networks",
            "/wifi/select",
            "/room/setup",
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
    live_status = adapter.get_live_status()
    return {
        "sources": adapter.get_sources(),
        "live_available": adapter.live_available(),
        "current_ssid": live_status.get("ssid") if live_status.get("ssid") != "unknown" else None,
        "vendor_hint": live_status.get("vendor_hint") or "unknown",
        "selected_source": adapter.get_selected_source(),
        "confidence_ceiling": confidence_engine.DEFAULT_MODE_CEILINGS[MODE_WIFI_ONLY_NON_CSI],
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }


@app.get("/wifi/networks")
def wifi_networks() -> Dict[str, Any]:
    return WifiNetworksResponse(networks=DEMO_WIFI_NETWORKS).to_dict()


@app.post("/wifi/select")
def select_wifi(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    global selected_wifi_environment

    ssid = str(payload.get("ssid") or "").strip()
    adapter_mode = str(payload.get("adapter_mode") or MODE_WIFI_ONLY_NON_CSI).strip()
    if not ssid:
        raise HTTPException(status_code=400, detail="ssid is required")
    if adapter_mode != MODE_WIFI_ONLY_NON_CSI:
        raise HTTPException(status_code=400, detail="adapter_mode must be wifi_only_non_csi")

    network = _network_by_ssid(ssid)
    if network is None:
        raise HTTPException(status_code=404, detail=f"Unknown WiFi environment: {ssid}")

    selected_wifi_environment = network.to_dict()
    adapter.select_wifi_environment(ssid)
    return WifiSelectionResponse(
        selected_ssid=ssid,
        adapter_mode=adapter_mode,
        confidence_ceiling=confidence_engine.DEFAULT_MODE_CEILINGS[MODE_WIFI_ONLY_NON_CSI],
    ).to_dict()


@app.post("/room/setup")
def setup_room(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    room_name = str(payload.get("room_name") or "").strip() or "Demo Room"
    width_m = _positive_float(payload.get("width_m"), "width_m")
    length_m = _positive_float(payload.get("length_m"), "length_m")
    shape = str(payload.get("shape") or "rectangle").strip().lower() or "rectangle"
    zones = _normalize_zones(payload.get("zones"))
    router_location = payload.get("router_location") if isinstance(payload.get("router_location"), dict) else {}
    router_x = _finite_float(router_location.get("x_m"), "router_location.x_m")
    router_y = _finite_float(router_location.get("y_m"), "router_location.y_m")
    room_id = _slug(room_name)

    room_setup = {
        "room_id": room_id,
        "room_name": room_name,
        "width_m": width_m,
        "length_m": length_m,
        "shape": shape,
        "zones": zones,
        "router_location": {"x_m": router_x, "y_m": router_y},
        "map_mode": "manual_dimensions_plus_wifi_fingerprint",
        "updated_at": utc_now_iso(),
        "limitations": ROOM_SETUP_LIMITATIONS,
        "notice": NOTICE,
    }
    save_json(ROOM_SETUP_FILE, room_setup)

    return RoomSetupResponse(
        room_id=room_id,
        status="configured",
        map_mode="manual_dimensions_plus_wifi_fingerprint",
    ).to_dict()


@app.post("/source/select")
def select_source(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    source_id = payload.get("source_id") or payload.get("id")
    if not source_id:
        raise HTTPException(status_code=400, detail="source_id is required")
    try:
        selected = adapter.select_source(str(source_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"selected": selected, "sources": adapter.get_sources()}


@app.get("/map/current")
def current_map() -> Dict[str, Any]:
    with state_lock:
        telemetry = latest_telemetry
    if telemetry is None:
        telemetry = build_telemetry()
    return {
        "timestamp": telemetry["timestamp"],
        "zone": telemetry["zone"],
        "room_map": telemetry["room_map"],
        "map": telemetry["map"],
        "signal_quality": telemetry["signal_quality"],
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }


@app.post("/calibrate/empty-room")
def calibrate_empty_room() -> Dict[str, Any]:
    samples = _collect_calibration_samples()
    observation = samples[-1]["observation"]
    payload = observation.to_dict()
    baseline_id = f"empty_room_{_slug(utc_now_iso())}"
    averaged_rssi = _average_rssi_by_bssid(samples)
    baseline = {
        "baseline_id": baseline_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "mode": MODE_WIFI_ONLY_NON_CSI,
        "source": adapter.get_selected_source_id(),
        "selected_network": _selected_wifi_network(payload, samples[-1]["live_status"]),
        "sample_count": len(samples),
        "rssi_by_bssid": averaged_rssi,
        "observation": _average_observation_payload(samples, averaged_rssi),
        "signal_quality": _average_signal_quality(samples),
        "status": "calibrated",
    }
    save_json(BASELINE_DIR / f"{baseline_id}.json", baseline)
    save_json(EMPTY_ROOM_BASELINE_FILE, baseline)
    adaptive_status = adaptive_baseline_engine.replace_baseline(baseline["observation"])
    return {
        "status": "calibrated",
        "baseline_id": baseline_id,
        "sample_count": baseline["sample_count"],
        "signal_quality": baseline["signal_quality"],
        "selected_ssid": baseline["selected_network"].get("ssid"),
        "baseline": {"available": True, "updated_at": baseline["updated_at"], "adaptive_status": adaptive_status},
        "limitations": LIMITATIONS,
        "notice": NOTICE,
    }


@app.post("/calibrate/zone")
def calibrate_zone(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    zone = str(payload.get("zone") or payload.get("zone_id") or "").strip()
    label = str(payload.get("label") or zone).strip()
    if not zone:
        raise HTTPException(status_code=400, detail="zone is required")
    samples = _collect_calibration_samples()
    observation = samples[-1]["observation"]
    averaged_rssi = _average_rssi_by_bssid(samples)
    fingerprint_id = f"{_slug(zone)}_{_slug(label)}_{_slug(utc_now_iso())}"
    fingerprint = {
        "fingerprint_id": fingerprint_id,
        "zone": zone,
        "label": label,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "mode": MODE_WIFI_ONLY_NON_CSI,
        "source": adapter.get_selected_source_id(),
        "sample_count": len(samples),
        "rssi_by_bssid": averaged_rssi,
        "gateway_latency_ms": _mean(sample["observation"].gateway_latency_ms for sample in samples),
        "jitter_ms": _mean(sample["observation"].jitter_ms for sample in samples),
        "signal_quality": _average_signal_quality(samples),
        "selected_network": _selected_wifi_network(observation.to_dict(), samples[-1]["live_status"]),
    }
    save_json(FINGERPRINT_DIR / f"{fingerprint_id}.json", fingerprint)
    return {
        "status": "calibrated",
        "fingerprint_id": fingerprint_id,
        "zone": zone,
        "label": label,
        "sample_count": fingerprint["sample_count"],
        "fingerprint": fingerprint,
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
        "session": session_learner.latest_session() or empty_session_state(),
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
    return next((source for source in adapter.get_sources() if source.get("selected")), None)


def _selected_wifi_network(
    observation_payload: Optional[Dict[str, Any]] = None,
    live_status: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    live_status = live_status or {}
    if adapter.get_selected_source_id() == SOURCE_LOCAL_WIFI_LIVE and live_status.get("ssid"):
        return {
            "ssid": live_status.get("ssid") or "unknown",
            "vendor_hint": live_status.get("vendor_hint") or "unknown",
            "bssid_masked": live_status.get("bssid_masked"),
        }

    selected = dict(selected_wifi_environment)
    if observation_payload and observation_payload.get("ssid"):
        selected.setdefault("ssid", observation_payload["ssid"])
    return selected


def _network_by_ssid(ssid: str) -> Optional[WifiNetworkEnvironment]:
    return next((network for network in DEMO_WIFI_NETWORKS if network.ssid == ssid), None)


def _room_setup() -> Dict[str, Any]:
    setup = load_json(ROOM_SETUP_FILE, None)
    if not isinstance(setup, dict):
        return dict(DEFAULT_ROOM_SETUP)
    merged = dict(DEFAULT_ROOM_SETUP)
    merged.update(setup)
    merged["zones"] = _normalize_zones(merged.get("zones"))
    return merged


def _room_map(zone_map: Dict[str, float]) -> Dict[str, Any]:
    setup = _room_setup()
    zones = setup["zones"]
    scored_zones = {zone: round(float(zone_map.get(zone, 0.0)), 2) for zone in zones}
    return {
        "room_name": setup["room_name"],
        "shape": setup["shape"],
        "width_m": float(setup["width_m"]),
        "length_m": float(setup["length_m"]),
        "zones": scored_zones,
    }


def _selected_zone(zone_hint: Any, zone_map: Dict[str, float]) -> str:
    if isinstance(zone_hint, str) and zone_hint in zone_map and zone_hint != "unknown":
        return zone_hint
    return max(zone_map, key=zone_map.get) if zone_map else "unknown"


def _raw_confidence(motion_score: float, quality_score: float, zone_score: float) -> float:
    return round(min(0.95, 0.25 + (quality_score * 0.32) + (motion_score * 0.28) + (zone_score * 0.18)), 2)


def _bounded_presence(presence: str, quality_score: float, packet_loss: float) -> str:
    if quality_score < 0.22 or packet_loss >= 0.75:
        return "unstable_scan"
    if presence == "presence_detected":
        return "possible_presence"
    if presence in {"possible_motion", "possible_presence", "clear", "unstable_scan"}:
        return presence
    return "possible_motion" if presence not in {"clear", "unknown"} else "clear"


def _map_ambiguity(zone_map: Dict[str, float]) -> float:
    if not zone_map:
        return 1.0
    scores = sorted(zone_map.values(), reverse=True)
    if len(scores) < 2 or scores[0] <= 0:
        return 0.0
    return round(max(0.0, min(1.0, 1.0 - (scores[0] - scores[1]))), 3)


def _device_motion_state() -> str:
    return os.getenv(DEVICE_MOTION_STATE_ENV, "stable")


def _normalize_zones(value: Any) -> list[str]:
    if isinstance(value, str):
        candidates = value.split(",")
    elif isinstance(value, list):
        candidates = value
    else:
        candidates = DEFAULT_ROOM_SETUP["zones"]
    zones: list[str] = []
    for candidate in candidates:
        zone = str(candidate).strip()
        if zone and zone not in zones:
            zones.append(zone)
    if not zones:
        zones = list(DEFAULT_ROOM_SETUP["zones"])
    return zones


def _positive_float(value: Any, field_name: str) -> float:
    number = _finite_float(value, field_name)
    if number <= 0:
        raise HTTPException(status_code=400, detail=f"{field_name} must be greater than 0")
    return number


def _finite_float(value: Any, field_name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a number") from exc
    if not number == number or number in (float("inf"), float("-inf")):
        raise HTTPException(status_code=400, detail=f"{field_name} must be finite")
    return round(number, 3)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_.-]+", "_", value.strip().lower()).strip("._-")
    return slug or "room"


def _update_adaptive_baseline(
    observation_payload: Dict[str, Any],
    motion_score: float,
    observation: Any,
    baseline: Any,
    device_motion: Any,
) -> Dict[str, Any]:
    if not isinstance(baseline, dict):
        return {"baseline_status": "unavailable", "reason": "empty_room_baseline_not_calibrated"}
    if getattr(device_motion, "device_stability", "unknown") != "stable":
        return {
            "baseline_status": "held",
            "reason": "device_motion_not_stable",
            "last_updated": adaptive_baseline_engine.last_updated,
        }
    return adaptive_baseline_engine.update(
        observation_payload,
        motion_score=motion_score,
        scan_stability=float(getattr(observation, "scan_stability", 0.0)),
        packet_loss=float(getattr(observation, "packet_loss", 1.0)),
    )


def _collect_calibration_samples(sample_count: int = 5, interval_seconds: float = 0.08) -> list[Dict[str, Any]]:
    samples: list[Dict[str, Any]] = []
    for index in range(sample_count):
        observation = adapter.get_observation()
        samples.append({"observation": observation, "live_status": adapter.get_live_status()})
        if index < sample_count - 1:
            time.sleep(interval_seconds)
    return samples


def _average_rssi_by_bssid(samples: list[Dict[str, Any]]) -> Dict[str, float]:
    grouped: Dict[str, list[float]] = {}
    for sample in samples:
        observation = sample["observation"]
        for bssid, rssi in observation.rssi_by_bssid.items():
            grouped.setdefault(str(bssid).lower(), []).append(float(rssi))
    return {bssid: round(_mean(values), 2) for bssid, values in grouped.items()}


def _average_observation_payload(samples: list[Dict[str, Any]], averaged_rssi: Dict[str, float]) -> Dict[str, Any]:
    observation = samples[-1]["observation"]
    payload = observation.to_dict()
    payload["rssi_by_bssid"] = averaged_rssi
    payload["sample_count"] = len(samples)
    payload["mean_rssi"] = round(_mean(sample["observation"].mean_rssi for sample in samples), 2)
    payload["gateway_latency_ms"] = round(_mean(sample["observation"].gateway_latency_ms for sample in samples), 2)
    payload["jitter_ms"] = round(_mean(sample["observation"].jitter_ms for sample in samples), 2)
    payload["packet_loss"] = round(_mean(sample["observation"].packet_loss for sample in samples), 4)
    payload["scan_stability"] = round(_mean(sample["observation"].scan_stability for sample in samples), 3)
    return payload


def _average_signal_quality(samples: list[Dict[str, Any]]) -> Dict[str, Any]:
    observations = [sample["observation"] for sample in samples]
    live_status = samples[-1]["live_status"]
    return {
        "visible_access_points": int(round(_mean(observation.bssid_count for observation in observations))),
        "gateway_latency_ms": round(_mean(observation.gateway_latency_ms for observation in observations), 2),
        "jitter_ms": round(_mean(observation.jitter_ms for observation in observations), 2),
        "packet_loss": round(_mean(observation.packet_loss for observation in observations), 4),
        "rssi_stability": round(_mean(observation.scan_stability for observation in observations), 3),
        "rssi_dbm": _optional_signal_float(live_status.get("rssi_dbm"), observations[-1].mean_rssi),
        "noise_dbm": _optional_signal_float(live_status.get("noise_dbm"), None),
    }


def _mean(values: Any) -> float:
    numbers = [float(value) for value in values]
    return sum(numbers) / len(numbers) if numbers else 0.0


def _optional_signal_float(value: Any, fallback: Any) -> Optional[float]:
    candidate = value if value is not None else fallback
    if candidate is None:
        return None
    try:
        return round(float(candidate), 3)
    except (TypeError, ValueError):
        return None


def empty_session_state() -> Dict[str, Any]:
    return {
        "session_id": None,
        "active": False,
        "started_at": None,
        "stopped_at": None,
        "scan_count": 0,
        "latest_scan": None,
    }


def env_flag_enabled(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def ai_status_payload() -> Dict[str, Any]:
    return {
        "enabled": True,
        "provider": "fallback",
        "mode": AI_MODE,
        "excluded_layers": AI_EXCLUDED_LAYERS,
        "confidence_policy": "never_increase_scan_confidence",
        "limitations": LIMITATIONS,
    }


def build_ai_analysis(scan_payload: Dict[str, Any]) -> Dict[str, Any]:
    analysis = ai_analyzer.analyze(scan_payload).to_dict()
    return {
        "summary": analysis["summary"],
        "confidence_explanation": analysis["confidence_explanation"],
        "false_positive_risks": analysis["false_positive_risks"],
        "recommended_next_action": analysis["recommended_next_action"],
        "confidence": min(float(scan_payload.get("confidence", 0.0)), float(analysis.get("confidence", 0.0))),
        "provider": analysis["provider"],
        "model": analysis["model"],
        "limitations": analysis["limitations"],
    }

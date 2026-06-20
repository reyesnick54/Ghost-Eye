from pathlib import Path
import sys

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random
import time
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

@app.get("/")
def root():
    return {
        "name": "Ghost-Eye",
        "status": "online",
        "mode": "simulated-demo"
    }

@app.get("/scan")
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

    if motion_score > 0.7:
        presence = "presence_detected"
    elif motion_score > 0.4:
        presence = "possible_presence"
    else:
        presence = "clear"

    return {
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

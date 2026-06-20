from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI(title="Ghost-Eye Demo API")

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
def scan():
    motion_score = round(random.uniform(0.05, 0.95), 2)

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
        "confidence": round(random.uniform(0.55, 0.96), 2),
        "notice": "Demo simulation only. Authorized test environments only."
    }

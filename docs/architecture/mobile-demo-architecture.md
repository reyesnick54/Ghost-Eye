# Abraxas GhostEye Mobile Demo Architecture

## Purpose

The mobile demo shows how Abraxas GhostEye could present WiFi sensing telemetry in a mobile app interface.

This first version is simulated. It exists to validate:

- User interface direction
- API schema
- Telemetry display
- Demo flow
- Safety and governance language

## Components

### 1. Mobile Demo UI

Path:

`prototypes/mobile-demo/index.html`

Responsibilities:

- Display presence state
- Display motion score
- Display zone estimate
- Display confidence
- Display timestamp
- Display authorized-use notice

### 2. Backend API

Path:

`ghost_eye/backend/app.py`

Responsibilities:

- Serve `/` health endpoint
- Serve `/scan` telemetry endpoint
- Generate simulated sensing output

### 3. Future CSI Adapter Layer

Path:

`ghost_eye/csi_adapters/`

Future responsibilities:

- Interface with ESP32 CSI capture
- Normalize CSI streams
- Pass clean frames to inference layer
- Maintain separation from third-party vendored repos

### 4. Future Inference Layer

Path:

`ghost_eye/inference/`

Future responsibilities:

- Presence detection
- Motion classification
- Zone estimation
- Confidence scoring
- Model evaluation

## Demo Flow

1. Start FastAPI backend.
2. Open mobile demo in browser.
3. UI calls `GET /scan`.
4. Backend returns simulated sensing telemetry.
5. UI updates the GhostEye dashboard.

## Safety Boundary

All demos must be authorized, consent-based, and performed in controlled test environments.

The system must not be presented as a covert surveillance tool or unauthorized monitoring system.

# Abraxas GhostEye Mobile

Expo + React Native + TypeScript scaffold for the Abraxas GhostEye WiFi-only non-CSI backend.

## Safety boundary

Abraxas GhostEye is intended only for authorized, consent-based, controlled-environment demonstrations and research. It must not be used for covert surveillance, unauthorized monitoring, or unlawful tracking.

WiFi-only non-CSI mode provides coarse probabilistic estimates only. This mobile app does not claim true through-wall imaging, does not claim validated operational intelligence, and does not access raw WiFi CSI from phone WiFi APIs.

## Backend expected by the app

Run the backend from the repository root:

```sh
cd ghost_eye/backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend test commands:

```sh
curl http://localhost:8000/health
curl http://localhost:8000/
curl http://localhost:8000/scan
curl http://localhost:8000/sources
curl http://localhost:8000/map/current
curl http://localhost:8000/session/latest
curl -X POST http://localhost:8000/calibrate/empty-room
curl -X POST http://localhost:8000/calibrate/zone \
  -H "Content-Type: application/json" \
  -d '{"zone":"zone_a"}'
curl -X POST http://localhost:8000/session/start
curl -X POST http://localhost:8000/session/stop
```

## Install

```sh
cd apps/ghosteye-mobile
npm install
```

## Run

Mobile app run commands:

```sh
cd apps/ghosteye-mobile
npm run start
```

For a physical phone on the same LAN as the backend:

```sh
cd apps/ghosteye-mobile
npm run start -- --lan
```

Then enter the backend LAN URL in the app, for example:

```text
http://192.168.1.100:8000
```

Use `http://localhost:8000` for a local simulator or browser when that address resolves to the backend from the running app environment.

## Screens

- `OnboardingSafetyScreen` requires authorized-use acknowledgement before continuing.
- `BackendConnectionScreen` edits the backend URL and tests `GET /health`.
- `SourceSelectionScreen` fetches `GET /sources` and shows `local_wifi_rssi_latency_simulated` and `csi:false` when returned.
- `CalibrationScreen` calls `POST /calibrate/empty-room` and `POST /calibrate/zone`.
- `LiveScanDashboard` polls `GET /scan` and displays probabilistic WiFi-only non-CSI telemetry every 2 seconds by default.
- `SessionScreen` calls `POST /session/start`, `POST /session/stop`, and `GET /session/latest`.
- `SettingsScreen` edits backend URL, scan refresh interval, safety notice, and diagnostics placeholder.

## Implementation notes

- Navigation is a lightweight tab-like state machine in `App.tsx`; React Navigation is not required for v0.1.
- Backend URL and refresh interval are local React state only.
- All backend calls use the Fetch API through `src/api/ghosteyeClient.ts`.
- No mobile WiFi CSI APIs are used or requested.

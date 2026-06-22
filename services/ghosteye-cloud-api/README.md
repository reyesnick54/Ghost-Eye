# GhostEye Cloud API

Hosted FastAPI backend for GhostEye v0.4.

The service is cloud-first and mobile-app friendly. It does not observe local
NetGear, TP-Link, or other WiFi RF conditions directly. Mobile clients collect
allowed WiFi/network observations and send them over HTTPS/WSS. The API stores
sessions, manages calibration, produces coarse WiFi-only non-CSI telemetry, and
calls the hosted S3M AI Service when configured.

## Run locally

```bash
cd services/ghosteye-cloud-api
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run with Docker

```bash
cd services/ghosteye-cloud-api
docker build -t ghosteye-cloud-api .
docker run --rm -p 8000:8000 \
  -e GHOSTEYE_ENV=development \
  -e GHOSTEYE_API_SECRET=dev-secret-change-me \
  -e S3M_AI_SERVICE_URL=http://host.docker.internal:8100 \
  -e CORS_ALLOWED_ORIGINS='*' \
  ghosteye-cloud-api
```

## Environment variables

| Variable | Purpose |
| --- | --- |
| `GHOSTEYE_ENV` | `development`, `test`, or hosted environment name. Non-development requires bearer tokens. |
| `GHOSTEYE_API_SECRET` | HMAC secret for the JWT-compatible placeholder token. Replace in hosted deployments. |
| `SUPABASE_URL` | Future Supabase project URL for team/device/session persistence. |
| `SUPABASE_JWT_SECRET` | Future Supabase JWT verification secret. |
| `S3M_AI_SERVICE_URL` | Base URL for the hosted S3M AI Service. Falls back if unset/unavailable. |
| `CORS_ALLOWED_ORIGINS` | Comma-separated mobile/web origins. Use explicit origins in production. |
| `GHOSTEYE_STORAGE_DIR` | JSON-compatible local storage directory. Defaults to `/tmp/ghosteye-cloud-api`. |

## Key endpoints

- `GET /health`
- `GET /system/readiness`
- `POST /auth/device/register`
- `POST /telemetry/observation`
- `POST /telemetry/batch`
- `POST /calibration/empty-room/start`
- `POST /calibration/empty-room/sample`
- `POST /calibration/empty-room/complete`
- `POST /calibration/zone/start`
- `POST /calibration/zone/sample`
- `POST /calibration/zone/complete`
- `POST /scan/analyze`
- `GET /sessions/latest`
- `GET /sessions/{session_id}`
- `POST /ai/analyze-scan`
- `POST /ai/analyze-session`
- `WS /ws/session/{session_id}`

All telemetry responses are confidence-capped, probabilistic, WiFi-only non-CSI
results. They do not claim exact through-wall object detection.

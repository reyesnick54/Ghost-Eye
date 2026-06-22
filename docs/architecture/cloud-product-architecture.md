# GhostEye Cloud Product Architecture v0.4

## Product topology

```text
GhostEye Mobile App
  -> HTTPS/WSS
GhostEye Cloud API
  -> internal HTTPS service call
Hosted S3M-Core AI Service
  -> Database / Storage / Team Registry
```

GhostEye v0.4 is cloud-first. The backend is no longer designed as a local-only
process attached to a laptop WiFi interface. The hosted Cloud API is the mobile
client boundary for authentication, device registration, telemetry ingestion,
calibration, session state, and AI analysis orchestration.

## Critical sensing boundary

A hosted cloud backend cannot directly observe RF conditions around a user's
local NetGear, TP-Link, or other WiFi access point. Cloud compute has no local
radio context for the mobile user's room. Therefore:

- The mobile app collects allowed platform WiFi/network observations.
- The mobile app sends those observations to the Cloud API over HTTPS/WSS.
- The Cloud API normalizes, stores, analyzes, and returns telemetry.
- All inference is WiFi-only non-CSI and confidence-capped.
- The product does not claim exact through-wall object detection.

## Services

### GhostEye Cloud API

Path: `services/ghosteye-cloud-api`

Responsibilities:

- Mobile JWT-compatible auth placeholder and device registration.
- Mobile WiFi observation ingestion.
- Rolling session state.
- Server-side empty-room calibration.
- Server-side zone fingerprint calibration.
- Coarse probabilistic `TelemetryScan` generation.
- WebSocket session telemetry.
- Internal HTTP calls to `S3M_AI_SERVICE_URL`.
- Deterministic fallback AI analysis if S3M service is unavailable.

### Hosted S3M AI Service

Path: `services/s3m-ai-service`

Responsibilities:

- Health and AI status endpoints.
- Scan/session analysis endpoints.
- Calibration recommendation endpoint.
- Optional import-safe S3M-Core bridge.
- Deterministic fallback analyzer when S3M-Core is unavailable.
- Stable `AIAnalysis` response contract with `mode: analysis_only_no_autonomy`.

## Data flow

1. Mobile app registers a device and receives a bearer token.
2. Mobile app starts or reuses a `session_id`.
3. Mobile app sends `MobileWifiObservation` payloads from allowed platform APIs.
4. Cloud API derives signal quality, motion score, coarse zone score, and capped
   confidence.
5. Cloud API stores latest scan and session summary in a JSON-compatible
   abstraction.
6. Cloud API calls the S3M AI Service for advisory analysis.
7. Mobile app displays `TelemetryScan` and `AIAnalysis` with limitations.

## Storage architecture

The current implementation uses thread-safe JSON-compatible storage adapters:

- `SessionStore` for device registrations, sessions, and scans.
- `CalibrationStore` for calibration sessions, baselines, and zone fingerprints.

These adapters define the persistence seam for future Supabase/Postgres, object
storage, or team registry integration.

## Security and deployment posture

- HTTPS is required in hosted environments.
- WSS is required for session WebSockets.
- Production should use explicit `CORS_ALLOWED_ORIGINS`.
- `GHOSTEYE_API_SECRET` must be replaced with a managed secret.
- `SUPABASE_URL` and `SUPABASE_JWT_SECRET` are reserved for managed identity and
  team registry integration.
- Service logs should capture request IDs, health status, and non-sensitive
  telemetry metadata only.

# GhostEye Mobile to Cloud API Contract v0.4

Base URL: hosted `GhostEye Cloud API`

Transport:

- HTTPS for REST endpoints.
- WSS for session telemetry.
- Bearer token authentication after device registration.

## Authenticate and register device

`POST /auth/device/register`

```json
{
  "team_id": "team_demo",
  "platform": "ios",
  "app_version": "0.4.0",
  "device_model": "iPhone",
  "capability_mode": "wifi_only_non_csi",
  "metadata": {}
}
```

Response includes `device_id`, `access_token`, and `expires_in_seconds`.
Hosted deployments should replace the placeholder token flow with Supabase/OIDC
verification while preserving the bearer contract.

## Create or reuse a session

The mobile app generates a stable `session_id` for a controlled scan session.
The Cloud API creates rolling session state when it receives the first
observation for that ID.

## Send one WiFi observation

`POST /telemetry/observation`

```json
{
  "device_id": "dev_123",
  "team_id": "team_demo",
  "session_id": "sess_living_room_001",
  "timestamp": "2026-06-22T16:18:00Z",
  "platform": "android",
  "capability_mode": "wifi_only_non_csi",
  "ssid": "HomeWiFi",
  "bssid_masked": "aa:bb:**:**:**:11",
  "vendor_hint": "tp_link",
  "rssi_dbm": -58,
  "gateway_latency_ms": 24.3,
  "jitter_ms": 5.4,
  "packet_loss": 0,
  "visible_access_points": 4,
  "device_motion_state": "stable",
  "room_id": "living_room",
  "zone_label": null,
  "calibration_phase": null,
  "metadata": {
    "room_name": "Living Room"
  }
}
```

Response: `TelemetryScan`.

Important: the phone collects only allowed platform WiFi/network observations.
The cloud backend cannot directly sample local RF conditions.

## Send a batch

`POST /telemetry/batch`

```json
{
  "observations": [
    { "...": "MobileWifiObservation" }
  ],
  "metadata": {}
}
```

Response: latest `TelemetryScan` after rolling session state is updated.

## Empty-room calibration

1. `POST /calibration/empty-room/start`
2. `POST /calibration/empty-room/sample`
3. `POST /calibration/empty-room/complete`

Start request:

```json
{
  "device_id": "dev_123",
  "team_id": "team_demo",
  "session_id": "sess_living_room_001",
  "room_id": "living_room",
  "metadata": {}
}
```

Sample request:

```json
{
  "calibration_id": "cal_empty_room_abc",
  "observation": { "...": "MobileWifiObservation" }
}
```

Complete request:

```json
{
  "calibration_id": "cal_empty_room_abc",
  "metadata": {}
}
```

The cloud stores an averaged baseline for the team/room.

## Zone calibration

1. `POST /calibration/zone/start`
2. `POST /calibration/zone/sample`
3. `POST /calibration/zone/complete`

Start request adds `zone_label`, for example `zone_a`.

Zone calibration stores coarse fingerprints. These fingerprints improve
probabilistic zone scoring but do not provide exact location tracking.

## Request scan analysis

`POST /ai/analyze-scan`

```json
{
  "scan": { "...": "TelemetryScan" },
  "metadata": {}
}
```

Response: `AIAnalysis`.

## Request session analysis

`POST /ai/analyze-session`

```json
{
  "session_id": "sess_living_room_001",
  "team_id": "team_demo",
  "metadata": {}
}
```

Response: `AIAnalysis`.

## Receive WebSocket telemetry

`WS /ws/session/{session_id}`

Development:

```text
wss://api.example.com/ws/session/sess_living_room_001
```

Production bearer placeholder:

```text
wss://api.example.com/ws/session/sess_living_room_001?token=<access_token>
```

Messages:

```json
{
  "type": "session_update",
  "session": {
    "session_id": "sess_living_room_001",
    "scan_count": 3,
    "latest_scan": { "...": "TelemetryScan" }
  }
}
```

## Display AI analysis

Mobile UI should show:

- `summary`
- `confidence_explanation`
- `false_positive_risks`
- `calibration_recommendations`
- `operator_notes`
- `recommended_next_action`
- `provider`
- `mode`

UI copy must preserve the limitation that WiFi-only non-CSI telemetry is coarse,
probabilistic, and not exact through-wall object detection.

# GhostEye Mobile WiFi Observation Layer v0.5

## Scope

GhostEye Mobile v0.5 collects permitted WiFi-only, non-CSI observations from Android
and iOS devices and posts them to the hosted GhostEye Cloud API.

The layer collects:

- Current connected WiFi metadata when platform APIs and permissions allow it.
- Nearby WiFi scan summaries on Android when permitted.
- App-level network probe latency, jitter, and packet-loss estimates.
- Device motion stability from accelerometer/gyroscope data.
- Calibration workflow state for empty-room and zone samples.

It does not claim raw CSI access, true RF imaging, deterministic through-wall
presence detection, or router firmware-level RF access.

## Data contract

Each upload serializes `MobileWifiObservation`:

- `device_id`
- `team_id`
- `session_id`
- `timestamp`
- `platform`
- `capability_mode`
- `selected_network`
- `wifi_current`
- `wifi_scan`
- `network_probe`
- `device_motion`
- `calibration`
- `metadata`

Single observations are posted to:

```text
POST /telemetry/observation
```

Batches are posted to:

```text
POST /telemetry/batch
```

The app can also read cloud scan/AI responses from existing GhostEye endpoints:

```text
GET /scan
POST /ai/analyze-scan
```

## Capability modes

| Mode | Platform | Description | Confidence ceiling guidance |
| --- | --- | --- | --- |
| `android_wifi_observation` | Android | Current WiFi, permitted scan results, probes, and motion are available. | Up to 0.68 when owned-router vendor hint is known. |
| `android_wifi_scan_limited` | Android | WiFi metadata or scans are permission-limited or throttled. | Up to 0.60. |
| `ios_network_limited` | iOS | Current SSID/BSSID may be available, nearby scanning is not exposed. | Up to 0.45. |
| `web_unavailable` / `native_unavailable` | Preview/runtime fallback | Native WiFi APIs are unavailable. | Up to 0.35. |

All UI output repeats the WiFi-only non-CSI limitation and caps confidence to the
selected capability mode.

## Router selection

The app prioritizes owned NetGear and TP-Link routers for tests. Vendor hints are
inferred from SSID strings and a small OUI allowlist when a masked BSSID preserves
the first three octets. The hint is advisory; users must explicitly confirm that
the selected router is owned and authorized before live upload or calibration.

## Live stream

The live screen streams observations every 1-5 seconds depending on capability:

- Android: normally 1.5 seconds or the configured interval when higher.
- iOS: reduced capability mode uses 5 seconds.

Each stream tick:

1. Reads current WiFi metadata.
2. Attempts a nearby WiFi scan when supported.
3. Detects WiFi RTT support without requiring RTT for operation.
4. Runs cloud and optional router app-level probes.
5. Classifies device motion as `stable`, `moving`, or `unknown`.
6. Posts a `MobileWifiObservation` to GhostEye Cloud.
7. Refreshes backend `TelemetryScan` and `AIAnalysis` panels when available.

## Calibration workflow

Supported phases:

- `empty_room_start`
- `empty_room_sample`
- `empty_room_complete`
- `zone_start`
- `zone_sample`
- `zone_complete`

Each phase uploads a normal `MobileWifiObservation` with a `calibration` object so
the cloud can associate WiFi/network/motion data with the calibration state.

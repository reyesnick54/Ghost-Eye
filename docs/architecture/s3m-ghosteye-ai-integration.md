# S3M GhostEye AI integration

GhostEye is a WiFi-only sensing application for authorized, controlled
environments. This document defines how S3M may be used as an AI analysis
runtime around GhostEye telemetry without expanding GhostEye into autonomy,
mission command, targeting, robotics, or weapons-related behavior.

## 1. GhostEye architecture

GhostEye keeps owned application code under `ghost_eye/` and treats vendored
WiFi-sensing repositories under `third_party/` as read-only references. The
runtime architecture is intentionally small:

- `ghost_eye.csi_adapters` normalizes supported signal sources into
  GhostEye-owned WiFi observation batches.
- `ghost_eye.wifi` defines scan, gateway-probe, and RSSI normalization helpers
  for non-CSI observations.
- `ghost_eye.inference` converts RSSI-only observations into coarse signal
  capability, disturbance, motion, presence, zone, tomography, confidence, and
  session-learning outputs.
- `ghost_eye.api` defines API-facing telemetry and calibration schemas,
  including the optional `AIAnalysisResult` placeholder.
- `ghost_eye.backend.app` exposes the demo API and WebSocket telemetry stream.

The backend notice remains authoritative: GhostEye is a demo and analysis tool
for authorized test environments only.

## 2. WiFi-only non-CSI algorithm stack

GhostEye's primary sensing mode is WiFi-only non-CSI. It consumes ordinary WiFi
metadata such as SSID, BSSID, channel, frequency, RSSI, gateway latency, jitter,
packet loss, and scan stability. It does not require raw channel-state
information tensors.

The algorithm stack is:

1. Signal collection from simulator, router, ESP32 metadata, or local WiFi scan
   adapters.
2. RSSI normalization into bounded features and baseline-relative deltas.
3. Signal capability profiling from AP count, RSSI stability, and packet health.
4. Device-motion compensation so moving scanner devices lower confidence rather
   than producing stronger claims.
5. Adaptive empty-room baselines that update only on stable, low-motion scans.
6. Disturbance-field estimation from RSSI residuals.
7. Motion and presence classification into coarse states such as `clear`,
   `possible_presence`, and `presence_detected`.
8. Room fingerprint matching and opportunistic RSSI tomography for coarse zones.
9. Confidence calibration and ceilings that cap RSSI-only outputs below stronger
   CSI-backed claims.
10. Session learning and telemetry serialization for API consumers.

See `docs/architecture/wifi-only-non-csi-algorithms.md` for the owned GhostEye
module map.

## 3. Why S3M is analysis-only

S3M is permitted only as an AI-assisted analysis layer. It may summarize
GhostEye telemetry, explain confidence limits, compare structured model outputs,
and reconcile contradictory analysis results. It must not control sensors,
select targets, dispatch actors, command vehicles, execute missions, or
initiate real-world actions.

This boundary keeps S3M downstream of GhostEye's sensing pipeline:

- Inputs are bounded telemetry snapshots, session summaries, and calibration
  metadata.
- Outputs are structured analysis artifacts for human review.
- GhostEye remains the source of deterministic signal-processing results.
- Human operators remain responsible for authorization, collection context, and
  any real-world interpretation.

## 4. Allowed S3M components

Only the following S3M components are in scope for GhostEye integration:

- `llm_core` engine registry: selects approved local or remote analysis engines
  by name.
- `llm_core` unified runtime: provides a single invocation path for AI analysis
  requests.
- Engine runtime: executes the selected engine with bounded prompts, timeouts,
  and telemetry-only inputs.
- Structured output: constrains AI responses to schemas such as summaries,
  confidence notes, limitations, anomalies, and recommended follow-up checks.
- Reconciliation: compares multiple analysis outputs or deterministic pipeline
  fields and reports agreement, disagreement, and uncertainty.

These components may enrich API-facing `ai_analysis` data, internal operator
notes, or offline session reports. They may not mutate GhostEye calibration
state unless a separate human-authorized workflow explicitly accepts the result.

## 5. Excluded S3M layers

The following S3M layers are explicitly excluded from GhostEye:

- C4ISR
- Autonomy
- Robotics
- Targeting
- Weapons
- Mission command

References to these layers must not appear in executable GhostEye workflows,
configuration presets, prompts, API operations, UI controls, or automated
decision logic. If an upstream S3M package includes these capabilities, the
GhostEye integration must import only the allowed analysis-only components and
must fail closed when a prohibited component is requested.

## 6. AI analysis workflow

The AI analysis workflow is optional and downstream of signal processing:

1. GhostEye collects a WiFi-only observation batch.
2. The deterministic inference stack produces telemetry with presence, motion,
   zone, confidence, limitations, signal quality, and session context.
3. A safety filter removes secrets, raw credentials, and unnecessary device
   identifiers before any AI call.
4. The S3M `llm_core` engine registry resolves an approved analysis engine.
5. The unified runtime invokes the engine with a bounded analysis prompt and a
   structured output schema.
6. Structured output validation rejects malformed, policy-violating, or
   action-oriented responses.
7. Reconciliation compares AI findings with deterministic GhostEye fields and,
   when configured, with a second engine's output.
8. GhostEye exposes the result as analysis metadata: summary, confidence notes,
   limitations, anomalies, and recommended human checks.

AI output never replaces deterministic telemetry fields. It is a secondary
interpretation layer for operators and tests.

## 7. Fallback mode

GhostEye must continue to operate when S3M is unavailable, disabled, misconfigured,
or rejected by safety validation. Fallback mode means:

- The WiFi-only non-CSI pipeline still produces `/scan`, `/map/current`, session,
  calibration, and WebSocket telemetry.
- `ai_analysis.available` is `false` or omitted.
- The response includes the standard limitation notice for authorized controlled
  environments.
- Confidence ceilings remain determined by GhostEye's deterministic inference
  pipeline.
- Errors from the AI runtime are logged for diagnostics but do not block sensing
  telemetry.

Fallback mode is the default safe behavior and should be exercised in tests.

## 8. Environment variables

The current GhostEye code has no required S3M environment variables. The
following names define the expected integration contract for any S3M adapter
that is added later:

| Variable | Default | Purpose |
| --- | --- | --- |
| `GHOSTEYE_AI_ANALYSIS_ENABLED` | `false` | Enables optional AI analysis when set to `true`. |
| `GHOSTEYE_AI_FALLBACK_ONLY` | `false` | Forces deterministic telemetry with AI disabled for demos and safety tests. |
| `S3M_LLM_ENGINE` | unset | Engine name resolved through the `llm_core` engine registry. |
| `S3M_LLM_MODEL` | unset | Model or deployment identifier passed to the selected engine. |
| `S3M_STRUCTURED_OUTPUT_SCHEMA` | `ghosteye_ai_analysis_v1` | Structured output schema identifier. |
| `S3M_RECONCILIATION_ENABLED` | `true` | Enables agreement and disagreement checks across analysis outputs. |
| `S3M_RUNTIME_TIMEOUT_SECONDS` | `10` | Maximum runtime for one AI analysis call. |
| `S3M_MAX_INPUT_BYTES` | `8192` | Upper bound for telemetry context sent to S3M. |
| `S3M_ALLOWED_COMPONENTS` | allowed list below | Must not include excluded S3M layers. |

`S3M_ALLOWED_COMPONENTS` may contain only:

```text
llm_core.engine_registry,llm_core.unified_runtime,engine_runtime,structured_output,reconciliation
```

Any missing, empty, or invalid AI configuration must resolve to fallback mode.

## 9. Testing commands

Recommended checks for this integration boundary:

```bash
# Owned GhostEye unit tests.
python -m unittest discover ghost_eye/tests

# Backend dependency smoke check, if FastAPI dependencies are installed.
python -m pip install -r ghost_eye/backend/requirements.txt
python -m uvicorn ghost_eye.backend.app:app --host 127.0.0.1 --port 8000

# Manual API smoke checks while the server is running.
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/scan
curl -s -X POST http://127.0.0.1:8000/calibrate/empty-room
curl -s http://127.0.0.1:8000/map/current

# Fallback-mode check for future S3M wiring.
GHOSTEYE_AI_ANALYSIS_ENABLED=false python -m unittest discover ghost_eye/tests
```

When S3M integration tests are added, include cases for allowed component
selection, excluded layer rejection, structured output validation failure, AI
runtime timeout, reconciliation disagreement, and fallback telemetry continuity.

## 10. Safety and authorization boundary

GhostEye and S3M integration are restricted to authorized, controlled
environments. The system must:

- Display and preserve the authorized-use limitation notice in API responses.
- Avoid collecting credentials, payload contents, or raw private traffic.
- Treat WiFi-only non-CSI results as coarse probabilistic estimates, not identity
  or biometric determinations.
- Never use AI analysis to control physical systems or initiate real-world
  action.
- Reject S3M components related to C4ISR, autonomy, robotics, targeting,
  weapons, or mission command.
- Fail closed to deterministic fallback mode when configuration, validation, or
  authorization checks fail.
- Keep human review in the loop for interpretation, calibration acceptance, and
  any operational decision outside the software.

This boundary is part of the architecture, not an optional deployment setting.

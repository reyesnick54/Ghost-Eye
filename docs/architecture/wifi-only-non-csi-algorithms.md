# WiFi-only non-CSI algorithms

GhostEye keeps its WiFi-only sensing code under `ghost_eye/` and treats
vendored upstream repositories as read-only inputs. The modules described here
operate on standard WiFi observations such as SSID, BSSID, channel, RSSI, and
gateway probe quality. They do not require raw CSI tensors.

## Signal collection

- `ghost_eye.wifi.wifi_scan` defines timestamped WiFi scan records.
- `ghost_eye.wifi.gateway_probe` summarizes gateway reachability, packet loss,
  latency, and optional RSSI.
- `ghost_eye.wifi.signal_normalizer` converts RSSI values into bounded features
  and baseline-relative deltas.

## Adapters

Adapters in `ghost_eye.csi_adapters` normalize supported sources into
GhostEye-owned scan batches:

- `SimulatorAdapter` provides deterministic local demo data.
- `Esp32CsiAdapter` accepts ESP32 telemetry but keeps only WiFi RSSI metadata.
- `RouterAdapter` normalizes router scan or station telemetry.
- `WifiOnlyAdapter` is the shared base for RSSI-only observation sources.

## Inference pipeline

The inference package is intentionally decomposed into small stages:

1. Profile signal capability from AP count and RSSI stability.
2. Maintain adaptive baselines for expected RSSI values.
3. Compensate common-mode shifts caused by sensing-device motion.
4. Estimate disturbance and motion from baseline residuals.
5. Combine disturbance and motion into presence states.
6. Match fingerprints or RSS tomography cells to coarse zones.
7. Calibrate confidence from evidence strength and signal coverage.

The initial implementation uses deterministic heuristics. These modules define
stable integration seams for later trained models or vendor-wrapped algorithms
without modifying upstream repositories.

## Session data

Runtime session artifacts should be written below `ghost_eye/sessions/`:

- `logs/` for raw authorized session logs.
- `baselines/` for learned RSSI baselines.
- `fingerprints/` for labeled room or zone fingerprints.

These directories are GhostEye-owned and safe to extend without changing
vendored upstream code.

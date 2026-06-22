import type { AIAnalysis } from "./ai";
import type { CalibrationObservationState } from "./calibration";

export const SAFETY_ACKNOWLEDGEMENT =
  "Abraxas GhostEye is intended only for authorized, consent-based, controlled-environment demonstrations and research. It must not be used for covert surveillance, unauthorized monitoring, or unlawful tracking.";

export const WIFI_ONLY_LIMITATION =
  "WiFi-only non-CSI mode provides coarse probabilistic estimates only. It does not provide validated through-wall imaging.";

export type ConnectionState = "idle" | "checking" | "connected" | "disconnected";

export type ZoneId = "zone_a" | "zone_b" | "zone_c";

export type GhostEyePlatform = "android" | "ios" | "web" | "unknown";

export type RouterVendorHint = "netgear" | "tp_link" | "unknown";

export type CapabilityMode =
  | "android_wifi_observation"
  | "android_wifi_scan_limited"
  | "ios_network_limited"
  | "web_unavailable"
  | "native_unavailable";

export type DeviceMotionState = "stable" | "moving" | "unknown";

export interface SelectedNetworkObservation {
  ssid?: string | null;
  bssid_masked?: string | null;
  vendor_hint: RouterVendorHint;
  owned_authorized_confirmed: boolean;
  confidence_ceiling: number;
}

export interface WifiCurrentObservation {
  ssid?: string | null;
  bssid_masked?: string | null;
  rssi_dbm?: number | null;
  link_speed_mbps?: number | null;
  frequency_mhz?: number | null;
  wifi_standard?: string | null;
  normalized_signal_strength?: number | null;
  capability_mode: CapabilityMode | string;
  warnings?: string[];
}

export interface NearbyAccessPointObservation {
  ssid?: string | null;
  bssid_masked?: string | null;
  rssi_dbm?: number | null;
  level?: number | null;
  frequency_mhz?: number | null;
  capabilities?: string | null;
  vendor_hint?: RouterVendorHint;
}

export interface WifiScanObservation {
  visible_access_points: number;
  target_router_seen: boolean;
  access_points: NearbyAccessPointObservation[];
  capability_mode: CapabilityMode | string;
  scan_throttled?: boolean;
  warnings?: string[];
}

export interface WifiRttCapabilities {
  rtt_supported: boolean;
  rtt_available: boolean;
  rtt_permission_state: "granted" | "denied" | "unknown" | "not_required";
  capability_mode: CapabilityMode | string;
  warnings?: string[];
}

export interface NetworkProbeObservation {
  cloud_latency_ms?: number | null;
  router_probe_latency_ms?: number | null;
  jitter_ms?: number | null;
  packet_loss_estimate: number;
  probe_count: number;
  failed_probe_count: number;
  warnings?: string[];
}

export interface DeviceMotionObservation {
  state: DeviceMotionState;
  confidence: number;
  accelerometer_magnitude_std?: number | null;
  gyroscope_magnitude_std?: number | null;
  sample_count?: number;
  capability_mode: CapabilityMode | string;
  warnings?: string[];
}

export interface MobileObservationMetadata {
  app_version: string;
  observation_schema_version: "0.5";
  rtt_supported?: boolean;
  rtt_available?: boolean;
  router_probe_host?: string | null;
  upload_reason?: string;
  limitations: string[];
  [key: string]: string | number | boolean | null | string[] | undefined;
}

export interface MobileWifiObservation {
  device_id: string;
  team_id?: string | null;
  session_id: string;
  timestamp: string;
  platform: GhostEyePlatform;
  capability_mode: CapabilityMode | string;
  selected_network?: SelectedNetworkObservation | null;
  wifi_current: WifiCurrentObservation;
  wifi_scan: WifiScanObservation;
  network_probe: NetworkProbeObservation;
  device_motion: DeviceMotionObservation;
  calibration?: CalibrationObservationState | null;
  metadata: MobileObservationMetadata;
}

export interface MobileObservationUploadResponse {
  status?: string;
  accepted?: boolean;
  observation_id?: string;
  telemetry_scan?: GhostEyeScanTelemetry;
  scan?: GhostEyeScanTelemetry;
  ai_analysis?: AIAnalysis;
  notice?: string;
  detail?: string;
}

export interface MobileObservationBatchResponse {
  status?: string;
  accepted?: number;
  rejected?: number;
  telemetry_scan?: GhostEyeScanTelemetry;
  scan?: GhostEyeScanTelemetry;
  ai_analysis?: AIAnalysis;
  notice?: string;
  detail?: string;
}

export interface SignalQuality {
  visible_access_points?: number;
  gateway_latency_ms?: number;
  jitter_ms?: number;
  packet_loss?: number;
  rssi_stability?: number;
  [key: string]: number | string | boolean | undefined;
}

export interface GhostEyeSource {
  id: string;
  name?: string;
  mode?: string;
  type?: string;
  simulated?: boolean;
  selected?: boolean;
  capabilities?: string[];
  csi?: boolean;
  can_use_as_csi_sensor?: boolean;
  selected_wifi_ssid?: string;
  limitations?: string;
  status?: string;
}

export interface WifiNetworkEnvironment {
  ssid: string;
  bssid_masked: string;
  vendor_hint: "tp_link" | "netgear" | "unknown" | string;
  signal_dbm: number;
  channel: number;
  capability: string;
  can_use_as_csi_sensor: boolean;
  notes: string;
}

export interface WifiNetworksResponse {
  networks: WifiNetworkEnvironment[];
  limitations?: string;
}

export interface WifiSelectionResponse {
  selected_ssid?: string;
  adapter_mode?: string;
  status?: string;
  confidence_ceiling?: number;
  notice?: string;
}

export interface RouterLocation {
  x_m: number;
  y_m: number;
}

export interface RoomSetupRequest {
  room_name: string;
  width_m: number;
  length_m: number;
  shape: string;
  zones: string[];
  router_location: RouterLocation;
}

export interface RoomSetupResponse {
  room_id?: string;
  status?: string;
  map_mode?: string;
  limitations?: string;
}

export interface RoomMap {
  room_name?: string;
  shape?: string;
  width_m?: number;
  length_m?: number;
  zones?: Record<string, number>;
}

export interface HealthResponse {
  status?: string;
  timestamp?: string;
  mode?: string;
  source?: GhostEyeSource | null;
  session?: SessionState | null;
}

export interface SourcesResponse {
  sources: GhostEyeSource[];
}

export interface GhostEyeScanTelemetry {
  timestamp?: string;
  mode?: string;
  source?: string;
  selected_network?: {
    ssid?: string;
    vendor_hint?: string;
  };
  selected_adapter?: GhostEyeSource | null;
  presence?: string;
  motion_score?: number;
  zone?: string;
  confidence?: number;
  confidence_ceiling?: number;
  signal_quality?: SignalQuality;
  room_map?: RoomMap;
  map?: Record<string, number>;
  limitations?: string;
  notice?: string;
  device_motion?: {
    state?: string;
    confidence_multiplier?: number;
    scan_valid?: boolean;
    reason?: string;
  };
  baseline?: Record<string, unknown>;
}

export interface CurrentMapResponse {
  timestamp?: string;
  zone?: string;
  room_map?: RoomMap;
  map?: Record<string, number>;
  signal_quality?: SignalQuality;
  limitations?: string;
  notice?: string;
}

export interface CalibrationResult {
  status?: string;
  zone?: string;
  baseline?: Record<string, unknown>;
  fingerprint?: Record<string, unknown>;
  fingerprint_count?: number;
  limitations?: string;
  notice?: string;
  detail?: string;
}

export interface SessionState {
  session_id?: string | null;
  active?: boolean;
  started_at?: string | null;
  stopped_at?: string | null;
  scan_count?: number;
  latest_scan?: GhostEyeScanTelemetry | null;
}

export interface SessionResponse {
  session?: SessionState;
  telemetry?: GhostEyeScanTelemetry | null;
  notice?: string;
}

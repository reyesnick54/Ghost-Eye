export const SAFETY_ACKNOWLEDGEMENT =
  "Abraxas GhostEye is intended only for authorized, consent-based, controlled-environment demonstrations and research. It must not be used for covert surveillance, unauthorized monitoring, or unlawful tracking.";

export const WIFI_ONLY_LIMITATION =
  "WiFi-only non-CSI mode provides coarse probabilistic estimates only. It does not provide validated through-wall imaging.";

export type ConnectionState = "idle" | "checking" | "connected" | "disconnected";

export type ZoneId = "zone_a" | "zone_b" | "zone_c";

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

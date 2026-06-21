export const SAFETY_ACKNOWLEDGEMENT =
  "Abraxas GhostEye is intended only for authorized, consent-based, controlled-environment demonstrations and research. It must not be used for covert surveillance, unauthorized monitoring, or unlawful tracking.";

export const WIFI_ONLY_LIMITATION =
  "WiFi-only non-CSI mode provides coarse probabilistic estimates only.";

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
  status?: string;
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
  presence?: string;
  motion_score?: number;
  zone?: string;
  confidence?: number;
  confidence_ceiling?: number;
  signal_quality?: SignalQuality;
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

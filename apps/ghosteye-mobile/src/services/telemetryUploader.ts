import { Platform } from "react-native";

import { getDeviceMotion } from "../native/MotionCollector";
import { measureNetworkProbe } from "../native/NetworkProbe";
import {
  confidenceCeilingForCapability,
  getCurrentWifi,
  getWifiRttCapabilities,
  inferRouterVendorHint,
  scanNearbyWifi,
} from "../native/WifiCollector";
import { CalibrationObservationState } from "../types/calibration";
import {
  MobileObservationBatchResponse,
  MobileObservationUploadResponse,
  MobileWifiObservation,
  SelectedNetworkObservation,
  WIFI_ONLY_LIMITATION,
} from "../types/telemetry";
import { postObservation, postObservationBatch } from "./ghosteyeCloudClient";
import { getOrCreateSession } from "./sessionManager";

interface CollectObservationOptions {
  cloudUrl: string;
  teamId?: string | null;
  selectedNetwork?: SelectedNetworkObservation | null;
  routerProbeHost?: string | null;
  calibration?: CalibrationObservationState | null;
  uploadReason?: string;
}

interface StreamUploaderOptions extends CollectObservationOptions {
  intervalMs?: number;
  onObservation?: (observation: MobileWifiObservation) => void;
  onUpload?: (response: MobileObservationUploadResponse) => void;
  onError?: (error: Error) => void;
}

export interface TelemetryUploadResult {
  observation: MobileWifiObservation;
  response: MobileObservationUploadResponse;
}

export async function collectMobileWifiObservation({
  cloudUrl,
  teamId,
  selectedNetwork,
  routerProbeHost,
  calibration,
  uploadReason = "manual_sample",
}: CollectObservationOptions): Promise<MobileWifiObservation> {
  const session = getOrCreateSession(teamId);
  const wifiCurrent = await getCurrentWifi();
  const vendorHint = inferRouterVendorHint(wifiCurrent.ssid, wifiCurrent.bssid_masked);
  const selected =
    selectedNetwork ??
    (wifiCurrent.ssid
      ? {
          ssid: wifiCurrent.ssid,
          bssid_masked: wifiCurrent.bssid_masked,
          vendor_hint: vendorHint,
          owned_authorized_confirmed: false,
          confidence_ceiling: confidenceCeilingForCapability(wifiCurrent.capability_mode, vendorHint),
        }
      : null);
  const [wifiScan, rttCapabilities, networkProbe, deviceMotion] = await Promise.all([
    scanNearbyWifi(selected),
    getWifiRttCapabilities(),
    measureNetworkProbe({ cloudUrl, routerProbeHost }),
    getDeviceMotion(),
  ]);
  const capabilityMode = chooseCapabilityMode(wifiCurrent.capability_mode, wifiScan.capability_mode);

  return {
    device_id: session.deviceId,
    team_id: session.teamId ?? null,
    session_id: session.sessionId,
    timestamp: new Date().toISOString(),
    platform: Platform.OS === "android" || Platform.OS === "ios" || Platform.OS === "web" ? Platform.OS : "unknown",
    capability_mode: capabilityMode,
    selected_network: selected,
    wifi_current: wifiCurrent,
    wifi_scan: wifiScan,
    network_probe: networkProbe,
    device_motion: deviceMotion,
    calibration: calibration ?? null,
    metadata: {
      app_version: "0.5.0",
      observation_schema_version: "0.5",
      rtt_supported: rttCapabilities.rtt_supported,
      rtt_available: rttCapabilities.rtt_available,
      router_probe_host: routerProbeHost ?? null,
      upload_reason: uploadReason,
      limitations: [
        WIFI_ONLY_LIMITATION,
        "Phone WiFi APIs do not expose raw CSI here.",
        "Mobile observations are probabilistic and confidence-capped.",
      ],
    },
  };
}

export async function uploadMobileWifiObservation(
  options: CollectObservationOptions,
): Promise<TelemetryUploadResult> {
  const observation = await collectMobileWifiObservation(options);
  const response = await postObservation(options.cloudUrl, observation);
  return { observation, response };
}

export function uploadMobileWifiObservationBatch(
  cloudUrl: string,
  observations: MobileWifiObservation[],
): Promise<MobileObservationBatchResponse> {
  return postObservationBatch(cloudUrl, observations);
}

export function startTelemetryUploadStream(options: StreamUploaderOptions): () => void {
  let stopped = false;
  let inFlight = false;
  const intervalMs = normalizeIntervalMs(options.intervalMs);

  async function tick() {
    if (stopped || inFlight) {
      return;
    }
    inFlight = true;
    try {
      const result = await uploadMobileWifiObservation({ ...options, uploadReason: "live_stream" });
      options.onObservation?.(result.observation);
      options.onUpload?.(result.response);
    } catch (error) {
      options.onError?.(error instanceof Error ? error : new Error("Telemetry upload failed."));
    } finally {
      inFlight = false;
    }
  }

  void tick();
  const timer = setInterval(() => {
    void tick();
  }, intervalMs);

  return () => {
    stopped = true;
    clearInterval(timer);
  };
}

export function recommendedObservationIntervalMs(): number {
  if (Platform.OS === "android") {
    return 1500;
  }
  if (Platform.OS === "ios") {
    return 5000;
  }
  return 5000;
}

function normalizeIntervalMs(value?: number): number {
  const fallback = recommendedObservationIntervalMs();
  if (typeof value !== "number" || Number.isNaN(value)) {
    return fallback;
  }
  return Math.max(1000, Math.min(5000, Math.round(value)));
}

function chooseCapabilityMode(currentMode: string, scanMode: string): string {
  if (currentMode === "android_wifi_observation" || scanMode === "android_wifi_observation") {
    return "android_wifi_observation";
  }
  if (currentMode === "ios_network_limited" || scanMode === "ios_network_limited") {
    return "ios_network_limited";
  }
  return currentMode || scanMode || "native_unavailable";
}

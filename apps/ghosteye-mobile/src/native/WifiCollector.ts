import { NativeModules, Platform } from "react-native";

import {
  CapabilityMode,
  NearbyAccessPointObservation,
  RouterVendorHint,
  SelectedNetworkObservation,
  WifiCurrentObservation,
  WifiRttCapabilities,
  WifiScanObservation,
} from "../types/telemetry";

type NativeWifiModule = {
  getCurrentWifi?: () => Promise<Record<string, unknown>>;
  scanNearbyWifi?: (targetSsid?: string | null, targetBssidMasked?: string | null) => Promise<Record<string, unknown>>;
  getRttCapabilities?: () => Promise<Record<string, unknown>>;
};

const nativeWifiModule = NativeModules.GhostEyeWifiModule as NativeWifiModule | undefined;

const NETGEAR_OUIS = new Set(["00:09:5b", "00:14:6c", "00:1b:2f", "20:4e:7f", "a0:40:a0", "c4:04:15", "e0:46:9a"]);
const TP_LINK_OUIS = new Set(["14:cc:20", "30:de:4b", "50:c7:bf", "a4:2b:b0", "b0:4e:26", "c0:06:c3", "d8:0d:17", "e8:48:b8"]);

export async function getCurrentWifi(): Promise<WifiCurrentObservation> {
  if (!nativeWifiModule?.getCurrentWifi) {
    return unavailableCurrentWifi("GhostEye native WiFi module is unavailable.");
  }

  try {
    const payload = await nativeWifiModule.getCurrentWifi();
    const bssidMasked = maskBssid(readString(payload.bssid_masked) ?? readString(payload.bssid));
    return {
      ssid: readString(payload.ssid),
      bssid_masked: bssidMasked,
      rssi_dbm: readNumber(payload.rssi_dbm),
      link_speed_mbps: readNumber(payload.link_speed_mbps),
      frequency_mhz: readNumber(payload.frequency_mhz),
      wifi_standard: readString(payload.wifi_standard),
      normalized_signal_strength: readNumber(payload.normalized_signal_strength),
      capability_mode: readString(payload.capability_mode) ?? defaultCapabilityMode(),
      warnings: readStringArray(payload.warnings),
    };
  } catch (error) {
    return unavailableCurrentWifi(error instanceof Error ? error.message : "Unable to read current WiFi.");
  }
}

export async function scanNearbyWifi(
  selectedNetwork?: SelectedNetworkObservation | null,
): Promise<WifiScanObservation> {
  if (!nativeWifiModule?.scanNearbyWifi) {
    return unavailableScan("Nearby WiFi scan is not available from this app runtime.");
  }

  try {
    const payload = await nativeWifiModule.scanNearbyWifi(
      selectedNetwork?.ssid ?? null,
      selectedNetwork?.bssid_masked ?? null,
    );
    const rawAccessPoints = Array.isArray(payload.access_points)
      ? payload.access_points
      : Array.isArray(payload.nearby_access_points)
        ? payload.nearby_access_points
        : [];
    const accessPoints = rawAccessPoints.map(normalizeAccessPoint);
    const targetSeen =
      readBoolean(payload.target_router_seen) ??
      accessPoints.some((accessPoint) => matchesSelectedRouter(accessPoint, selectedNetwork));

    return {
      visible_access_points: readNumber(payload.visible_access_points) ?? accessPoints.length,
      target_router_seen: targetSeen,
      access_points: accessPoints,
      capability_mode: readString(payload.capability_mode) ?? defaultCapabilityMode(),
      scan_throttled: readBoolean(payload.scan_throttled) ?? false,
      warnings: readStringArray(payload.warnings),
    };
  } catch (error) {
    return unavailableScan(error instanceof Error ? error.message : "Unable to scan nearby WiFi.");
  }
}

export async function getWifiRttCapabilities(): Promise<WifiRttCapabilities> {
  if (!nativeWifiModule?.getRttCapabilities) {
    return {
      rtt_supported: false,
      rtt_available: false,
      rtt_permission_state: "unknown",
      capability_mode: defaultCapabilityMode(),
      warnings: ["WiFi RTT capability detection is unavailable in this app runtime."],
    };
  }

  try {
    const payload = await nativeWifiModule.getRttCapabilities();
    return {
      rtt_supported: readBoolean(payload.rtt_supported) ?? false,
      rtt_available: readBoolean(payload.rtt_available) ?? false,
      rtt_permission_state:
        readPermissionState(payload.rtt_permission_state) ?? (Platform.OS === "android" ? "unknown" : "not_required"),
      capability_mode: readString(payload.capability_mode) ?? defaultCapabilityMode(),
      warnings: readStringArray(payload.warnings),
    };
  } catch (error) {
    return {
      rtt_supported: false,
      rtt_available: false,
      rtt_permission_state: "unknown",
      capability_mode: defaultCapabilityMode(),
      warnings: [error instanceof Error ? error.message : "Unable to detect WiFi RTT capability."],
    };
  }
}

export function inferRouterVendorHint(ssid?: string | null, bssidMasked?: string | null): RouterVendorHint {
  const normalizedSsid = (ssid ?? "").toLowerCase();
  if (normalizedSsid.includes("netgear") || normalizedSsid.includes("nighthawk") || normalizedSsid.includes("orbi")) {
    return "netgear";
  }
  if (
    normalizedSsid.includes("tp-link") ||
    normalizedSsid.includes("tplink") ||
    normalizedSsid.includes("archer") ||
    normalizedSsid.includes("deco")
  ) {
    return "tp_link";
  }

  const oui = extractOui(bssidMasked);
  if (oui && NETGEAR_OUIS.has(oui)) {
    return "netgear";
  }
  if (oui && TP_LINK_OUIS.has(oui)) {
    return "tp_link";
  }
  return "unknown";
}

export function confidenceCeilingForCapability(capabilityMode: string, vendorHint: RouterVendorHint): number {
  if (capabilityMode === "ios_network_limited") {
    return 0.45;
  }
  if (capabilityMode === "android_wifi_observation" && vendorHint !== "unknown") {
    return 0.68;
  }
  if (capabilityMode === "android_wifi_observation" || capabilityMode === "android_wifi_scan_limited") {
    return 0.6;
  }
  return 0.35;
}

export function maskBssid(value?: string | null): string | null {
  if (!value) {
    return null;
  }
  const parts = value.trim().toLowerCase().split(":");
  if (parts.length !== 6) {
    return value.trim().toLowerCase();
  }
  return `${parts.slice(0, 3).join(":")}:xx:xx:xx`;
}

function normalizeAccessPoint(value: unknown): NearbyAccessPointObservation {
  const payload = typeof value === "object" && value !== null ? (value as Record<string, unknown>) : {};
  const ssid = readString(payload.ssid);
  const bssidMasked = maskBssid(readString(payload.bssid_masked) ?? readString(payload.bssid));
  return {
    ssid,
    bssid_masked: bssidMasked,
    rssi_dbm: readNumber(payload.rssi_dbm) ?? readNumber(payload.level),
    level: readNumber(payload.level),
    frequency_mhz: readNumber(payload.frequency_mhz) ?? readNumber(payload.frequency),
    capabilities: readString(payload.capabilities),
    vendor_hint: inferRouterVendorHint(ssid, bssidMasked),
  };
}

function matchesSelectedRouter(
  accessPoint: NearbyAccessPointObservation,
  selectedNetwork?: SelectedNetworkObservation | null,
): boolean {
  if (!selectedNetwork) {
    return false;
  }
  if (selectedNetwork.bssid_masked && accessPoint.bssid_masked === selectedNetwork.bssid_masked) {
    return true;
  }
  return Boolean(selectedNetwork.ssid && accessPoint.ssid === selectedNetwork.ssid);
}

function unavailableCurrentWifi(warning: string): WifiCurrentObservation {
  return {
    ssid: null,
    bssid_masked: null,
    rssi_dbm: null,
    link_speed_mbps: null,
    frequency_mhz: null,
    wifi_standard: null,
    normalized_signal_strength: null,
    capability_mode: defaultCapabilityMode(),
    warnings: [warning],
  };
}

function unavailableScan(warning: string): WifiScanObservation {
  return {
    visible_access_points: 0,
    target_router_seen: false,
    access_points: [],
    capability_mode: defaultCapabilityMode(),
    scan_throttled: Platform.OS === "android",
    warnings: [warning],
  };
}

function defaultCapabilityMode(): CapabilityMode {
  if (Platform.OS === "android") {
    return "android_wifi_scan_limited";
  }
  if (Platform.OS === "ios") {
    return "ios_network_limited";
  }
  if (Platform.OS === "web") {
    return "web_unavailable";
  }
  return "native_unavailable";
}

function extractOui(value?: string | null): string | null {
  const parts = value?.toLowerCase().split(":") ?? [];
  if (parts.length < 3) {
    return null;
  }
  return parts.slice(0, 3).join(":");
}

function readString(value: unknown): string | null {
  return typeof value === "string" && value.trim() ? value.trim() : null;
}

function readNumber(value: unknown): number | null {
  const number = typeof value === "number" ? value : typeof value === "string" ? Number(value) : Number.NaN;
  return Number.isFinite(number) ? number : null;
}

function readBoolean(value: unknown): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function readStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function readPermissionState(value: unknown): WifiRttCapabilities["rtt_permission_state"] | null {
  if (value === "granted" || value === "denied" || value === "unknown" || value === "not_required") {
    return value;
  }
  return null;
}

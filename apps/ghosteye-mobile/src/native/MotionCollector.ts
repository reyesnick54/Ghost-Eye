import { NativeModules, Platform } from "react-native";

import { DeviceMotionObservation, DeviceMotionState } from "../types/telemetry";

type NativeMotionModule = {
  getDeviceMotion?: (sampleWindowMs?: number) => Promise<Record<string, unknown>>;
};

const nativeMotionModule = NativeModules.GhostEyeWifiModule as NativeMotionModule | undefined;

export async function getDeviceMotion(sampleWindowMs = 650): Promise<DeviceMotionObservation> {
  if (!nativeMotionModule?.getDeviceMotion) {
    return {
      state: "unknown",
      confidence: 0,
      capability_mode: Platform.OS === "ios" ? "ios_network_limited" : "native_unavailable",
      warnings: ["Device motion native collector is unavailable in this app runtime."],
    };
  }

  try {
    const payload = await nativeMotionModule.getDeviceMotion(sampleWindowMs);
    return {
      state: readMotionState(payload.state),
      confidence: clamp01(readNumber(payload.confidence) ?? 0),
      accelerometer_magnitude_std: readNumber(payload.accelerometer_magnitude_std),
      gyroscope_magnitude_std: readNumber(payload.gyroscope_magnitude_std),
      sample_count: Math.max(0, Math.round(readNumber(payload.sample_count) ?? 0)),
      capability_mode: readString(payload.capability_mode) ?? defaultCapabilityMode(),
      warnings: readStringArray(payload.warnings),
    };
  } catch (error) {
    return {
      state: "unknown",
      confidence: 0,
      capability_mode: defaultCapabilityMode(),
      warnings: [error instanceof Error ? error.message : "Unable to collect device motion."],
    };
  }
}

function readMotionState(value: unknown): DeviceMotionState {
  return value === "stable" || value === "moving" || value === "unknown" ? value : "unknown";
}

function defaultCapabilityMode(): string {
  return Platform.OS === "ios" ? "ios_network_limited" : Platform.OS === "android" ? "android_wifi_observation" : "native_unavailable";
}

function readString(value: unknown): string | null {
  return typeof value === "string" && value.trim() ? value.trim() : null;
}

function readNumber(value: unknown): number | null {
  const number = typeof value === "number" ? value : typeof value === "string" ? Number(value) : Number.NaN;
  return Number.isFinite(number) ? number : null;
}

function readStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}

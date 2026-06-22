import {
  GhostEyeScanTelemetry,
  MobileObservationBatchResponse,
  MobileObservationUploadResponse,
  MobileWifiObservation,
} from "../types/telemetry";
import { AIAnalysisEnvelope } from "../types/ai";

const DEFAULT_TIMEOUT_MS = 8000;

export function normalizeCloudUrl(url: string): string {
  return url.trim().replace(/\/+$/, "");
}

async function requestJson<T>(
  cloudUrl: string,
  path: string,
  init: RequestInit = {},
  timeoutMs = DEFAULT_TIMEOUT_MS,
): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  const hasBody = typeof init.body !== "undefined";

  try {
    const response = await fetch(`${normalizeCloudUrl(cloudUrl)}${path}`, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(hasBody ? { "Content-Type": "application/json" } : {}),
        ...init.headers,
      },
      signal: controller.signal,
    });
    const text = await response.text();
    const payload = text ? JSON.parse(text) : {};

    if (!response.ok) {
      const detail = payload?.detail ?? payload?.message ?? response.statusText;
      throw new Error(`GhostEye Cloud ${response.status}: ${detail}`);
    }

    return payload as T;
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("GhostEye Cloud request timed out.");
      }
      throw error;
    }
    throw new Error("GhostEye Cloud request failed.");
  } finally {
    clearTimeout(timeout);
  }
}

export function postObservation(
  cloudUrl: string,
  observation: MobileWifiObservation,
): Promise<MobileObservationUploadResponse> {
  return requestJson<MobileObservationUploadResponse>(cloudUrl, "/telemetry/observation", {
    method: "POST",
    body: JSON.stringify(observation),
  });
}

export function postObservationBatch(
  cloudUrl: string,
  observations: MobileWifiObservation[],
): Promise<MobileObservationBatchResponse> {
  return requestJson<MobileObservationBatchResponse>(cloudUrl, "/telemetry/batch", {
    method: "POST",
    body: JSON.stringify({ observations }),
  });
}

export function getTelemetryScan(cloudUrl: string): Promise<GhostEyeScanTelemetry> {
  return requestJson<GhostEyeScanTelemetry>(cloudUrl, "/scan");
}

export function analyzeScan(
  cloudUrl: string,
  telemetry: MobileWifiObservation | GhostEyeScanTelemetry,
): Promise<AIAnalysisEnvelope> {
  return requestJson<AIAnalysisEnvelope>(cloudUrl, "/ai/analyze-scan", {
    method: "POST",
    body: JSON.stringify(telemetry),
  });
}

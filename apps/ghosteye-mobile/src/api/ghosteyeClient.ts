import {
  CalibrationResult,
  CurrentMapResponse,
  GhostEyeScanTelemetry,
  HealthResponse,
  RoomSetupRequest,
  RoomSetupResponse,
  SessionResponse,
  SourcesResponse,
  WifiNetworksResponse,
  WifiSelectionResponse,
  ZoneId,
} from "../types/telemetry";

const DEFAULT_TIMEOUT_MS = 8000;

export function normalizeBackendUrl(url: string): string {
  return url.trim().replace(/\/+$/, "");
}

async function requestJson<T>(
  backendUrl: string,
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);
  const hasBody = typeof init.body !== "undefined";

  try {
    const response = await fetch(`${normalizeBackendUrl(backendUrl)}${path}`, {
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
      const detail = payload?.detail ?? response.statusText;
      throw new Error(`GhostEye backend ${response.status}: ${detail}`);
    }

    return payload as T;
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("GhostEye backend request timed out.");
      }
      throw error;
    }
    throw new Error("GhostEye backend request failed.");
  } finally {
    clearTimeout(timeout);
  }
}

export function getHealth(backendUrl: string): Promise<HealthResponse> {
  return requestJson<HealthResponse>(backendUrl, "/health");
}

export function getSources(backendUrl: string): Promise<SourcesResponse> {
  return requestJson<SourcesResponse>(backendUrl, "/sources");
}

export function selectSource(backendUrl: string, sourceId: string): Promise<SourcesResponse> {
  return requestJson<SourcesResponse>(backendUrl, "/source/select", {
    method: "POST",
    body: JSON.stringify({ source_id: sourceId }),
  });
}

export function getWifiNetworks(backendUrl: string): Promise<WifiNetworksResponse> {
  return requestJson<WifiNetworksResponse>(backendUrl, "/wifi/networks");
}

export function selectWifiNetwork(
  backendUrl: string,
  ssid: string,
  adapterMode = "wifi_only_non_csi",
): Promise<WifiSelectionResponse> {
  return requestJson<WifiSelectionResponse>(backendUrl, "/wifi/select", {
    method: "POST",
    body: JSON.stringify({ ssid, adapter_mode: adapterMode }),
  });
}

export function setupRoom(
  backendUrl: string,
  roomSetup: RoomSetupRequest,
): Promise<RoomSetupResponse> {
  return requestJson<RoomSetupResponse>(backendUrl, "/room/setup", {
    method: "POST",
    body: JSON.stringify(roomSetup),
  });
}

export function getScan(backendUrl: string): Promise<GhostEyeScanTelemetry> {
  return requestJson<GhostEyeScanTelemetry>(backendUrl, "/scan");
}

export function getCurrentMap(backendUrl: string): Promise<CurrentMapResponse> {
  return requestJson<CurrentMapResponse>(backendUrl, "/map/current");
}

export function runEmptyRoomCalibration(backendUrl: string): Promise<CalibrationResult> {
  return requestJson<CalibrationResult>(backendUrl, "/calibrate/empty-room", {
    method: "POST",
  });
}

export function calibrateZone(
  backendUrl: string,
  zone: ZoneId,
): Promise<CalibrationResult> {
  return requestJson<CalibrationResult>(backendUrl, "/calibrate/zone", {
    method: "POST",
    body: JSON.stringify({ zone }),
  });
}

export function startSession(backendUrl: string): Promise<SessionResponse> {
  return requestJson<SessionResponse>(backendUrl, "/session/start", {
    method: "POST",
    body: JSON.stringify({ metadata: { client: "abraxas-ghosteye-mobile" } }),
  });
}

export function stopSession(backendUrl: string): Promise<SessionResponse> {
  return requestJson<SessionResponse>(backendUrl, "/session/stop", {
    method: "POST",
  });
}

export function getLatestSession(backendUrl: string): Promise<SessionResponse> {
  return requestJson<SessionResponse>(backendUrl, "/session/latest");
}

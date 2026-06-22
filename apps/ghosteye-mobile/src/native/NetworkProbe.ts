import { normalizeCloudUrl } from "../services/ghosteyeCloudClient";
import { NetworkProbeObservation } from "../types/telemetry";

interface NetworkProbeOptions {
  cloudUrl: string;
  routerProbeHost?: string | null;
  probeCount?: number;
  timeoutMs?: number;
}

interface ProbeResult {
  latencyMs: number | null;
  ok: boolean;
  warning?: string;
}

export async function measureNetworkProbe({
  cloudUrl,
  routerProbeHost,
  probeCount = 4,
  timeoutMs = 3500,
}: NetworkProbeOptions): Promise<NetworkProbeObservation> {
  const boundedProbeCount = Math.max(1, Math.min(8, Math.round(probeCount)));
  const cloudResults: ProbeResult[] = [];
  const warnings: string[] = [];

  for (let index = 0; index < boundedProbeCount; index += 1) {
    const result = await timeFetch(`${normalizeCloudUrl(cloudUrl)}/health`, timeoutMs);
    cloudResults.push(result);
    if (result.warning) {
      warnings.push(`cloud probe ${index + 1}: ${result.warning}`);
    }
  }

  const routerResult = routerProbeHost
    ? await timeFetch(normalizeRouterProbeUrl(routerProbeHost), timeoutMs)
    : null;
  if (routerResult?.warning) {
    warnings.push(`router probe: ${routerResult.warning}`);
  }

  const failedProbeCount =
    cloudResults.filter((result) => !result.ok).length + (routerResult && !routerResult.ok ? 1 : 0);
  const totalProbeCount = cloudResults.length + (routerResult ? 1 : 0);
  const cloudLatencies = cloudResults
    .map((result) => result.latencyMs)
    .filter((value): value is number => typeof value === "number");

  return {
    cloud_latency_ms: mean(cloudLatencies),
    router_probe_latency_ms: routerResult?.latencyMs ?? null,
    jitter_ms: jitter(cloudLatencies),
    packet_loss_estimate: totalProbeCount > 0 ? round(failedProbeCount / totalProbeCount, 4) : 1,
    probe_count: totalProbeCount,
    failed_probe_count: failedProbeCount,
    warnings,
  };
}

async function timeFetch(url: string, timeoutMs: number): Promise<ProbeResult> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  const startedAt = Date.now();

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { Accept: "application/json, text/plain, */*" },
      signal: controller.signal,
    });
    const latencyMs = Date.now() - startedAt;
    return {
      latencyMs,
      ok: response.ok || response.status < 500,
      warning: response.ok || response.status < 500 ? undefined : `HTTP ${response.status}`,
    };
  } catch (error) {
    return {
      latencyMs: null,
      ok: false,
      warning: error instanceof Error ? error.message : "request failed",
    };
  } finally {
    clearTimeout(timeout);
  }
}

function normalizeRouterProbeUrl(routerProbeHost: string): string {
  const trimmed = routerProbeHost.trim();
  if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
    return trimmed;
  }
  return `http://${trimmed}`;
}

function mean(values: number[]): number | null {
  if (values.length === 0) {
    return null;
  }
  return round(values.reduce((sum, value) => sum + value, 0) / values.length, 2);
}

function jitter(values: number[]): number | null {
  if (values.length < 2) {
    return null;
  }
  const average = mean(values);
  if (average === null) {
    return null;
  }
  const variance = values.reduce((sum, value) => sum + Math.abs(value - average), 0) / values.length;
  return round(variance, 2);
}

function round(value: number, digits: number): number {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

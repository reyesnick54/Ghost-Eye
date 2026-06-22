import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { StatusCard } from "../components/StatusCard";
import { analyzeScan, getTelemetryScan } from "../services/ghosteyeCloudClient";
import {
  recommendedObservationIntervalMs,
  startTelemetryUploadStream,
} from "../services/telemetryUploader";
import { AIAnalysis } from "../types/ai";
import {
  GhostEyeScanTelemetry,
  MobileObservationUploadResponse,
  MobileWifiObservation,
  SelectedNetworkObservation,
  WIFI_ONLY_LIMITATION,
} from "../types/telemetry";

interface LiveScanScreenProps {
  backendUrl: string;
  refreshIntervalMs: number;
  selectedNetwork: SelectedNetworkObservation | null;
  routerProbeHost?: string | null;
  teamId?: string | null;
}

function formatNumber(value?: number | null, digits = 2): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "unavailable";
  }
  return value.toFixed(digits);
}

function formatPercent(value?: number | null): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "unavailable";
  }
  return `${Math.round(value * 100)}%`;
}

export function LiveScanScreen({
  backendUrl,
  refreshIntervalMs,
  selectedNetwork,
  routerProbeHost,
  teamId,
}: LiveScanScreenProps) {
  const [streaming, setStreaming] = useState(false);
  const [observation, setObservation] = useState<MobileWifiObservation | null>(null);
  const [uploadResponse, setUploadResponse] = useState<MobileObservationUploadResponse | null>(null);
  const [telemetryScan, setTelemetryScan] = useState<GhostEyeScanTelemetry | null>(null);
  const [aiAnalysis, setAiAnalysis] = useState<AIAnalysis | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const streamIntervalMs = useMemo(
    () => Math.max(Math.min(refreshIntervalMs, 5000), recommendedObservationIntervalMs()),
    [refreshIntervalMs],
  );

  const refreshBackendPanels = useCallback(
    async (latestObservation?: MobileWifiObservation) => {
      try {
        const scan = await getTelemetryScan(backendUrl);
        setTelemetryScan(scan);
        const analysis = await analyzeScan(backendUrl, latestObservation ?? scan);
        setAiAnalysis(analysis.ai_analysis ?? null);
      } catch (requestError) {
        setError(requestError instanceof Error ? requestError.message : "Unable to refresh cloud scan.");
      }
    },
    [backendUrl],
  );

  useEffect(() => {
    if (!streaming) {
      return undefined;
    }

    const stop = startTelemetryUploadStream({
      cloudUrl: backendUrl,
      intervalMs: streamIntervalMs,
      selectedNetwork,
      routerProbeHost,
      teamId,
      onObservation: (payload) => {
        setObservation(payload);
        setLastUpdated(new Date().toLocaleTimeString());
        void refreshBackendPanels(payload);
      },
      onUpload: (response) => {
        setUploadResponse(response);
        setTelemetryScan(response.telemetry_scan ?? response.scan ?? null);
        setAiAnalysis(response.ai_analysis ?? null);
        setError(null);
      },
      onError: (streamError) => {
        setError(streamError.message);
      },
    });

    return stop;
  }, [backendUrl, refreshBackendPanels, routerProbeHost, selectedNetwork, streamIntervalMs, streaming, teamId]);

  const scan = telemetryScan ?? uploadResponse?.telemetry_scan ?? uploadResponse?.scan ?? null;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Live scan</Text>
        <Text style={styles.title}>Mobile WiFi observation stream</Text>
        <Text style={styles.copy}>
          Streams permitted WiFi/network/device-motion observations every {streamIntervalMs / 1000}s.
          Outputs remain probabilistic, confidence-capped, WiFi-only, and non-CSI.
        </Text>
      </View>

      <View style={styles.noticeCard}>
        <Text style={styles.noticeTitle}>Limitations</Text>
        <Text style={styles.noticeText}>{scan?.limitations ?? WIFI_ONLY_LIMITATION}</Text>
        <Text style={styles.noticeText}>
          This app does not claim raw CSI access, true RF imaging, or deterministic presence detection.
        </Text>
      </View>

      <View style={styles.statusGrid}>
        <StatusCard
          label="Stream"
          value={streaming ? "running" : "stopped"}
          tone={streaming ? "good" : "warn"}
        />
        <StatusCard label="Selected router" value={selectedNetwork?.ssid ?? "none"} />
        <StatusCard label="Upload status" value={uploadResponse?.status ?? "pending"} />
        <StatusCard label="Capability" value={observation?.capability_mode ?? "unknown"} />
        <StatusCard label="Cloud latency" value={formatNumber(observation?.network_probe.cloud_latency_ms, 1)} />
        <StatusCard label="Router latency" value={formatNumber(observation?.network_probe.router_probe_latency_ms, 1)} />
        <StatusCard label="Jitter" value={formatNumber(observation?.network_probe.jitter_ms, 1)} />
        <StatusCard label="Packet loss" value={formatPercent(observation?.network_probe.packet_loss_estimate)} />
        <StatusCard label="Device motion" value={observation?.device_motion.state ?? "unknown"} />
        <StatusCard
          label="Confidence ceiling"
          value={formatPercent(selectedNetwork?.confidence_ceiling ?? scan?.confidence_ceiling)}
        />
      </View>

      <View style={styles.buttonRow}>
        <Pressable
          disabled={!selectedNetwork?.owned_authorized_confirmed}
          onPress={() => setStreaming((value) => !value)}
          style={({ pressed }) => [
            styles.primaryButton,
            !selectedNetwork?.owned_authorized_confirmed && styles.buttonDisabled,
            streaming && styles.stopButton,
            pressed && styles.buttonPressed,
          ]}
        >
          <Text style={styles.primaryButtonText}>
            {streaming ? "Stop observation stream" : "Start observation stream"}
          </Text>
        </Pressable>
        <Pressable
          onPress={() => void refreshBackendPanels(observation ?? undefined)}
          style={({ pressed }) => [styles.secondaryButton, pressed && styles.buttonPressed]}
        >
          <Text style={styles.secondaryButtonText}>Refresh cloud scan</Text>
        </Pressable>
      </View>

      {!selectedNetwork?.owned_authorized_confirmed ? (
        <Text style={styles.warning}>Select and authorize an owned test router before streaming observations.</Text>
      ) : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Backend TelemetryScan</Text>
        {scan ? (
          <>
            <Text style={styles.meta}>Presence: {scan.presence ?? "unavailable"}</Text>
            <Text style={styles.meta}>Zone: {scan.zone ?? "unavailable"}</Text>
            <Text style={styles.meta}>Confidence: {formatPercent(scan.confidence)}</Text>
            <Text style={styles.json}>{JSON.stringify(scan, null, 2)}</Text>
          </>
        ) : (
          <Text style={styles.empty}>No backend TelemetryScan returned yet.</Text>
        )}
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>AIAnalysis</Text>
        {aiAnalysis ? (
          <>
            <Text style={styles.meta}>Provider: {aiAnalysis.provider ?? "unknown"}</Text>
            <Text style={styles.meta}>Confidence: {formatPercent(aiAnalysis.confidence)}</Text>
            <Text style={styles.meta}>Summary: {aiAnalysis.summary ?? "unavailable"}</Text>
            <Text style={styles.json}>{JSON.stringify(aiAnalysis, null, 2)}</Text>
          </>
        ) : (
          <Text style={styles.empty}>No AIAnalysis returned yet.</Text>
        )}
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Latest MobileWifiObservation</Text>
        <Text style={styles.meta}>Last update: {lastUpdated ?? "never"}</Text>
        {observation ? (
          <Text style={styles.json}>{JSON.stringify(observation, null, 2)}</Text>
        ) : (
          <Text style={styles.empty}>No mobile observation collected yet.</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 16,
  },
  header: {
    gap: 8,
  },
  kicker: {
    color: "#38bdf8",
    fontSize: 12,
    fontWeight: "900",
    letterSpacing: 1.5,
    textTransform: "uppercase",
  },
  title: {
    color: "#f8fafc",
    fontSize: 28,
    fontWeight: "900",
  },
  copy: {
    color: "#cbd5e1",
    fontSize: 14,
    lineHeight: 21,
  },
  noticeCard: {
    backgroundColor: "#111827",
    borderColor: "#334155",
    borderRadius: 16,
    borderWidth: 1,
    gap: 6,
    padding: 14,
  },
  noticeTitle: {
    color: "#facc15",
    fontSize: 12,
    fontWeight: "900",
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  noticeText: {
    color: "#e5e7eb",
    fontSize: 13,
    lineHeight: 19,
  },
  statusGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  buttonRow: {
    gap: 10,
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 14,
    paddingVertical: 13,
  },
  stopButton: {
    backgroundColor: "#fb7185",
  },
  primaryButtonText: {
    color: "#03130a",
    fontSize: 14,
    fontWeight: "900",
  },
  secondaryButton: {
    alignItems: "center",
    borderColor: "#38bdf8",
    borderRadius: 14,
    borderWidth: 1,
    paddingVertical: 13,
  },
  secondaryButtonText: {
    color: "#bae6fd",
    fontSize: 14,
    fontWeight: "900",
  },
  buttonDisabled: {
    opacity: 0.55,
  },
  buttonPressed: {
    opacity: 0.75,
  },
  warning: {
    backgroundColor: "#2a2308",
    borderColor: "#854d0e",
    borderRadius: 14,
    borderWidth: 1,
    color: "#fde68a",
    fontSize: 13,
    lineHeight: 19,
    padding: 12,
  },
  error: {
    backgroundColor: "#2a0b12",
    borderColor: "#7f1d1d",
    borderRadius: 14,
    borderWidth: 1,
    color: "#fecdd3",
    fontSize: 13,
    lineHeight: 19,
    padding: 12,
  },
  panel: {
    backgroundColor: "#0f172a",
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    gap: 8,
    padding: 14,
  },
  panelTitle: {
    color: "#f8fafc",
    fontSize: 17,
    fontWeight: "900",
  },
  meta: {
    color: "#cbd5e1",
    fontSize: 13,
    lineHeight: 19,
  },
  empty: {
    color: "#94a3b8",
    fontSize: 13,
  },
  json: {
    color: "#cbd5e1",
    fontFamily: "monospace",
    fontSize: 11,
    lineHeight: 16,
  },
});

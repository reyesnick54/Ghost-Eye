import React, { useCallback, useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { getScan } from "../api/ghosteyeClient";
import { StatusCard } from "../components/StatusCard";
import { ZoneMap } from "../components/ZoneMap";
import { GhostEyeScanTelemetry, WIFI_ONLY_LIMITATION } from "../types/telemetry";

interface LiveScanDashboardProps {
  backendUrl: string;
  refreshIntervalMs: number;
}

function formatNumber(value?: number, digits = 2): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "unavailable";
  }
  return value.toFixed(digits);
}

function formatPercent(value?: number): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "unavailable";
  }
  return `${Math.round(value * 100)}%`;
}

export function LiveScanDashboard({ backendUrl, refreshIntervalMs }: LiveScanDashboardProps) {
  const [telemetry, setTelemetry] = useState<GhostEyeScanTelemetry | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadScan = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = await getScan(backendUrl);
      setTelemetry(payload);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load scan.");
    } finally {
      setLoading(false);
    }
  }, [backendUrl]);

  useEffect(() => {
    let active = true;

    async function poll() {
      if (!active) {
        return;
      }
      await loadScan();
    }

    void poll();
    const timer = setInterval(() => {
      void poll();
    }, refreshIntervalMs);

    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [loadScan, refreshIntervalMs]);

  const quality = telemetry?.signal_quality;
  const zoneMap = telemetry?.map ?? {};

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Live scan</Text>
        <Text style={styles.title}>WiFi-only non-CSI dashboard</Text>
        <Text style={styles.copy}>
          Outputs are probabilistic WiFi-only non-CSI estimates. This app does not claim
          true through-wall imaging or validated operational intelligence.
        </Text>
      </View>

      <View style={styles.noticeCard}>
        <Text style={styles.noticeTitle}>Mode boundary</Text>
        <Text style={styles.noticeText}>
          {telemetry?.limitations ?? WIFI_ONLY_LIMITATION}
        </Text>
        {telemetry?.notice ? <Text style={styles.noticeText}>{telemetry.notice}</Text> : null}
      </View>

      <View style={styles.statusGrid}>
        <StatusCard label="Presence" value={telemetry?.presence} tone="neutral" />
        <StatusCard label="Motion score" value={formatNumber(telemetry?.motion_score)} />
        <StatusCard label="Zone" value={telemetry?.zone} tone="good" />
        <StatusCard label="Confidence" value={formatPercent(telemetry?.confidence)} />
        <StatusCard
          label="Confidence ceiling"
          value={formatPercent(telemetry?.confidence_ceiling)}
          detail="Backend cap for WiFi-only non-CSI mode"
        />
        <StatusCard
          label="Signal quality"
          value={quality ? `${quality.visible_access_points ?? "?"} APs` : "unavailable"}
          detail={
            quality
              ? `latency ${formatNumber(quality.gateway_latency_ms, 1)} ms, jitter ${formatNumber(
                  quality.jitter_ms,
                  1,
                )} ms`
              : undefined
          }
        />
      </View>

      <ZoneMap selectedZone={telemetry?.zone} zoneMap={zoneMap} />

      <View style={styles.mapValues}>
        <Text style={styles.sectionTitle}>Map zone values</Text>
        {Object.keys(zoneMap).length === 0 ? (
          <Text style={styles.emptyText}>No map values returned yet.</Text>
        ) : (
          Object.entries(zoneMap).map(([zone, value]) => (
            <View key={zone} style={styles.mapRow}>
              <Text style={styles.mapZone}>{zone}</Text>
              <Text style={styles.mapValue}>{formatNumber(value, 3)}</Text>
            </View>
          ))
        )}
      </View>

      <View style={styles.footerRow}>
        <Text style={styles.footerText}>
          {loading ? "Polling /scan..." : `Refresh interval: ${refreshIntervalMs / 1000}s`}
        </Text>
        <Text style={styles.footerText}>Last update: {lastUpdated ?? "never"}</Text>
      </View>

      <Pressable
        disabled={loading}
        onPress={loadScan}
        style={({ pressed }) => [
          styles.secondaryButton,
          loading && styles.secondaryButtonDisabled,
          pressed && styles.secondaryButtonPressed,
        ]}
      >
        <Text style={styles.secondaryButtonText}>{loading ? "Refreshing..." : "Refresh now"}</Text>
      </Pressable>

      {error ? <Text style={styles.error}>{error}</Text> : null}
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
    borderColor: "#334155",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#111827",
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
  mapValues: {
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    gap: 8,
    padding: 14,
  },
  sectionTitle: {
    color: "#f8fafc",
    fontSize: 16,
    fontWeight: "900",
  },
  emptyText: {
    color: "#94a3b8",
    fontSize: 13,
  },
  mapRow: {
    alignItems: "center",
    borderTopColor: "#1e293b",
    borderTopWidth: 1,
    flexDirection: "row",
    justifyContent: "space-between",
    paddingTop: 8,
  },
  mapZone: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "800",
    textTransform: "uppercase",
  },
  mapValue: {
    color: "#bae6fd",
    fontSize: 15,
    fontWeight: "900",
  },
  footerRow: {
    gap: 4,
  },
  footerText: {
    color: "#94a3b8",
    fontSize: 12,
  },
  secondaryButton: {
    alignItems: "center",
    borderColor: "#38bdf8",
    borderRadius: 14,
    borderWidth: 1,
    paddingVertical: 13,
  },
  secondaryButtonDisabled: {
    borderColor: "#334155",
  },
  secondaryButtonPressed: {
    opacity: 0.75,
  },
  secondaryButtonText: {
    color: "#bae6fd",
    fontSize: 14,
    fontWeight: "900",
  },
  error: {
    borderColor: "#7f1d1d",
    borderRadius: 14,
    borderWidth: 1,
    backgroundColor: "#2a0b12",
    color: "#fecdd3",
    fontSize: 13,
    lineHeight: 19,
    padding: 12,
  },
});

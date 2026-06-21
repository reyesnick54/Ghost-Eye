import React, { useCallback, useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { getSources } from "../api/ghosteyeClient";
import { StatusCard } from "../components/StatusCard";
import { GhostEyeSource } from "../types/telemetry";

interface SourceSelectionScreenProps {
  backendUrl: string;
}

export function SourceSelectionScreen({ backendUrl }: SourceSelectionScreenProps) {
  const [sources, setSources] = useState<GhostEyeSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSources = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = await getSources(backendUrl);
      setSources(payload.sources ?? []);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load sources.");
    } finally {
      setLoading(false);
    }
  }, [backendUrl]);

  useEffect(() => {
    void loadSources();
  }, [loadSources]);

  const selectedSource =
    sources.find((source) => source.selected) ??
    sources.find((source) => source.id === "local_wifi_rssi_latency_simulated");

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Signal source</Text>
        <Text style={styles.title}>WiFi RSSI + latency input</Text>
        <Text style={styles.copy}>
          The mobile app displays backend telemetry only. It does not attempt raw WiFi CSI
          access from phone APIs.
        </Text>
      </View>

      <View style={styles.statusGrid}>
        <StatusCard
          label="Selected"
          tone={selectedSource ? "good" : "warn"}
          value={selectedSource?.id ?? "none"}
        />
        <StatusCard
          label="CSI"
          tone={selectedSource?.csi === false ? "good" : "warn"}
          value={selectedSource?.csi === false ? "false" : "unknown"}
          detail={selectedSource?.csi === false ? "Backend reports no CSI capture." : undefined}
        />
      </View>

      <Pressable
        disabled={loading}
        onPress={loadSources}
        style={({ pressed }) => [
          styles.secondaryButton,
          loading && styles.secondaryButtonDisabled,
          pressed && styles.secondaryButtonPressed,
        ]}
      >
        <Text style={styles.secondaryButtonText}>{loading ? "Refreshing..." : "Refresh sources"}</Text>
      </Pressable>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={styles.sourceList}>
        {sources.length === 0 && !loading ? (
          <Text style={styles.empty}>No backend sources returned.</Text>
        ) : null}
        {sources.map((source) => {
          const highlighted =
            source.selected || source.id === "local_wifi_rssi_latency_simulated";

          return (
            <View key={source.id} style={[styles.sourceCard, highlighted && styles.sourceSelected]}>
              <View style={styles.sourceHeader}>
                <Text style={styles.sourceName}>{source.name ?? source.id}</Text>
                <Text style={[styles.badge, highlighted && styles.badgeSelected]}>
                  {highlighted ? "selected" : source.status ?? "available"}
                </Text>
              </View>
              <Text style={styles.sourceId}>{source.id}</Text>
              <Text style={styles.sourceMeta}>Mode: {source.mode ?? "unknown"}</Text>
              <Text style={styles.sourceMeta}>Type: {source.type ?? "unknown"}</Text>
              <Text style={styles.sourceMeta}>Simulated: {String(source.simulated ?? false)}</Text>
              <Text style={styles.sourceMeta}>CSI: {String(source.csi ?? "unknown")}</Text>
              {source.capabilities?.length ? (
                <Text style={styles.capabilities}>
                  Capabilities: {source.capabilities.join(", ")}
                </Text>
              ) : null}
            </View>
          );
        })}
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
  statusGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
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
  sourceList: {
    gap: 12,
  },
  empty: {
    color: "#94a3b8",
    fontSize: 14,
  },
  sourceCard: {
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    gap: 6,
    padding: 14,
  },
  sourceSelected: {
    borderColor: "#22c55e",
    backgroundColor: "#082f25",
  },
  sourceHeader: {
    alignItems: "flex-start",
    flexDirection: "row",
    gap: 8,
    justifyContent: "space-between",
  },
  sourceName: {
    color: "#f8fafc",
    flex: 1,
    fontSize: 16,
    fontWeight: "900",
  },
  badge: {
    borderColor: "#334155",
    borderRadius: 999,
    borderWidth: 1,
    color: "#cbd5e1",
    fontSize: 11,
    fontWeight: "900",
    paddingHorizontal: 8,
    paddingVertical: 4,
    textTransform: "uppercase",
  },
  badgeSelected: {
    borderColor: "#22c55e",
    color: "#bbf7d0",
  },
  sourceId: {
    color: "#93c5fd",
    fontSize: 12,
    fontWeight: "800",
  },
  sourceMeta: {
    color: "#cbd5e1",
    fontSize: 13,
  },
  capabilities: {
    color: "#94a3b8",
    fontSize: 12,
    lineHeight: 18,
  },
});

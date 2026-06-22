import React, { useCallback, useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { getCurrentMap } from "../api/ghosteyeClient";
import { StatusCard } from "../components/StatusCard";
import { ZoneMap } from "../components/ZoneMap";
import { CurrentMapResponse } from "../types/telemetry";

interface RoomMapScreenProps {
  backendUrl: string;
}

function formatMeters(value?: number): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "unavailable";
  }
  return `${value.toFixed(1)} m`;
}

export function RoomMapScreen({ backendUrl }: RoomMapScreenProps) {
  const [mapPayload, setMapPayload] = useState<CurrentMapResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadMap = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setMapPayload(await getCurrentMap(backendUrl));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load room map.");
    } finally {
      setLoading(false);
    }
  }, [backendUrl]);

  useEffect(() => {
    void loadMap();
  }, [loadMap]);

  const roomMap = mapPayload?.room_map;
  const zoneScores = roomMap?.zones ?? mapPayload?.map ?? {};

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Room map</Text>
        <Text style={styles.title}>Zone heatmap</Text>
        <Text style={styles.copy}>
          The heatmap is a coarse backend estimate from WiFi-only RSSI/latency simulation
          and fingerprints. It is not true RF imaging or operational intelligence.
        </Text>
      </View>

      <View style={styles.statusGrid}>
        <StatusCard label="Room" value={roomMap?.room_name ?? "Demo Room"} />
        <StatusCard label="Shape" value={roomMap?.shape ?? "rectangle"} />
        <StatusCard label="Width" value={formatMeters(roomMap?.width_m)} />
        <StatusCard label="Length" value={formatMeters(roomMap?.length_m)} />
      </View>

      <ZoneMap selectedZone={mapPayload?.zone} zoneMap={zoneScores} />

      <View style={styles.valuesCard}>
        <Text style={styles.sectionTitle}>Zone scores</Text>
        {Object.keys(zoneScores).length === 0 ? (
          <Text style={styles.empty}>No zone scores returned yet.</Text>
        ) : (
          Object.entries(zoneScores).map(([zone, value]) => (
            <View key={zone} style={styles.row}>
              <Text style={styles.zone}>{zone}</Text>
              <Text style={styles.score}>{value.toFixed(2)}</Text>
            </View>
          ))
        )}
      </View>

      {mapPayload?.limitations ? <Text style={styles.notice}>{mapPayload.limitations}</Text> : null}
      {mapPayload?.notice ? <Text style={styles.notice}>{mapPayload.notice}</Text> : null}

      <Pressable
        disabled={loading}
        onPress={loadMap}
        style={({ pressed }) => [
          styles.secondaryButton,
          loading && styles.buttonDisabled,
          pressed && styles.buttonPressed,
        ]}
      >
        <Text style={styles.secondaryButtonText}>
          {loading ? "Refreshing map..." : "Refresh room map"}
        </Text>
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
  statusGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  valuesCard: {
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
  empty: {
    color: "#94a3b8",
    fontSize: 13,
  },
  row: {
    alignItems: "center",
    borderTopColor: "#1e293b",
    borderTopWidth: 1,
    flexDirection: "row",
    justifyContent: "space-between",
    paddingTop: 8,
  },
  zone: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "800",
    textTransform: "uppercase",
  },
  score: {
    color: "#bae6fd",
    fontSize: 15,
    fontWeight: "900",
  },
  notice: {
    borderColor: "#334155",
    borderRadius: 14,
    borderWidth: 1,
    backgroundColor: "#111827",
    color: "#e5e7eb",
    fontSize: 13,
    lineHeight: 19,
    padding: 12,
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

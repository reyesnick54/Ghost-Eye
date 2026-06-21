import React, { useMemo } from "react";
import { StyleSheet, Text, View } from "react-native";

const DEFAULT_ZONES = ["zone_a", "zone_b", "zone_c"];

interface ZoneMapProps {
  zoneMap?: Record<string, number>;
  selectedZone?: string;
}

function formatScore(score?: number): string {
  if (typeof score !== "number" || Number.isNaN(score)) {
    return "--";
  }
  return `${Math.round(score * 100)}%`;
}

export function ZoneMap({ zoneMap = {}, selectedZone }: ZoneMapProps) {
  const zones = useMemo(() => {
    const allZones = new Set([...DEFAULT_ZONES, ...Object.keys(zoneMap)]);
    return Array.from(allZones);
  }, [zoneMap]);

  const strongestZone = zones.reduce<string | undefined>((current, zone) => {
    if (!current) {
      return zone;
    }
    return (zoneMap[zone] ?? -1) > (zoneMap[current] ?? -1) ? zone : current;
  }, undefined);

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.title}>Probabilistic room map</Text>
        <Text style={styles.subtitle}>WiFi-only non-CSI estimates</Text>
      </View>
      <View style={styles.zoneGrid}>
        {zones.map((zone) => {
          const score = zoneMap[zone];
          const isStrongest = zone === strongestZone && typeof score === "number";
          const isSelected = zone === selectedZone;

          return (
            <View
              key={zone}
              style={[
                styles.zoneCard,
                isStrongest && styles.strongestZone,
                isSelected && styles.selectedZone,
              ]}
            >
              <Text style={styles.zoneLabel}>{zone}</Text>
              <Text style={styles.zoneScore}>{formatScore(score)}</Text>
              <Text style={styles.zoneHint}>
                {isStrongest ? "strongest signal estimate" : "relative estimate"}
              </Text>
            </View>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderColor: "#1f3b4d",
    borderRadius: 18,
    borderWidth: 1,
    backgroundColor: "#08111f",
    padding: 14,
    gap: 12,
  },
  headerRow: {
    gap: 4,
  },
  title: {
    color: "#e0f2fe",
    fontSize: 17,
    fontWeight: "900",
  },
  subtitle: {
    color: "#93c5fd",
    fontSize: 12,
    fontWeight: "700",
  },
  zoneGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  zoneCard: {
    flex: 1,
    minWidth: 96,
    borderColor: "#233044",
    borderRadius: 14,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    padding: 12,
  },
  strongestZone: {
    borderColor: "#22c55e",
    backgroundColor: "#082f25",
  },
  selectedZone: {
    shadowColor: "#38bdf8",
    shadowOpacity: 0.35,
    shadowRadius: 8,
  },
  zoneLabel: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "800",
    marginBottom: 8,
    textTransform: "uppercase",
  },
  zoneScore: {
    color: "#f8fafc",
    fontSize: 26,
    fontWeight: "900",
  },
  zoneHint: {
    color: "#94a3b8",
    fontSize: 11,
    lineHeight: 16,
    marginTop: 6,
  },
});

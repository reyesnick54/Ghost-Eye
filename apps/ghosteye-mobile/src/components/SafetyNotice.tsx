import React from "react";
import { StyleSheet, Text, View } from "react-native";

import { SAFETY_ACKNOWLEDGEMENT, WIFI_ONLY_LIMITATION } from "../types/telemetry";

interface SafetyNoticeProps {
  compact?: boolean;
}

export function SafetyNotice({ compact = false }: SafetyNoticeProps) {
  return (
    <View style={[styles.container, compact && styles.compact]}>
      <Text style={styles.eyebrow}>Safety boundary</Text>
      <Text style={styles.body}>{SAFETY_ACKNOWLEDGEMENT}</Text>
      <Text style={styles.limitation}>{WIFI_ONLY_LIMITATION}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderColor: "#334155",
    borderRadius: 18,
    borderWidth: 1,
    backgroundColor: "#111827",
    padding: 16,
    gap: 8,
  },
  compact: {
    padding: 12,
    borderRadius: 14,
  },
  eyebrow: {
    color: "#facc15",
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 1.4,
    textTransform: "uppercase",
  },
  body: {
    color: "#e5e7eb",
    fontSize: 14,
    lineHeight: 21,
  },
  limitation: {
    color: "#93c5fd",
    fontSize: 13,
    fontWeight: "700",
    lineHeight: 19,
  },
});

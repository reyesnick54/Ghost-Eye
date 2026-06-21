import React from "react";
import { StyleSheet, Text, View } from "react-native";

interface StatusCardProps {
  label: string;
  value?: string | number | boolean | null;
  detail?: string;
  tone?: "neutral" | "good" | "warn" | "danger";
}

const toneColors = {
  neutral: "#38bdf8",
  good: "#22c55e",
  warn: "#facc15",
  danger: "#fb7185",
};

export function StatusCard({ label, value, detail, tone = "neutral" }: StatusCardProps) {
  const displayValue =
    typeof value === "boolean" ? (value ? "true" : "false") : value ?? "unavailable";

  return (
    <View style={styles.card}>
      <Text style={styles.label}>{label}</Text>
      <Text style={[styles.value, { color: toneColors[tone] }]}>{displayValue}</Text>
      {detail ? <Text style={styles.detail}>{detail}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flex: 1,
    minWidth: 142,
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    padding: 14,
  },
  label: {
    color: "#94a3b8",
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 8,
    textTransform: "uppercase",
  },
  value: {
    fontSize: 20,
    fontWeight: "900",
  },
  detail: {
    color: "#cbd5e1",
    fontSize: 12,
    lineHeight: 18,
    marginTop: 8,
  },
});

import React, { useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { SafetyNotice } from "../components/SafetyNotice";

interface OnboardingSafetyScreenProps {
  onAcknowledge: () => void;
}

export function OnboardingSafetyScreen({ onAcknowledge }: OnboardingSafetyScreenProps) {
  const [acknowledged, setAcknowledged] = useState(false);

  return (
    <View style={styles.container}>
      <Text style={styles.kicker}>Abraxas GhostEye</Text>
      <Text style={styles.title}>Authorized demonstration mode</Text>
      <Text style={styles.copy}>
        This mobile console connects to a GhostEye backend on your trusted LAN. It does not
        read raw phone WiFi CSI and does not provide validated operational intelligence.
      </Text>

      <SafetyNotice />

      <Pressable
        accessibilityRole="checkbox"
        accessibilityState={{ checked: acknowledged }}
        onPress={() => setAcknowledged((current) => !current)}
        style={styles.ackRow}
      >
        <View style={[styles.checkbox, acknowledged && styles.checkboxChecked]}>
          {acknowledged ? <Text style={styles.checkmark}>OK</Text> : null}
        </View>
        <Text style={styles.ackText}>
          I acknowledge this safety boundary and will use GhostEye only in authorized,
          consent-based, controlled environments.
        </Text>
      </Pressable>

      <Pressable
        disabled={!acknowledged}
        onPress={onAcknowledge}
        style={({ pressed }) => [
          styles.primaryButton,
          !acknowledged && styles.primaryButtonDisabled,
          pressed && acknowledged && styles.primaryButtonPressed,
        ]}
      >
        <Text style={styles.primaryButtonText}>Continue</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 18,
  },
  kicker: {
    color: "#38bdf8",
    fontSize: 13,
    fontWeight: "900",
    letterSpacing: 1.8,
    textTransform: "uppercase",
  },
  title: {
    color: "#f8fafc",
    fontSize: 34,
    fontWeight: "900",
    lineHeight: 40,
  },
  copy: {
    color: "#cbd5e1",
    fontSize: 15,
    lineHeight: 23,
  },
  ackRow: {
    alignItems: "flex-start",
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    flexDirection: "row",
    gap: 12,
    padding: 14,
  },
  checkbox: {
    alignItems: "center",
    borderColor: "#64748b",
    borderRadius: 8,
    borderWidth: 2,
    height: 26,
    justifyContent: "center",
    width: 26,
  },
  checkboxChecked: {
    backgroundColor: "#22c55e",
    borderColor: "#22c55e",
  },
  checkmark: {
    color: "#052e16",
    fontSize: 18,
    fontWeight: "900",
  },
  ackText: {
    color: "#e5e7eb",
    flex: 1,
    fontSize: 14,
    lineHeight: 21,
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 16,
    paddingVertical: 16,
  },
  primaryButtonDisabled: {
    backgroundColor: "#334155",
  },
  primaryButtonPressed: {
    opacity: 0.78,
  },
  primaryButtonText: {
    color: "#03130a",
    fontSize: 16,
    fontWeight: "900",
  },
});

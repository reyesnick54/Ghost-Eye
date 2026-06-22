import React, { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { SafetyNotice } from "../components/SafetyNotice";

interface SettingsScreenProps {
  backendUrl: string;
  refreshIntervalMs: number;
  onBackendUrlChange: (url: string) => void;
  onRefreshIntervalChange: (milliseconds: number) => void;
}

export function SettingsScreen({
  backendUrl,
  refreshIntervalMs,
  onBackendUrlChange,
  onRefreshIntervalChange,
}: SettingsScreenProps) {
  const [intervalSeconds, setIntervalSeconds] = useState(String(refreshIntervalMs / 1000));
  const [diagnosticsEnabled, setDiagnosticsEnabled] = useState(false);

  function handleIntervalChange(value: string) {
    setIntervalSeconds(value);
    const parsed = Number(value);
    if (Number.isFinite(parsed) && parsed >= 1) {
      onRefreshIntervalChange(Math.round(parsed * 1000));
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Settings / diagnostics</Text>
        <Text style={styles.title}>Mobile console configuration</Text>
        <Text style={styles.copy}>
          Settings are held in local React state for this v0.1 scaffold. Restarting the app
          resets them to defaults.
        </Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>Backend URL</Text>
        <TextInput
          autoCapitalize="none"
          autoCorrect={false}
          keyboardType="url"
          onChangeText={onBackendUrlChange}
          placeholder="http://localhost:8000"
          placeholderTextColor="#64748b"
          style={styles.input}
          value={backendUrl}
        />
        <Text style={styles.helper}>Physical devices usually need a LAN URL such as http://192.168.1.100:8000.</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>Scan refresh interval</Text>
        <TextInput
          keyboardType="numeric"
          onChangeText={handleIntervalChange}
          placeholder="2"
          placeholderTextColor="#64748b"
          style={styles.input}
          value={intervalSeconds}
        />
        <Text style={styles.helper}>Seconds between dashboard `/scan` polls. Minimum accepted value is 1 second.</Text>
      </View>

      <View style={styles.card}>
        <View style={styles.toggleRow}>
          <View style={styles.toggleCopy}>
            <Text style={styles.label}>Developer diagnostics</Text>
            <Text style={styles.helper}>
              Placeholder toggle for future request logs, payload inspection, and backend timing.
            </Text>
          </View>
          <Pressable
            accessibilityRole="switch"
            accessibilityState={{ checked: diagnosticsEnabled }}
            onPress={() => setDiagnosticsEnabled((enabled) => !enabled)}
            style={[styles.switchTrack, diagnosticsEnabled && styles.switchTrackEnabled]}
          >
            <View style={[styles.switchThumb, diagnosticsEnabled && styles.switchThumbEnabled]} />
          </Pressable>
        </View>
        <Text style={styles.diagnosticsState}>
          Diagnostics placeholder: {diagnosticsEnabled ? "enabled" : "disabled"}
        </Text>
      </View>

      <SafetyNotice compact />
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
  card: {
    borderColor: "#1f3b4d",
    borderRadius: 18,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    gap: 10,
    padding: 14,
  },
  label: {
    color: "#94a3b8",
    fontSize: 12,
    fontWeight: "900",
    letterSpacing: 0.8,
    textTransform: "uppercase",
  },
  input: {
    borderColor: "#334155",
    borderRadius: 14,
    borderWidth: 1,
    color: "#f8fafc",
    fontSize: 16,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
  helper: {
    color: "#93c5fd",
    fontSize: 12,
    lineHeight: 18,
  },
  toggleRow: {
    alignItems: "center",
    flexDirection: "row",
    gap: 14,
    justifyContent: "space-between",
  },
  toggleCopy: {
    flex: 1,
    gap: 8,
  },
  switchTrack: {
    borderRadius: 999,
    backgroundColor: "#334155",
    height: 34,
    justifyContent: "center",
    paddingHorizontal: 4,
    width: 62,
  },
  switchTrackEnabled: {
    backgroundColor: "#166534",
  },
  switchThumb: {
    borderRadius: 999,
    backgroundColor: "#cbd5e1",
    height: 26,
    width: 26,
  },
  switchThumbEnabled: {
    alignSelf: "flex-end",
    backgroundColor: "#bbf7d0",
  },
  diagnosticsState: {
    color: "#cbd5e1",
    fontSize: 13,
  },
});

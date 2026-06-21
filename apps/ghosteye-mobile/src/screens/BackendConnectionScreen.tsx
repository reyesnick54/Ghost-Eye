import React, { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { getHealth } from "../api/ghosteyeClient";
import { StatusCard } from "../components/StatusCard";
import { ConnectionState, HealthResponse } from "../types/telemetry";

interface BackendConnectionScreenProps {
  backendUrl: string;
  connectionState: ConnectionState;
  onBackendUrlChange: (url: string) => void;
  onConnectionStateChange: (state: ConnectionState) => void;
}

export function BackendConnectionScreen({
  backendUrl,
  connectionState,
  onBackendUrlChange,
  onConnectionStateChange,
}: BackendConnectionScreenProps) {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleTestConnection() {
    setError(null);
    setHealth(null);
    onConnectionStateChange("checking");

    try {
      const payload = await getHealth(backendUrl);
      setHealth(payload);
      onConnectionStateChange(payload.status === "ok" ? "connected" : "disconnected");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to reach backend.");
      onConnectionStateChange("disconnected");
    }
  }

  const connected = connectionState === "connected";

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Backend link</Text>
        <Text style={styles.title}>Connect over LAN</Text>
        <Text style={styles.copy}>
          Enter the FastAPI backend URL. Use localhost for an emulator or a LAN IP address
          for a physical device.
        </Text>
      </View>

      <View style={styles.formCard}>
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
        <Text style={styles.helper}>Common LAN example: http://192.168.1.100:8000</Text>
        <Pressable
          disabled={connectionState === "checking"}
          onPress={handleTestConnection}
          style={({ pressed }) => [
            styles.primaryButton,
            connectionState === "checking" && styles.primaryButtonDisabled,
            pressed && styles.primaryButtonPressed,
          ]}
        >
          <Text style={styles.primaryButtonText}>
            {connectionState === "checking" ? "Testing /health..." : "Test connection"}
          </Text>
        </Pressable>
      </View>

      <View style={styles.statusGrid}>
        <StatusCard
          label="Status"
          tone={connected ? "good" : connectionState === "checking" ? "warn" : "danger"}
          value={connectionState}
        />
        <StatusCard label="Mode" value={health?.mode ?? "unknown"} />
      </View>

      {health?.source ? (
        <StatusCard
          label="Selected source"
          value={health.source.id}
          detail={health.source.csi === false ? "CSI reported false by backend" : undefined}
          tone={health.source.csi === false ? "good" : "warn"}
        />
      ) : null}

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
  formCard: {
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
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#38bdf8",
    borderRadius: 14,
    marginTop: 4,
    paddingVertical: 14,
  },
  primaryButtonDisabled: {
    backgroundColor: "#334155",
  },
  primaryButtonPressed: {
    opacity: 0.78,
  },
  primaryButtonText: {
    color: "#031827",
    fontSize: 15,
    fontWeight: "900",
  },
  statusGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
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

import React, { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { setupRoom } from "../api/ghosteyeClient";
import { SafetyNotice } from "../components/SafetyNotice";
import { RoomSetupRequest, RoomSetupResponse } from "../types/telemetry";

interface RoomSetupScreenProps {
  backendUrl: string;
}

function parseNumber(value: string, fallback: number): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function parseZones(value: string): string[] {
  const zones = value
    .split(",")
    .map((zone) => zone.trim())
    .filter(Boolean);
  return zones.length ? zones : ["zone_a", "zone_b", "zone_c"];
}

export function RoomSetupScreen({ backendUrl }: RoomSetupScreenProps) {
  const [roomName, setRoomName] = useState("Demo Room");
  const [widthM, setWidthM] = useState("5.2");
  const [lengthM, setLengthM] = useState("4.1");
  const [shape, setShape] = useState("rectangle");
  const [zones, setZones] = useState("zone_a, zone_b, zone_c");
  const [routerX, setRouterX] = useState("0.5");
  const [routerY, setRouterY] = useState("2.0");
  const [result, setResult] = useState<RoomSetupResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    const request: RoomSetupRequest = {
      room_name: roomName.trim() || "Demo Room",
      width_m: parseNumber(widthM, 5.2),
      length_m: parseNumber(lengthM, 4.1),
      shape: shape.trim() || "rectangle",
      zones: parseZones(zones),
      router_location: {
        x_m: parseNumber(routerX, 0.5),
        y_m: parseNumber(routerY, 2.0),
      },
    };

    setLoading(true);
    setError(null);
    try {
      setResult(await setupRoom(backendUrl, request));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to configure room.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Room setup</Text>
        <Text style={styles.title}>Manual dimensions and zones</Text>
        <Text style={styles.copy}>
          Define the controlled room, zones, and router/access point position used by backend
          mapping. WiFi-only mode estimates coarse probabilistic zones, not true RF imaging.
        </Text>
      </View>

      <SafetyNotice compact />

      <View style={styles.formCard}>
        <Text style={styles.label}>Room name</Text>
        <TextInput
          onChangeText={setRoomName}
          placeholder="Demo Room"
          placeholderTextColor="#64748b"
          style={styles.input}
          value={roomName}
        />

        <View style={styles.fieldRow}>
          <View style={styles.fieldHalf}>
            <Text style={styles.label}>Width (m)</Text>
            <TextInput
              keyboardType="decimal-pad"
              onChangeText={setWidthM}
              placeholder="5.2"
              placeholderTextColor="#64748b"
              style={styles.input}
              value={widthM}
            />
          </View>
          <View style={styles.fieldHalf}>
            <Text style={styles.label}>Length (m)</Text>
            <TextInput
              keyboardType="decimal-pad"
              onChangeText={setLengthM}
              placeholder="4.1"
              placeholderTextColor="#64748b"
              style={styles.input}
              value={lengthM}
            />
          </View>
        </View>

        <Text style={styles.label}>Shape</Text>
        <TextInput
          autoCapitalize="none"
          onChangeText={setShape}
          placeholder="rectangle"
          placeholderTextColor="#64748b"
          style={styles.input}
          value={shape}
        />

        <Text style={styles.label}>Zones</Text>
        <TextInput
          autoCapitalize="none"
          onChangeText={setZones}
          placeholder="zone_a, zone_b, zone_c"
          placeholderTextColor="#64748b"
          style={styles.input}
          value={zones}
        />
        <Text style={styles.helper}>Use comma-separated zone IDs.</Text>

        <View style={styles.fieldRow}>
          <View style={styles.fieldHalf}>
            <Text style={styles.label}>Router X (m)</Text>
            <TextInput
              keyboardType="decimal-pad"
              onChangeText={setRouterX}
              placeholder="0.5"
              placeholderTextColor="#64748b"
              style={styles.input}
              value={routerX}
            />
          </View>
          <View style={styles.fieldHalf}>
            <Text style={styles.label}>Router Y (m)</Text>
            <TextInput
              keyboardType="decimal-pad"
              onChangeText={setRouterY}
              placeholder="2.0"
              placeholderTextColor="#64748b"
              style={styles.input}
              value={routerY}
            />
          </View>
        </View>

        <Pressable
          disabled={loading}
          onPress={handleSubmit}
          style={({ pressed }) => [
            styles.primaryButton,
            loading && styles.buttonDisabled,
            pressed && styles.buttonPressed,
          ]}
        >
          <Text style={styles.primaryButtonText}>
            {loading ? "Configuring room..." : "Save Room Setup"}
          </Text>
        </Pressable>
      </View>

      {result ? (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>Room configured</Text>
          <Text style={styles.resultText}>room_id: {result.room_id ?? "unknown"}</Text>
          <Text style={styles.resultText}>status: {result.status ?? "unknown"}</Text>
          <Text style={styles.resultText}>map_mode: {result.map_mode ?? "unknown"}</Text>
          {result.limitations ? <Text style={styles.resultText}>{result.limitations}</Text> : null}
        </View>
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
  fieldRow: {
    flexDirection: "row",
    gap: 10,
  },
  fieldHalf: {
    flex: 1,
    gap: 8,
  },
  helper: {
    color: "#93c5fd",
    fontSize: 12,
    lineHeight: 18,
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 14,
    marginTop: 4,
    paddingVertical: 14,
  },
  primaryButtonText: {
    color: "#03130a",
    fontSize: 14,
    fontWeight: "900",
  },
  buttonDisabled: {
    opacity: 0.55,
  },
  buttonPressed: {
    opacity: 0.75,
  },
  resultCard: {
    borderColor: "#22c55e",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#082f25",
    gap: 8,
    padding: 14,
  },
  resultTitle: {
    color: "#bbf7d0",
    fontSize: 16,
    fontWeight: "900",
  },
  resultText: {
    color: "#e5e7eb",
    fontSize: 13,
    lineHeight: 19,
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

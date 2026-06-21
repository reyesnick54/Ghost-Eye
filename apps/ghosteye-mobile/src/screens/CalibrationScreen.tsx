import React, { useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { calibrateZone, runEmptyRoomCalibration } from "../api/ghosteyeClient";
import { SafetyNotice } from "../components/SafetyNotice";
import { CalibrationResult, ZoneId } from "../types/telemetry";

const ZONES: ZoneId[] = ["zone_a", "zone_b", "zone_c"];

interface CalibrationScreenProps {
  backendUrl: string;
}

export function CalibrationScreen({ backendUrl }: CalibrationScreenProps) {
  const [result, setResult] = useState<CalibrationResult | null>(null);
  const [loadingLabel, setLoadingLabel] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function runCalibration(label: string, action: () => Promise<CalibrationResult>) {
    setLoadingLabel(label);
    setError(null);
    setResult(null);

    try {
      const payload = await action();
      setResult(payload);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Calibration failed.");
    } finally {
      setLoadingLabel(null);
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Calibration</Text>
        <Text style={styles.title}>Room baseline and zones</Text>
        <Text style={styles.copy}>
          Calibrations are submitted to the backend. Keep the room controlled and consent-based
          before recording empty-room or zone fingerprints.
        </Text>
      </View>

      <SafetyNotice compact />

      <Pressable
        disabled={Boolean(loadingLabel)}
        onPress={() =>
          runCalibration("empty-room", () => runEmptyRoomCalibration(backendUrl))
        }
        style={({ pressed }) => [
          styles.primaryButton,
          loadingLabel === "empty-room" && styles.buttonDisabled,
          pressed && styles.buttonPressed,
        ]}
      >
        <Text style={styles.primaryButtonText}>
          {loadingLabel === "empty-room" ? "Running Empty Room Calibration..." : "Run Empty Room Calibration"}
        </Text>
      </Pressable>

      <View style={styles.zonePanel}>
        <Text style={styles.panelTitle}>Zone calibration</Text>
        <Text style={styles.panelCopy}>
          Capture one backend observation for the selected zone fingerprint.
        </Text>
        <View style={styles.zoneButtons}>
          {ZONES.map((zone) => (
            <Pressable
              disabled={Boolean(loadingLabel)}
              key={zone}
              onPress={() => runCalibration(zone, () => calibrateZone(backendUrl, zone))}
              style={({ pressed }) => [
                styles.zoneButton,
                loadingLabel === zone && styles.buttonDisabled,
                pressed && styles.buttonPressed,
              ]}
            >
              <Text style={styles.zoneButtonText}>
                {loadingLabel === zone ? `Calibrating ${zone}...` : `Calibrate ${zone}`}
              </Text>
            </Pressable>
          ))}
        </View>
      </View>

      {error ? <Text style={styles.error}>{error}</Text> : null}
      {result ? (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>Calibration result</Text>
          <Text style={styles.resultText}>{JSON.stringify(result, null, 2)}</Text>
        </View>
      ) : null}
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
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 16,
    paddingVertical: 16,
  },
  primaryButtonText: {
    color: "#03130a",
    fontSize: 15,
    fontWeight: "900",
  },
  buttonDisabled: {
    opacity: 0.55,
  },
  buttonPressed: {
    opacity: 0.75,
  },
  zonePanel: {
    borderColor: "#1f3b4d",
    borderRadius: 18,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    gap: 12,
    padding: 14,
  },
  panelTitle: {
    color: "#f8fafc",
    fontSize: 18,
    fontWeight: "900",
  },
  panelCopy: {
    color: "#cbd5e1",
    fontSize: 13,
    lineHeight: 19,
  },
  zoneButtons: {
    gap: 10,
  },
  zoneButton: {
    alignItems: "center",
    borderColor: "#38bdf8",
    borderRadius: 14,
    borderWidth: 1,
    paddingVertical: 13,
  },
  zoneButtonText: {
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
  resultCard: {
    borderColor: "#334155",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#020617",
    gap: 10,
    padding: 14,
  },
  resultTitle: {
    color: "#f8fafc",
    fontSize: 16,
    fontWeight: "900",
  },
  resultText: {
    color: "#cbd5e1",
    fontFamily: "monospace",
    fontSize: 12,
    lineHeight: 18,
  },
});

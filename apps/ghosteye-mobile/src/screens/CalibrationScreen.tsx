import React, { useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { SafetyNotice } from "../components/SafetyNotice";
import { StatusCard } from "../components/StatusCard";
import { uploadMobileWifiObservation } from "../services/telemetryUploader";
import {
  CALIBRATION_WORKFLOW,
  CalibrationObservationState,
  CalibrationPhase,
} from "../types/calibration";
import { MobileWifiObservation, SelectedNetworkObservation, ZoneId } from "../types/telemetry";

const ZONES: ZoneId[] = ["zone_a", "zone_b", "zone_c"];

interface CalibrationScreenProps {
  backendUrl: string;
  selectedNetwork: SelectedNetworkObservation | null;
  routerProbeHost?: string | null;
  teamId?: string | null;
}

function phaseLabel(phase?: CalibrationPhase): string {
  return CALIBRATION_WORKFLOW.find((step) => step.phase === phase)?.label ?? "Idle";
}

export function CalibrationScreen({
  backendUrl,
  selectedNetwork,
  routerProbeHost,
  teamId,
}: CalibrationScreenProps) {
  const [calibrationState, setCalibrationState] = useState<CalibrationObservationState>({ phase: "idle" });
  const [latestObservation, setLatestObservation] = useState<MobileWifiObservation | null>(null);
  const [selectedZone, setSelectedZone] = useState<ZoneId>("zone_a");
  const [sampleCount, setSampleCount] = useState(0);
  const [loadingPhase, setLoadingPhase] = useState<CalibrationPhase | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function captureCalibrationPhase(phase: CalibrationPhase, zoneId?: ZoneId) {
    if (!selectedNetwork?.owned_authorized_confirmed) {
      setError("Select and authorize an owned test router before calibration.");
      return;
    }

    const nextSampleCount =
      phase === "empty_room_sample" || phase === "zone_sample" ? sampleCount + 1 : sampleCount;
    const now = new Date().toISOString();
    const state: CalibrationObservationState = {
      phase,
      zone_id: phase.startsWith("zone") ? zoneId ?? selectedZone : null,
      sample_index: nextSampleCount,
      sample_count: nextSampleCount,
      started_at: phase.endsWith("_start") ? now : calibrationState.started_at,
      completed_at: phase.endsWith("_complete") ? now : undefined,
      notes: "Mobile WiFi-only non-CSI calibration observation.",
    };

    setLoadingPhase(phase);
    setError(null);
    try {
      const result = await uploadMobileWifiObservation({
        cloudUrl: backendUrl,
        teamId,
        selectedNetwork,
        routerProbeHost,
        calibration: state,
        uploadReason: `calibration_${phase}`,
      });
      setCalibrationState(state);
      setLatestObservation(result.observation);
      setSampleCount(nextSampleCount);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Calibration upload failed.");
    } finally {
      setLoadingPhase(null);
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Calibration</Text>
        <Text style={styles.title}>Empty-room and zone workflow</Text>
        <Text style={styles.copy}>
          Capture calibration observations from the mobile WiFi/network/motion layer and send
          them to GhostEye Cloud. These samples remain probabilistic and non-CSI.
        </Text>
      </View>

      <SafetyNotice compact />

      <View style={styles.statusGrid}>
        <StatusCard label="Current phase" value={phaseLabel(calibrationState.phase)} />
        <StatusCard label="Samples" value={sampleCount} />
        <StatusCard label="Router" value={selectedNetwork?.ssid ?? "not selected"} />
        <StatusCard label="Zone" value={selectedZone} />
      </View>

      {!selectedNetwork?.owned_authorized_confirmed ? (
        <Text style={styles.warning}>Select an owned authorized router before calibration.</Text>
      ) : null}

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Empty-room baseline</Text>
        <Text style={styles.panelCopy}>
          Start with the room empty, capture one or more baseline samples, then complete the
          baseline phase.
        </Text>
        <WorkflowButton
          disabled={Boolean(loadingPhase)}
          label="empty_room_start"
          loadingPhase={loadingPhase}
          onPress={() => captureCalibrationPhase("empty_room_start")}
        />
        <WorkflowButton
          disabled={Boolean(loadingPhase)}
          label="empty_room_sample"
          loadingPhase={loadingPhase}
          onPress={() => captureCalibrationPhase("empty_room_sample")}
        />
        <WorkflowButton
          disabled={Boolean(loadingPhase)}
          label="empty_room_complete"
          loadingPhase={loadingPhase}
          onPress={() => captureCalibrationPhase("empty_room_complete")}
        />
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Zone fingerprint</Text>
        <Text style={styles.panelCopy}>
          Select a coarse zone, capture authorized test samples, and complete the zone phase.
        </Text>
        <View style={styles.zoneButtons}>
          {ZONES.map((zone) => (
            <Pressable
              key={zone}
              onPress={() => setSelectedZone(zone)}
              style={[styles.zoneButton, selectedZone === zone && styles.zoneButtonActive]}
            >
              <Text style={[styles.zoneButtonText, selectedZone === zone && styles.zoneButtonTextActive]}>
                {zone}
              </Text>
            </Pressable>
          ))}
        </View>
        <WorkflowButton
          disabled={Boolean(loadingPhase)}
          label="zone_start"
          loadingPhase={loadingPhase}
          onPress={() => captureCalibrationPhase("zone_start", selectedZone)}
        />
        <WorkflowButton
          disabled={Boolean(loadingPhase)}
          label="zone_sample"
          loadingPhase={loadingPhase}
          onPress={() => captureCalibrationPhase("zone_sample", selectedZone)}
        />
        <WorkflowButton
          disabled={Boolean(loadingPhase)}
          label="zone_complete"
          loadingPhase={loadingPhase}
          onPress={() => captureCalibrationPhase("zone_complete", selectedZone)}
        />
      </View>

      {error ? <Text style={styles.error}>{error}</Text> : null}
      {latestObservation ? (
        <View style={styles.resultCard}>
          <Text style={styles.panelTitle}>Latest calibration observation</Text>
          <Text style={styles.resultText}>{JSON.stringify(latestObservation.calibration, null, 2)}</Text>
        </View>
      ) : null}
    </View>
  );
}

interface WorkflowButtonProps {
  label: CalibrationPhase;
  loadingPhase: CalibrationPhase | null;
  disabled: boolean;
  onPress: () => void;
}

function WorkflowButton({ label, loadingPhase, disabled, onPress }: WorkflowButtonProps) {
  const loading = loadingPhase === label;
  return (
    <Pressable
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.workflowButton,
        disabled && styles.buttonDisabled,
        pressed && styles.buttonPressed,
      ]}
    >
      <Text style={styles.workflowButtonText}>{loading ? `Uploading ${label}...` : label}</Text>
    </Pressable>
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
  panel: {
    backgroundColor: "#0f172a",
    borderColor: "#1f3b4d",
    borderRadius: 18,
    borderWidth: 1,
    gap: 12,
    padding: 14,
  },
  panelTitle: {
    color: "#f8fafc",
    fontSize: 17,
    fontWeight: "900",
  },
  panelCopy: {
    color: "#cbd5e1",
    fontSize: 13,
    lineHeight: 19,
  },
  workflowButton: {
    alignItems: "center",
    borderColor: "#38bdf8",
    borderRadius: 14,
    borderWidth: 1,
    paddingVertical: 13,
  },
  workflowButtonText: {
    color: "#bae6fd",
    fontSize: 14,
    fontWeight: "900",
  },
  zoneButtons: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  zoneButton: {
    borderColor: "#334155",
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  zoneButtonActive: {
    backgroundColor: "#22c55e",
    borderColor: "#86efac",
  },
  zoneButtonText: {
    color: "#cbd5e1",
    fontSize: 12,
    fontWeight: "900",
  },
  zoneButtonTextActive: {
    color: "#03130a",
  },
  buttonDisabled: {
    opacity: 0.55,
  },
  buttonPressed: {
    opacity: 0.75,
  },
  warning: {
    backgroundColor: "#2a2308",
    borderColor: "#854d0e",
    borderRadius: 14,
    borderWidth: 1,
    color: "#fde68a",
    fontSize: 13,
    lineHeight: 19,
    padding: 12,
  },
  error: {
    backgroundColor: "#2a0b12",
    borderColor: "#7f1d1d",
    borderRadius: 14,
    borderWidth: 1,
    color: "#fecdd3",
    fontSize: 13,
    lineHeight: 19,
    padding: 12,
  },
  resultCard: {
    backgroundColor: "#020617",
    borderColor: "#334155",
    borderRadius: 16,
    borderWidth: 1,
    gap: 10,
    padding: 14,
  },
  resultText: {
    color: "#cbd5e1",
    fontFamily: "monospace",
    fontSize: 12,
    lineHeight: 18,
  },
});

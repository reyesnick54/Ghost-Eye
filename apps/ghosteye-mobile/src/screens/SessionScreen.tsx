import React, { useCallback, useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { getLatestSession, startSession, stopSession } from "../api/ghosteyeClient";
import { StatusCard } from "../components/StatusCard";
import { SessionState } from "../types/telemetry";

interface SessionScreenProps {
  backendUrl: string;
}

export function SessionScreen({ backendUrl }: SessionScreenProps) {
  const [session, setSession] = useState<SessionState | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [loadingAction, setLoadingAction] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadLatestSession = useCallback(async () => {
    setError(null);
    try {
      const payload = await getLatestSession(backendUrl);
      setSession(payload.session ?? null);
      setNotice(payload.notice ?? null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load session.");
    }
  }, [backendUrl]);

  useEffect(() => {
    void loadLatestSession();
  }, [loadLatestSession]);

  async function runSessionAction(actionLabel: "start" | "stop") {
    setLoadingAction(actionLabel);
    setError(null);
    try {
      const payload = actionLabel === "start" ? await startSession(backendUrl) : await stopSession(backendUrl);
      setSession(payload.session ?? null);
      setNotice(payload.notice ?? null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : `Unable to ${actionLabel} session.`);
    } finally {
      setLoadingAction(null);
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Session logs</Text>
        <Text style={styles.title}>Capture and review scan sessions</Text>
        <Text style={styles.copy}>
          Start and stop backend sessions while the live scanner appends probabilistic
          WiFi-only non-CSI observations.
        </Text>
      </View>

      <View style={styles.buttonRow}>
        <Pressable
          disabled={Boolean(loadingAction)}
          onPress={() => runSessionAction("start")}
          style={({ pressed }) => [
            styles.primaryButton,
            loadingAction === "start" && styles.buttonDisabled,
            pressed && styles.buttonPressed,
          ]}
        >
          <Text style={styles.primaryButtonText}>
            {loadingAction === "start" ? "Starting..." : "Start Session"}
          </Text>
        </Pressable>
        <Pressable
          disabled={Boolean(loadingAction)}
          onPress={() => runSessionAction("stop")}
          style={({ pressed }) => [
            styles.stopButton,
            loadingAction === "stop" && styles.buttonDisabled,
            pressed && styles.buttonPressed,
          ]}
        >
          <Text style={styles.stopButtonText}>
            {loadingAction === "stop" ? "Stopping..." : "Stop Session"}
          </Text>
        </Pressable>
      </View>

      <Pressable
        disabled={Boolean(loadingAction)}
        onPress={loadLatestSession}
        style={({ pressed }) => [styles.secondaryButton, pressed && styles.buttonPressed]}
      >
        <Text style={styles.secondaryButtonText}>Fetch latest session</Text>
      </Pressable>

      <View style={styles.statusGrid}>
        <StatusCard label="Session ID" value={session?.session_id ?? "none"} />
        <StatusCard
          label="Active"
          tone={session?.active ? "good" : "warn"}
          value={session?.active ?? false}
        />
        <StatusCard label="Scan count" value={session?.scan_count ?? 0} />
      </View>

      <View style={styles.detailCard}>
        <Text style={styles.detailTitle}>Timing</Text>
        <Text style={styles.detailText}>started_at: {session?.started_at ?? "none"}</Text>
        <Text style={styles.detailText}>stopped_at: {session?.stopped_at ?? "none"}</Text>
      </View>

      {session?.latest_scan ? (
        <View style={styles.detailCard}>
          <Text style={styles.detailTitle}>Latest scan summary</Text>
          <Text style={styles.detailText}>timestamp: {session.latest_scan.timestamp ?? "unknown"}</Text>
          <Text style={styles.detailText}>selected_wifi: {session.latest_scan.selected_network?.ssid ?? "none"}</Text>
          <Text style={styles.detailText}>presence: {session.latest_scan.presence ?? "unknown"}</Text>
          <Text style={styles.detailText}>zone: {session.latest_scan.zone ?? "unknown"}</Text>
          <Text style={styles.detailText}>confidence: {session.latest_scan.confidence ?? "unknown"}</Text>
          <Text style={styles.detailText}>ceiling: {session.latest_scan.confidence_ceiling ?? "unknown"}</Text>
        </View>
      ) : null}

      {notice ? <Text style={styles.notice}>{notice}</Text> : null}
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
  buttonRow: {
    flexDirection: "row",
    gap: 10,
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 14,
    flex: 1,
    paddingVertical: 14,
  },
  primaryButtonText: {
    color: "#03130a",
    fontSize: 14,
    fontWeight: "900",
  },
  stopButton: {
    alignItems: "center",
    backgroundColor: "#fb7185",
    borderRadius: 14,
    flex: 1,
    paddingVertical: 14,
  },
  stopButtonText: {
    color: "#2a0b12",
    fontSize: 14,
    fontWeight: "900",
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
  statusGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  detailCard: {
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    gap: 8,
    padding: 14,
  },
  detailTitle: {
    color: "#f8fafc",
    fontSize: 16,
    fontWeight: "900",
  },
  detailText: {
    color: "#cbd5e1",
    fontSize: 13,
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

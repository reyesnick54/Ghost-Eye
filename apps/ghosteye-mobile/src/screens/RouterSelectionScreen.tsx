import React, { useCallback, useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { SafetyNotice } from "../components/SafetyNotice";
import { StatusCard } from "../components/StatusCard";
import {
  confidenceCeilingForCapability,
  getCurrentWifi,
  inferRouterVendorHint,
  scanNearbyWifi,
} from "../native/WifiCollector";
import {
  SelectedNetworkObservation,
  WifiCurrentObservation,
  WifiScanObservation,
} from "../types/telemetry";

interface RouterSelectionScreenProps {
  selectedNetwork: SelectedNetworkObservation | null;
  onSelectedNetworkChange: (network: SelectedNetworkObservation | null) => void;
}

function vendorLabel(value?: string): string {
  if (value === "netgear") {
    return "NetGear";
  }
  if (value === "tp_link") {
    return "TP-Link";
  }
  return "unknown";
}

function formatPercent(value?: number): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "unavailable";
  }
  return `${Math.round(value * 100)}%`;
}

export function RouterSelectionScreen({
  selectedNetwork,
  onSelectedNetworkChange,
}: RouterSelectionScreenProps) {
  const [currentWifi, setCurrentWifi] = useState<WifiCurrentObservation | null>(null);
  const [scan, setScan] = useState<WifiScanObservation | null>(null);
  const [authorized, setAuthorized] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadWifi = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const current = await getCurrentWifi();
      const vendorHint = inferRouterVendorHint(current.ssid, current.bssid_masked);
      const candidate = current.ssid
        ? {
            ssid: current.ssid,
            bssid_masked: current.bssid_masked,
            vendor_hint: vendorHint,
            owned_authorized_confirmed: authorized,
            confidence_ceiling: confidenceCeilingForCapability(current.capability_mode, vendorHint),
          }
        : selectedNetwork;
      setCurrentWifi(current);
      setScan(await scanNearbyWifi(candidate));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to inspect WiFi.");
    } finally {
      setLoading(false);
    }
  }, [authorized, selectedNetwork]);

  useEffect(() => {
    void loadWifi();
  }, [loadWifi]);

  const vendorHint = inferRouterVendorHint(currentWifi?.ssid, currentWifi?.bssid_masked);
  const confidenceCeiling = confidenceCeilingForCapability(
    currentWifi?.capability_mode ?? "native_unavailable",
    vendorHint,
  );

  function handleConfirmRouter() {
    if (!currentWifi?.ssid) {
      setError("Current SSID is unavailable; connect to the owned test router first.");
      return;
    }
    onSelectedNetworkChange({
      ssid: currentWifi.ssid,
      bssid_masked: currentWifi.bssid_masked,
      vendor_hint: vendorHint,
      owned_authorized_confirmed: true,
      confidence_ceiling: confidenceCeiling,
    });
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>Router selection</Text>
        <Text style={styles.title}>Confirm an owned authorized test router</Text>
        <Text style={styles.copy}>
          GhostEye Mobile v0.5 observes permitted WiFi/network metadata only. It does not access
          CSI and does not claim true RF imaging.
        </Text>
      </View>

      <SafetyNotice compact />

      <View style={styles.statusGrid}>
        <StatusCard label="Current SSID" value={currentWifi?.ssid ?? "unavailable"} />
        <StatusCard label="Vendor hint" value={vendorLabel(vendorHint)} />
        <StatusCard label="Capability mode" value={currentWifi?.capability_mode ?? "unknown"} />
        <StatusCard
          label="Confidence ceiling"
          value={formatPercent(confidenceCeiling)}
          detail="Maximum displayed confidence for mobile WiFi-only observations"
        />
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Authorization check</Text>
        <Text style={styles.cardCopy}>
          Confirm the current network is an owned NetGear, TP-Link, or otherwise authorized
          router in a controlled test environment.
        </Text>
        <Pressable
          accessibilityRole="checkbox"
          accessibilityState={{ checked: authorized }}
          onPress={() => setAuthorized((value) => !value)}
          style={[styles.checkRow, authorized && styles.checkRowActive]}
        >
          <Text style={styles.checkbox}>{authorized ? "✓" : ""}</Text>
          <Text style={styles.checkText}>I confirm this is an owned authorized test router.</Text>
        </Pressable>
        <Pressable
          disabled={!authorized || !currentWifi?.ssid}
          onPress={handleConfirmRouter}
          style={({ pressed }) => [
            styles.primaryButton,
            (!authorized || !currentWifi?.ssid) && styles.buttonDisabled,
            pressed && styles.buttonPressed,
          ]}
        >
          <Text style={styles.primaryButtonText}>Use current router for observations</Text>
        </Pressable>
      </View>

      {selectedNetwork ? (
        <View style={styles.selectedCard}>
          <Text style={styles.cardTitle}>Selected router</Text>
          <Text style={styles.meta}>SSID: {selectedNetwork.ssid}</Text>
          <Text style={styles.meta}>BSSID: {selectedNetwork.bssid_masked ?? "unavailable"}</Text>
          <Text style={styles.meta}>Vendor hint: {vendorLabel(selectedNetwork.vendor_hint)}</Text>
          <Text style={styles.meta}>Authorized: {selectedNetwork.owned_authorized_confirmed ? "yes" : "no"}</Text>
        </View>
      ) : null}

      <Pressable
        disabled={loading}
        onPress={loadWifi}
        style={({ pressed }) => [
          styles.secondaryButton,
          loading && styles.buttonDisabled,
          pressed && styles.buttonPressed,
        ]}
      >
        <Text style={styles.secondaryButtonText}>{loading ? "Refreshing..." : "Refresh WiFi observation"}</Text>
      </Pressable>

      {currentWifi?.warnings?.map((warning) => (
        <Text key={warning} style={styles.warning}>
          {warning}
        </Text>
      ))}
      {scan?.warnings?.map((warning) => (
        <Text key={warning} style={styles.warning}>
          {warning}
        </Text>
      ))}
      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Nearby APs</Text>
        <Text style={styles.cardCopy}>
          Visible AP count: {scan?.visible_access_points ?? 0}. Target router seen:{" "}
          {scan?.target_router_seen ? "yes" : "no"}.
        </Text>
        {(scan?.access_points ?? []).slice(0, 8).map((accessPoint) => (
          <View key={`${accessPoint.ssid}-${accessPoint.bssid_masked}`} style={styles.apRow}>
            <Text style={styles.apSsid}>{accessPoint.ssid ?? "hidden SSID"}</Text>
            <Text style={styles.meta}>
              {accessPoint.rssi_dbm ?? "?"} dBm | {accessPoint.frequency_mhz ?? "?"} MHz |{" "}
              {vendorLabel(accessPoint.vendor_hint)}
            </Text>
            <Text style={styles.meta}>BSSID: {accessPoint.bssid_masked ?? "unavailable"}</Text>
          </View>
        ))}
      </View>
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
  statusGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  card: {
    backgroundColor: "#0f172a",
    borderColor: "#1f3b4d",
    borderRadius: 18,
    borderWidth: 1,
    gap: 10,
    padding: 14,
  },
  selectedCard: {
    backgroundColor: "#082f25",
    borderColor: "#22c55e",
    borderRadius: 18,
    borderWidth: 1,
    gap: 8,
    padding: 14,
  },
  cardTitle: {
    color: "#f8fafc",
    fontSize: 17,
    fontWeight: "900",
  },
  cardCopy: {
    color: "#cbd5e1",
    fontSize: 13,
    lineHeight: 19,
  },
  checkRow: {
    alignItems: "center",
    borderColor: "#334155",
    borderRadius: 14,
    borderWidth: 1,
    flexDirection: "row",
    gap: 10,
    padding: 12,
  },
  checkRowActive: {
    borderColor: "#22c55e",
  },
  checkbox: {
    borderColor: "#64748b",
    borderRadius: 6,
    borderWidth: 1,
    color: "#bbf7d0",
    fontSize: 16,
    fontWeight: "900",
    height: 24,
    textAlign: "center",
    width: 24,
  },
  checkText: {
    color: "#e5e7eb",
    flex: 1,
    fontSize: 13,
    fontWeight: "800",
    lineHeight: 18,
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 14,
    paddingVertical: 13,
  },
  primaryButtonText: {
    color: "#03130a",
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
  meta: {
    color: "#cbd5e1",
    fontSize: 13,
  },
  apRow: {
    borderTopColor: "#1e293b",
    borderTopWidth: 1,
    gap: 5,
    paddingTop: 10,
  },
  apSsid: {
    color: "#e0f2fe",
    fontSize: 15,
    fontWeight: "900",
  },
});

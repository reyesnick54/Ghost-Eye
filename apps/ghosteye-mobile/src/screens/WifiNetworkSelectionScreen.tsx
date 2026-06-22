import React, { useCallback, useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { getWifiNetworks, selectWifiNetwork } from "../api/ghosteyeClient";
import { StatusCard } from "../components/StatusCard";
import {
  WifiNetworkEnvironment,
  WifiNetworksResponse,
  WifiSelectionResponse,
} from "../types/telemetry";

interface WifiNetworkSelectionScreenProps {
  backendUrl: string;
}

function vendorLabel(vendorHint?: string): string {
  if (vendorHint === "tp_link") {
    return "TP-Link";
  }
  if (vendorHint === "netgear") {
    return "NetGear";
  }
  return "unknown";
}

export function WifiNetworkSelectionScreen({ backendUrl }: WifiNetworkSelectionScreenProps) {
  const [payload, setPayload] = useState<WifiNetworksResponse | null>(null);
  const [selection, setSelection] = useState<WifiSelectionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectingSsid, setSelectingSsid] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadNetworks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setPayload(await getWifiNetworks(backendUrl));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load WiFi networks.");
    } finally {
      setLoading(false);
    }
  }, [backendUrl]);

  useEffect(() => {
    void loadNetworks();
  }, [loadNetworks]);

  async function handleSelect(network: WifiNetworkEnvironment) {
    setSelectingSsid(network.ssid);
    setError(null);
    try {
      setSelection(await selectWifiNetwork(backendUrl, network.ssid));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to select WiFi network.");
    } finally {
      setSelectingSsid(null);
    }
  }

  const networks = payload?.networks ?? [];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.kicker}>WiFi network selection</Text>
        <Text style={styles.title}>Choose a controlled WiFi environment</Text>
        <Text style={styles.copy}>
          This selector tells the backend which access point environment to model. It does
          not claim that ordinary phone WiFi APIs expose raw CSI.
        </Text>
      </View>

      <View style={styles.statusGrid}>
        <StatusCard label="Networks" value={networks.length} />
        <StatusCard
          label="Selected"
          tone={selection?.status === "selected" ? "good" : "warn"}
          value={selection?.selected_ssid ?? "none"}
          detail={selection?.notice}
        />
      </View>

      <Pressable
        disabled={loading}
        onPress={loadNetworks}
        style={({ pressed }) => [
          styles.secondaryButton,
          loading && styles.buttonDisabled,
          pressed && styles.buttonPressed,
        ]}
      >
        <Text style={styles.secondaryButtonText}>
          {loading ? "Refreshing networks..." : "Refresh WiFi networks"}
        </Text>
      </Pressable>

      {payload?.limitations ? <Text style={styles.limitations}>{payload.limitations}</Text> : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={styles.networkList}>
        {networks.length === 0 && !loading ? (
          <Text style={styles.empty}>No backend WiFi environments returned.</Text>
        ) : null}
        {networks.map((network) => {
          const selected = selection?.selected_ssid === network.ssid;
          const csiVerified = network.can_use_as_csi_sensor === true;
          return (
            <View key={`${network.ssid}-${network.bssid_masked}`} style={[styles.networkCard, selected && styles.networkSelected]}>
              <View style={styles.networkHeader}>
                <Text style={styles.ssid}>{network.ssid}</Text>
                <Text style={[styles.badge, selected && styles.badgeSelected]}>
                  {selected ? "selected" : "environment"}
                </Text>
              </View>
              <Text style={styles.networkMeta}>Signal: {network.signal_dbm} dBm on channel {network.channel}</Text>
              <Text style={styles.networkMeta}>Vendor hint: {vendorLabel(network.vendor_hint)}</Text>
              <Text style={styles.networkMeta}>BSSID: {network.bssid_masked}</Text>
              <Text style={styles.networkMeta}>Usable as environment only: yes</Text>
              <Text style={styles.networkMeta}>CSI capability verified: {csiVerified ? "yes" : "no"}</Text>
              {!csiVerified ? (
                <Text style={styles.warning}>CSI is not verified for this network. Use only for WiFi-only RSSI/latency demo analysis.</Text>
              ) : null}
              <Text style={styles.notes}>{network.notes}</Text>
              <Pressable
                disabled={Boolean(selectingSsid)}
                onPress={() => handleSelect(network)}
                style={({ pressed }) => [
                  styles.primaryButton,
                  selectingSsid === network.ssid && styles.buttonDisabled,
                  pressed && styles.buttonPressed,
                ]}
              >
                <Text style={styles.primaryButtonText}>
                  {selectingSsid === network.ssid ? "Selecting..." : "Select WiFi environment"}
                </Text>
              </Pressable>
            </View>
          );
        })}
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
  limitations: {
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
  networkList: {
    gap: 12,
  },
  empty: {
    color: "#94a3b8",
    fontSize: 14,
  },
  networkCard: {
    borderColor: "#1f3b4d",
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: "#0f172a",
    gap: 8,
    padding: 14,
  },
  networkSelected: {
    borderColor: "#22c55e",
    backgroundColor: "#082f25",
  },
  networkHeader: {
    alignItems: "flex-start",
    flexDirection: "row",
    gap: 8,
    justifyContent: "space-between",
  },
  ssid: {
    color: "#f8fafc",
    flex: 1,
    fontSize: 18,
    fontWeight: "900",
  },
  badge: {
    borderColor: "#334155",
    borderRadius: 999,
    borderWidth: 1,
    color: "#cbd5e1",
    fontSize: 11,
    fontWeight: "900",
    paddingHorizontal: 8,
    paddingVertical: 4,
    textTransform: "uppercase",
  },
  badgeSelected: {
    borderColor: "#22c55e",
    color: "#bbf7d0",
  },
  networkMeta: {
    color: "#cbd5e1",
    fontSize: 13,
  },
  warning: {
    color: "#facc15",
    fontSize: 13,
    fontWeight: "800",
    lineHeight: 19,
  },
  notes: {
    color: "#94a3b8",
    fontSize: 12,
    lineHeight: 18,
  },
  primaryButton: {
    alignItems: "center",
    backgroundColor: "#22c55e",
    borderRadius: 14,
    marginTop: 4,
    paddingVertical: 13,
  },
  primaryButtonText: {
    color: "#03130a",
    fontSize: 14,
    fontWeight: "900",
  },
});

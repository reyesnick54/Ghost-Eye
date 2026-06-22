import React, { useMemo, useState } from "react";
import {
  Pressable,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { BackendConnectionScreen } from "./src/screens/BackendConnectionScreen";
import { CalibrationScreen } from "./src/screens/CalibrationScreen";
import { LiveScanDashboard } from "./src/screens/LiveScanDashboard";
import { OnboardingSafetyScreen } from "./src/screens/OnboardingSafetyScreen";
import { RoomMapScreen } from "./src/screens/RoomMapScreen";
import { RoomSetupScreen } from "./src/screens/RoomSetupScreen";
import { SessionScreen } from "./src/screens/SessionScreen";
import { SettingsScreen } from "./src/screens/SettingsScreen";
import { SourceSelectionScreen } from "./src/screens/SourceSelectionScreen";
import { WifiNetworkSelectionScreen } from "./src/screens/WifiNetworkSelectionScreen";
import { ConnectionState } from "./src/types/telemetry";

type ScreenKey =
  | "connection"
  | "wifi"
  | "sources"
  | "roomSetup"
  | "calibration"
  | "dashboard"
  | "roomMap"
  | "session"
  | "settings";

interface ScreenDefinition {
  key: ScreenKey;
  label: string;
}

const DEFAULT_BACKEND_URL = "http://localhost:8000";
const DEFAULT_REFRESH_INTERVAL_MS = 2000;

const SCREENS: ScreenDefinition[] = [
  { key: "connection", label: "Connect" },
  { key: "wifi", label: "WiFi" },
  { key: "sources", label: "Adapters" },
  { key: "roomSetup", label: "Room" },
  { key: "calibration", label: "Calibrate" },
  { key: "dashboard", label: "Live" },
  { key: "roomMap", label: "Map" },
  { key: "session", label: "Logs" },
  { key: "settings", label: "Diagnostics" },
];

export default function App() {
  const [safetyAcknowledged, setSafetyAcknowledged] = useState(false);
  const [activeScreen, setActiveScreen] = useState<ScreenKey>("connection");
  const [backendUrl, setBackendUrl] = useState(DEFAULT_BACKEND_URL);
  const [connectionState, setConnectionState] = useState<ConnectionState>("idle");
  const [refreshIntervalMs, setRefreshIntervalMs] = useState(DEFAULT_REFRESH_INTERVAL_MS);

  const activeTitle = useMemo(
    () => SCREENS.find((screen) => screen.key === activeScreen)?.label ?? "GhostEye",
    [activeScreen],
  );

  function handleBackendUrlChange(url: string) {
    setBackendUrl(url);
    setConnectionState("idle");
  }

  function renderScreen() {
    switch (activeScreen) {
      case "connection":
        return (
          <BackendConnectionScreen
            backendUrl={backendUrl}
            connectionState={connectionState}
            onBackendUrlChange={handleBackendUrlChange}
            onConnectionStateChange={setConnectionState}
          />
        );
      case "wifi":
        return <WifiNetworkSelectionScreen backendUrl={backendUrl} />;
      case "sources":
        return <SourceSelectionScreen backendUrl={backendUrl} />;
      case "roomSetup":
        return <RoomSetupScreen backendUrl={backendUrl} />;
      case "calibration":
        return <CalibrationScreen backendUrl={backendUrl} />;
      case "dashboard":
        return (
          <LiveScanDashboard backendUrl={backendUrl} refreshIntervalMs={refreshIntervalMs} />
        );
      case "session":
        return <SessionScreen backendUrl={backendUrl} />;
      case "roomMap":
        return <RoomMapScreen backendUrl={backendUrl} />;
      case "settings":
        return (
          <SettingsScreen
            backendUrl={backendUrl}
            refreshIntervalMs={refreshIntervalMs}
            onBackendUrlChange={handleBackendUrlChange}
            onRefreshIntervalChange={setRefreshIntervalMs}
          />
        );
      default:
        return null;
    }
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" />
      <View style={styles.appShell}>
        <View style={styles.brandBar}>
          <View>
            <Text style={styles.brand}>ABRAXAS GHOSTEYE</Text>
            <Text style={styles.subtitle}>WiFi-only non-CSI mobile console</Text>
          </View>
          {safetyAcknowledged ? (
            <View
              style={[
                styles.connectionPill,
                connectionState === "connected" && styles.connectionPillConnected,
                connectionState === "disconnected" && styles.connectionPillDisconnected,
              ]}
            >
              <Text style={styles.connectionPillText}>{connectionState}</Text>
            </View>
          ) : null}
        </View>

        {!safetyAcknowledged ? (
          <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
            <OnboardingSafetyScreen
              onAcknowledge={() => {
                setSafetyAcknowledged(true);
                setActiveScreen("connection");
              }}
            />
          </ScrollView>
        ) : (
          <>
            <ScrollView
              horizontal
              contentContainerStyle={styles.tabContent}
              showsHorizontalScrollIndicator={false}
              style={styles.tabBar}
            >
              {SCREENS.map((screen) => {
                const selected = activeScreen === screen.key;
                return (
                  <Pressable
                    key={screen.key}
                    onPress={() => setActiveScreen(screen.key)}
                    style={[styles.tab, selected && styles.tabSelected]}
                  >
                    <Text style={[styles.tabText, selected && styles.tabTextSelected]}>
                      {screen.label}
                    </Text>
                  </Pressable>
                );
              })}
            </ScrollView>

            <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
              <View style={styles.screenHeader}>
                <Text style={styles.screenEyebrow}>Current screen</Text>
                <Text style={styles.screenTitle}>{activeTitle}</Text>
              </View>
              {renderScreen()}
            </ScrollView>
          </>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    backgroundColor: "#020617",
    flex: 1,
  },
  appShell: {
    backgroundColor: "#020617",
    flex: 1,
  },
  brandBar: {
    alignItems: "center",
    borderBottomColor: "#132033",
    borderBottomWidth: 1,
    flexDirection: "row",
    gap: 12,
    justifyContent: "space-between",
    paddingHorizontal: 18,
    paddingVertical: 14,
  },
  brand: {
    color: "#f8fafc",
    fontSize: 16,
    fontWeight: "900",
    letterSpacing: 1.4,
  },
  subtitle: {
    color: "#38bdf8",
    fontSize: 12,
    fontWeight: "700",
    marginTop: 3,
  },
  connectionPill: {
    borderColor: "#334155",
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 6,
  },
  connectionPillConnected: {
    borderColor: "#22c55e",
  },
  connectionPillDisconnected: {
    borderColor: "#fb7185",
  },
  connectionPillText: {
    color: "#e5e7eb",
    fontSize: 11,
    fontWeight: "900",
    textTransform: "uppercase",
  },
  tabBar: {
    borderBottomColor: "#132033",
    borderBottomWidth: 1,
    flexGrow: 0,
  },
  tabContent: {
    gap: 8,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  tab: {
    borderColor: "#1f3b4d",
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 14,
    paddingVertical: 9,
  },
  tabSelected: {
    backgroundColor: "#0ea5e9",
    borderColor: "#38bdf8",
  },
  tabText: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "900",
  },
  tabTextSelected: {
    color: "#031827",
  },
  content: {
    gap: 18,
    padding: 18,
    paddingBottom: 36,
  },
  screenHeader: {
    gap: 4,
  },
  screenEyebrow: {
    color: "#64748b",
    fontSize: 11,
    fontWeight: "900",
    letterSpacing: 1.2,
    textTransform: "uppercase",
  },
  screenTitle: {
    color: "#e0f2fe",
    fontSize: 22,
    fontWeight: "900",
  },
});

import statistics
import unittest

from ghost_eye.csi_adapters import (
    WIFI_ONLY_NON_CSI_MODE,
    WiFiOnlyAdapter,
    WiFiSignalObservation,
)


class WiFiOnlyAdapterTest(unittest.TestCase):
    def test_default_adapter_generates_wifi_only_observation(self) -> None:
        adapter = WiFiOnlyAdapter(seed=123, bssid_count=4, platform_name="test-platform")

        observation = adapter.get_observation()

        self.assertIsInstance(observation, WiFiSignalObservation)
        self.assertEqual(observation.mode, WIFI_ONLY_NON_CSI_MODE)
        self.assertEqual(observation.platform, "test-platform")
        self.assertEqual(observation.bssid_count, 4)
        self.assertEqual(len(observation.visible_access_points), 4)
        self.assertEqual(len(observation.rssi_vector), 4)
        self.assertEqual(observation.mean_rssi, round(statistics.fmean(observation.rssi_vector), 2))
        self.assertEqual(observation.rssi_std, round(statistics.pstdev(observation.rssi_vector), 2))
        self.assertGreaterEqual(observation.gateway_latency_ms, 1.0)
        self.assertGreaterEqual(observation.jitter_ms, 0.0)
        self.assertGreaterEqual(observation.packet_loss, 0.0)
        self.assertLessEqual(observation.packet_loss, 0.08)
        self.assertGreaterEqual(observation.scan_stability, 0.0)
        self.assertLessEqual(observation.scan_stability, 1.0)

    def test_scanner_callback_can_supply_observation_dict(self) -> None:
        def scanner():
            return {
                "timestamp": 123.0,
                "ssid": "LabWiFi",
                "bssid_count": 1,
                "visible_access_points": [
                    {"ssid": "LabWiFi", "bssid": "02:00:00:00:00:01", "channel": 6, "rssi": -51.0}
                ],
                "rssi_vector": [-51.0],
                "mean_rssi": -51.0,
                "rssi_std": 0.0,
                "gateway_latency_ms": 12.5,
                "jitter_ms": 1.2,
                "packet_loss": 0.0,
                "scan_stability": 0.99,
                "platform": "test-platform",
                "mode": WIFI_ONLY_NON_CSI_MODE,
            }

        adapter = WiFiOnlyAdapter(simulated=False, scanner=scanner)

        observation = adapter.get_observation()

        self.assertEqual(observation.ssid, "LabWiFi")
        self.assertEqual(observation.mode, WIFI_ONLY_NON_CSI_MODE)


if __name__ == "__main__":
    unittest.main()

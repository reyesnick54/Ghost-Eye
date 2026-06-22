import unittest

from ghost_eye.api.schemas import MODE_WIFI_ONLY_NON_CSI
from ghost_eye.backend.app import ROOM_SETUP_FILE, scan, select_wifi, session_latest, setup_room, wifi_networks


class BackendWiFiV02Test(unittest.TestCase):
    def test_scan_returns_wifi_only_non_csi_contract(self) -> None:
        payload = scan()
        for key in (
            "timestamp",
            "mode",
            "source",
            "presence",
            "motion_score",
            "zone",
            "confidence",
            "confidence_ceiling",
            "signal_quality",
            "map",
            "limitations",
            "notice",
        ):
            self.assertIn(key, payload)
        self.assertEqual(payload["mode"], MODE_WIFI_ONLY_NON_CSI)
        self.assertLessEqual(payload["confidence"], payload["confidence_ceiling"])
        self.assertLessEqual(payload["confidence_ceiling"], 0.65)
        self.assertIn("device_motion", payload)
        self.assertEqual(payload["device_motion"]["state"], "stable")

    def test_session_latest_returns_empty_state_without_session(self) -> None:
        payload = session_latest()
        self.assertIn("session", payload)
        self.assertIn("active", payload["session"])

    def test_wifi_networks_are_safe_non_csi_demo_schema(self) -> None:
        payload = wifi_networks()

        self.assertIn("networks", payload)
        self.assertGreaterEqual(len(payload["networks"]), 2)
        self.assertIn("does not provide raw CSI", payload["limitations"])
        first = payload["networks"][0]
        self.assertEqual(first["ssid"], "TP-Link_Demo")
        self.assertFalse(first["can_use_as_csi_sensor"])
        self.assertIn("bssid_masked", first)

    def test_wifi_select_limits_adapter_mode_and_confidence(self) -> None:
        payload = select_wifi({"ssid": "TP-Link_Demo", "adapter_mode": MODE_WIFI_ONLY_NON_CSI})

        self.assertEqual(payload["selected_ssid"], "TP-Link_Demo")
        self.assertEqual(payload["adapter_mode"], MODE_WIFI_ONLY_NON_CSI)
        self.assertEqual(payload["status"], "selected")
        self.assertLessEqual(payload["confidence_ceiling"], 0.65)

    def test_room_setup_configures_manual_room_map(self) -> None:
        try:
            payload = setup_room(
                {
                    "room_name": "Demo Room",
                    "width_m": 5.2,
                    "length_m": 4.1,
                    "shape": "rectangle",
                    "zones": ["zone_a", "zone_b", "zone_c"],
                    "router_location": {"x_m": 0.5, "y_m": 2.0},
                }
            )

            self.assertEqual(payload["room_id"], "demo_room")
            self.assertEqual(payload["status"], "configured")
            self.assertEqual(payload["map_mode"], "manual_dimensions_plus_wifi_fingerprint")
            self.assertIn("probabilistic disturbance zones", payload["limitations"])
        finally:
            ROOM_SETUP_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

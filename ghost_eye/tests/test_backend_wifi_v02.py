import unittest

from fastapi.testclient import TestClient

from ghost_eye.api.schemas import MODE_WIFI_ONLY_NON_CSI
from ghost_eye.backend.app import app


class BackendWiFiV02Test(unittest.TestCase):
    def test_scan_returns_wifi_only_non_csi_contract(self) -> None:
        client = TestClient(app)

        response = client.get("/scan")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
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
        client = TestClient(app)

        response = client.get("/session/latest")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("session", payload)
        self.assertIn("active", payload["session"])


if __name__ == "__main__":
    unittest.main()

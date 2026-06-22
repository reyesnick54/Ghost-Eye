import unittest
from unittest.mock import patch

from ghost_eye.api.schemas import SOURCE_LOCAL_WIFI_LIVE, SOURCE_LOCAL_WIFI_SIMULATED
import ghost_eye.backend.app as backend_app


class BackendReadinessV03Test(unittest.TestCase):
    def test_readiness_reports_blockers_when_live_wifi_is_unavailable(self) -> None:
        with (
            patch.object(backend_app.adapter, "live_available", return_value=False),
            patch.object(
                backend_app.adapter,
                "get_live_status",
                return_value={
                    "ssid": "unknown",
                    "vendor_hint": "unknown",
                    "live_error": "unsupported_platform",
                },
            ),
            patch.object(backend_app.adapter, "get_live_error", return_value="unsupported_platform"),
            patch.object(backend_app, "_baseline_ready", return_value=False),
            patch.object(backend_app, "_fingerprints_ready", return_value=False),
        ):
            payload = backend_app.system_readiness()

        self.assertEqual(payload["backend"], "ok")
        self.assertFalse(payload["live_wifi_available"])
        self.assertEqual(payload["selected_source"], SOURCE_LOCAL_WIFI_SIMULATED)
        self.assertFalse(payload["demo_ready"])
        self.assertIn("live_wifi_unavailable", payload["blocking_issues"])
        self.assertIn("empty_room_baseline_missing", payload["blocking_issues"])
        self.assertIn("zone_fingerprints_missing", payload["blocking_issues"])
        self.assertTrue(payload["ai_ready"])
        self.assertTrue(payload["websocket_ready"])

    def test_sources_include_live_simulated_and_fallback_metadata(self) -> None:
        with (
            patch.object(backend_app.adapter, "live_available", return_value=True),
            patch.object(
                backend_app.adapter,
                "get_live_status",
                return_value={
                    "ssid": "Netgear Demo",
                    "vendor_hint": "netgear",
                    "available": True,
                },
            ),
            patch.object(backend_app.adapter, "get_live_error", return_value=None),
        ):
            payload = backend_app.sources()

        self.assertIn(SOURCE_LOCAL_WIFI_LIVE, payload["source_ids"])
        self.assertIn(SOURCE_LOCAL_WIFI_SIMULATED, payload["source_ids"])
        self.assertTrue(payload["live_available"])
        self.assertTrue(payload["fallback_available"])
        self.assertEqual(payload["current_ssid"], "Netgear Demo")
        self.assertEqual(payload["vendor_hint"], "netgear")

    def test_ai_analyze_scan_uses_fallback_without_s3m(self) -> None:
        payload = backend_app.analyze_scan(
            {
                "source": SOURCE_LOCAL_WIFI_SIMULATED,
                "presence": "possible_motion",
                "motion_score": 0.48,
                "zone": "zone_a",
                "confidence": 0.41,
                "confidence_ceiling": 0.65,
                "signal_quality": {
                    "visible_access_points": 1,
                    "packet_loss": 0.0,
                    "jitter_ms": 2.0,
                    "rssi_stability": 0.7,
                },
                "map": {"zone_a": 0.6},
            }
        )

        analysis = payload["ai_analysis"]
        self.assertEqual(analysis["provider"], "fallback")
        self.assertLessEqual(analysis["confidence"], 0.41)
        self.assertIn("simulated_source_not_live_wifi", analysis["false_positive_risks"])
        self.assertTrue(payload["status"]["fallback_available"])


if __name__ == "__main__":
    unittest.main()

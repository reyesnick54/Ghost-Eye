import unittest

from ghost_eye.ai import FallbackAIAnalyzer
from ghost_eye.api.schemas import GhostEyeTelemetry, ZoneMap


class FallbackAIAnalyzerTest(unittest.TestCase):
    def test_low_confidence_and_scan_geometry_risks(self):
        analyzer = FallbackAIAnalyzer()

        result = analyzer.analyze(
            {
                "confidence": 0.22,
                "motion_score": 0.2,
                "zone": "unknown",
                "observation": {
                    "jitter_ms": 42.0,
                    "visible_access_points": [{"bssid": "ap-1"}],
                },
            }
        )

        self.assertTrue(result.available)
        self.assertEqual(result.confidence, 0.22)
        self.assertIn("low confidence / scan quality weak", result.summary)
        self.assertEqual(
            result.limitations,
            [
                "wifi_only_non_csi",
                "confidence_capped",
                "authorized_environment_required",
            ],
        )
        self.assertIn("network_jitter_possible", result.metadata["risk_flags"])
        self.assertIn("weak_ap_geometry", result.metadata["risk_flags"])

    def test_motion_and_likely_zone_from_pydantic_telemetry(self):
        analyzer = FallbackAIAnalyzer()
        telemetry = GhostEyeTelemetry(
            motion_score=0.78,
            zone="zone_b",
            confidence=0.61,
            map=ZoneMap(confidence_by_zone={"zone_a": 0.2, "zone_b": 0.8}),
        )

        result = analyzer(telemetry)

        self.assertEqual(result.confidence, telemetry.confidence)
        self.assertIn("elevated disturbance", result.summary)
        self.assertIn("likely zone: zone_b", result.summary)
        self.assertEqual(result.metadata["likely_zone"], "zone_b")
        self.assertEqual(result.metadata["risk_flags"], [])

    def test_zone_not_mentioned_when_not_highest_map_value(self):
        analyzer = FallbackAIAnalyzer()

        result = analyzer.analyze(
            {
                "confidence": 0.5,
                "motion_score": 0.1,
                "zone": "zone_a",
                "map": {"zone_a": 0.3, "zone_b": 0.7},
                "visible_access_points": [{}, {}],
            }
        )

        self.assertNotIn("likely zone", result.summary)
        self.assertLessEqual(result.confidence, 0.5)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

from ghost_eye.ai.ai_analysis_schema import AIAnalysisConfig
from ghost_eye.ai.s3m_bridge import S3MBridge
from ghost_eye.ai.telemetry_prompt_builder import build_telemetry_prompt, sanitize_telemetry


SAMPLE_TELEMETRY = {
    "presence": "possible_presence",
    "motion_score": 0.72,
    "confidence": 0.58,
    "zone": "zone_a",
    "source": {
        "ssid": "private-lab-network",
        "bssid": "02:00:00:00:00:01",
        "kind": "wifi_non_csi",
    },
    "ignored_field": "not sent to prompt",
}


class GhostEyeAIBridgeTest(unittest.TestCase):
    def test_config_defaults_keep_ai_disabled_and_fallback_provider(self):
        config = AIAnalysisConfig.from_env({})

        self.assertFalse(config.enabled)
        self.assertEqual(config.provider, "fallback")
        self.assertEqual(config.s3m_path, "")

    def test_prompt_builder_redacts_wifi_identifiers(self):
        sanitized = sanitize_telemetry(SAMPLE_TELEMETRY)
        prompt = build_telemetry_prompt(SAMPLE_TELEMETRY)

        self.assertNotIn("ignored_field", sanitized)
        self.assertEqual(sanitized["source"]["ssid"], "[redacted]")
        self.assertEqual(sanitized["source"]["bssid"], "[redacted]")
        self.assertNotIn("private-lab-network", prompt)
        self.assertNotIn("02:00:00:00:00:01", prompt)

    def test_disabled_bridge_returns_unavailable_without_s3m(self):
        bridge = S3MBridge(config=AIAnalysisConfig(enabled=False, provider="fallback"))

        result = bridge.analyze(SAMPLE_TELEMETRY)

        self.assertFalse(result.available)
        self.assertEqual(result.provider, "fallback")
        self.assertEqual(result.metadata["enabled"], False)

    def test_s3m_provider_falls_back_when_runtime_unavailable(self):
        bridge = S3MBridge(config=AIAnalysisConfig(enabled=True, provider="s3m"))

        with patch("ghost_eye.ai.s3m_bridge.S3M_AVAILABLE", False):
            result = bridge.analyze(SAMPLE_TELEMETRY)

        self.assertTrue(result.available)
        self.assertEqual(result.provider, "fallback")
        self.assertEqual(result.metadata["fallback_reason"], "s3m_unavailable")


if __name__ == "__main__":
    unittest.main()

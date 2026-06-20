import json
import unittest
from dataclasses import dataclass

from ghost_eye.ai.telemetry_prompt_builder import build_scan_analysis_prompt


@dataclass(frozen=True)
class PromptTelemetry:
    mode: str
    confidence: float
    confidence_ceiling: float
    notice: str


class TelemetryPromptBuilderTest(unittest.TestCase):
    def test_prompt_includes_required_s3m_constraints(self):
        prompt = build_scan_analysis_prompt(
            {
                "mode": "wifi_non_csi",
                "confidence": 0.42,
                "confidence_ceiling": 0.65,
                "notice": "Authorized controlled environments only.",
                "disturbance": {"score": 0.31, "label": "moderate"},
            }
        )

        self.assertIn("You are S3M analyzing GhostEye scan telemetry.", prompt)
        self.assertIn("Analyze only the provided GhostEye telemetry", prompt)
        self.assertIn("Do not invent sensor data", prompt)
        self.assertIn("Do not increase confidence beyond the provided confidence", prompt)
        self.assertIn("Preserve the confidence ceiling", prompt)
        self.assertIn("likely causes of signal disturbance", prompt)
        self.assertIn("Identify false-positive risks", prompt)
        self.assertIn("Recommend calibration or scan-quality improvements", prompt)
        self.assertIn("WiFi-only non-CSI mode is coarse and probabilistic", prompt)
        self.assertIn("authorized controlled environments only", prompt)
        self.assertIn("Return structured JSON-compatible analysis only", prompt)

    def test_prompt_embeds_json_compatible_telemetry_without_changing_confidence(self):
        telemetry = PromptTelemetry(
            mode="simulated",
            confidence=0.33,
            confidence_ceiling=0.65,
            notice="Authorized controlled environments only.",
        )

        prompt = build_scan_analysis_prompt(telemetry)
        embedded_json = prompt.split("Provided GhostEye telemetry:\n", maxsplit=1)[1]
        embedded = json.loads(embedded_json)

        self.assertEqual(embedded["confidence"], 0.33)
        self.assertEqual(embedded["confidence_ceiling"], 0.65)
        self.assertEqual(embedded["mode"], "simulated")
        self.assertIn('"analysis_confidence": 0.0', prompt)


if __name__ == "__main__":
    unittest.main()

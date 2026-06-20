import unittest

from ghost_eye.ai.ai_analysis_schema import AIAnalysisRequest, AIAnalysisResult, AIStatus


class AIAnalysisSchemaTest(unittest.TestCase):
    def test_result_exposes_requested_fields(self) -> None:
        result = AIAnalysisResult()
        fields = getattr(AIAnalysisResult, "model_fields", None)
        if fields is None:
            fields = result.__fields__

        self.assertEqual(
            set(fields),
            {
                "enabled",
                "provider",
                "summary",
                "likely_explanation",
                "recommended_action",
                "risk_flags",
                "operator_confidence",
                "consensus_status",
                "limitations",
                "created_at",
            },
        )

    def test_operator_confidence_is_capped_by_consensus_telemetry_confidence(self) -> None:
        result = AIAnalysisResult(
            enabled=True,
            provider="test-provider",
            operator_confidence=0.91,
            consensus_status=AIStatus(
                enabled=True,
                provider="test-provider",
                status="available",
                telemetry_confidence=0.42,
            ),
        )

        self.assertEqual(result.operator_confidence, 0.42)

    def test_operator_confidence_can_use_telemetry_input_without_extra_result_field(self) -> None:
        result = AIAnalysisResult(
            operator_confidence=0.88,
            telemetry={"confidence": 0.57},
        )

        self.assertEqual(result.operator_confidence, 0.57)
        self.assertFalse(hasattr(result, "telemetry"))

    def test_operator_confidence_defaults_to_zero_without_telemetry_context(self) -> None:
        result = AIAnalysisResult(operator_confidence=0.88)

        self.assertEqual(result.operator_confidence, 0.0)

    def test_request_derives_telemetry_confidence_from_telemetry_payload(self) -> None:
        request = AIAnalysisRequest(telemetry={"confidence": 0.73})

        self.assertEqual(request.telemetry_confidence, 0.73)


if __name__ == "__main__":
    unittest.main()

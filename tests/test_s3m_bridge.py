import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from ghost_eye.ai.s3m_bridge import (
    MISSION_TYPE,
    RULES_OF_ENGAGEMENT,
    S3MBridge,
    telemetry_prompt_builder,
)


class S3MBridgeTests(unittest.TestCase):
    def tearDown(self) -> None:
        for module_name in ("llm_core.unified_runtime", "llm_core"):
            sys.modules.pop(module_name, None)

    def test_missing_runtime_returns_fallback_analysis(self) -> None:
        with patch.dict(
            "os.environ",
            {"GHOSTEYE_AI_PROVIDER": "s3m", "GHOSTEYE_S3M_PATH": "/missing/s3m"},
            clear=False,
        ):
            sys.modules["llm_core"] = None

            result = S3MBridge().analyze_scan({"presence": "possible_presence", "confidence": 0.42})

        self.assertFalse(result.available)
        self.assertEqual(result.confidence, 0.42)
        self.assertEqual(result.metadata["mode"], "fallback")
        self.assertEqual(result.metadata["reason"], "runtime_import_failed")
        self.assertEqual(result.metadata["rules_of_engagement"], RULES_OF_ENGAGEMENT)

    def test_existing_s3m_path_is_appended_to_sys_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict("os.environ", {"GHOSTEYE_S3M_PATH": temp_dir}, clear=False):
                bridge = S3MBridge()
                status = bridge.status()

            self.assertIn(temp_dir, sys.path)
            self.assertTrue(status["s3m_path_exists"])
            self.assertTrue(status["s3m_path_added"] or temp_dir in sys.path)

    def test_successful_runtime_result_becomes_ai_analysis_result(self) -> None:
        captured = {}

        class FakeMissionRequest:
            def __init__(self, **kwargs):
                captured["request"] = kwargs

        class FakeUnifiedRuntime:
            def __init__(self, provider=None):
                captured["provider"] = provider

            def execute(self, request):
                captured["request_object"] = request
                return {
                    "summary": "Signals suggest coarse movement near zone_a.",
                    "confidence": 0.77,
                    "model": "fake-s3m",
                    "limitations": ["coarse WiFi RSSI estimate"],
                    "metadata": {"trace_id": "abc123"},
                }

        self._install_fake_runtime(FakeUnifiedRuntime, FakeMissionRequest)

        with patch.dict("os.environ", {"GHOSTEYE_AI_PROVIDER": "test-provider"}, clear=False):
            result = S3MBridge().analyze_scan({"presence": "possible_presence", "zone": "zone_a"})

        self.assertTrue(result.available)
        self.assertEqual(result.summary, "Signals suggest coarse movement near zone_a.")
        self.assertEqual(result.confidence, 0.77)
        self.assertEqual(result.model, "fake-s3m")
        self.assertEqual(result.limitations, ["coarse WiFi RSSI estimate"])
        self.assertEqual(result.metadata["trace_id"], "abc123")
        self.assertEqual(result.metadata["mode"], "runtime")
        self.assertEqual(captured["provider"], "test-provider")
        self.assertEqual(captured["request"]["mission_type"], MISSION_TYPE)
        self.assertEqual(captured["request"]["rules_of_engagement"], RULES_OF_ENGAGEMENT)
        self.assertFalse(captured["request"]["consensus_mode"])
        self.assertIn("Ghost-Eye WiFi sensing telemetry", captured["request"]["prompt"])

    def test_runtime_failure_returns_fallback_analysis(self) -> None:
        class FakeMissionRequest:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class FailingUnifiedRuntime:
            def execute(self, request):
                raise RuntimeError("runtime exploded")

        self._install_fake_runtime(FailingUnifiedRuntime, FakeMissionRequest)

        result = S3MBridge().analyze_scan({"confidence": 0.35})

        self.assertFalse(result.available)
        self.assertEqual(result.confidence, 0.35)
        self.assertEqual(result.metadata["mode"], "fallback")
        self.assertEqual(result.metadata["reason"], "runtime_failed")
        self.assertIn("runtime exploded", result.metadata["detail"])

    def test_prompt_builder_serializes_scan_telemetry(self) -> None:
        prompt = telemetry_prompt_builder({"presence": "clear", "motion_score": 0.1})

        self.assertIn('"presence": "clear"', prompt)
        self.assertIn('"motion_score": 0.1', prompt)
        self.assertIn("authorized, controlled research environment only", prompt)

    def _install_fake_runtime(self, runtime_cls, request_cls) -> None:
        package = types.ModuleType("llm_core")
        module = types.ModuleType("llm_core.unified_runtime")
        module.UnifiedRuntime = runtime_cls
        module.MissionRequest = request_cls
        package.unified_runtime = module
        sys.modules["llm_core"] = package
        sys.modules["llm_core.unified_runtime"] = module


if __name__ == "__main__":
    unittest.main()

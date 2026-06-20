import unittest

from ghost_eye.inference.confidence import ConfidenceCeilingEngine


class ConfidenceCeilingEngineTest(unittest.TestCase):
    def test_mode_ceiling_caps_raw_confidence(self):
        engine = ConfidenceCeilingEngine()

        result = engine.evaluate(
            raw_confidence=0.92,
            signal_mode="simulated",
            signal_quality="excellent",
            device_motion_status="stable",
            map_ambiguity="clear",
        )

        self.assertEqual(
            set(result),
            {"raw_confidence", "confidence_ceiling", "final_confidence", "reason"},
        )
        self.assertEqual(result["raw_confidence"], 0.92)
        self.assertEqual(result["confidence_ceiling"], 0.65)
        self.assertEqual(result["final_confidence"], 0.65)
        self.assertLessEqual(result["final_confidence"], result["confidence_ceiling"])
        self.assertIn("signal mode 'simulated'", result["reason"])

    def test_contextual_inputs_can_tighten_mode_ceiling(self):
        engine = ConfidenceCeilingEngine()

        result = engine.evaluate(
            raw_confidence=0.95,
            signal_mode="csi",
            signal_quality=0.88,
            device_motion_status="stable",
            map_ambiguity="high",
        )

        self.assertEqual(result["confidence_ceiling"], 0.55)
        self.assertEqual(result["final_confidence"], 0.55)
        self.assertIn("map ambiguity 'high'", result["reason"])

    def test_low_raw_confidence_is_not_raised(self):
        engine = ConfidenceCeilingEngine()

        result = engine.evaluate(
            raw_confidence=0.42,
            signal_mode="rssi",
            signal_quality="good",
            device_motion_status=False,
            map_ambiguity=False,
        )

        self.assertEqual(result["confidence_ceiling"], 0.78)
        self.assertEqual(result["final_confidence"], 0.42)
        self.assertLessEqual(result["final_confidence"], result["confidence_ceiling"])

    def test_aliases_and_custom_mode_ceilings(self):
        engine = ConfidenceCeilingEngine({"lab-mode": 82})

        applied = engine.apply(
            raw_confidence=0.91,
            signal_mode="lab mode",
            signal_quality=75,
            device_motion_status="stationary",
            map_ambiguity=0.10,
        )
        computed = engine.compute(
            raw_confidence=0.91,
            mode="lab-mode",
            signal_quality=75,
            device_motion_status="stationary",
            map_ambiguity=0.10,
        )

        self.assertEqual(applied["confidence_ceiling"], 0.82)
        self.assertEqual(applied, computed)

    def test_raw_confidence_is_clamped_before_capping(self):
        engine = ConfidenceCeilingEngine()

        result = engine(
            raw_confidence=1.2,
            signal_mode="calibrated_csi",
            signal_quality="excellent",
            device_motion_status="stable",
            map_ambiguity="clear",
        )

        self.assertEqual(result["raw_confidence"], 1.0)
        self.assertEqual(result["confidence_ceiling"], 0.96)
        self.assertEqual(result["final_confidence"], 0.96)
        self.assertLessEqual(result["final_confidence"], result["confidence_ceiling"])


if __name__ == "__main__":
    unittest.main()

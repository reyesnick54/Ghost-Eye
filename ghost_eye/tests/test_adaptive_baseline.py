from tempfile import TemporaryDirectory
import unittest

from ghost_eye.inference.adaptive_baseline import AdaptiveBaselineEngine


class AdaptiveBaselineEngineTest(unittest.TestCase):
    def test_updates_adaptive_baseline_only_when_scan_is_stable(self):
        with TemporaryDirectory() as baseline_dir:
            engine = AdaptiveBaselineEngine(session_id="stable-room", baseline_dir=baseline_dir)

            first_scan = {"csi": [1.0, 2.0, 3.0], "zone": "zone_a"}
            result = engine.update(
                first_scan,
                motion_score=0.10,
                scan_stability=0.80,
                packet_loss=0.01,
            )

            self.assertEqual(result["baseline_status"], "updated")
            self.assertEqual(result["drift_score"], 0.0)
            self.assertIsNotNone(result["last_updated"])
            self.assertEqual(engine.static_baseline, first_scan)
            self.assertEqual(engine.adaptive_baseline, first_scan)

            last_updated = result["last_updated"]
            high_motion_scan = {"csi": [9.0, 9.0, 9.0], "zone": "zone_b"}
            held = engine.update(
                high_motion_scan,
                motion_score=0.20,
                scan_stability=0.90,
                packet_loss=0.01,
            )

            self.assertEqual(
                held,
                {
                    "baseline_status": "held",
                    "drift_score": 0.0,
                    "last_updated": last_updated,
                },
            )
            self.assertEqual(engine.static_baseline, first_scan)
            self.assertEqual(engine.adaptive_baseline, first_scan)

    def test_holds_adaptive_baseline_for_unstable_scan_and_packet_loss(self):
        with TemporaryDirectory() as baseline_dir:
            engine = AdaptiveBaselineEngine(session_id="unstable-room", baseline_dir=baseline_dir)

            unstable = engine.update(
                {"csi": [1.0, 1.0]},
                motion_score=0.10,
                scan_stability=0.70,
                packet_loss=0.01,
            )

            self.assertEqual(
                unstable,
                {
                    "baseline_status": "held",
                    "drift_score": 0.0,
                    "last_updated": None,
                },
            )
            self.assertEqual(engine.static_baseline, {"csi": [1.0, 1.0]})
            self.assertIsNone(engine.adaptive_baseline)

            packet_loss = engine.update(
                {"csi": [2.0, 2.0]},
                motion_score=0.10,
                scan_stability=0.80,
                packet_loss=0.05,
            )

            self.assertEqual(
                packet_loss,
                {
                    "baseline_status": "held",
                    "drift_score": 0.0,
                    "last_updated": None,
                },
            )
            self.assertIsNone(engine.adaptive_baseline)

    def test_persists_and_reloads_baselines(self):
        with TemporaryDirectory() as baseline_dir:
            engine = AdaptiveBaselineEngine(session_id="reload-room", baseline_dir=baseline_dir)
            engine.update(
                {"csi": [2.0, 4.0]},
                motion_score=0.10,
                scan_stability=0.80,
                packet_loss=0.01,
            )
            engine.update(
                {"csi": [3.0, 6.0]},
                motion_score=0.10,
                scan_stability=0.80,
                packet_loss=0.01,
            )

            reloaded = AdaptiveBaselineEngine(session_id="reload-room", baseline_dir=baseline_dir)

            self.assertEqual(reloaded.static_baseline, {"csi": [2.0, 4.0]})
            self.assertEqual(reloaded.adaptive_baseline, {"csi": [3.0, 6.0]})
            self.assertEqual(reloaded.last_updated, engine.last_updated)
            self.assertEqual(reloaded.drift_score(), 0.5)


if __name__ == "__main__":
    unittest.main()

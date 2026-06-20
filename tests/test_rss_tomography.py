import unittest

from ghost_eye.inference.rss_tomography import OpportunisticRSSITomography


class OpportunisticRSSITomographyTest(unittest.TestCase):
    def test_infers_most_likely_zone_from_rssi_disturbance(self):
        localizer = OpportunisticRSSITomography()

        current = {
            "ap_a": -58,
            "ap_b": -71,
            "ap_c": -80,
        }
        baseline = {
            "ap_a": -60,
            "ap_b": -70,
            "ap_c": -75,
        }
        fingerprints = {
            "zone_a": {"ap_a": -7, "ap_b": 5, "ap_c": 6},
            "zone_b": {"ap_a": 2, "ap_b": -1, "ap_c": -5},
            "zone_c": {"ap_a": 4, "ap_b": 4, "ap_c": 5},
        }

        result = localizer.infer(current, baseline, fingerprints)

        self.assertEqual(result.most_likely_zone, "zone_b")
        self.assertEqual(result.confidence_hint, "high")
        self.assertEqual(set(result.heatmap), {"zone_a", "zone_b", "zone_c"})
        self.assertEqual(result.heatmap["zone_b"], 1.0)
        self.assertGreater(result.heatmap["zone_b"], result.heatmap["zone_a"])
        self.assertGreater(result.heatmap["zone_b"], result.heatmap["zone_c"])
        for score in result.heatmap.values():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_supports_structured_observations_and_sampled_fingerprints(self):
        localizer = OpportunisticRSSITomography(min_common_signals=2)

        current = [
            {"bssid": "ap_a", "rssi": -52},
            {"bssid": "ap_b", "rssi": -71},
        ]
        baseline = {"rssi": {"ap_a": -60, "ap_b": -70}}
        fingerprints = {
            "zone_a": {
                "samples": [
                    [{"bssid": "ap_a", "rssi": 7}, {"bssid": "ap_b", "rssi": -1}],
                    [{"bssid": "ap_a", "rssi": 9}, {"bssid": "ap_b", "rssi": -1}],
                ]
            },
            "zone_b": {"disturbance": {"ap_a": -2, "ap_b": 6}},
        }

        result = localizer.infer_dict(current, baseline, fingerprints)

        self.assertEqual(result["most_likely_zone"], "zone_a")
        self.assertEqual(result["confidence_hint"], "high")
        self.assertEqual(result["heatmap"]["zone_a"], 1.0)

    def test_returns_insufficient_data_when_observations_do_not_overlap(self):
        localizer = OpportunisticRSSITomography()

        result = localizer.infer(
            current_observation={"ap_a": -55},
            baseline_observation={"ap_b": -70},
            saved_zone_fingerprints={"zone_a": {"ap_a": 5}},
        )

        self.assertIsNone(result.most_likely_zone)
        self.assertEqual(result.confidence_hint, "insufficient_data")
        self.assertEqual(result.heatmap, {"zone_a": 0.0})


if __name__ == "__main__":
    unittest.main()

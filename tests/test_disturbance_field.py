import unittest

from ghost_eye.inference.disturbance_field import (
    NO_PRESENCE_DETECTED,
    POSSIBLE_MOTION,
    POSSIBLE_PRESENCE,
    UNSTABLE_SCAN,
    DisturbanceFieldDetector,
)


class DisturbanceFieldDetectorTests(unittest.TestCase):
    def setUp(self):
        self.empty_room = {
            "access_points": [
                {"bssid": "ap-a", "rssi": -50},
                {"bssid": "ap-b", "rssi": -62},
                {"bssid": "ap-c", "rssi": -70},
            ],
            "jitter_ms": 5,
            "latency_ms": 25,
            "packet_loss_rate": 0.01,
        }

    def test_quiet_scan_returns_no_presence_with_explanation_features(self):
        detector = DisturbanceFieldDetector(alpha=1.0)
        current = {
            "access_points": [
                {"bssid": "ap-a", "rssi": -51},
                {"bssid": "ap-b", "rssi": -61},
                {"bssid": "ap-c", "rssi": -69},
            ],
            "jitter_ms": 6,
            "latency_ms": 28,
            "packet_loss_rate": 0.01,
        }

        result = detector.detect(current, self.empty_room)

        self.assertEqual(result.presence_state, NO_PRESENCE_DETECTED)
        self.assertGreaterEqual(result.motion_score, 0.0)
        self.assertLess(result.motion_score, detector.no_presence_threshold)
        for feature_name in (
            "rssi_delta_score",
            "jitter_delta_score",
            "latency_delta_score",
            "packet_loss_delta_score",
            "ap_visibility_delta_score",
        ):
            self.assertIn(feature_name, result.explanation_features)
            self.assertGreaterEqual(result.explanation_features[feature_name], 0.0)
            self.assertLessEqual(result.explanation_features[feature_name], 1.0)

    def test_motion_scan_returns_possible_presence(self):
        detector = DisturbanceFieldDetector(alpha=1.0)
        current = {
            "access_points": [
                {"bssid": "ap-a", "rssi": -34},
                {"bssid": "ap-b", "rssi": -81},
                {"bssid": "ap-x", "rssi": -55},
            ],
            "jitter_ms": 42,
            "latency_ms": 190,
            "packet_loss_rate": 0.05,
        }

        result = detector(current, self.empty_room)

        self.assertEqual(result.presence_state, POSSIBLE_PRESENCE)
        self.assertGreaterEqual(result.motion_score, detector.possible_presence_threshold)
        self.assertGreater(result.explanation_features["rssi_delta_score"], 0.5)
        self.assertGreater(result.explanation_features["ap_visibility_delta_score"], 0.0)

    def test_smoothing_uses_previous_motion_score(self):
        detector = DisturbanceFieldDetector(alpha=0.5)
        disturbed = {
            "access_points": [
                {"bssid": "ap-a", "rssi": -34},
                {"bssid": "ap-b", "rssi": -81},
                {"bssid": "ap-x", "rssi": -55},
            ],
            "jitter_ms": 42,
            "latency_ms": 190,
            "packet_loss_rate": 0.05,
        }
        quiet = dict(self.empty_room)

        first = detector.detect(disturbed, self.empty_room)
        second = detector.detect(quiet, self.empty_room)

        self.assertGreater(first.motion_score, second.motion_score)
        self.assertGreater(second.motion_score, 0.0)
        self.assertEqual(second.presence_state, POSSIBLE_MOTION)
        self.assertEqual(second.explanation_features["previous_motion_score"], first.motion_score)

    def test_adaptive_baseline_overrides_empty_room_drift(self):
        detector = DisturbanceFieldDetector(alpha=1.0)
        empty_room = {
            "rssi": {"ap-a": -45, "ap-b": -46},
            "visible_aps": ["ap-a", "ap-b"],
        }
        adaptive = {
            "rssi": {"ap-a": -60, "ap-b": -61},
            "visible_aps": ["ap-a", "ap-b"],
        }
        current = {
            "rssi": {"ap-a": -60, "ap-b": -61},
            "visible_aps": ["ap-a", "ap-b"],
        }

        without_adaptive = detector.detect(current, empty_room)
        detector.reset()
        with_adaptive = detector.detect(current, empty_room, adaptive_baseline=adaptive)

        self.assertGreater(without_adaptive.motion_score, detector.no_presence_threshold)
        self.assertEqual(with_adaptive.presence_state, NO_PRESENCE_DETECTED)
        self.assertLess(with_adaptive.motion_score, without_adaptive.motion_score)
        self.assertEqual(with_adaptive.explanation_features["baseline_source"], "adaptive_baseline")

    def test_empty_or_missing_scan_is_unstable(self):
        detector = DisturbanceFieldDetector(alpha=1.0)

        result = detector.detect({}, self.empty_room)

        self.assertEqual(result.presence_state, UNSTABLE_SCAN)
        self.assertTrue(result.explanation_features["scan_unstable"])


if __name__ == "__main__":
    unittest.main()

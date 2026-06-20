import json
import tempfile
import unittest
from pathlib import Path

from ghost_eye.inference.room_fingerprint_mapper import RoomFingerprintMapper


class RoomFingerprintMapperTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mapper = RoomFingerprintMapper(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_fingerprint_persists_simple_json(self):
        fingerprint = self.mapper.create_fingerprint(
            "Kitchen",
            {
                "rssi": {"gateway_a": -48, "gateway_b": -72},
                "latency_ms": {"gateway_a": 12, "gateway_b": 35},
                "jitter_ms": {"gateway_a": 3, "gateway_b": 9},
            },
        )

        path = Path(self.temp_dir.name) / "Kitchen.json"
        self.assertTrue(path.exists())
        saved = json.loads(path.read_text())
        self.assertEqual(saved["zone"], "Kitchen")
        self.assertEqual(saved["rssi"], fingerprint["rssi"])
        self.assertIn("rssi_weights", saved)

    def test_compare_to_zone_scores_similar_observations_higher(self):
        kitchen = self.mapper.create_fingerprint(
            "kitchen",
            {
                "gateways": {
                    "gateway_a": {"rssi": -45, "latency_ms": 15, "jitter_ms": 4},
                    "gateway_b": {"rssi": -70, "latency_ms": 40, "jitter_ms": 12},
                }
            },
        )
        similar = {
            "gateways": {
                "gateway_a": {"rssi": -47, "latency_ms": 17, "jitter_ms": 5},
                "gateway_b": {"rssi": -69, "latency_ms": 42, "jitter_ms": 11},
            }
        }
        different = {
            "gateways": {
                "gateway_a": {"rssi": -82, "latency_ms": 120, "jitter_ms": 45},
                "gateway_c": {"rssi": -43, "latency_ms": 9, "jitter_ms": 3},
            }
        }

        similar_score = self.mapper.compare_to_zone(similar, kitchen)
        different_score = self.mapper.compare_to_zone(different, kitchen)

        self.assertGreater(similar_score, different_score)
        self.assertEqual(similar_score["zone"], "kitchen")
        self.assertIn("gateway_latency", similar_score["metrics"])
        self.assertIn("jitter", similar_score["metrics"])

    def test_estimate_zone_returns_best_zone_scores_and_confidence_hint(self):
        kitchen = self.mapper.create_fingerprint(
            "kitchen",
            {
                "rssi": {"gateway_a": -45, "gateway_b": -70},
                "latency_ms": {"gateway_a": 15, "gateway_b": 40},
                "jitter_ms": {"gateway_a": 4, "gateway_b": 12},
            },
        )
        office = self.mapper.create_fingerprint(
            "office",
            {
                "rssi": {"gateway_a": -80, "gateway_c": -42},
                "latency_ms": {"gateway_a": 100, "gateway_c": 10},
                "jitter_ms": {"gateway_a": 40, "gateway_c": 2},
            },
        )

        result = self.mapper.estimate_zone(
            {
                "rssi": {"gateway_a": -46, "gateway_b": -69},
                "latency_ms": {"gateway_a": 16, "gateway_b": 41},
                "jitter_ms": {"gateway_a": 5, "gateway_b": 11},
            },
            [kitchen, office],
        )

        self.assertEqual(result["zone"], "kitchen")
        self.assertIn("kitchen", result["zone_scores"])
        self.assertIn("office", result["zone_scores"])
        self.assertIn(result["confidence_hint"], {"low", "medium", "high"})

    def test_estimate_zone_loads_saved_fingerprints_from_directory(self):
        self.mapper.create_fingerprint(
            "living_room",
            {
                "access_points": [
                    {"id": "gateway_a", "rssi": -52, "latency": 20, "jitter": 5},
                    {"id": "gateway_b", "rssi": -76, "latency": 55, "jitter": 14},
                ]
            },
        )

        result = self.mapper.estimate_zone(
            {
                "access_points": [
                    {"id": "gateway_a", "rssi": -53, "latency": 19, "jitter": 5},
                    {"id": "gateway_b", "rssi": -75, "latency": 57, "jitter": 13},
                ]
            }
        )

        self.assertEqual(result["zone"], "living_room")
        self.assertGreater(result["zone_scores"]["living_room"], 0.8)


if __name__ == "__main__":
    unittest.main()

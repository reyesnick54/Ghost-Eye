import json
import tempfile
import unittest
from pathlib import Path

from ghost_eye.inference.session_learner import GhostEyeSessionLearner


class GhostEyeSessionLearnerTest(unittest.TestCase):
    def test_save_and_infer_nearest_session_match(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = GhostEyeSessionLearner(session_log_dir=temp_dir, k_neighbors=2)

            learner.save_labeled_fingerprint(
                "one_person_zone_a",
                {"rssi": -40, "csi": [0.1, 0.2, 0.3]},
                session_id="zone-a",
                timestamp=1.0,
            )
            learner.save_labeled_fingerprint(
                "one_person_zone_b",
                {"rssi": -80, "csi": [1.1, 1.2, 1.3]},
                session_id="zone-b",
                timestamp=2.0,
            )

            result = learner.infer_session({"rssi": -41, "csi": [0.1, 0.22, 0.29]})

        self.assertEqual(
            set(result),
            {"nearest_session_matches", "learned_zone_hint", "confidence_hint"},
        )
        self.assertEqual(result["learned_zone_hint"], "one_person_zone_a")
        self.assertGreater(result["confidence_hint"], 0.45)
        self.assertEqual(result["nearest_session_matches"][0]["session_id"], "zone-a")
        self.assertEqual(
            result["nearest_session_matches"][0]["label"], "one_person_zone_a"
        )
        self.assertEqual(len(result["nearest_session_matches"]), 2)

    def test_supports_all_required_session_labels(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = GhostEyeSessionLearner(session_log_dir=temp_dir)

            self.assertEqual(
                GhostEyeSessionLearner.SUPPORTED_SESSION_LABELS,
                {
                    "empty_room",
                    "one_person_zone_a",
                    "one_person_zone_b",
                    "walking_path",
                    "door_open",
                    "door_closed",
                    "router_near",
                    "router_far",
                },
            )

            for index, label in enumerate(
                sorted(GhostEyeSessionLearner.SUPPORTED_SESSION_LABELS)
            ):
                learner.save_labeled_fingerprint(
                    label,
                    {"feature": index},
                    session_id=f"session-{index}",
                    timestamp=float(index),
                )

            labels = {session["label"] for session in learner.load_labeled_sessions()}

        self.assertEqual(labels, GhostEyeSessionLearner.SUPPORTED_SESSION_LABELS)

    def test_invalid_labels_and_empty_fingerprints_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = GhostEyeSessionLearner(session_log_dir=temp_dir)

            with self.assertRaisesRegex(ValueError, "unsupported session label"):
                learner.save_labeled_fingerprint("unknown", {"feature": 1})

            with self.assertRaisesRegex(ValueError, "at least one numeric value"):
                learner.save_labeled_fingerprint(
                    "empty_room", {"note": "no numeric values"}
                )

    def test_infer_skips_malformed_or_unsupported_session_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            learner = GhostEyeSessionLearner(session_log_dir=temp_path)
            learner.save_labeled_fingerprint(
                "door_open",
                {"door_delta": 0.9},
                session_id="valid-door-open",
            )
            (temp_path / "bad-json.json").write_text("{", encoding="utf-8")
            (temp_path / "unsupported-label.json").write_text(
                json.dumps(
                    {
                        "session_id": "bad-label",
                        "label": "unsupported",
                        "fingerprint": {"door_delta": 0.9},
                    }
                ),
                encoding="utf-8",
            )

            result = learner.infer_session({"door_delta": 1.0})

        self.assertEqual(result["learned_zone_hint"], "door_open")
        self.assertEqual(
            [match["session_id"] for match in result["nearest_session_matches"]],
            ["valid-door-open"],
        )

    def test_infer_without_training_data_returns_empty_hints(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = GhostEyeSessionLearner(session_log_dir=temp_dir)

            result = learner.infer_session({"rssi": -40})

        self.assertEqual(
            result,
            {
                "nearest_session_matches": [],
                "learned_zone_hint": None,
                "confidence_hint": 0.0,
            },
        )


if __name__ == "__main__":
    unittest.main()

"""Focused verification for the post-publication traffic follow-up."""

import tempfile
import unittest
from pathlib import Path

import analyze_followup


class FollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = (
            analyze_followup.ROOT /
            "evidence/live/2026-10-23/github-traffic-response.json"
        )
        cls.payload, cls.evidence_hash = analyze_followup.load(cls.evidence)
        cls.rows, cls.summary = analyze_followup.derive(
            cls.payload, cls.evidence_hash
        )

    def test_baseline_and_discontinuity_reconcile(self):
        self.assertEqual(self.summary["baseline"]["daily_clone_events"],
                         [568, 568, 572, 571, 575, 568, 582])
        self.assertEqual(self.summary["baseline"]["mean_clone_events_per_day"], 572)
        self.assertEqual(
            self.summary["investigation_repository_public_event_utc"],
            "2026-10-19T16:36:10Z",
        )
        observed = self.summary["first_full_days_after_public_event"]
        self.assertEqual([observed[day]["clone_events"] for day in
                          analyze_followup.FOLLOWUP_DATES], [808, 152, 22])
        self.assertAlmostEqual(
            self.summary["october_22_decline_from_baseline_mean_percent"],
            96.15384615384616,
        )

    def test_daily_unique_values_remain_labelled_as_nonadditive_observations(self):
        observed = self.summary["first_full_days_after_public_event"]
        self.assertEqual([
            observed[day]["summed_repository_daily_unique_cloner_observations"]
            for day in analyze_followup.FOLLOWUP_DATES
        ], [628, 4, 13])
        self.assertIn("not an account-wide audience", self.summary["interpretation_boundary"])

    def test_generated_outputs_are_current(self):
        expected_csv = analyze_followup.csv_bytes(self.rows)
        expected_summary = (
            __import__("json").dumps(self.summary, indent=2, sort_keys=True) + "\n"
        ).encode()
        self.assertEqual(
            (analyze_followup.ROOT / "data/post-publication-traffic-2026-10-23.csv").read_bytes(),
            expected_csv,
        )
        self.assertEqual(
            (analyze_followup.ROOT / "data/post-publication-summary-2026-10-23.json").read_bytes(),
            expected_summary,
        )

    def test_missing_focal_repository_is_rejected(self):
        changed = dict(self.payload)
        changed["repositories"] = dict(self.payload["repositories"])
        changed["repositories"].pop("DEGS")
        with self.assertRaises(ValueError):
            analyze_followup.validated_rows(changed)


if __name__ == "__main__":
    unittest.main()

"""Focused arithmetic, schema, and negative-input checks; no network access."""

import math
import tempfile
import unittest
from pathlib import Path

import analyze


class AnalysisTests(unittest.TestCase):
    def test_known_aggregate_uses_sample_standard_deviation(self):
        result = analyze.metrics([568, 568, 572, 571, 575, 568])
        self.assertEqual(result["total"], 3422)
        self.assertAlmostEqual(result["mean"], 3422 / 6)
        self.assertAlmostEqual(result["sample_sd"], math.sqrt(124 / 15))
        self.assertAlmostEqual(result["sample_cv_percent"], 0.5041229375300484, places=12)

    def test_two_dates_are_not_a_second_fourteen_day_window(self):
        result = analyze.metrics([575, 568])
        self.assertEqual(result["n_days"], 2)
        self.assertEqual(result["total"], 1143)
        self.assertEqual(result["mean"], 571.5)
        self.assertAlmostEqual(result["sample_sd"], 7 / math.sqrt(2))

    def test_zero_mean_and_one_day_are_explicitly_undefined(self):
        self.assertIsNone(analyze.metrics([0, 0])["sample_cv_percent"])
        self.assertIsNone(analyze.metrics([1])["sample_sd"])
        self.assertEqual(analyze.metrics([5, 5])["range_percent_of_mean"], 0)

    def test_negative_fractional_and_boolean_counts_are_rejected(self):
        for value in ("-1", "1.5", "NaN", "1e2", " 1", "True", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze.count(value, "test")
        with self.assertRaises(ValueError):
            analyze.metrics([True, 2])

    def test_csv_header_and_row_width_are_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            for text in ("a,a\n1,2\n", "a,b\n1\n", "a,b\n1,2,3\n"):
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text), self.assertRaises(ValueError):
                    analyze.read_csv(path, "a,b")
            path.write_bytes(b"a,b\n\xff,2\n")
            with self.assertRaises(ValueError):
                analyze.read_csv(path, "a,b")

    def test_duplicate_daily_key_and_missing_day_are_rejected(self):
        path = analyze.ROOT / "data/traffic-snapshot-2026-10-19.csv"
        rows, _ = analyze.read_csv(path, analyze.SCHEMAS[path.name])
        for malformed in (rows + [rows[0]], rows[1:]):
            with self.assertRaises(ValueError):
                analyze.validate_snapshot(malformed)

    def test_preserved_tables_and_revised_exclusion(self):
        result = analyze.analyze(analyze.ROOT / "data")
        summary, windows, comparisons = result[:3]
        self.assertEqual(summary["original_window"]["total_clones"], 8372)
        self.assertEqual(summary["comparison_summaries"][0]["n_series"], 136)
        self.assertEqual(summary["comparison_summaries"][1]["n_series"], 134)
        self.assertEqual(summary["comparison_summaries"][1]["n_mean_below_25"], 118)
        self.assertEqual(summary["comparison_summaries"][2]["n_series"], 2)
        fixture = [row for row in comparisons if
                   (row["source_host_repository"], row["path"]) == analyze.UNCERTAIN_FIXTURE]
        self.assertEqual(len(fixture), 1)
        self.assertFalse(fixture[0]["included_in_reanalysis"])
        ambiguous = [row for row in comparisons if
                     (row["source_host_repository"], row["path"]) == analyze.AMBIGUOUS_MULTI_REPOSITORY]
        self.assertEqual(len(ambiguous), 1)
        self.assertFalse(ambiguous[0]["included_in_reanalysis"])
        accounts = {row["field"]: row for row in summary["account_summary"]}
        self.assertEqual(accounts["public_repositories"]["median"], 5)
        self.assertEqual(accounts["stars_on_original_repositories_in_first_20"]["zero_count"], 27)

    def test_reanalysis_outputs_are_byte_deterministic(self):
        result = analyze.analyze(analyze.ROOT / "data")
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first", Path(directory) / "second"
            analyze.write_outputs(first, result)
            analyze.write_outputs(second, result)
            self.assertEqual(sorted(path.name for path in first.iterdir()),
                             sorted(path.name for path in second.iterdir()))
            for path in first.iterdir():
                self.assertEqual(path.read_bytes(), (second / path.name).read_bytes(), path.name)

    def test_recovered_original_window_is_correlated_not_added(self):
        summary, windows = analyze.analyze(analyze.ROOT / "data")[:2]
        if summary["recovered_original_daily_data"] is None:
            self.skipTest("Optional recovered daily TSV is absent")
        original = [row for row in windows if row["window"] == "original_focal_14_days"]
        self.assertEqual(len(original), 5)
        aggregate = next(row for row in original if row["repository"] == "Four-repository total")
        self.assertEqual(aggregate["total"], 8271)
        self.assertEqual(summary["followup_window"]["days_overlapping_original"], 12)
        self.assertEqual(summary["recovered_original_daily_data"]["overlap_count_differences"], [])


if __name__ == "__main__":
    unittest.main()

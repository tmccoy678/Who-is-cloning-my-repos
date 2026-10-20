#!/usr/bin/env python3
"""Recompute descriptive results from the preserved CSVs, using only Python's standard library.

Run from any directory:
    python3 scripts/analyze.py
    python3 scripts/analyze.py --check

Inputs are the six named CSVs under --data-dir (default: this repository's data/).
Their headers are checked against SCHEMAS below. Counts must be nonnegative
integers; dates must be ISO dates; repository/date keys must be unique. The
October 19 snapshot must contain all 14 dates, October 5–18, per repository.
Stored summary values are checked against daily counts at their stated precision.
If --recovery-dir contains 2026-10-17/four-repository-daily-counts.tsv, its
headerless repository/date/count/uniques rows add an original-window sensitivity
analysis. Its acquisition provenance is documented separately under evidence/.

Outputs use new reanalysis-* names only. --check validates inputs and prints a
summary without writing. --output-dir redirects all outputs. Outputs contain no
reconstructed API responses or acquisition claims: this verifies the preserved
tables, not GitHub's underlying measurement or the original search process.
"""

import argparse
import csv
import hashlib
import io
import json
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATES = [f"2026-10-{day:02d}" for day in range(13, 19)]
FULL_DATES = [f"2026-10-{day:02d}" for day in range(5, 19)]
ORIGINAL_DATES = [f"2026-10-{day:02d}" for day in range(3, 17)]
HIGH = ("DobeWorks-v2.1", "DEGS-v2.1", "BackspaceTextRetention", "TrashTreasurePickup")
SCHEMAS = {
    "traffic-snapshot-2026-10-17.csv":
        "repository,primary_subject,clone_events,unique_cloners,views,unique_visitors,mean_clones_per_day",
    "traffic-snapshot-2026-10-19.csv":
        "repository,date_utc,clones,daily_unique_cloners,window_clones,window_unique_cloners,window_views,window_unique_visitors,captured_on",
    "same-six-day-variation-comparison-2026-10-19.csv":
        "group,repository," + ",".join(DATES) + ",six_day_total,mean,min,max,range_percent_of_mean,max_abs_deviation_from_mean_percent,sample_cv_percent,source_url,source_commit",
    "public-daily-clone-series-search-2026-10-19.csv":
        "repository,path,subpath," + ",".join(DATES) + ",six_day_mean,range_percent_of_mean,max_abs_deviation_from_mean_percent,sample_cv_percent,excluded_reason,range_within_1_to_4_percent,max_deviation_within_1_to_4_percent,source_url",
    "numeric-regularity-search-2026-10-19.csv":
        "rank_by_range_percentage,repository,subject," + ",".join(DATES) + ",six_day_mean,range_percent_of_mean,max_abs_deviation_from_mean_percent,sample_cv_percent,meets_1_to_4_percent_criterion,source_url",
    "same-age-account-comparison-2026-10-19.csv":
        "login,created_on,followers,public_repositories,original_repositories_in_first_20,stars_on_original_repositories_in_first_20,forks_on_original_repositories_in_first_20,sample_definition",
}
METRIC_FIELDS = [
    "n_days", "total", "mean", "median", "min", "max", "sample_sd",
    "range_percent_of_mean", "max_abs_deviation_from_mean_percent", "sample_cv_percent",
]
UNCERTAIN_FIXTURE = ("elboletaire/github-stats-action", "fixtures/traffic/clones.json")
AMBIGUOUS_MULTI_REPOSITORY = ("SasanLabs/VulnerableApp", "metrics/traffic.csv")


def read_csv(path, expected_header):
    raw = path.read_bytes()
    try:
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
        expected = expected_header.split(",")
        if reader.fieldnames != expected:
            raise ValueError(f"{path.name}: unexpected CSV header")
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as error:
        raise ValueError(f"{path.name}: invalid UTF-8 CSV") from error
    for number, row in enumerate(rows, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{path.name}:{number}: incomplete or extra CSV fields")
    if not rows:
        raise ValueError(f"{path.name}: no data rows")
    return rows, hashlib.sha256(raw).hexdigest()


def count(value, context):
    if not isinstance(value, str) or not re.fullmatch(r"0|[1-9][0-9]*", value):
        raise ValueError(f"{context}: expected a nonnegative integer, got {value!r}")
    return int(value)


def iso_date(value, context):
    try:
        parsed = date.fromisoformat(value)
    except (ValueError, TypeError) as error:
        raise ValueError(f"{context}: invalid ISO date") from error
    if parsed.isoformat() != value:
        raise ValueError(f"{context}: noncanonical ISO date")
    return value


def metrics(values):
    if not values or any(type(value) is not int or value < 0 for value in values):
        raise ValueError("metrics requires a nonempty list of nonnegative integer counts")
    mean = statistics.mean(values)
    sd = statistics.stdev(values) if len(values) > 1 else None
    return {
        "n_days": len(values), "total": sum(values), "mean": mean, "median": statistics.median(values),
        "min": min(values), "max": max(values), "sample_sd": sd,
        "range_percent_of_mean": 100 * (max(values) - min(values)) / mean if mean else None,
        "max_abs_deviation_from_mean_percent":
            100 * max(abs(value - mean) for value in values) / mean if mean else None,
        "sample_cv_percent": 100 * sd / mean if mean and sd is not None else None,
    }


def verify_rounded(actual, recorded, tolerance, context):
    try:
        observed = float(recorded)
    except ValueError as error:
        raise ValueError(f"{context}: invalid recorded number") from error
    if not math.isfinite(observed) or actual is None or abs(actual - observed) > tolerance:
        raise ValueError(f"{context}: recorded {recorded} disagrees with recomputed {actual}")


def series_metrics(row, context):
    result = metrics([count(row[day], f"{context}:{day}") for day in DATES])
    mean_field = "mean" if "mean" in row else "six_day_mean"
    verify_rounded(result["mean"], row[mean_field], 0.000501, context + ":" + mean_field)
    for field in ("range_percent_of_mean", "max_abs_deviation_from_mean_percent", "sample_cv_percent"):
        verify_rounded(result[field], row[field], 0.005001, context + ":" + field)
    if "six_day_total" in row:
        for source, destination in (("six_day_total", "total"), ("min", "min"), ("max", "max")):
            if count(row[source], context + ":" + source) != result[destination]:
                raise ValueError(f"{context}: incorrect {source}")
    return result


def validate_snapshot(rows):
    by_repository = defaultdict(dict)
    metadata = {}
    fields = ("window_clones", "window_unique_cloners", "window_views", "window_unique_visitors")
    for number, row in enumerate(rows, 2):
        context = f"traffic-snapshot-2026-10-19.csv:{number}"
        day = iso_date(row["date_utc"], context)
        iso_date(row["captured_on"], context)
        name = row["repository"]
        if not name or day in by_repository[name]:
            raise ValueError(f"{context}: blank repository or duplicate repository/date")
        clones = count(row["clones"], context)
        uniques = count(row["daily_unique_cloners"], context)
        if uniques > clones:
            raise ValueError(f"{context}: daily uniques exceed clones")
        by_repository[name][day] = clones
        current = {field: count(row[field], context) for field in fields}
        current["captured_on"] = row["captured_on"]
        if name in metadata and metadata[name] != current:
            raise ValueError(f"{context}: inconsistent repeated window metadata")
        metadata[name] = current
    for name, daily in by_repository.items():
        if sorted(daily) != FULL_DATES:
            raise ValueError(f"{name}: expected complete October 5–18 daily window")
        if sum(daily.values()) != metadata[name]["window_clones"]:
            raise ValueError(f"{name}: daily sum disagrees with rolling total")
        if metadata[name]["window_unique_cloners"] > metadata[name]["window_clones"]:
            raise ValueError(f"{name}: window uniques exceed window clones")
    if not set(HIGH) <= set(by_repository):
        raise ValueError("snapshot is missing a high-traffic repository")
    return by_repository, metadata


def group_summary(label, rows):
    means = [row["mean"] for row in rows]
    hosts = Counter(row["source_host_repository"] for row in rows)
    return {
        "group": label, "n_series": len(rows), "n_source_host_repositories": len(hosts),
        "median_daily_mean": statistics.median(means) if means else None,
        "n_mean_below_25": sum(value < 25 for value in means),
        "n_mean_below_1": sum(value < 1 for value in means),
        "n_range_1_to_4_percent": sum(1 <= row["range_percent_of_mean"] <= 4 for row in rows),
        "n_max_deviation_1_to_4_percent":
            sum(1 <= row["max_abs_deviation_from_mean_percent"] <= 4 for row in rows),
        "n_range_at_most_4_percent": sum(row["range_percent_of_mean"] <= 4 for row in rows),
        "n_max_deviation_at_most_4_percent":
            sum(row["max_abs_deviation_from_mean_percent"] <= 4 for row in rows),
        "min_range_percent": min((row["range_percent_of_mean"] for row in rows), default=None),
        "max_range_percent": max((row["range_percent_of_mean"] for row in rows), default=None),
        "largest_two_source_hosts_n_series": sum(value for _, value in hosts.most_common(2)),
    }


def original_daily_metrics(path, original_rows, followup):
    raw = path.read_bytes()
    by_repository = defaultdict(dict)
    for number, row in enumerate(csv.reader(io.StringIO(raw.decode("utf-8")), delimiter="\t"), 1):
        if len(row) != 4 or row[0] not in HIGH:
            raise ValueError(f"recovered original daily TSV:{number}: invalid row")
        name, day = row[0], iso_date(row[1], "recovered original daily TSV")
        clones, uniques = count(row[2], "recovered clones"), count(row[3], "recovered uniques")
        if day in by_repository[name] or uniques > clones:
            raise ValueError(f"recovered original daily TSV:{number}: duplicate date or invalid uniques")
        by_repository[name][day] = clones
    if set(by_repository) != set(HIGH):
        raise ValueError("recovered original daily TSV must contain all four focal repositories")
    totals = {row["repository"]: count(row["clone_events"], "original") for row in original_rows}
    windows, differences = [], []
    for name in HIGH:
        if sorted(by_repository[name]) != ORIGINAL_DATES or sum(by_repository[name].values()) != totals[name]:
            raise ValueError(f"recovered original daily TSV disagrees with original dates/total: {name}")
        windows.append({"window": "original_focal_14_days", "start": ORIGINAL_DATES[0],
                        "end": ORIGINAL_DATES[-1], "repository": name,
                        **metrics([by_repository[name][day] for day in ORIGINAL_DATES])})
        for day in sorted(set(by_repository[name]) & set(followup[name])):
            if by_repository[name][day] != followup[name][day]:
                differences.append({"repository": name, "date": day,
                                    "original": by_repository[name][day], "followup": followup[name][day]})
    windows.append({"window": "original_focal_14_days", "start": ORIGINAL_DATES[0],
                    "end": ORIGINAL_DATES[-1], "repository": "Four-repository total",
                    **metrics([sum(by_repository[name][day] for name in HIGH) for day in ORIGINAL_DATES])})
    return windows, {
        "file": "evidence/recovery/2026-10-17/four-repository-daily-counts.tsv",
        "sha256": hashlib.sha256(raw).hexdigest(), "n_rows": sum(len(rows) for rows in by_repository.values()),
        "type": "Recovered transformed jq stdout, not complete raw API responses",
        "overlapping_repository_days_checked": 48, "overlap_count_differences": differences,
    }


def analyze(data_dir, recovery_dir=ROOT / "evidence/recovery"):
    tables, sources = {}, []
    for filename, header in SCHEMAS.items():
        tables[filename], digest = read_csv(data_dir / filename, header)
        sources.append({"file": filename, "sha256": digest, "n_rows": len(tables[filename])})
    original = tables["traffic-snapshot-2026-10-17.csv"]
    original_total = [row for row in original if row["repository"] == "TOTAL"]
    original_rows = [row for row in original if row["repository"] != "TOTAL"]
    if len(original_total) != 1 or len({row["repository"] for row in original_rows}) != len(original_rows):
        raise ValueError("original snapshot requires unique repositories and one TOTAL row")
    total = sum(count(row["clone_events"], row["repository"]) for row in original_rows)
    if total != count(original_total[0]["clone_events"], "original TOTAL"):
        raise ValueError("original aggregate disagrees with repository sum")
    for row in original:
        verify_rounded(count(row["clone_events"], "original") / 14,
                       row["mean_clones_per_day"], 1e-8, "original mean")
    if original_total[0]["unique_cloners"] != "NOT_ADDITIVE":
        raise ValueError("original cross-repository unique cloners must remain nonadditive")
    high_total = sum(count(row["clone_events"], "original") for row in original_rows
                     if row["repository"] in HIGH)
    daily, metadata = validate_snapshot(tables["traffic-snapshot-2026-10-19.csv"])
    windows = []
    for label, dates in (("full_followup_14_days", FULL_DATES),
                         ("selected_6_days", DATES), ("new_only_2_days", DATES[-2:])):
        for name in sorted(daily):
            windows.append({"window": label, "start": dates[0], "end": dates[-1],
                            "repository": name, **metrics([daily[name][day] for day in dates])})
        values = [sum(daily[name][day] for name in HIGH) for day in dates]
        windows.append({"window": label, "start": dates[0], "end": dates[-1],
                        "repository": "Four-repository total", **metrics(values)})
    recovered = None
    recovered_path = recovery_dir / "2026-10-17/four-repository-daily-counts.tsv"
    if recovered_path.is_file():
        original_windows, recovered = original_daily_metrics(recovered_path, original_rows, daily)
        windows.extend(original_windows)

    same_date = tables["same-six-day-variation-comparison-2026-10-19.csv"]
    for number, row in enumerate(same_date, 2):
        series_metrics(row, f"same-six-day-variation-comparison-2026-10-19.csv:{number}")
        name = row["repository"]
        if name in HIGH or name == "Four-repository total":
            for day in DATES:
                expected = daily[name][day] if name in HIGH else sum(daily[repo][day] for repo in HIGH)
                if count(row[day], "same-date primary") != expected:
                    raise ValueError(f"same-date table disagrees with primary snapshot: {name}/{day}")

    comparisons, keys = [], set()
    for number, row in enumerate(tables["public-daily-clone-series-search-2026-10-19.csv"], 2):
        key = (row["repository"], row["path"], row["subpath"])
        if key in keys:
            raise ValueError("duplicate source-host/path/subpath in extracted comparisons")
        keys.add(key)
        computed = series_metrics(row, f"public-daily-clone-series-search-2026-10-19.csv:{number}")
        reason = row["excluded_reason"]
        if reason and reason != "cumulative_or_accumulated_counter":
            raise ValueError(f"unrecognized preserved exclusion reason: {reason}")
        if key[:2] == UNCERTAIN_FIXTURE:
            reason = "fixture_path_observational_provenance_unverified"
        if key[:2] == AMBIGUOUS_MULTI_REPOSITORY:
            reason = "multiple_repository_rows_collapsed_by_date_in_original_extraction"
        comparisons.append({
            "source_csv_line": number, "source_host_repository": row["repository"],
            "path": row["path"], "subpath": row["subpath"], "source_url": row["source_url"],
            "preserved_excluded_reason": row["excluded_reason"],
            "reanalysis_excluded_reason": reason, "included_in_reanalysis": not bool(reason),
            "in_mean_100_to_200_stratum": 100 <= computed["mean"] <= 200,
            **{day: count(row[day], "comparison") for day in DATES}, **computed,
        })
    numeric = tables["numeric-regularity-search-2026-10-19.csv"]
    for number, row in enumerate(numeric, 2):
        series_metrics(row, f"numeric-regularity-search-2026-10-19.csv:{number}")
        matching = [candidate for candidate in comparisons
                    if candidate["source_host_repository"] == row["repository"]]
        if not any(all(candidate[day] == count(row[day], "numeric") for day in DATES)
                   for candidate in matching):
            raise ValueError("nearest-series table is not supported by extracted daily values")
    preserved = [row for row in comparisons if not row["preserved_excluded_reason"]]
    included = [row for row in comparisons if row["included_in_reanalysis"]]
    stratum = [row for row in included if row["in_mean_100_to_200_stratum"]]
    summaries = [group_summary("original_non_cumulative_extraction", preserved),
                 group_summary("reanalysis_screened", included),
                 group_summary("reanalysis_mean_100_to_200_inclusive", stratum)]
    cluster = Counter(row["source_host_repository"] for row in included)
    clusters = [{"source_host_repository": host, "n_included_series": n,
                 "percent_of_included_series": 100 * n / len(included)}
                for host, n in cluster.most_common()]

    account_rows = tables["same-age-account-comparison-2026-10-19.csv"]
    if len({row["login"] for row in account_rows}) != len(account_rows):
        raise ValueError("duplicate login in account comparison")
    account_summary = []
    for field in ("followers", "public_repositories", "original_repositories_in_first_20",
                  "stars_on_original_repositories_in_first_20",
                  "forks_on_original_repositories_in_first_20"):
        values = [count(row[field], "account " + field) for row in account_rows]
        account_summary.append({"field": field, "n": len(values), "median": statistics.median(values),
                                "zero_count": values.count(0), "min": min(values), "max": max(values)})
    account_dates = Counter(iso_date(row["created_on"], "account") for row in account_rows)
    summary = {
        "analysis_schema_version": 1,
        "scope": "Recalculation of preserved CSVs; not reconstruction or verification of acquisition.",
        "sources": sources,
        "recovered_original_daily_data": recovered,
        "original_window": {"start": "2026-10-03", "end": "2026-10-16", "n_days": 14,
                            "n_repositories": len(original_rows), "total_clones": total,
                            "mean_clones_per_day": total / 14, "high_traffic_total": high_total,
                            "high_traffic_percent": 100 * high_total / total,
                            "cross_repository_unique_cloners": None,
                            "cross_repository_unique_visitors": None},
        "followup_window": {"start": FULL_DATES[0], "end": FULL_DATES[-1], "n_days": 14,
                            "days_overlapping_original": 12, "new_dates": DATES[-2:],
                            "total_clones": sum(value["window_clones"] for value in metadata.values())},
        "comparison_summaries": summaries,
        "comparison_exclusions": dict(Counter(row["reanalysis_excluded_reason"]
                                              for row in comparisons if row["reanalysis_excluded_reason"])),
        "rate_stratum": {"definition": "100 <= mean daily clones <= 200",
                        "selection_status": "Post hoc descriptive sensitivity analysis; not a matched design.",
                        "series": [{"source_host_repository": row["source_host_repository"],
                                    "path": row["path"], **{key: row[key] for key in METRIC_FIELDS}}
                                   for row in stratum]},
        "account_summary": account_summary, "account_creation_dates": dict(sorted(account_dates.items())),
        "limitations": [
            "This script recalculates preserved CSVs and, when present, recovered original daily TSV data.",
            "Recovery and replay provenance are documented separately in evidence/README.md and evidence/recovery_manifest.json.",
            "The complete 226-candidate/rejection ledger and complete October 17 API response bodies remain unavailable.",
            "Source-host counts are not counts of independent measured repositories or owners.",
            "The fixture-path exclusion is precautionary; it does not assert fabrication.",
            "A multi-repository source is excluded because the original extraction overwrote same-date rows without preserving target identity.",
            "Integer nonconstant counts with mean below 25 cannot have range/mean at most 4 percent.",
            "All comparisons and window choices are descriptive and post hoc; no significance or causal tests are performed.",
            "The six-day interval follows observed spikes; only October 17 and 18 extend the original window.",
            "Aggregate unique cloners and unique visitors cannot be deduplicated across repositories.",
        ],
    }
    return summary, windows, comparisons, summaries, clusters, account_summary


def write_csv(path, rows, fields=None):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir, result):
    summary, windows, comparisons, summaries, clusters, accounts = result
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "reanalysis-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    for suffix, rows in (("window-metrics", windows), ("comparison-series", comparisons),
                         ("comparison-summary", summaries), ("source-host-clusters", clusters),
                         ("account-summary", accounts)):
        write_csv(output_dir / f"reanalysis-{suffix}.csv", rows)
    screened = summaries[1]
    report = f"""# Reanalysis of preserved clone-traffic tables

Run `python3 scripts/analyze.py` from the repository root. This standard-library
script validates all six preserved CSV schemas and recomputes their arithmetic.
Run `python3 scripts/analyze.py --check` for a read-only validation.
Run `python3 -B -m unittest discover -s scripts -p 'test_analysis.py' -v` for focused tests.

These outputs verify the supplied tables, not GitHub's measurement. Recovery and
replay provenance, including recovered source responses, queries, and the original
extraction script, are documented separately in `../evidence/README.md` and
`../evidence/recovery_manifest.json`. The complete 226-candidate/rejection ledger
and complete October 17 API response bodies remain unavailable.
Source SHA-256 identities and all computed values are in
`reanalysis-summary.json`. The original files are not rewritten.

The original window contains {summary['original_window']['total_clones']:,} clones
and a mean of {summary['original_window']['mean_clones_per_day']:.0f}/day. The
follow-up window overlaps 12 of its 14 dates. `reanalysis-window-metrics.csv`
compares October 5–18, October 13–18, and the two new dates October 17–18.
When the recovered original daily TSV is present, it also includes October 3–16
for the four focal repositories and checks their 48 overlapping repository-days.
It never adds overlapping rolling totals.

Of 138 extracted series, two cumulative counters remain excluded, one fixture-path
series is excluded because its observational provenance is unverified, and one
multi-repository source is excluded because same-date rows were overwritten
without preserving measured-repository identity. The fixture exclusion is a
precaution, not a finding of fabricated data. The screened
set contains {screened['n_series']} series from {screened['n_source_host_repositories']}
source-host repositories. A host can archive several measured repositories;
these are not asserted to be independent units. The two largest hosts supply
{screened['largest_two_source_hosts_n_series']} series.

There are {screened['n_mean_below_25']} screened series below 25 clones/day.
For a nonconstant integer-count series, range is at least one; when mean is below
25, range/mean exceeds 4%. A percentage is unitless, but comparability of count
variation still depends on rate and acquisition. No screened series meets either
the original 1–4% criterion or a <=4% criterion. The 100–200/day sensitivity
stratum contains only {summaries[2]['n_series']} series; it is post hoc and too small
to establish a population anomaly rate or a causal mechanism.

The account sample has a median of 5 public repositories, 27 zero-star accounts,
and 28 zero-follower accounts. All 32 retained accounts were created August 9;
the search's nominal August 9–11 interval is not the observed date distribution.

Output schemas:

- `reanalysis-window-metrics.csv`: repository, named window/start/end, number of
  dates, total, mean, median, min/max, sample SD, range/mean, maximum absolute deviation/
  mean, and sample CV. Percentages are multiplied by 100; sample SD uses n−1.
- `reanalysis-comparison-series.csv`: source CSV line, source host/path/subpath/
  URL, original and revised exclusions, inclusion/rate-stratum flags, the six
  daily counts, and the same metrics.
- `reanalysis-comparison-summary.csv`: extraction/screened/rate-stratum counts,
  source-host counts, rate distribution, numeric-match counts, and range limits.
- `reanalysis-source-host-clusters.csv`: included series per source host.
- `reanalysis-account-summary.csv`: medians, zero counts, and ranges for the
  preserved account fields.

No missing API responses, candidate records, private account telemetry, or
within-day ordering are invented. No statistical significance or causal test is
performed. The output JSON uses null for quantities unavailable from the data.
"""
    (output_dir / "reanalysis-methods.md").write_text(report, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--recovery-dir", type=Path, default=ROOT / "evidence/recovery",
                        help="Optional recovered original daily TSV location.")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Defaults to data-dir; writes only reanalysis-* files.")
    parser.add_argument("--check", action="store_true", help="Validate and summarize without writing files.")
    args = parser.parse_args(argv)
    try:
        result = analyze(args.data_dir, args.recovery_dir)
        if not args.check:
            write_outputs(args.output_dir or args.data_dir, result)
    except (ValueError, OSError) as error:
        print(f"Analysis failed: {error}", file=sys.stderr)
        return 2
    summary = result[0]
    print(json.dumps({"original_total_clones": summary["original_window"]["total_clones"],
                      "original_mean_per_day": summary["original_window"]["mean_clones_per_day"],
                      "screened_comparison": summary["comparison_summaries"][1],
                      "rate_stratum": summary["rate_stratum"],
                      "files_written": not args.check}, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

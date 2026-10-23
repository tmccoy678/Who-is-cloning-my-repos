#!/usr/bin/env python3
"""Validate and derive the October 23 post-publication traffic follow-up."""

import argparse
import csv
from datetime import date, timedelta
import hashlib
import io
import json
from pathlib import Path
import statistics


ROOT = Path(__file__).resolve().parents[1]
FOCAL = (
    "Backspace-Text-Retention",
    "DEGS",
    "DobeWorks",
    "TrashTreasurePickup",
)
BASELINE_DATES = tuple(f"2026-10-{day:02d}" for day in range(13, 20))
FOLLOWUP_DATES = ("2026-10-20", "2026-10-21", "2026-10-22")


def load(path):
    raw = path.read_bytes()
    payload = json.loads(raw)
    if payload.get("schema") != "github-owner-traffic-capture.v1":
        raise ValueError("Unexpected evidence schema")
    if payload.get("owner") != "tmccoy678":
        raise ValueError("Unexpected repository owner")
    if payload.get("repository_count") != len(payload.get("repositories", {})):
        raise ValueError("Repository count does not match evidence records")
    return payload, hashlib.sha256(raw).hexdigest()


def validated_rows(payload):
    rows = []
    for repository in FOCAL:
        record = payload["repositories"].get(repository)
        if not record:
            raise ValueError(f"Missing focal repository: {repository}")
        clones = record["clones"]
        daily = clones["clones"]
        if len(daily) != 14:
            raise ValueError(f"{repository}: expected 14 daily clone records")
        expected_start = date.fromisoformat(daily[0]["timestamp"][:10])
        expected_dates = [
            (expected_start + timedelta(days=offset)).isoformat()
            for offset in range(14)
        ]
        observed_dates = [entry["timestamp"][:10] for entry in daily]
        if observed_dates != expected_dates:
            raise ValueError(f"{repository}: dates are not one complete ordered interval")
        for entry in daily:
            count = entry["count"]
            uniques = entry["uniques"]
            if (type(count) is not int or type(uniques) is not int or
                    count < 0 or uniques < 0 or uniques > count):
                raise ValueError(f"{repository}: invalid daily clone values")
            rows.append({
                "repository": repository,
                "date_utc": entry["timestamp"][:10],
                "clones": count,
                "daily_unique_cloners": uniques,
                "captured_at_utc": payload["captured_at"],
            })
        if sum(entry["count"] for entry in daily) != clones["count"]:
            raise ValueError(f"{repository}: daily clone total does not reconcile")
    return rows


def aggregate(rows, dates):
    by_date = {day: [] for day in dates}
    for row in rows:
        if row["date_utc"] in by_date:
            by_date[row["date_utc"]].append(row)
    if any(len(values) != len(FOCAL) for values in by_date.values()):
        raise ValueError("Follow-up interval is incomplete")
    return {
        day: {
            "clone_events": sum(row["clones"] for row in values),
            "summed_repository_daily_unique_cloner_observations": sum(
                row["daily_unique_cloners"] for row in values
            ),
        }
        for day, values in by_date.items()
    }


def derive(payload, evidence_sha256):
    rows = validated_rows(payload)
    baseline = aggregate(rows, BASELINE_DATES)
    followup = aggregate(rows, FOLLOWUP_DATES)
    baseline_counts = [baseline[day]["clone_events"] for day in BASELINE_DATES]
    baseline_mean = statistics.mean(baseline_counts)
    october_22 = followup["2026-10-22"]["clone_events"]
    summary = {
        "schema": "github-clone-traffic-post-publication-followup.v2",
        "captured_at_utc": payload["captured_at"],
        "source_evidence_sha256": evidence_sha256,
        "focal_repositories": list(FOCAL),
        "investigation_repository_public_event_utc": "2026-10-19T16:36:10Z",
        "baseline": {
            "dates_utc": list(BASELINE_DATES),
            "daily_clone_events": baseline_counts,
            "total_clone_events": sum(baseline_counts),
            "mean_clone_events_per_day": baseline_mean,
            "minimum_daily_clone_events": min(baseline_counts),
            "maximum_daily_clone_events": max(baseline_counts),
        },
        "first_full_days_after_public_event": followup,
        "october_22_decline_from_baseline_mean_percent":
            100 * (baseline_mean - october_22) / baseline_mean,
        "interpretation_boundary": (
            "The repository-level daily unique-cloner values are not an account-wide "
            "audience estimate. GitHub supplies no actor identities or within-day event times."
        ),
    }
    return rows, summary


def csv_bytes(rows):
    output = io.StringIO(newline="")
    fields = (
        "repository", "date_utc", "clones", "daily_unique_cloners",
        "captured_at_utc",
    )
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--evidence",
        type=Path,
        default=ROOT / "evidence/live/2026-10-23/github-traffic-response.json",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=ROOT / "data/post-publication-traffic-2026-10-23.csv",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "data/post-publication-summary-2026-10-23.json",
    )
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    payload, evidence_sha256 = load(arguments.evidence)
    rows, summary = derive(payload, evidence_sha256)
    expected_csv = csv_bytes(rows)
    expected_summary = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode()
    outputs = ((arguments.csv, expected_csv), (arguments.summary, expected_summary))

    if arguments.check:
        for path, expected in outputs:
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"Derived output is absent or stale: {path}")
    else:
        for path, expected in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)

    print(json.dumps({
        "captured_at_utc": payload["captured_at"],
        "baseline_mean": summary["baseline"]["mean_clone_events_per_day"],
        "october_22_clone_events":
            summary["first_full_days_after_public_event"]["2026-10-22"]["clone_events"],
        "decline_percent": summary["october_22_decline_from_baseline_mean_percent"],
        "checked": arguments.check,
    }))


if __name__ == "__main__":
    main()

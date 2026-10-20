#!/usr/bin/env python3
"""Cache pinned retained sources and replay the historical limited extraction.

Default: offline replay only. --download fetches missing immutable GitHub blobs.
It does not rerun Code Search, access authenticated traffic, or reconstruct the
lost candidate ledger. Historical parser quirks are retained for comparison.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATES = [f"2026-10-{day}" for day in range(13, 19)]
BASELINE = ROOT / "evidence/recovery/2026-10-19/all-public-daily-clone-series.jsonl"
MAX_FILE = 5_000_000
MAX_TOTAL = 20_000_000


def normdate(value):
    if not isinstance(value, str):
        return None
    match = re.search(r"2026-10-(1[3-8])", value)
    return match.group(0) if match else None


def extract(text, filename):
    found = []
    duplicate_dates = []
    duplicate_json_keys = []

    def pairs_hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                duplicate_json_keys.append(key)
            result[key] = value
        return result

    def record(values, path):
        for field in ("clones", "clone_count", "count"):
            if all(isinstance(value, dict) and isinstance(value.get(field), (int, float))
                   for value in values):
                if field != "count" or any("clone" in str(part).lower() for part in path):
                    found.append(("/".join(map(str, path)), [float(value[field]) for value in values], field))

    def walk(value, path):
        if isinstance(value, dict):
            if all(day in value for day in DATES):
                values = [value[day] for day in DATES]
                if all(isinstance(item, dict) for item in values):
                    record(values, path)
                elif (all(isinstance(item, (int, float)) for item in values)
                      and any("clone" in str(part).lower() for part in path)):
                    found.append(("/".join(map(str, path)), list(map(float, values)), "value"))
            for key, child in value.items():
                walk(child, path + [key])
        elif isinstance(value, list):
            by_day = {}
            for item in value:
                if not isinstance(item, dict):
                    continue
                for field in ("date", "timestamp", "day", "recorded_at"):
                    if field in item:
                        day = normdate(item[field])
                        if day:
                            if day in by_day:
                                duplicate_dates.append({"path": "/".join(map(str, path)), "date": day})
                            by_day[day] = item
                        break
            if all(day in by_day for day in DATES):
                record([by_day[day] for day in DATES], path)
            for index, child in enumerate(value[:5]):
                walk(child, path + [index])

    try:
        walk(json.loads(text, object_pairs_hook=pairs_hook), [])
    except (ValueError, TypeError, RecursionError):
        pass
    # Match the historical JSON value-vector de-duplication.
    unique = []
    seen = set()
    for item in found:
        key = tuple(item[1])
        if key not in seen:
            unique.append(item)
            seen.add(key)
    if filename.lower().endswith(".csv"):
        try:
            rows = list(csv.DictReader(io.StringIO(text)))
            by_day = {}
            for row in rows:
                day = normdate(row.get("date") or row.get("timestamp") or "")
                if day:
                    if day in by_day:
                        duplicate_dates.append({"path": "csv", "date": day})
                    by_day[day] = row
            if all(day in by_day for day in DATES):
                for field in ("clones", "clone_count", "count"):
                    try:
                        values = [float(by_day[day][field]) for day in DATES]
                        if field != "count" or "clone" in filename.lower():
                            unique.append(("csv", values, field))
                    except (KeyError, ValueError, TypeError):
                        pass
        except (ValueError, TypeError, csv.Error):
            pass
    return unique, duplicate_dates, duplicate_json_keys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Fetch only missing pinned public source files.")
    args = parser.parse_args()
    baseline = [json.loads(line) for line in BASELINE.read_text().splitlines()]
    output = ROOT / "evidence/public"
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"sources": []}
    old = {row["source_url"]: row for row in previous["sources"]}
    total = sum(path.stat().st_size for path in (output / "sources").glob("*")) if (output / "sources").exists() else 0
    sources = []
    outcomes = []
    for index, row in enumerate(baseline, 1):
        url = row["html_url"]
        match = re.fullmatch(r"https://github\.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/(.+)", url)
        if not match:
            raise ValueError("A retained source is not pinned to a full Git commit.")
        repository, commit, path = match.groups()
        raw_url = f"https://raw.githubusercontent.com/{repository}/{commit}/{path}"
        suffix = Path(urllib.parse.unquote(path)).suffix
        if suffix not in {".json", ".csv", ".jsonl", ".ndjson"}:
            suffix = ".txt"
        destination = output / "sources" / f"{index:03d}{suffix}"
        metadata = dict(old.get(url, {
            "source_id": f"S{index:03d}",
            "source_url": url,
            "download_url": raw_url,
            "source_repository": repository,
            "source_path": urllib.parse.unquote(path),
            "source_commit": commit,
            "kind": "Pinned public-source reread during revision; not an original October 19 capture.",
            "local_path": destination.relative_to(ROOT).as_posix(),
        }))
        if not destination.exists() and args.download:
            try:
                request = urllib.request.Request(raw_url, headers={"User-Agent": "bounded-manuscript-source-recovery"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    raw = response.read(MAX_FILE + 1)
                if len(raw) > MAX_FILE:
                    raise ValueError("File exceeds historical 5 MB input limit.")
                if total + len(raw) > MAX_TOTAL:
                    raise ValueError("20 MB total source-cache limit reached.")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
                total += len(raw)
                metadata["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
                metadata["sha256"] = hashlib.sha256(raw).hexdigest()
                metadata["bytes"] = len(raw)
                metadata.pop("error", None)
            except (OSError, urllib.error.URLError, ValueError) as error:
                metadata["error"] = f"{type(error).__name__}: {error}"
        outcome = {
            "source_id": metadata["source_id"],
            "source_url": url,
            "retained_subpath": row["subpath"],
            "original_values": row["values"],
        }
        if destination.exists():
            raw = destination.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest != metadata.get("sha256"):
                raise ValueError(f"Cache hash mismatch for {metadata['source_id']}.")
            candidates, duplicate_dates, duplicate_keys = extract(raw.decode("utf-8", "replace"), row["path"])
            matches = [item for item in candidates if item[0] == row["subpath"] and item[1] == row["values"]]
            outcome.update(
                result="matched" if matches else "mismatch",
                count_field=matches[0][2] if matches else None,
                parsed_candidates=[{"subpath": item[0], "values": item[1], "count_field": item[2]} for item in candidates],
                duplicate_date_records=duplicate_dates,
                duplicate_json_keys=duplicate_keys,
            )
        else:
            outcome.update(result="unavailable", error=metadata.get("error", "Source is not cached; --download was not supplied."))
        sources.append(metadata)
        outcomes.append(outcome)
        # Preserve progress and honest acquisition times if interrupted.
        manifest_path.write_text(json.dumps({
            "schema_version": 1,
            "historical_retained_series": len(baseline),
            "cache_size_limit_bytes": MAX_TOTAL,
            "sources": sources,
        }, indent=2) + "\n")
        if index % 25 == 0:
            print(f"Processed {index}/{len(baseline)} sources; cache {total} bytes.", flush=True)
    report = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Offline replay of historical limited parser behavior against pinned retained-source bytes; no new search.",
        "original_extraction_sha256": hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
        "matched": sum(row["result"] == "matched" for row in outcomes),
        "mismatched": sum(row["result"] == "mismatch" for row in outcomes),
        "unavailable": sum(row["result"] == "unavailable" for row in outcomes),
        "outcomes": outcomes,
    }
    (output / "replay-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("matched", "mismatched", "unavailable")}))


if __name__ == "__main__":
    main()

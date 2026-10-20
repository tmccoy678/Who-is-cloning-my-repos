#!/usr/bin/env python3
"""Recover narrowly selected research artifacts; never execute recovered code.

The private session log and temporary root are explicit local inputs. Neither
input path nor unrelated session content is included in the published output.
"""
import argparse
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = {
    "BackspaceTextRetention", "DEGS-v2.1", "DobeWorks-v2.1",
    "TrashTreasurePickup", "grok-bridge-writeup", "WeatherTicker",
}
CALLS = {
    "oct17_summary": "call_d908bd35aff940b7b2e30e6753847f5f",
    "oct17_daily": "call_ec80203fc2224cc49d9d4ee04fa3412c",
    "oct17_clone_summary": "call_07d78a8144944ab89c63f9a7ecb299e0",
    "oct19_two": "call_cd9175a8d41d4ae3b474cfd1afb6ca9f",
    "oct19_four": "call_52b83c2a8fa34ccfb331215080f1e693",
    "comparison_download": "call_afb3c08d647a437791fc3d831c62d7ef",
    "numeric_search": "call_31cf6a5b8d58436ea6dbbc9470edc297",
}
COMPARISONS = {
    "GrantAgent.csv": ("joshua-d-campbell/GrantAgent", "traffic/clones.csv"),
    "claude-skills.json": ("Wubabalala/claude-skills", "traffic/data.json"),
    "pcap-analyzer-mcp.json": ("aws-samples/sample-pcap-analyzer-mcp", "traffic-data/clones_latest.json"),
    "ENZO.json": ("theguysudo/ENZO", "traffic/history.json"),
    "AgentHarbor.json": ("abhiunix/AgentHarbor", "traffic/data.json"),
    "ARIA.json": ("youxch/ARIA", "traffic/stats.json"),
    "AgrusScanner.json": ("NYBaywatch/AgrusScanner", "docs/traffic-stats.json"),
    "CorvusCapture.json": ("NYBaywatch/CorvusCapture", "docs/traffic-stats.json"),
    "CoWork-OS.json": ("CoWork-OS/CoWork-OS", "data/adoption/public-stats-latest.json"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--temporary-root", type=Path, required=True)
    args = parser.parse_args()
    records = {}
    wanted = set(CALLS.values())
    with args.session.open() as stream:
        for line in stream:
            item = json.loads(line)
            payload = item.get("payload", {})
            call = payload.get("call_id")
            if item.get("type") != "response_item" or call not in wanted:
                continue
            record = records.setdefault(call, {})
            kind = payload.get("type", "")
            if kind in {"custom_tool_call", "function_call"}:
                record["call_at_utc"] = item["timestamp"]
            elif kind in {"custom_tool_call_output", "function_call_output"}:
                record["completed_at_utc"] = item["timestamp"]
                record["chunks"] = [
                    block["text"] for block in payload.get("output", [])
                    if isinstance(block, dict) and block.get("type") == "input_text"
                ]
    manifest = {
        "recovered_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Selected original research artifacts and tool stdout only; no conversations or private filesystem paths.",
        "artifacts": [],
        "limitations": [
            "No original HTTP headers were recovered.",
            "Session-extracted client stdout is not an original HTTP-response capture.",
            "The exact requests that wrote the October 19 CSV did not preserve their response bodies; earlier same-day stdout is corroborating evidence.",
            "No full October 17 clone/view response bodies were found in the scoped session and temporary artifacts; transformed stdout survives.",
            "The 226-candidate inventory, seven individual search responses, and fetch/parse rejection ledger were not saved by the recovered parser and were not recovered.",
            "Original historical hashes were not recorded for the recovered temporary files; hashes here identify their bytes at recovery.",
        ],
    }

    def save(relative, raw, kind, call_name, **extra):
        path = ROOT / "evidence" / "recovery" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        call = records[CALLS[call_name]]
        metadata = {
            "path": path.relative_to(ROOT).as_posix(),
            "kind": kind,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "original_call_at_utc": call["call_at_utc"],
            "original_call_completed_at_utc": call["completed_at_utc"],
            **extra,
        }
        manifest["artifacts"].append(metadata)

    # Retain only the six public repositories; the original aggregate command
    # also inspected private repositories, which are intentionally excluded.
    summary = []
    for chunk in records[CALLS["oct17_summary"]]["chunks"]:
        for line in chunk.splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict) and row.get("repo") in {"tmccoy678/" + name for name in PUBLIC}:
                summary.append(line)
    if len(summary) != 6:
        raise ValueError("Expected six public aggregate records.")
    save("2026-10-17/public-repository-summary.jsonl",
         ("\n".join(summary) + "\n").encode(),
         "session-extracted transformed API stdout; private-repository rows omitted",
         "oct17_summary")
    daily = records[CALLS["oct17_daily"]]["chunks"][1]
    if any(line.split("\t")[0] not in PUBLIC for line in daily.splitlines() if line):
        raise ValueError("Unexpected repository in daily stdout.")
    save("2026-10-17/four-repository-daily-counts.tsv", daily.encode(),
         "session-extracted jq-transformed API stdout; no header in original", "oct17_daily")
    clone_summary = records[CALLS["oct17_clone_summary"]]["chunks"][1]
    save("2026-10-17/five-repository-clone-summary.txt", clone_summary.encode(),
         "session-extracted Python-transformed API stdout", "oct17_clone_summary")

    labels = {
        "Dobe clones": ("DobeWorks-v2.1", "clones"),
        "DEGS clones": ("DEGS-v2.1", "clones"),
        "Dobe views": ("DobeWorks-v2.1", "views"),
        "DEGS views": ("DEGS-v2.1", "views"),
    }
    for chunk in records[CALLS["oct19_two"]]["chunks"]:
        label, _, text = chunk.partition("\n")
        if label not in labels:
            continue
        outer = json.loads(text)
        raw = outer["output"].encode()
        json.loads(raw)
        repo, endpoint = labels[label]
        save(f"2026-10-19/{repo}-{endpoint}.json", raw,
             "session-extracted gh api stdout", "oct19_two",
             endpoint=f"repos/tmccoy678/{repo}/traffic/{endpoint}")
    for chunk in records[CALLS["oct19_four"]]["chunks"]:
        repo, _, body = chunk.partition("\n")
        if repo not in PUBLIC:
            continue
        json.loads(body)
        save(f"2026-10-19/{repo}-clones.json", body.encode(),
             "session-extracted gh api stdout", "oct19_four",
             endpoint=f"repos/tmccoy678/{repo}/traffic/clones")

    recovered_parser = (args.temporary_root / "find_daily_clone_series.py").read_bytes()
    tree = ast.parse(recovered_parser)
    queries = next(
        ast.literal_eval(node.value) for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "queries" for target in node.targets)
    )
    save("2026-10-19/find_daily_clone_series.py.txt", recovered_parser,
         "original temporary parser bytes; inert text; not executed during recovery", "numeric_search")
    original_output = (args.temporary_root / "all-public-daily-clone-series.jsonl").read_bytes()
    if len(original_output.splitlines()) != 138:
        raise ValueError("Expected 138 original output records.")
    save("2026-10-19/all-public-daily-clone-series.jsonl", original_output,
         "original temporary extraction output bytes", "numeric_search")
    search = {
        "queries": queries,
        "endpoint": "GET search/code",
        "per_page": 100,
        "pagination": "none",
        "recorded_candidate_file_count": 226,
        "recorded_extracted_series_count": 138,
        "candidate_key": ["repository.full_name", "path"],
        "candidate_ledger": "not recovered; original program retained it only in memory",
        "parser_limitations": [
            "Parses one JSON document or CSV; no JSONL/NDJSON parsing branch.",
            "Regex date recognition is restricted to October 13-18, 2026.",
            "Repeated date records use the last encountered record.",
            "Nested arrays are searched through only their first five elements after direct date-record parsing.",
            "Identical value vectors within a JSON file are deduplicated without regard to path.",
            "Files exceeding 5,000,000 bytes and fetch failures are omitted.",
            "UTF-8 decoding replaces errors; several parse/conversion errors are silently ignored.",
            "Cumulative exclusion was applied afterward by path/subpath containing cumulative or accum.",
        ],
    }
    save("2026-10-19/search-protocol.json",
         (json.dumps(search, indent=2) + "\n").encode(),
         "reconstructed protocol from recovered parser and contemporaneous count output", "numeric_search")
    for name, (repo, source_path) in COMPARISONS.items():
        raw = (args.temporary_root / "github-traffic-comparison" / name).read_bytes()
        save("2026-10-19/comparisons/" + name, raw,
             "original temporary public-source download bytes", "comparison_download",
             source_repository=repo, source_path=source_path,
             original_endpoint=f"repos/{repo}/contents/{source_path}",
             original_request_ref="default branch at collection time")
    destination = ROOT / "evidence" / "recovery_manifest.json"
    destination.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Recovered {len(manifest['artifacts'])} selected artifacts.")


if __name__ == "__main__":
    main()

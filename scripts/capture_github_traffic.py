#!/usr/bin/env python3
"""Capture authenticated GitHub Traffic responses without credentials or headers.

The GitHub Traffic endpoints require push access even for public repositories.
This script delegates authentication to the installed ``gh`` client and records
only decoded response bodies plus selected public repository metadata.

Usage:
    python3 scripts/capture_github_traffic.py --output evidence/live/DATE/github-traffic-response.json
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess


OWNER = "tmccoy678"


def gh_json(path):
    result = subprocess.run(
        ["gh", "api", path],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def capture():
    repositories = gh_json(
        "user/repos?visibility=public&affiliation=owner&per_page=100&sort=full_name"
    )
    if len(repositories) >= 100:
        raise RuntimeError("Repository listing reached one page; add pagination before capture")

    owned = [
        repository for repository in repositories
        if repository["owner"]["login"] == OWNER and not repository["private"]
    ]
    records = {}
    for repository in sorted(owned, key=lambda item: item["name"].lower()):
        name = repository["name"]
        base = f"repos/{OWNER}/{name}"
        records[name] = {
            "metadata": {
                "name": name,
                "html_url": repository["html_url"],
                "created_at": repository["created_at"],
                "updated_at": repository["updated_at"],
                "pushed_at": repository["pushed_at"],
                "stargazers_count": repository["stargazers_count"],
                "forks_count": repository["forks_count"],
                "open_issues_count": repository["open_issues_count"],
                "visibility": repository["visibility"],
                "default_branch": repository["default_branch"],
            },
            "clones": gh_json(base + "/traffic/clones"),
            "views": gh_json(base + "/traffic/views"),
            "popular_referrers": gh_json(base + "/traffic/popular/referrers"),
            "popular_paths": gh_json(base + "/traffic/popular/paths"),
        }

    return {
        "schema": "github-owner-traffic-capture.v1",
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        "owner": OWNER,
        "repository_count": len(records),
        "collection": {
            "client": "GitHub CLI gh api",
            "scope": "all owner public repositories returned in one 100-item page",
            "traffic_window": "rolling 14-day response supplied by GitHub",
            "authentication_material_recorded": False,
            "http_headers_recorded": False,
        },
        "repositories": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    if arguments.output.exists():
        raise SystemExit(f"Refusing to overwrite existing evidence: {arguments.output}")
    payload = capture()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "output": str(arguments.output),
        "captured_at": payload["captured_at"],
        "repository_count": payload["repository_count"],
    }))


if __name__ == "__main__":
    main()

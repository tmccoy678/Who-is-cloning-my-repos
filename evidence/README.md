# Evidence provenance and source replay

The evidence comprises surviving October 17 and 19 research artifacts and pinned public-source files retrieved during the October 20 revision. Each manifest identifies the acquisition method and relevant timestamps.

## Current authenticated snapshot

[`live/2026-10-20/github-traffic-response.json`](live/2026-10-20/github-traffic-response.json) is the complete research response captured at 2026-10-20 14:30:13 UTC from GitHub's authenticated clone, view, popular-referrer, and popular-path endpoints for the six public repositories. It contains response data only; authentication headers and credentials were never written to the file. Its SHA-256 is `9efe0a041498518b44365b67756ffb0e56eb9990e73fbb9f29957516704fb1fd`.

[`live/2026-10-20/github-repository-metadata.json`](live/2026-10-20/github-repository-metadata.json) preserves selected public repository metadata retrieved from GitHub's repository endpoint, including descriptions, topics, language, stars, forks, dates, visibility, and default branch. It contains no credentials or headers. Its SHA-256 is `0c7e22764fea07cc312198f31b1764056a708502102e7c7bfca3e8312690289a`.

[`live/2026-10-20/comparison-repository-metadata.json`](live/2026-10-20/comparison-repository-metadata.json) preserves GitHub descriptions, topics, languages, and URLs for the two rate-stratum repositories and the nearest screened repository by range-to-mean percentage. It supports the subject labels in manuscript Table 5. Its SHA-256 is `7390d5dd9e4c0b4135c11fea6d6c76908bd88f40167e06104f43548ab73418cb`.

[`live/2026-10-20/codex-security-scan-history-summary.json`](live/2026-10-20/codex-security-scan-history-summary.json) records the read-only connected-app query, reduction method, total job count, daily and repository totals, first and last timestamps, and current usage state. [`../data/codex-security-scan-history-summary-2026-10-20.csv`](../data/codex-security-scan-history-summary-2026-10-20.csv) contains the reduced rows used in R. The reduction omits account and commit identifiers, email addresses, and generated threat-model bodies.

`scripts/analyze_and_plot.R` reads the preserved GitHub JSON, screened comparison table, and reduced Codex Security history locally. It creates the current long-form traffic table, window metrics, Security Cloud alignment metrics, and two manuscript figures. [`../figures/r-figure-provenance-2026-10-20.json`](../figures/r-figure-provenance-2026-10-20.json) records input hashes, code and lockfile hashes, software versions, derived-table hashes, and figure hashes. Regeneration performs no network requests.

## Surviving historical artifacts

[`recovery_manifest.json`](recovery_manifest.json) records the SHA-256, size, type, and original tool-call/completion UTC timestamps for 23 artifacts.

- `recovery/2026-10-17/public-repository-summary.jsonl`: original transformed command output for the six public repositories; private-repository rows were omitted.
- `recovery/2026-10-17/four-repository-daily-counts.tsv`: original `jq` output for the four focal repositories, October 3–16. The original has no header: columns are repository, UTC date, clone count, and daily uniques.
- `recovery/2026-10-17/five-repository-clone-summary.txt`: a later same-day transformed summary for those four repositories and WeatherTicker.
- `recovery/2026-10-19/*-clones.json`: six original API-client stdout bodies extracted from the session record. DobeWorks and DEGS view bodies also survive.
- `recovery/2026-10-19/comparisons/`: nine original temporary public-comparison downloads from the initial shortlist.
- `recovery/2026-10-19/find_daily_clone_series.py.txt`: original temporary parser, preserved as inert text. It was inspected and parsed for syntax, not executed during recovery.
- `recovery/2026-10-19/all-public-daily-clone-series.jsonl`: the original 138-record extraction output.
- [`recovery/2026-10-19/search-protocol.json`](recovery/2026-10-19/search-protocol.json): the exact seven queries, first-100-results-per-query limit, and extraction behavior reconstructed from the recovered parser and contemporaneous count output.

The session-derived JSON files preserve API-client stdout; HTTP headers were not recovered. The precise October 19 requests that wrote the CSV discarded their bodies, leaving earlier same-day stdout as corroborating evidence. The recovery hashes identify the bytes found during revision; historical hashes for the temporary files were not recovered.

Full October 17 clone/view JSON bodies were not found in the scoped original session and temporary artifacts. Neither the full 226-candidate ledger nor the seven individual query responses and fetch/parse rejection records were recovered. The parser kept its candidate dictionary in memory and saved only extracted results. These absences prevent reconstruction of the entire original search.

## Public retained-source replay

[`public/manifest.json`](public/manifest.json) identifies 138 files by their original immutable GitHub commit URLs and records retrieval timestamps and SHA-256 values. Their combined size is 2,630,351 bytes. These files were retrieved on October 20 from the pinned revisions.

[`public/replay-report.json`](public/replay-report.json) records a successful replay of all 138 historical six-day vectors against those pinned files. The result establishes extraction reproducibility for the retained set. Search completeness, observational provenance, independence among series, and GitHub-wide prevalence require separate evidence.

To repeat the retained-source replay without network access:

```sh
python3 scripts/recover_public_sources.py
```

This command verifies cached source hashes, repeats the extraction, and rewrites `public/manifest.json` and `public/replay-report.json`. The report receives a new generation timestamp; the cached source bytes and their original retrieval timestamps remain unchanged.

The optional `--download` flag fetches missing pinned sources, with a 5 MB per-file and 20 MB total cache limit. Its requests are limited to the recorded public commit URLs. The historical-recovery utility reads the original private archive through explicit local source arguments:

```sh
python3 scripts/recover_historical_evidence.py --session PATH --temporary-root PATH
```

This command writes the selected artifacts under `recovery/` and regenerates `recovery_manifest.json`, including its recovery timestamp.

## Extraction limitations and classifications

The original parser handles a JSON document or CSV and has no JSONL/NDJSON branch. It uses a date regex restricted to October 13–18, keeps the last record encountered for each date, examines only the first five nested array elements after direct date-record handling, and deduplicates identical JSON value vectors within a file. Its `repository` field identifies the source-host repository, which can differ from the repository measured by an archived series. Replay preserves these extraction rules; source classification establishes which extracted series enter the revised comparison.

Two specific provenance problems were established:

- [`fixture-classification.json`](public/provenance/fixture-classification.json) documents the `github-stats-action` fixture source and its builder's `manga-downloader` target. The clone counts' observational origin is unresolved. The builder's synthetic-data comment concerns stargazers only.
- [`multi-repository-classification.json`](public/provenance/multi-repository-classification.json) documents four repository records per date in SasanLabs' CSV. The original date-only parser retained the last `SasanLabs/SAFE` record while retaining `SasanLabs/VulnerableApp` as its source-host label.

The revised comparison excludes both rows and the two path-identified cumulative counters, retaining 134 extracted series. All 138 historical rows remain intact for audit. The four exclusions are applied separately in the revised analysis.

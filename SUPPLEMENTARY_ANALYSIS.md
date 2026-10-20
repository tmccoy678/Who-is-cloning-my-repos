# Supplementary Analysis and Reproduction

For *Who Is Cloning My Repositories? An Exploration of 598 Daily Clone Events Across Six Public Repositories From Exactly 8,372 Recorded Clone Events ÷ 14 Days—With 0 Visitors, 0 Views, No Referrals, Stars, Forks, or External Public Discussion for DobeWorks and DEGS at the Original Snapshot*.<br>
Revised October 20, 2026.

## Reproduce the current R analysis and figures

Open `Who-is-cloning-my-repos.Rproj` in RStudio and run:

```r
renv::restore()
source("scripts/analyze_and_plot.R")
```

The equivalent terminal command is:

```sh
Rscript scripts/analyze_and_plot.R
```

`renv::restore()` recreates the package environment pinned in `renv.lock` and is required only for a new or changed R library. The hand-written R script itself performs no network requests. It reads the preserved October 20 GitHub response, screened external-series table, and reduced Codex Security history. It validates complete daily coverage and window totals, cross-checks the October 13–18 focal statistics against the independent Python output, validates the 99-job/four-repository Security Cloud summary, rewrites three derived tables, then generates Figures 1 and 3 in PNG and vector PDF formats. The final run was sourced from RStudio Desktop 2026.10.0+233 “Blue Mistflower” using R 4.6.1. `figures/r-figure-provenance-2026-10-20.json` records execution context, input, code, lockfile, output, R, and package identities.

## Reproduce the independent preserved-window analysis

From the repository root, using Python 3.9 or later:

```sh
python3 scripts/analyze.py --check
python3 scripts/analyze.py
python3 -B -m unittest discover -s scripts -p 'test_analysis.py' -v
```

The first command validates the preserved CSV inputs without writing. The second generates `data/reanalysis-*` outputs. The tests check arithmetic, input integrity, explicit exclusions, and deterministic regeneration. The analysis uses the Python standard library. Plotting has separate dependencies and instructions in the plotting script.

The generated `data/reanalysis-summary.json` contains source hashes, original totals, window overlap, comparison exclusions, count-rate summaries, and account statistics. `data/reanalysis-window-metrics.csv` reports every focal series over October 5–18, October 13–18, and October 17–18, and the four high-traffic repositories over the recovered original October 3–16 window. `data/reanalysis-comparison-series.csv` preserves the link from each original row to its inclusion decision and recalculated values. Undefined relative statistics are represented explicitly. This Python workflow is retained as an independent implementation of the historical analysis; it is no longer the manuscript figure renderer.

## What was preserved and recovered

The six original CSV inputs remain unchanged. They are derived research records, not raw HTTP responses. The revision adds recovered collection evidence and new, independently executable calculations. `evidence/recovery_manifest.json` records the identity, byte length, provenance kind, and original call times of the recovered artifacts.

The recovered evidence includes:

- October 17 transformed client output for six public-repository summaries and a four-repository daily table;
- October 19 client-output JSON for all six focal clone series and DobeWorks/DEGS views;
- the original comparison-search parser, preserved as inert text;
- its 138-record JSONL extraction output and seven-query search protocol; and
- original downloads for several public comparisons.

The recovered October 19 responses were collected earlier that day than the CSV-writing calls. Their values corroborate the retained CSVs; their capture times identify them as separate response bodies. Session recovery copies selected research output; private conversations and unrelated account records are excluded. Later retrieval of a public file at its recorded Git commit is separately identified as a revision-time retrieval.

Full October 17 response bodies and the complete original 226-candidate/rejection ledger were not recovered. The original parser and output establish the search procedure and retained results. Candidate-level rejection reasons remain unavailable. Today’s rolling endpoint cannot restore an expired historical window.

All 138 retained public-source files were retrieved at their original immutable commits during revision. Replay reproduced all 138 historical vectors. The recovered original four-repository daily table reproduces the October 17 totals, and all 48 overlapping repository-days agree with the follow-up data. The [evidence guide](evidence/README.md) records file types, acquisition times, hashes, and the offline replay command:

```sh
python3 scripts/recover_public_sources.py
```

Offline replay reads the cached source files and rewrites the manifest and replay report, including the report's generation time. Original retrieval timestamps and cached bytes remain unchanged.

## Search protocol and screening

The original search made seven Code Search requests with `per_page=100`, without pagination. A set keyed by repository and file path produced the recorded count of 226 candidates. The parser attempted JSON and CSV, kept positive-mean series containing all six target dates, retained the last encountered record for repeated dates, and collapsed identical value vectors within a file. Its input branches cover JSON documents and CSV files; JSONL input is absent. The recovered query text and source script are retained in `evidence/recovery/2026-10-19/`.

Of the 138 extracted series, two cumulative counters were excluded in the original analysis. I also excluded the `elboletaire/github-stats-action` fixture-path series because the observational provenance is uncertain. Its fixture builder identifies the measured repository as `elboletaire/manga-downloader`; archive host and measurement target are different fields. The builder's synthetic-data comment concerns stargazers, leaving the clone counts' origin unresolved.

A second new exclusion concerns `SasanLabs/VulnerableApp`'s `metrics/traffic.csv`, which contains four repositories per date. The date-only parser retained the last `SasanLabs/SAFE` record while labeling the source host `SasanLabs/VulnerableApp`. I excluded that ambiguous extraction and preserved the original row and source for inspection. The [classification record](evidence/public/provenance/multi-repository-classification.json) documents the collision.

The screened set contains 134 series in 34 source-host repositories. Two tracker hosts supply 99 series (73.88%). A host may archive multiple measurement targets; this clustering prevents treating the rows as an independent sample of GitHub. The `source_host_repository`, source path, and subpath identify each extracted record. Target identities require source-level verification.

## Rate and window sensitivity

The original 1%–4% criterion and the revised at-most-4% criterion each find zero matches in the screened data, for both range-to-mean and maximum-deviation measures. The nearest range remains `dikeckaan/easy-vphone`, with mean 79.67/day, range-to-mean 27.62%, maximum deviation 15.48%, and sample CV 9.68%.

There are 118 series below 25 clones/day, including 76 below one/day. The screened corpus's median mean is 0.67/day. For a nonconstant integer series, range is at least one, so a mean below 25 entails a range-to-mean percentage above 4%. This constraint explains why the numerical threshold is a poor comparison for much of the corpus.

An exploratory 100–200/day stratum contains two series: `Romaxa55/MegaV_Public` (194.67/day; range 87.84%; CV 35.29%) and `databricks-solutions/consort` (127.83/day; range 191.66%; CV 72.02%). The band was selected during revision around the focal rate. Its size is insufficient to estimate a population anomaly rate.

The October 3–16 and October 6–19 windows overlap by 11 days. The shared external-comparison interval remains October 13–18; the current continuation extends through October 19. The four-repository aggregate has a 0.90% sample CV and a 2.45% range-to-mean percentage over October 13–19, compared with a 7.40% CV in the original October 3–16 interval and 7.43% in the current October 6–19 interval. Across the three new dates, October 17–19, the aggregate CV is 1.22%. The individual-repository metrics are reported alongside the aggregate in the generated R window table. Each rolling total remains attached to its own window.

The two current analytical figures use the R-generated tables. [Figure provenance](figures/README.md) identifies their source and output hashes. The original eight images remain preserved in Git history and the six original source screenshots remain in the working tree; the main manuscript uses the original overview screenshot and two R figures. The unique-cloner figure was removed because the undeduplicated cross-repository sum restricted interpretation and the exact comparison was clearer in prose.

## Codex Security Cloud evidence

The connected read-only scan-history query returned 99 successful commit-scan jobs and no failed or unfinished jobs. Eighty-one began on September 28, two on October 2, three on October 5, nine on October 6, and four on October 11. The repository totals are 45 for TrashTreasurePickup, 36 for DobeWorks, 12 for DEGS, and six for BackspaceTextRetention. Those are exactly the four repositories displayed as monitored in the supplied dashboard captures.

The full connected response contained generated threat models and identifiers unnecessary for this analysis. The preserved reduction keeps repository names, UTC dates, counts, success counts, and first/last start times. Its JSON record states the query and omitted fields. The R workflow validates the exact four-repository set, total jobs, success count, current-window scan dates, and last scan timestamp before producing the alignment table or Figure 1.

Within the October 6–19 traffic window, DobeWorks had nine recorded scan jobs on its 272-clone peak day, 130 above its no-scan-day median of 142. TrashTreasurePickup had four recorded jobs on its 235-clone peak day, 93 above its no-scan-day median. These scan-job observations rank first and second among the 56 focal repository-days. No completed scan job is recorded after October 11, while the stable four-repository aggregate continues through October 19. The read-only interface does not expose Cloud repository-acquisition events, so the recorded-job history cannot allocate individual GitHub clone events.

## Corrections to historical tables

The original October 17 CSV’s `TOTAL` row retains a unique-visitors value of `2`, the arithmetic sum of two repository-level values. Account-wide visitor overlap is unknown. The revised manuscript marks this cell “Not additive,” and the generated summary uses `null` for both account-wide unique measures. The source row remains available for tracing the correction.

The account-age comparison has 32 rows, all created August 9, 2026. Taking the first 50 ascending results truncated the nominal August 9–11 search to August 9 accounts. The observed median public-repository count is 5; 27 accounts have zero stars, 28 have zero followers, and 31 have zero forks in the inspected sets. Earlier prose reported 6 and 28 for the first two figures. The generated account summary corrects those values. This sample supplies contextual public-engagement data; its clone traffic is unavailable and stays outside the main comparison.

The original subject-related table and closest-series table remain preserved with their source commits. The two recorded AgentHarbor source commits return identical JSON bytes, so their different identifiers do not change the calculations.

## Known owner activity and event interpretation

The original investigation identified an owner-authorized October 2 usability review that cloned the then-public repositories. That date falls before the October 3–16 analysis window. A separate October 19 architecture review acquired fresh copies; the current follow-up includes that date, and the daily aggregate cannot isolate its contribution. The inventory of owner-side automation is incomplete.

GitHub Community discussion #208852 documents a public-repository traffic interruption after September 23 and a GitHub staff statement on September 30 that a fix had shipped. This platform event overlaps the beginning of the preserved history. The October 13–19 continuation occurs after the reported fix and remains the cleanest interval for describing sustained regularity.

Push dates, recorded Codex Security jobs, and clone spikes can be aligned by UTC day. Within-day order and actor identity are unavailable. Repository-local Actions histories describe another acquisition route. The exact monitored-set match makes Codex Security Cloud the leading candidate mechanism, while a controlled monitoring intervention remains necessary to estimate its contribution to the recurring floor.

## Materials outside the manuscript’s empirical claims

The engineering review and replacement-cost scenarios remain in `READ_ONLY_REVIEW_AND_VALUATION.md` and `COMPARABLE_SYSTEMS_COST_CONTEXT.md` as separate portfolio material. Their labor-hour estimates are judgment-based scenarios. Career and academic material remains under `academic-context/`. These materials are not variables or supporting observations in the clone-traffic analysis.

The pre-revision manuscript, original comparison tables, and earlier interpretations remain recoverable in Git history at `25c4a40b8f5932acf7e054b66a5a586268f9da3a`. `REVISION_NOTES.md` records the response to the methodological review.

# Reanalysis of preserved clone-traffic tables

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

The original window contains 8,372 clones
and a mean of 598/day. The
follow-up window overlaps 12 of its 14 dates. `reanalysis-window-metrics.csv`
compares October 5–18, October 13–18, and the two new dates October 17–18.
When the recovered original daily TSV is present, it also includes October 3–16
for the four focal repositories and checks their 48 overlapping repository-days.
It never adds overlapping rolling totals.

Of 138 extracted series, two cumulative counters remain excluded, one fixture-path
series is excluded because its observational provenance is unverified, and one
multi-repository source is excluded because same-date rows were overwritten
without preserving measured-repository identity. The fixture exclusion follows
from its unresolved observational origin. The screened set contains 134 series
from 34 source-host repositories. A host can archive several measured
repositories, creating dependence among rows. The two largest hosts supply
99 series.

There are 118 screened series below 25 clones/day.
For a nonconstant integer-count series, range is at least one; when mean is below
25, range/mean exceeds 4%. Comparability of count variation depends on rate and
acquisition. No screened series meets either
the original 1–4% criterion or a <=4% criterion. The 100–200/day sensitivity
stratum contains only 2 series; it is post hoc and too small
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

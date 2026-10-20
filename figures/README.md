# Figure Provenance

The original eight images remain preserved under their existing filenames. Original files 1 and 2 are byte-identical copies of the supplied captures. Original files 3–6 are unedited window captures of the cited primary webpages made with the isolated Codex browser. Original files 7 and 8 are charts from the earlier analysis.

The revised manuscript numbers its selected figures separately: Figure 1 is the R scan-alignment result, Figure 2 is the original GitHub Traffic screenshot, and Figure 3 is the R rate–variation comparison. This numbering leaves the historical filenames stable.

## Revised Analytical Figures

| Manuscript figure | Files | Data and purpose |
|---|---|---|
| 1 | [PNG](r-window-sensitivity-2026-10-20.png), [vector PDF](r-window-sensitivity-2026-10-20.pdf) | October 6–19 authenticated daily counts with recorded Codex Security scan dates; shows scan-aligned spikes and continuation after the final recorded job |
| 3 | [PNG](r-rate-comparison-2026-10-20.png), [vector PDF](r-rate-comparison-2026-10-20.pdf) | Recalculated six-day rates and relative variation; shows the integer-count lower bound, 134 screened external series, and the two-series 100–200/day stratum |

[The R provenance manifest](r-figure-provenance-2026-10-20.json) records the execution context, raw and derived input hashes, code and lockfile hashes, output hashes, R version, and package versions. Both analytical figures use black-and-white marks and were reopened for visual inspection. The final figures were generated from RStudio Desktop 2026.10.0+233 “Blue Mistflower” with R 4.6.1, cowplot 1.2.0, digest 0.6.39, ggplot2 4.0.3, jsonlite 2.0.0, ragg 1.5.2, rstudioapi 0.19.0, and scales 1.4.0. [`renv.lock`](../renv.lock) pins the complete R package dependency graph.

Open `Who-is-cloning-my-repos.Rproj` in RStudio and run:

```r
renv::restore()
source("scripts/analyze_and_plot.R")
```

`renv::restore()` is required only when recreating the recorded dependency environment. The equivalent analysis command is `Rscript scripts/analyze_and_plot.R`. The hand-written R script reads the preserved raw response, screened comparison CSV, and reduced Codex Security scan history without network access. It validates daily coverage and totals, cross-checks its six-day focal metrics against the independent Python output, validates the four-repository/99-job Security Cloud summary, regenerates three current derived tables, and writes the two PNG/PDF pairs plus the provenance manifest. Fonts, PDF timestamps, and rendering-library versions can affect output bytes; the manifest identifies the produced files.

The earlier unique-cloner chart was removed during visual-quality review. Its repository-level unique counts could not be deduplicated across repositories, and its main observation was clearer as an exact textual comparison. Removing it leaves each manuscript figure with a separate analytical purpose.

The earlier Python-rendered `reanalysis-*` figures remain in Git history at revision `71bb9e1`; the manuscript now uses the R figures.

## Preserved Original Figures

| File | Type | Capture date | Source | SHA-256 |
|---|---|---|---|---|
| [`figure-1-degs-traffic-overview-2026-10-14.png`](figure-1-degs-traffic-overview-2026-10-14.png) | Original screenshot | 2026-10-14 | [GitHub Traffic page for tmccoy678/DEGS-v2.1](https://github.com/tmccoy678/DEGS-v2.1/graphs/traffic) | `8041a8e3ddb9f2aea90b2d1951f26d0f8091f37aaba3e2aa66b65ed6bec194d7` |
| [`figure-2-degs-unique-cloners-2026-10-14.png`](figure-2-degs-unique-cloners-2026-10-14.png) | Original screenshot | 2026-10-14 | [GitHub unique-cloner chart for tmccoy678/DEGS-v2.1](https://github.com/tmccoy678/DEGS-v2.1/graphs/traffic) | `fbdb66024932d88b22f33fc00bcf918267a4a664ff7aba7bad4c8a032fbf2e37` |
| [`figure-3-github-clone-api-documentation.png`](figure-3-github-clone-api-documentation.png) | Source-page screenshot | 2026-10-19 | [GitHub repository traffic API documentation](https://docs.github.com/en/rest/metrics/traffic#get-repository-clones) | `efe846f5391334a753f1c1e6b839474c4aae67764c826d7f6a113de2e7671b9c` |
| [`figure-4-github-public-events-api.png`](figure-4-github-public-events-api.png) | Source-page screenshot | 2026-10-19 | [GitHub public-events API documentation](https://docs.github.com/en/rest/activity/events#list-public-events) | `91631a8f090b3aad4285738fb9f19054e4f61d3343a62732bccf436ac0855b2a` |
| [`figure-5-ecosystems-sync-documentation.png`](figure-5-ecosystems-sync-documentation.png) | Source-page screenshot | 2026-10-19 | [ecosyste.ms synchronization documentation](https://github.com/ecosyste-ms/repos/blob/main/docs/syncing.md) | `f7c6f48a04814c26f971ee6b3a626455a0bd09b8ddfdbc1b6246ed8a323c5c96` |
| [`figure-6-funasr-traffic-comparison.png`](figure-6-funasr-traffic-comparison.png) | Source-page screenshot | 2026-10-19 | [ModelScope FunASR traffic-funnel snapshot](https://github.com/modelscope/FunASR/blob/main/docs/community_growth_20k.md#traffic-funnel-snapshot) | `e425f5d6e46867e23bdd39d1415d7f94c150f9611ccedb7dd8e44cd7af20ed47` |
| [`figure-7-daily-clone-regularity-2026-10-19.png`](figure-7-daily-clone-regularity-2026-10-19.png) | Study-generated chart | 2026-10-19 | [`traffic-snapshot-2026-10-19.csv`](../data/traffic-snapshot-2026-10-19.csv) from authenticated GitHub Traffic API | `3e692651798bcaeaeaa92bd5e93ccb8a147097d5d0dcf121973a2816ebc13d25` |
| [`figure-8-six-day-variation-comparison-2026-10-19.png`](figure-8-six-day-variation-comparison-2026-10-19.png) | Study-generated comparison chart | 2026-10-19 | [`same-six-day-variation-comparison-2026-10-19.csv`](../data/same-six-day-variation-comparison-2026-10-19.csv) from authenticated and owner-published GitHub Traffic data | `9e3610cc00cb0d8bfdb2afca0bcb37a16061d9bf5e5e269e4135694686e8b381` |

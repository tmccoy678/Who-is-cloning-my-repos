# Figure Provenance

The original eight images remain preserved under their existing filenames. Original files 1 and 2 are byte-identical copies of the supplied captures. Original files 3–6 are unedited window captures of the cited primary webpages made with the isolated Codex browser. Original files 7 and 8 are charts from the earlier analysis.

The revised manuscript numbers its selected figures separately: Figure 1 uses the original overview screenshot; Figures 2 and 3 use the new window-sensitivity and rate-comparison plots below. This numbering leaves the historical filenames stable.

## Revised Analytical Figures

| Manuscript figure | Files | Data and purpose |
|---|---|---|
| 2 | [PNG](reanalysis-window-sensitivity.png), [vector PDF](reanalysis-window-sensitivity.pdf) | Preserved October 5–18 daily counts and recalculated window metrics; distinguishes the full window, selected six-day interval, and two new dates |
| 3 | [PNG](reanalysis-rate-comparison.png), [vector PDF](reanalysis-rate-comparison.pdf) | Recalculated six-day rates and relative variation; shows the 134 screened external series and the two-series 100–200/day stratum |

[The provenance manifest](reanalysis-provenance.json) records the input, output, and plotting-script hashes and library versions. Both figures use black-and-white marks and were reopened for visual inspection. The analysis uses Python's standard library; plotting additionally requires Matplotlib and NumPy. The recorded environment used Python 3.14.7, Matplotlib 3.11.2, and NumPy 2.5.4.

From the repository root, in an environment with those plotting dependencies:

```sh
python3 scripts/analyze.py
python3 scripts/plot_reanalysis.py
```

The plotting script writes only the new `figures/reanalysis-*` files. Fonts and rendering-library versions can affect output bytes; the manifest identifies the produced files.

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

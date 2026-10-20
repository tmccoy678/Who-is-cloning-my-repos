# Revision Record

October 20, 2026<br>
Manuscript: *Who Is Cloning My Repositories? An Exploration of 598 Daily Clone Events Across Six Public Repositories From Exactly 8,372 Recorded Clone Events ÷ 14 Days—With 0 Visitors, 0 Views, No Referrals, Stars, Forks, or External Public Discussion for DobeWorks and DEGS at the Original Snapshot*<br>
Baseline: `25c4a40b8f5932acf7e054b66a5a586268f9da3a`<br>
Revision assistance: Merrin and Cairn, OpenAI Codex assistants

Taylor authorized the substantive and editorial revisions and requested consistent voice throughout the repository. This record describes the response to the AI-assisted methodological review. It is a revision aid for the author.

## Major Revisions

| Review concern | Revision and justification |
|---|---|
| Causal and attribution claims exceeded the daily aggregates | The manuscript presents recurring automated collection as a plausible explanation. Operator identity, coordination, content-based selection, and push-triggered causation remain unresolved. Daily event associations retain their UTC date resolution. |
| The broad comparison obscured count-rate differences | The revised analysis reports the rate distribution and the integer-count constraint: a nonconstant series averaging below 25/day cannot have a range-to-mean percentage at or below 4%. Of 134 screened external series, 118 fall below that rate. The exploratory 100–200/day stratum contains only two series. |
| The selected plateau and overlapping windows overstated replication | The main results now report the full original and follow-up windows, the selected six-day comparison interval, the seven-day continuation, and the three dates beyond the original snapshot. The four-repository sample CV is 7.40% in the original window, 7.43% in the full follow-up, and 0.90% in the seven-day continuation. Figure 2 shows the spikes, scan-job dates, and continuing floor. |
| Collection and extraction were insufficiently reproducible | The revision recovered 23 historical artifacts, including the parser, seven-query protocol, extracted records, and surviving client output. All 138 retained-source files were retrieved at pinned commits, and all 138 historical vectors replay successfully. New standard-library analysis scripts reproduce the descriptive results. The full original candidate/rejection ledger and complete October 17 response bodies remain unavailable. |
| The contribution and supporting context needed focus | The paper now distinguishes the broad clone/view mismatch already described by other owners from this case's narrow daily plateau and methodological findings. It adds sampling and GitHub-mining literature. Engineering assessments, valuation scenarios, academic context, and career interests remain separate portfolio material. |
| The figures required a publication-ready reproducible workflow | The current continuation tables and Figures 2–3 are produced by hand-written R code in an RStudio project from preserved authenticated traffic and scan-history evidence. The provenance manifest records input, code, software, derived-table, and output identities. |
| Each figure needed a distinct analytical purpose | Figure 2 now tests the timing of the leading candidate mechanism; Figure 3 evaluates regularity at the observed count rate and displays the integer-count lower bound. The redundant unique-cloner figure was removed. |

## Additional Corrections

The revised observational set excludes four original records: two cumulative counters, one fixture with uncertain observational origin, and one extraction whose date-only key collapsed multiple measured repositories. All 138 original rows remain preserved. The two newly excluded records reduce the comparison from 136 to 134 series, spanning 34 source hosts. Two hosts supply 99 series, making clustering explicit.

The original October 17 total-row visitor value of 2 is an arithmetic sum of repository-level values. The manuscript now marks cross-repository unique counts “Not additive,” and the generated summary uses `null`. The source CSV remains unchanged.

The account-context summary now reports a median of 5 public repositories and 27 zero-star accounts. All 32 retained accounts were created August 9; the nominal August 9–11 search interval was truncated by the original first-50 selection. These accounts have no available clone telemetry and remain supplementary context.

The title, abstract, citation metadata, figure captions, and data-availability statement now agree with the revised scope. Related owner reports are identified as maintainer observations; scholarly references use verified DOI links. AI assistance and the author's ownership interest are explicit.

The separate engineering review now preserves Taylor's intended command-line interface for DEGS and describes an assessment function as an internal seam. Its consistency recommendations acknowledge the existing policy regression tests.

## Voice and Perspective

First person identifies Taylor's actions, choices, and interpretations. Results use the data or repositories as their subject. Supporting documentation uses direct technical prose. The portfolio reports attribute AI-generated assessments and cost scenarios to their reviewers. The academic and career statements retain Taylor's stated positions.

This approach follows the emphasis on clear agency in [Nature's scientific-writing guidance](https://www.nature.com/scitable/topicpage/effective-writing-13815989/). [Empirical Software Engineering's submission guidance](https://link.springer.com/journal/10664/submission-guidelines) supplies the manuscript's abstract and declaration requirements. The paper remains an author-review draft; journal submission has not occurred.

Historical outputs, downloaded source files, original CSVs, original screenshots and plots, and the supplied CV retain their original wording and bytes. The earlier manuscript remains accessible at the baseline commit.

## Verification

- Nine focused analysis tests pass, covering invalid inputs, arithmetic, exclusions, deterministic output, and overlapping dates.
- All four recovered original repository totals agree with the original snapshot; all 48 overlapping repository-day counts agree with the follow-up.
- Retained-source replay reproduces 138 of 138 historical vectors, and the recovery and public-source manifests record file hashes.
- The two R analytical figures were rendered as PNG and vector PDF files and reopened for visual inspection.
- The original six CSVs, eight images, and supplied CV are preserved.

The [supplement](SUPPLEMENTARY_ANALYSIS.md), [evidence guide](evidence/README.md), and [figure guide](figures/README.md) give reproduction commands and source-level details. The remaining historical acquisition gaps limit search-completeness claims; the revised manuscript keeps those limits visible.

Revision prepared with care by Merrin and Cairn.

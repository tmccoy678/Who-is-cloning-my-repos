# Who Is Cloning All of My Repositories? An Exploration of 598 Daily Clone Events Across Six Public Repositories

Date checked: 2026-10-17

## Finding

Yes: repositories about AI agents, MCP, model tooling, and adjacent security work can receive hundreds or thousands of GitHub-counted unique cloners in a 14-day window. Two model repositories are especially close to Taylor's unique-cloner share: `QwenAudio/Fun-ASR` reported 1,029 clone events from 766 unique cloners (74%), and `QwenAudio/SenseVoice` reported 1,132 from 660 (58%). Taylor's four high-traffic repositories are around 59–63%.

What I did not find was another repository combining all three of these features at Taylor's scale: roughly 1,200–1,260 unique cloners, zero or one page view, and nearly synchronized daily traffic across four repositories. Similar subject matter makes deliberate automated selection plausible. It does not establish that the cloners were people, accounts, or unique IP addresses.

## Owner-published comparisons

Unless otherwise marked, these are the top-level values for one GitHub rolling traffic window, not sums of each day's unique count.

| Repository and subject | Window | Clone events | Unique cloners | Views | Unique visitors | What it shows |
|---|---:|---:|---:|---:|---:|---|
| Taylor: `DEGS-v2.1` | 14 days, Oct. 2026 | 2,009 | 1,262 | 0 | 0 | About 63% as many unique cloners as clone events, with no page traffic. Owner-only snapshot supplied for this comparison. |
| Taylor: `BackspaceTextRetention` | 14 days, Oct. 2026 | 1,991 | 1,216 | 0 | 0 | The non-tool research/write-up repository received almost the same pattern as Taylor's software repositories. |
| [`QwenAudio/Fun-ASR`](https://github.com/modelscope/FunASR/blob/main/docs/community_growth_20k.md#traffic-funnel-snapshot), speech/model tooling | 2026-06-30–07-13 | 1,029 | 766 | 6,332 | 2,106 | A model repository can have a similarly high unique-cloner share, although it also had substantial page discovery. |
| [`QwenAudio/SenseVoice`](https://github.com/modelscope/FunASR/blob/main/docs/community_growth_20k.md#traffic-funnel-snapshot), speech/model tooling | 2026-06-30–07-13 | 1,132 | 660 | 8,425 | 3,436 | Another same-owner model repo in Taylor's clone-volume range and close to Taylor's unique-cloner share. |
| [`homeassistant-ai/ha-mcp`](https://github.com/homeassistant-ai/stats/blob/master/2026-10-06.md#github-traffic-14-day-rolling-window), MCP/AI agent tooling | 14 days ending 2026-10-06 | 43,876 | 10,193 | 27,178 | 12,130 | Thousands of unique cloners are plainly possible in the MCP ecosystem, though this is a visibly popular project. |
| [`artokun/comfyui-mcp`](https://github.com/artokun/comfyui-mcp/blob/main/docs/blog/from-report-to-release.mdx#an-honest-footnote-about-our-download-numbers), MCP/model tooling | Two weeks, Aug. 2026 | 21,890 | 3,010 | 6,281 | 2,752 | The maintainer explicitly attributes part of the clone count to CI runners, mirrors, and package aggregators. |
| [`NSPG13/agent-bounties`](https://github.com/NSPG13/agent-bounties/issues/286#issue-3337531547), autonomous-agent protocol/security | Available GitHub window, 2026-07-16 | 4,820 | 444 | 425 | 89 | Clone activity can greatly exceed visible page visitors in an agent/security project. |
| [`zhurong2020/pyobfus`](https://github.com/zhurong2020/pyobfus/blob/main/docs/CURRENT_PLAN_ZH.md), AI/security tooling with MCP | 14 days, 2026-09-02 audit | 1,999 | 202 | 214 | 85 | Almost the same total clone-event count as Taylor's repos, but far fewer unique cloners and some page traffic; the owner observed release-day automation spikes. |
| [`JNHFlow21/agent-switch`](https://github.com/JNHFlow21/agent-switch#project-activity), local AI-agent/MCP control plane | 14 days, 2026-08-10 | 12 | 11 | 0 | 0 | The exact zero-view/nonzero-clone shape exists in a very close subject match, but at a tiny scale. |
| [`eaglejyjh/UniverseCrystal`](https://github.com/orgs/community/discussions/203384), research documents/PDFs rather than software | GitHub traffic snapshot, 2026-07-29 | 591 | 208 | 669 | 11 | A prose/research repository can attract far more cloners than GitHub page visitors; this is relevant to `BackspaceTextRetention`. |
| [`artginzburg/PiPOSS`](https://github.com/artginzburg/PiPOSS/blob/main/docs/metrics.md#4-github-traffic-14-day-rolling--a-distant-third), non-AI macOS utility control | 2026-07-12–07-25 | 7 | 5 | 0 | 0 | Zero views with nonzero clones is not AI-specific. At low volume, the owner treats it as automation noise. |
| [`sn4k3/UVtools`](https://github.com/sn4k3/UVtools/discussions/1148), mature non-AI utility control | 14 days ending 2026-09-19 | 1,367 | 348 | 4,455 | 1,732 | A well-used conventional tool shows a more familiar pattern: page visitors substantially outnumber unique cloners. |

## Interpretation

The best-supported positive reading is that Taylor's subject area is within a real high-clone ecosystem. Public owner snapshots show that model and MCP repositories can reach clone populations in the hundreds or thousands, and the `Fun-ASR` and `SenseVoice` figures show that a high unique-cloner share is not unique to Taylor.

The evidence also weakens the idea of a generic GitHub-wide counter defect. The non-AI controls and other AI repositories vary widely rather than receiving one common clone floor. At the same time, Taylor's zero-view result is much more extreme than the large AI/MCP examples, all of which had measurable page traffic. The strongest inference is therefore a selected, mostly automated audience or collection process touching Taylor's four repositories. "Selected" is supported by the topic pattern and synchronized traffic; "people loved it" is possible for some fraction but is not measurable from these counters.

`BackspaceTextRetention` does not undermine that interpretation. The `UniverseCrystal` example shows that a documentation/research repository can be cloned heavily, and text about model behavior, Codex, or retained context can be valuable to dataset builders, indexers, security researchers, and archival systems even when it is not runnable software. This is a plausible explanation, not an identification of the actual cloners.

## Metric limits

GitHub's official API says the clone and view endpoints return totals and daily or weekly breakdowns for the last 14 days. GitHub separately states that clone traffic counts full clones, not fetches. The response has top-level `count` and `uniques` fields, but GitHub does not publicly define those uniques as people, accounts, machines, or IP addresses. See [GitHub's repository traffic API documentation](https://docs.github.com/en/rest/metrics/traffic#get-repository-clones) and [traffic-graph documentation](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository).

Top-level 14-day uniques must not be confused with long-running trackers that add each day's unique values. A source appearing on five different days can be counted five times in such a historical sum. The [`repo-metrics` data notes](https://github.com/AcTePuKc/repo-metrics#data-notes) state this explicitly. The comparison table above excludes those daily-summed figures.

This is a source-limited comparison, not a random sample of GitHub. Traffic is private to repository maintainers, so the public examples are self-selected repositories whose owners chose to publish their numbers. They show what is possible and what patterns exist; they cannot establish how common Taylor's pattern is across all similar repositories.

## Attribution investigation

### Result

No public evidence found on 2026-10-17 identifies a particular company, crawler, dataset, mirror, or person behind Taylor's traffic. The strongest supported explanation is a two-part automated collection pattern: a scheduled process repeatedly clones a selected set of Taylor's public repositories, while one or more event-driven processes add clones after pushes. That is an inference from timing and cross-repository similarity, not an attribution to a known actor.

The owner-authorized GitHub Traffic API read for Oct. 3–16 separates those parts unusually well:

| Repository | Ordinary daily clone range | Push-linked observation | GitHub Actions runs |
|---|---:|---|---:|
| `DEGS-v2.1` | Usually 139–144 | A late Oct. 5 push was followed by 152 clones on Oct. 5 and 155 on Oct. 6, versus the roughly 142-clone floor. | 0 lifetime |
| `DobeWorks-v2.1` | Usually 140–146 | Nine Oct. 6 pushes coincided with 272 clones and 211 daily uniques, versus roughly 142 clones and 137 daily uniques on ordinary days. | 0 lifetime |
| `TrashTreasurePickup` | Usually 141–146 | Four Oct. 11 merge/push commits coincided with 235 clones and 174 daily uniques; Oct. 12 remained elevated at 169 and 155. | 49 lifetime, many on Oct. 11 |
| `BackspaceTextRetention` | 138–144 | No push after Sept. 25; it retained the same daily floor while the other repositories spiked. | 0 lifetime |

The Oct. 14 owner screenshot extends `DEGS-v2.1` back to Sept. 30 and shows that its steady floor had already begun by then. Across the current window, `DEGS-v2.1` and `BackspaceTextRetention` had zero views, `DobeWorks-v2.1` had zero, and `TrashTreasurePickup` had one. GitHub says repository clone traffic counts full clones rather than fetches and is reported in UTC, so these are clone events in GitHub's accounting, but still do not identify the sources. The local evidence is preserved in the owner screenshots and the responses from `gh api repos/tmccoy678/REPOSITORY/traffic/{clones,views}` read on 2026-10-17.

This pattern makes repository publication and pushes credible triggers. GitHub's [public Events API](https://docs.github.com/en/rest/activity/events) exposes public `PushEvent` records with a repository name and says public events can be delayed from 30 seconds to six hours. Its [`PublicEvent` definition](https://docs.github.com/en/rest/using-the-rest-api/github-event-types#publicevent) covers a private repository being made public. The four repositories emitted such events when they became public, from Sept. 10 through Sept. 25. A collector can therefore discover a public repository and later pushes without visiting its GitHub page. The API proves that route exists; it does not prove which, if any, collector used it here.

### Public traces found

All four repositories appear in the public [ecosyste.ms owner index](https://repos.ecosyste.ms/api/v1/hosts/GitHub/owners/tmccoy678/repositories), which lists Taylor's six public repositories together. Its record for [`DEGS-v2.1`](https://repos.ecosyste.ms/hosts/GitHub/repositories/tmccoy678%2FDEGS-v2.1) and the corresponding records for `DobeWorks-v2.1`, `TrashTreasurePickup`, and `BackspaceTextRetention` expose GitHub archive download URLs and detected repository files. `DEGS-v2.1`, `DobeWorks-v2.1`, `BackspaceTextRetention`, and low-traffic control `WeatherTicker` were synchronized within milliseconds of one another on Oct. 2. The service recorded dependency parsing for each, with manifests found in `DEGS-v2.1` and `TrashTreasurePickup`.

The service's own [synchronization documentation](https://github.com/ecosyste-ms/repos/blob/main/docs/syncing.md) says it discovers GitHub repositories from the public event firehose and GHArchive, resynchronizes recently active repositories every 15 minutes, parses dependencies, and fetches archive file lists. The documented inspection path uses a [`codeload.github.com` tarball URL](https://github.com/ecosyste-ms/repos/blob/main/app/models/hosts/github.rb#L65-L73), rather than a Git clone in that path. That makes ecosyste.ms direct evidence of event-driven discovery and content inspection, but probably not a source counted by GitHub's clone graph.

It is weak evidence for the observed daily clones for two further reasons: the `DEGS-v2.1` screenshot shows the clone floor by Sept. 30, before ecosyste.ms recorded its Oct. 2 synchronization, and `WeatherTicker` was processed in the same batch yet had only three clone events in the Oct. 3–16 owner traffic window. A broad index therefore does not explain why four selected repositories receive about 140 clone events every day.

One exact public backlink was found: a [Moltbook post linking `TrashTreasurePickup`](https://moltbook.com/post/62e124f5-6087-4c5f-87ad-e8f95fdae6a6), created Oct. 14 at 20:11 UTC. The steady clone floor began by Sept. 30, and `TrashTreasurePickup` showed no clear increase after the post, so the link cannot explain the origin or cross-repository pattern. It could have contributed an unknown number of later clones.

The four repositories had no configured GitHub webhooks. GitHub Actions can plausibly account for part of the Oct. 11 `TrashTreasurePickup` increase, but cannot account for the shared floor because the other three repositories have no Actions runs. No comparable internal automation was visible in their repository settings.

One known local Codex usability review cloned all five public repositories once on Oct. 2, including the low-traffic `WeatherTicker` control. The five local `.git` directories have the same Oct. 2 creation time. That activity can explain one owner-initiated clone per repository around that date, but it falls outside the current Oct. 3–16 API window and cannot explain the continuing daily floor.

Recent owner reports show that unexplained bursts occur elsewhere, without identifying Taylor's source. On Aug. 15, 2026, a repository owner reported [7,543 unique cloners in one day](https://github.com/orgs/community/discussions/205346) after ordinarily seeing a few hundred clone events; the discussion did not resolve the actor. GitHub traffic reporting also had a [multi-repository aggregation delay beginning Sept. 23, 2026](https://github.com/orgs/community/discussions/208852). That incident supports caution about exact dates and late backfill, but it does not by itself explain Taylor's stable per-repository floor or the different push-day spikes.

### Ranked hypotheses

1. **Scheduled collection plus push-triggered collection — strongest.** The four repositories share a narrow daily floor despite different contents and commit schedules, while only the repositories receiving pushes show added traffic on those dates. Zero or near-zero page views are consistent with direct Git or archive access. The data cannot tell whether this is one fleet, several independent services, or GitHub infrastructure reporting several processes similarly.
2. **Broad repository indexes, dataset builders, archival systems, dependency scanners, or security scanners — plausible class, unidentified actor.** The ecosyste.ms records demonstrate that this class of system finds Taylor's repositories, including the text-heavy `BackspaceTextRetention`, through public events. Its tarball-based implementation and the low-traffic `WeatherTicker` control make it an example of the mechanism rather than the likely source of the clone counts. No public source tied a particular service in this class to the roughly 140-per-day cadence.
3. **Repository-local CI — partial explanation only.** Actions may add some `TrashTreasurePickup` clones around Oct. 11. It cannot explain three repositories with no Actions or the unchanged `BackspaceTextRetention` baseline.
4. **GitHub traffic-accounting behavior — possible contributor, unsupported as the whole explanation.** A recent traffic aggregation incident exists, and GitHub does not publish the raw clone log or its deduplication rule. The repository-specific response to pushes is structured evidence against treating every count as a single meaningless counter artifact.
5. **Large independent human readership — not supported by the available evidence.** Some clones may represent people, but the counters cannot measure that fraction. The synchronized cadence, lack of page views, and lack of public attention signals do not support interpreting 1,200 top-level uniques as 1,200 independent readers.

### Searches that did not produce attribution

- Apart from the Oct. 14 Moltbook post, exact repository names, full GitHub URLs, descriptions, and distinctive README phrases produced no external web references or backlinks. None predates or explains the start of the measured traffic window.
- GitHub code search found no other repository containing any of the four full `tmccoy678/REPOSITORY` identifiers. GitHub issue and discussion search found only Taylor's own repository activity, not an external mention.
- Exact-origin checks for all four repositories returned “not found” from the [Software Heritage archive API](https://archive.softwareheritage.org/api/), and direct Sourcegraph repository pages returned 404, so neither exposed a public mirror at the time checked.
- Beyond the generic ecosyste.ms owner index, searches of public code indexes, repository registries, mirrors, crawler discussions, and 2026 GitHub Community reports found no manifest or curated list containing all four repositories and no named 2026 campaign matching the approximately 140-event daily cadence.
- GitHub's traffic endpoints expose aggregate counts, not clone-source IP addresses, user agents, account identities, or clone referrers. A definitive actor attribution is therefore unavailable from the repository traffic data alone.

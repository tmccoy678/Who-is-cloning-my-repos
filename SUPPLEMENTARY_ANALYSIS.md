# Supplementary Analysis for “Who Is Cloning My Repositories? An Exploration of 598 Daily Clone Events Across Six Public Repositories From Exactly 8,372 Recorded Clone Events ÷ 14 Days—With 0 Visitors, 0 Views, No Referrals, Stars, Forks, or External Public Discussion for DobeWorks and DEGS at the Original Snapshot”

Original window checked: 2026-10-17

Follow-up checked: 2026-10-19

## October 19 follow-up

The recurring floor continued through the completed October 18 UTC bucket. DobeWorks recorded 141–144 clones/day during October 13–18; DEGS recorded 141–143. Across DobeWorks, DEGS, BackspaceTextRetention, and TrashTreasurePickup, the daily totals were 568, 568, 572, 571, 575, and 568. Their mean was 570.33/day and sample coefficient of variation was 0.50%. WeatherTicker recorded two clones during the same six days.

The moving 14-day totals were:

| Repository | Clones | Top-level unique cloners | Views | Unique visitors |
|---|---:|---:|---:|---:|
| DobeWorks | 2,144 | 1,253 | 0 | 0 |
| DEGS | 2,008 | 1,249 | 2 | 1 |
| BackspaceTextRetention | 1,991 | 1,189 | 0 | 0 |
| TrashTreasurePickup | 2,124 | 1,231 | 1 | 1 |
| grok-bridge-writeup | 100 | 65 | 7 | 1 |
| WeatherTicker | 4 | 4 | 0 | 0 |

The two DEGS views from one visitor appeared on October 17, after the original zero-view screenshot and snapshot. The visitor's identity remains private. The manuscript title therefore states that the zero result applies to the original snapshot.

The account-age comparison used 32 public accounts returned from a GitHub user search centered on Taylor's August 10, 2026 creation date. The sample median was 0 followers, 6 public repositories, 0 stars, and 0 forks. Taylor's visible engagement is ordinary for a new account while her clone telemetry is unusual; clone traffic for the comparison accounts remains private.

The read-only engineering review and cost model are preserved in [`READ_ONLY_REVIEW_AND_VALUATION.md`](READ_ONLY_REVIEW_AND_VALUATION.md). Current tests produced 124 passes and 32 documented skips for the reviewed DobeWorks suites, and 72 passes for DEGS. The combined conventional replacement-cost estimate is $181,000–$508,000 after accounting for overlapping governance material; commercial sale value remains unknown.

### Same-date variation comparison

Seven owners published daily GitHub Traffic series for AI-agent, Claude-skill, MCP, and AI-security repositories covering the same six completed UTC dates, October 13–18. For each series, the requested total variation percentage was defined as `100 × (maximum − minimum) ÷ six-day mean`; the sample coefficient of variation was retained as a second scale-independent measure.

Taylor's four individual high-traffic repositories had range percentages of 1.40%–3.50%, maximum absolute daily deviations from their means of 0.70%–2.10%, and sample CVs of 0.63%–1.47%. The seven external repositories had range percentages of 66.67%–396.69%, maximum deviations of 51.11%–313.59%, and sample CVs of 25.88%–154.45%. The least variable external case, `AgentHarbor`, was more than 19 times as variable by range percentage as Taylor's most variable selected repository. The four-repository Taylor aggregate had a 1.23% range percentage, 0.82% maximum deviation, and 0.50% sample CV, but individual-repository comparisons are fairer because aggregation can reduce noise.

The complete date-matched values, calculations, source commits, and permalinks are preserved in [`data/same-six-day-variation-comparison-2026-10-19.csv`](data/same-six-day-variation-comparison-2026-10-19.csv). This purposive sample leaves the GitHub-wide base rate unknown. The much larger variation among same-date subject peers isolates Taylor's near-flat series from the Traffic API itself and from subject matter alone.

### Numeric-first search regardless of subject

A separate GitHub Code Search sweep inspected 226 candidate public files and extracted 136 non-cumulative daily clone series covering October 13–18. None met the requested 1%–4% criterion when measured either as range divided by mean or maximum absolute daily deviation divided by mean. The mean for a qualifying external group is therefore undefined because no repository qualified.

The nearest valid series was `dikeckaan/easy-vphone`: 92, 82, 80, 81, 70, and 73 daily clones, for a mean of 79.67/day, range percentage of 27.62%, maximum deviation from the mean of 15.48%, and sample CV of 9.68%. Its subject is a native macOS GUI for virtual-phone VM management and an integrated IPA library. The next four closest series ranged from 66.67% to 87.84% and covered an AI coding-agent application, internship listings, an OpenTelemetry example, and a VPN client.

One 1.47% apparent match was rejected because the source file recorded a cumulative clone total and contained no daily clone-event series. Including it would confuse a running counter's expected smoothness with stable daily traffic. The closest valid results, subjects, dates, means, calculations, and exact source links are in [`data/numeric-regularity-search-2026-10-19.csv`](data/numeric-regularity-search-2026-10-19.csv). The complete extracted set is preserved in [`data/public-daily-clone-series-search-2026-10-19.csv`](data/public-daily-clone-series-search-2026-10-19.csv): 138 series total, two excluded cumulative counters, 136 valid daily series, and zero 1%–4% matches under either the range/mean or maximum-deviation/mean definition.

### Read-only Astra audit

A source audit may be read-only while still using `git clone`; GitHub can count that download without a page view. An Astra code review completed October 19 was treated as a possible owner-authorized clone event if it used a fresh checkout; its acquisition method is unknown. The October 19 UTC bucket was incomplete and was excluded from all trend and same-date calculations. At the final October 19 read, GitHub had not yet emitted an October 19 daily clone bucket for any of the six repositories, and the rolling totals were unchanged from the earlier follow-up. No audit-associated increment was therefore observable yet. GitHub's aggregate daily data leave any later increase ambiguous and prevent assignment to a particular audit event.

## Finding

Yes: repositories about AI agents, MCP, model tooling, and adjacent security work can receive hundreds or thousands of GitHub-counted unique cloners in a 14-day window. Two model repositories are especially close to Taylor's unique-cloner share: `QwenAudio/Fun-ASR` reported 1,029 clone events from 766 unique cloners (74%), and `QwenAudio/SenseVoice` reported 1,132 from 660 (58%). Taylor's four high-traffic repositories are around 59–63%.

The search found no other repository combining all three features at Taylor's scale: roughly 1,200–1,260 unique cloners, zero or one page view, and nearly synchronized daily traffic across four repositories. Similar subject matter makes deliberate automated selection plausible. GitHub leaves the unit behind `uniques` undefined.

## Owner-published comparisons

Unless otherwise marked, these are the top-level values for one GitHub rolling traffic window. Each day's unique count was excluded from the totals.

| Repository and subject | Window | Clone events | Unique cloners | Views | Unique visitors | Observed relevance |
|---|---:|---:|---:|---:|---:|---|
| Taylor: `DEGS-v2.1` | 14 days, Oct. 2026 | 2,009 | 1,262 | 0 | 0 | About 63% as many unique cloners as clone events, with no page traffic. Owner-only snapshot supplied for this comparison. |
| Taylor: `BackspaceTextRetention` | 14 days, Oct. 2026 | 1,991 | 1,216 | 0 | 0 | The non-tool research/write-up repository received almost the same pattern as Taylor's software repositories. |
| [`QwenAudio/Fun-ASR`](https://github.com/modelscope/FunASR/blob/main/docs/community_growth_20k.md#traffic-funnel-snapshot), speech/model tooling | 2026-06-30–07-13 | 1,029 | 766 | 6,332 | 2,106 | A model repository can have a similarly high unique-cloner share, although it also had substantial page discovery. |
| [`QwenAudio/SenseVoice`](https://github.com/modelscope/FunASR/blob/main/docs/community_growth_20k.md#traffic-funnel-snapshot), speech/model tooling | 2026-06-30–07-13 | 1,132 | 660 | 8,425 | 3,436 | Another same-owner model repo in Taylor's clone-volume range and close to Taylor's unique-cloner share. |
| [`homeassistant-ai/ha-mcp`](https://github.com/homeassistant-ai/stats/blob/master/2026-10-06.md#github-traffic-14-day-rolling-window), MCP/AI agent tooling | 14 days ending 2026-10-06 | 43,876 | 10,193 | 27,178 | 12,130 | Thousands of unique cloners are plainly possible in the MCP ecosystem, though this is a visibly popular project. |
| [`artokun/comfyui-mcp`](https://github.com/artokun/comfyui-mcp/blob/main/docs/blog/from-report-to-release.mdx#an-honest-footnote-about-our-download-numbers), MCP/model tooling | Two weeks, Aug. 2026 | 21,890 | 3,010 | 6,281 | 2,752 | The maintainer explicitly attributes part of the clone count to CI runners, mirrors, and package aggregators. |
| [`NSPG13/agent-bounties`](https://github.com/NSPG13/agent-bounties/issues/286#issue-3337531547), autonomous-agent protocol/security | Available GitHub window, 2026-07-16 | 4,820 | 444 | 425 | 89 | Clone activity can greatly exceed visible page visitors in an agent/security project. |
| [`zhurong2020/pyobfus`](https://github.com/zhurong2020/pyobfus/blob/main/docs/CURRENT_PLAN_ZH.md), AI/security tooling with MCP | 14 days, 2026-09-02 audit | 1,999 | 202 | 214 | 85 | Almost the same total clone-event count as Taylor's repos, but far fewer unique cloners and some page traffic; the owner observed release-day automation spikes. |
| [`N3oRay/proton-autogen`](https://github.com/N3oRay/proton-autogen/blob/main/docs/activity.md), independent Linux utility | Published August 2026 baseline | 2,091 | 509 | 393 | 157 | The closest public total above 2,000; much lower unique-cloner share and measurable page traffic. |
| [`mapbox/mapbox-agent-skills`](https://github.com/mapbox/mapbox-agent-skills/blob/main/metrics/metrics-latest.md), agent skills | 14 days | 1,579 | 577 | 829 | 215 | Related subject matter and substantial clone volume, but ordinary visible discovery. |
| [`sollawen/microNeo`](https://github.com/sollawen/microNeo/blob/master/docs/MKT/seo-progress.md), software project | 14 days | 1,312 | 441 | 271 | 45 | The owner attributes clone traffic to developer, CI, and bot activity and excludes it from the installation count. |
| [`duhu2000/dsh-mcp-connector`](https://github.com/duhu2000/dsh-mcp-connector/blob/main/docs/GROWTH-BASELINE.md), MCP connector | 14 days, Oct. 1–14 | 1,314 | 329 | 2,283 | 1,194 | Similar ecosystem but a conventional view-heavy funnel. |
| [`JNHFlow21/agent-switch`](https://github.com/JNHFlow21/agent-switch#project-activity), local AI-agent/MCP control plane | 14 days, 2026-08-10 | 12 | 11 | 0 | 0 | The exact zero-view/nonzero-clone shape exists in a very close subject match, but at a tiny scale. |
| [`eaglejyjh/UniverseCrystal`](https://github.com/orgs/community/discussions/203384), research documents/PDFs | GitHub traffic snapshot, 2026-07-29 | 591 | 208 | 669 | 11 | A prose/research repository can attract far more cloners than GitHub page visitors; this is relevant to `BackspaceTextRetention`. |
| [`artginzburg/PiPOSS`](https://github.com/artginzburg/PiPOSS/blob/main/docs/metrics.md#4-github-traffic-14-day-rolling--a-distant-third), non-AI macOS utility control | 2026-07-12–07-25 | 7 | 5 | 0 | 0 | The same zero-view phenomenon occurs outside AI at low volume; the owner treats it as automation noise. |
| [`sn4k3/UVtools`](https://github.com/sn4k3/UVtools/discussions/1148), mature non-AI utility control | 14 days ending 2026-09-19 | 1,367 | 348 | 4,455 | 1,732 | Page visitors substantially outnumber unique cloners in this well-used conventional tool. |

## Interpretation

Taylor's subject area sits within a real high-clone ecosystem. Public owner snapshots record clone populations in the hundreds or thousands for model and MCP repositories, and `Fun-ASR` and `SenseVoice` also have high unique-cloner shares.

The non-AI controls and other AI repositories vary widely, which weakens a generic GitHub-wide counter-defect explanation. Taylor's zero-view result is also far more extreme than the large AI/MCP examples, all of which had measurable page traffic. A selected, mostly automated collection process best explains the topic pattern and synchronized traffic across Taylor's four repositories. The human share remains unknown.

`BackspaceTextRetention` fits that interpretation. `UniverseCrystal` documents heavy cloning of a research repository, and text about model behavior, Codex, or retained context can be valuable to dataset builders, indexers, security researchers, and archival systems. The actual cloners remain unidentified.

## Metric limits

GitHub's official API says the clone and view endpoints return totals and daily or weekly breakdowns for the last 14 days. GitHub separately states that clone traffic counts full clones, not fetches. The response has top-level `count` and `uniques` fields, while the unit behind `uniques` remains unpublished and may represent people, accounts, machines, IP addresses, or another deduplication unit. See [GitHub's repository traffic API documentation](https://docs.github.com/en/rest/metrics/traffic#get-repository-clones) and [traffic-graph documentation](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository).

Top-level 14-day uniques are deduplicated-window figures. Long-running trackers that add daily unique values measure repeated daily appearances, so one source appearing on five days can enter their historical sum five times. The [`repo-metrics` data notes](https://github.com/AcTePuKc/repo-metrics#data-notes) state this explicitly. The comparison table above excludes those daily-summed figures.

This source-limited comparison uses GitHub repositories whose owners chose to publish their private traffic numbers. The examples define possible patterns; the prevalence of Taylor's pattern across similar repositories remains unknown.

## Attribution investigation

### Result

The October 17 public search left the actor unidentified. A two-part automated collection pattern best explains the traffic: a scheduled process repeatedly clones a selected set of Taylor's public repositories, while one or more event-driven processes add clones after pushes.

The owner-authorized GitHub Traffic API read for Oct. 3–16 separates those parts unusually well:

| Repository | Ordinary daily clone range | Push-linked observation | GitHub Actions runs |
|---|---:|---|---:|
| `DEGS-v2.1` | Usually 139–144 | A late Oct. 5 push was followed by 152 clones on Oct. 5 and 155 on Oct. 6, versus the roughly 142-clone floor. | 0 lifetime |
| `DobeWorks-v2.1` | Usually 140–146 | Nine Oct. 6 pushes coincided with 272 clones and 211 daily uniques, versus roughly 142 clones and 137 daily uniques on ordinary days. | 0 lifetime |
| `TrashTreasurePickup` | Usually 141–146 | Four Oct. 11 merge/push commits coincided with 235 clones and 174 daily uniques; Oct. 12 remained elevated at 169 and 155. | 49 lifetime, many on Oct. 11 |
| `BackspaceTextRetention` | 138–144 | No push after Sept. 25; it retained the same daily floor while the other repositories spiked. | 0 lifetime |

The Oct. 14 owner screenshot documents an established `DEGS-v2.1` floor by Sept. 30. Across the current window, `DEGS-v2.1` and `BackspaceTextRetention` had zero views, `DobeWorks-v2.1` had zero, and `TrashTreasurePickup` had one. GitHub says repository clone traffic counts full clones, excludes fetches, and is reported in UTC. These are clone events in GitHub's accounting, with source identity withheld. The local evidence is preserved in the owner screenshots and the responses from `gh api repos/tmccoy678/REPOSITORY/traffic/{clones,views}` read on 2026-10-17.

Repository publication and pushes are credible triggers. GitHub's [public Events API](https://docs.github.com/en/rest/activity/events) exposes public `PushEvent` records with a repository name and says public events can be delayed from 30 seconds to six hours. Its [`PublicEvent` definition](https://docs.github.com/en/rest/using-the-rest-api/github-event-types#publicevent) covers a private repository being made public. The four repositories emitted such events when they became public, from Sept. 10 through Sept. 25. A collector can therefore discover a public repository and later pushes without visiting its GitHub page. The API documents the route; its use by the observed collector remains unknown.

### Public traces found

All four repositories appear in the public [ecosyste.ms owner index](https://repos.ecosyste.ms/api/v1/hosts/GitHub/owners/tmccoy678/repositories), which lists Taylor's six public repositories together. Its record for [`DEGS-v2.1`](https://repos.ecosyste.ms/hosts/GitHub/repositories/tmccoy678%2FDEGS-v2.1) and the corresponding records for `DobeWorks-v2.1`, `TrashTreasurePickup`, and `BackspaceTextRetention` expose GitHub archive download URLs and detected repository files. `DEGS-v2.1`, `DobeWorks-v2.1`, `BackspaceTextRetention`, and low-traffic control `WeatherTicker` were synchronized within milliseconds of one another on Oct. 2. The service recorded dependency parsing for each, with manifests found in `DEGS-v2.1` and `TrashTreasurePickup`.

The service's own [synchronization documentation](https://github.com/ecosyste-ms/repos/blob/main/docs/syncing.md) says it discovers GitHub repositories from the public event firehose and GHArchive, resynchronizes recently active repositories every 15 minutes, parses dependencies, and fetches archive file lists. The documented inspection path uses a [`codeload.github.com` tarball URL](https://github.com/ecosyste-ms/repos/blob/main/app/models/hosts/github.rb#L65-L73). ecosyste.ms directly demonstrates event-driven discovery and content inspection. Its archive-based route makes it an unlikely source of GitHub-counted clones.

The `DEGS-v2.1` screenshot shows the clone floor by Sept. 30, before ecosyste.ms recorded its Oct. 2 synchronization, and `WeatherTicker` was processed in the same batch yet had only three clone events in the Oct. 3–16 owner traffic window. A broad-index explanation fails the observed selectivity: four repositories receive about 140 clone events every day while the same-batch WeatherTicker control remains near zero.

One exact public backlink was found: a [Moltbook post linking `TrashTreasurePickup`](https://moltbook.com/post/62e124f5-6087-4c5f-87ad-e8f95fdae6a6), created Oct. 14 at 20:11 UTC. The steady clone floor began by Sept. 30, and `TrashTreasurePickup` showed no clear increase after the post. The cross-repository pattern therefore predates the link. It could have contributed an unknown number of later clones.

The four repositories had no configured GitHub webhooks. GitHub Actions plausibly account for part of the Oct. 11 `TrashTreasurePickup` increase. The shared floor also spans three repositories with zero Actions runs. No comparable internal automation was visible in their repository settings.

One known local Codex usability review cloned all five public repositories once on Oct. 2, including the low-traffic `WeatherTicker` control. The five local `.git` directories have the same Oct. 2 creation time. That activity contributes one owner-initiated clone per repository outside the current Oct. 3–16 API window. The continuing daily floor has another source.

Recent owner reports document unexplained bursts elsewhere; Taylor's source remains unknown. On Aug. 15, 2026, a repository owner reported [7,543 unique cloners in one day](https://github.com/orgs/community/discussions/205346) after ordinarily seeing a few hundred clone events; the actor remained unresolved. GitHub traffic reporting also had a [multi-repository aggregation delay beginning Sept. 23, 2026](https://github.com/orgs/community/discussions/208852). That incident introduces uncertainty about exact dates and late backfill. Taylor's stable per-repository floor and repository-specific push-day spikes remain a separate pattern.

### Ranked hypotheses

1. **Scheduled collection plus push-triggered collection — strongest.** The four repositories share a narrow daily floor despite different contents and commit schedules, while only the repositories receiving pushes show added traffic on those dates. Zero or near-zero page views are consistent with direct Git or archive access. The data leave three architectures open: one fleet, several independent services, or GitHub infrastructure reporting several processes similarly.
2. **Broad repository indexes, dataset builders, archival systems, dependency scanners, or security scanners — plausible class, unidentified actor.** The ecosyste.ms records demonstrate discovery of Taylor's repositories, including the text-heavy `BackspaceTextRetention`, through public events. Its tarball-based implementation and the low-traffic `WeatherTicker` control make it an unlikely source of the clone counts. The roughly 140-per-day operator remains unknown.
3. **Repository-local CI — partial explanation only.** Actions may add some `TrashTreasurePickup` clones around Oct. 11. Its reach is confined to `TrashTreasurePickup`; three repositories have zero Actions runs and `BackspaceTextRetention` remains unchanged.
4. **GitHub traffic-accounting behavior — possible contributor.** A recent traffic aggregation incident exists, and GitHub keeps the raw clone log and deduplication rule private. Repository selectivity and push-linked spikes require an additional mechanism and rule out a single meaningless counter artifact as a complete explanation.
5. **Large independent human readership — weak fit.** The counters leave the human fraction unknown. The synchronized cadence, lack of page views, and lack of public attention signals favor automated collection over 1,200 independent readers.

### Attribution Search Results

- Apart from the Oct. 14 Moltbook post, exact repository names, full GitHub URLs, descriptions, and distinctive README phrases produced no external web references or backlinks. None predates or explains the start of the measured traffic window.
- GitHub code search found the four full `tmccoy678/REPOSITORY` identifiers only in Taylor's repositories. GitHub issue and discussion search likewise returned Taylor's own repository activity exclusively.
- Exact-origin checks for all four repositories returned “not found” from the [Software Heritage archive API](https://archive.softwareheritage.org/api/), and direct Sourcegraph repository pages returned 404. Both services lacked a public mirror at the time checked.
- Beyond the generic ecosyste.ms owner index, searches of public code indexes, repository registries, mirrors, crawler discussions, and 2026 GitHub Community reports found no manifest or curated list containing all four repositories and no named 2026 campaign matching the approximately 140-event daily cadence.
- GitHub's traffic endpoints expose aggregate counts, not clone-source IP addresses, user agents, account identities, or clone referrers. A definitive actor attribution is therefore unavailable from the repository traffic data alone.

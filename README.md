# Who Is Cloning All of My Repositories? An Exploration of 598 Daily Clone Events Across Six Public Repositories From Exactly 8,372 Recorded Clone Events ÷ 14 Days

**Taylor McCoy**<br>
**October 19, 2026**

Research and drafting assistance: OpenAI Codex, GPT-6

## Abstract

This descriptive case study examined an anomalous pattern in GitHub Traffic data for six public repositories owned by one developer. During the 14-day window ending October 16, 2026, the repositories received exactly 8,372 GitHub-counted clone events, an average of 598 per day. Four repositories associated with AI agents, model behavior, developer tooling, or security contributed 8,271 events and each received approximately 1,200–1,260 top-level unique cloners, while a conventional weather utility received three clones. The high-traffic repositories exhibited a stable daily floor of approximately 138–146 clone events. Repository-specific deviations aligned with public pushes: `DobeWorks-v2.1` reached 272 clones during an October 6 push burst, and `TrashTreasurePickup` reached 235 during October 11 security and workflow changes. The same repositories recorded zero or one page view. Data were collected from authenticated GitHub Traffic endpoints, GitHub repository metadata and event histories, repository configuration, owner screenshots, and purposively selected owner-published comparison records. Descriptive totals, daily ranges, temporal alignment, negative controls, and competing explanations were evaluated. The findings support a recurring automated collection process supplemented by push-triggered collection. Public-event indexing provides a technically plausible discovery route, and one public index was confirmed to have processed the repository set. The evidence does not identify a particular company, government, dataset, crawler, or person, and GitHub does not define “unique cloner” as a unique human or IP address. The appropriate conclusion is selective automated collection without actor attribution.

**Keywords:** GitHub Traffic, repository cloning, automated collection, public events, AI repositories, software archives

## Introduction

GitHub presents repository owners with 14-day traffic summaries for clones, unique cloners, views, and unique visitors. GitHub states that its clone metric represents full clones rather than subsequent fetches and supplies daily or weekly breakdowns through an authenticated repository-traffic endpoint (GitHub, 2026a, 2026b). GitHub does not publicly explain whether a “unique cloner” corresponds to a person, account, machine, network address, or another deduplication unit. That distinction matters when clone traffic greatly exceeds page traffic.

The present investigation began after `DEGS-v2.1` displayed 2,011 clone events, 1,254 unique cloners, and zero views in an owner screenshot dated October 14, 2026 (Figures 1 and 2). Similar totals subsequently appeared across three other public repositories, including `BackspaceTextRetention`, a text-centered record rather than a conventional software tool. The pattern was large enough to invite two competing intuitive interpretations: either the repositories had attracted an unusually broad human audience, or an automated system was repeatedly collecting them.

The central question was therefore: **What explanation best fits the scale, selectivity, timing, and zero-view character of the observed clone traffic?** A secondary question was whether repositories with similar AI, model-tooling, Model Context Protocol (MCP), or security subject matter showed comparable clone-heavy patterns.

This study does not attempt to identify a person or organization without source-level evidence. Its purpose is to distinguish observed data from inference, test common explanations against the available record, and identify the narrowest conclusion supported by that record.

## Methods

### Study Design

The investigation used a descriptive, observational case-study design. The primary units were repository-day observations within GitHub’s rolling 14-day traffic window. Six public repositories owned by the same GitHub account formed the complete public-repository set at the time of analysis. Four high-traffic repositories were compared with two low-traffic public repositories and with the owner’s private-repository traffic. A purposive external comparison set was then assembled from repository owners who had publicly preserved their own GitHub Traffic figures.

No experiment was conducted, no repository was deliberately pushed to provoke a response, and no attempt was made to deanonymize clone sources. Temporal associations are therefore interpreted as evidence of a mechanism rather than proof of a particular actor or causal process.

## Data Collection

Authenticated owner access was used on October 17, 2026, to read GitHub’s clone and view endpoints for each repository. GitHub documents these endpoints as returning top-level totals and daily or weekly breakdowns for the preceding 14 days (GitHub, 2026a). The principal analysis window was October 3–16, 2026, in UTC. An owner screenshot captured on October 14 extended the visible `DEGS-v2.1` series back to September 30 (Figures 1 and 2).

For each repository, the following fields were collected where available:

- total clone events and top-level unique cloners;
- daily clone events and daily unique cloners;
- total views and unique visitors;
- repository creation, publication, and last-push dates;
- public push events and commit descriptions;
- GitHub Actions runs;
- configured repository webhooks;
- popular referrers and paths; and
- stars, forks, public mentions, mirrors, and external exact-name references.

GitHub’s public Events API and event-type documentation were examined to assess whether a third party could discover repository publication and push activity without viewing a repository page. GitHub documents a public-events endpoint requiring no repository permission and describes `PushEvent` and `PublicEvent` records that identify affected repositories (GitHub, 2026c, 2026d; Figure 4).

External discovery checks included exact repository names, full GitHub URLs, distinctive descriptions and README phrases, GitHub code references, issues and discussions, Software Heritage origins, Sourcegraph repository pages, public registries, and mirror or crawler reports. One exact later backlink was found on Moltbook, but it postdated the onset of the measured traffic pattern (Moltbook, 2026).

The external comparison sample included only public owner- or maintainer-published traffic values with a discernible reporting window. Long-running trackers that sum each day’s unique value were excluded because daily unique counts cannot be added into a deduplicated multi-day audience estimate (AcTePuKc, n.d.). The comparison set is illustrative and self-selected rather than a random sample of GitHub.

### Data Integrity and Privacy

The two GitHub Traffic screenshots in Figures 1 and 2 were copied byte-for-byte from the owner’s original October 14 captures. Public-source figures were captured from the cited primary webpages on October 19, 2026. Image provenance and SHA-256 hashes are recorded in [`figures/README.md`](figures/README.md). The repository excludes residential address information, personal email addresses, phone numbers, credentials, local filesystem paths, and secrets.

## Data Analysis

Analysis proceeded in five stages.

First, the six repository-level clone totals were summed: 1,991 + 2,009 + 2,149 + 2,122 + 98 + 3 = exactly 8,372 clone events. Dividing by GitHub’s 14-day window produced the title value of exactly 598 clone events per day. The four high-traffic repositories contributed 8,271 events, or approximately 591 per day.

Second, daily medians and ranges were used to characterize the recurring baseline. This avoided allowing the large update-associated spikes to define the ordinary level.

Third, daily traffic was aligned with public push dates. A push-linked association was considered notable when the updated repository deviated sharply while an unchanged high-traffic repository retained the baseline.

Fourth, candidate explanations were tested against negative controls and configuration evidence. `WeatherTicker` served as a public, non-AI control. Private repositories tested whether the pattern operated account-wide. GitHub Actions and webhooks were checked as possible owner-controlled sources. Views, referrers, stars, forks, and backlinks were checked as indicators of ordinary human discovery.

Fifth, hypotheses were ranked by explanatory fit across scale, selectivity, recurrence, direct-access behavior, and update response. No inferential significance test was used because the observation period was short, the source sample was not random, GitHub’s deduplication method is undisclosed, and repository-day observations were unlikely to be independent.

Per-repository unique-cloner totals were not summed into a cross-repository total. GitHub does not reveal overlap, so the same underlying source may appear in several repositories. Treating the sum as a count of distinct people, accounts, or IP addresses would be unsupported.

## Results

### Scale and Repository Selectivity

**Table 1**<br>
*GitHub Traffic Across the Six Public Repositories*

| Repository | Primary subject | Clone events | Unique cloners | Views | Unique visitors | Mean clones/day |
|---|---|---:|---:|---:|---:|---:|
| `BackspaceTextRetention` | Codex/model behavior and text retention | 1,991 | 1,216 | 0 | 0 | 142.21 |
| `DEGS-v2.1` | Evidence governance for agent systems | 2,009 | 1,262 | 0 | 0 | 143.50 |
| `DobeWorks-v2.1` | Agent worker/observer architecture | 2,149 | 1,262 | 0 | 0 | 153.50 |
| `TrashTreasurePickup` | Agent context-management tooling | 2,122 | 1,253 | 1 | 1 | 151.57 |
| `grok-bridge-writeup` | AI-agent bridge and security write-up | 98 | 63 | 7 | 1 | 7.00 |
| `WeatherTicker` | Conventional weather utility | 3 | 3 | 0 | 0 | 0.21 |
| **Total** |  | **8,372** | **Not additive** | **8** | **2** | **598.00** |

*Note.* Values are owner-accessible GitHub Traffic totals read October 17, 2026, for the rolling window ending October 16. “Not additive” means that GitHub provides no cross-repository deduplication rule.

The distribution was strongly selective. The four high-traffic repositories accounted for 98.8% of all clone events and shared AI-, agent-, model-behavior-, or security-adjacent subject matter. `WeatherTicker`, despite being public and indexed in the same account-wide batch by ecosyste.ms, received three clones. Most private repositories received zero clone traffic; three private repositories showed only 15/2, 2/1, and 1/1 clone/unique totals. The pattern therefore did not operate uniformly across the owner’s account.

### Stable Baseline and Push-Associated Spikes

The four high-traffic repositories shared a narrow ordinary daily level. `BackspaceTextRetention` had a daily median of 142 clone events and a range of 138–144. `DEGS-v2.1` had a median of 142 and a range of 139–155. `DobeWorks-v2.1` had a median of 143 and a range of 140–272. `TrashTreasurePickup` had a median of 142 and a range of 141–235. The large ranges for the last two repositories were created by isolated update-associated spikes; their non-spike values remained close to the shared floor.

**Table 2**<br>
*Temporal Alignment Between Public Pushes and Clone Spikes*

| Repository | Ordinary daily level | Public repository activity | Observed traffic response | Internal Actions explanation |
|---|---:|---|---|---|
| `DEGS-v2.1` | approximately 139–144 | Late October 5 documentation push | 152 clones October 5; 155 October 6 | No Actions runs |
| `DobeWorks-v2.1` | approximately 140–146 | Nine October 6 pushes involving Nova/Grok bridge work | 272 clones and 211 daily uniques October 6 | No Actions runs |
| `TrashTreasurePickup` | approximately 141–146 | Four October 11 merge/push commits involving security and workflow changes | 235 clones/174 uniques October 11; 169/155 October 12 | Actions can explain only part of the increase |
| `BackspaceTextRetention` | 138–144 | No push after September 25 | Remained at the shared floor while other repositories spiked | No Actions runs |

This separation is the central analytical result. The unchanged repository preserved the recurring floor while the updated repository received an added burst. Because three high-traffic repositories had no GitHub Actions history, repository-local continuous integration could not explain the common baseline.

### Clone Traffic Without Page Traffic

The `DEGS-v2.1` owner screenshot displayed 2,011 clones and 1,254 unique cloners with zero views and zero unique visitors (Figure 1). Its daily series remained tightly clustered near 140 clone events and 130–145 daily unique cloners (Figure 2). `BackspaceTextRetention` and `DobeWorks-v2.1` also recorded zero views in the current API window, while `TrashTreasurePickup` recorded one.

GitHub’s public events interface provides a route that does not require page navigation. Public activity streams can expose repository publication and later pushes, after which a collector can invoke Git directly (GitHub, 2026c, 2026d). The zero-view pattern is therefore consistent with programmatic discovery and direct repository access.

### Public Indexing Trace

The ecosyste.ms repository index contained all six public repositories in a common owner listing (ecosyste.ms, 2026b). `DEGS-v2.1`, `DobeWorks-v2.1`, `BackspaceTextRetention`, and `WeatherTicker` were synchronized within milliseconds of one another on October 2. The service’s own documentation states that it discovers repositories through public-event infrastructure, periodically revisits recently changed projects, and imports GHArchive events (ecosyste.ms, 2026a; Figure 5).

This finding demonstrates event-driven discovery of the repository set. It does not identify ecosyste.ms as the clone source. Its documented GitHub inspection route uses archive downloads, `DEGS-v2.1` showed the daily clone floor before the recorded October 2 synchronization, and the same-batch `WeatherTicker` control received only three GitHub-counted clones.

A known owner-side Codex usability review cloned all five then-public repositories once on October 2. That activity can explain one owner-initiated clone per repository near that date, lies outside the October 3–16 analysis window, and cannot explain the continuing daily floor.

### Comparison With Other Repositories

AI-, MCP-, model-tooling-, and security-related repositories can receive hundreds or thousands of unique cloners. The published Fun-ASR report recorded 1,029 clones from 766 unique cloners for `QwenAudio/Fun-ASR` and 1,132 from 660 for `QwenAudio/SenseVoice` in one 14-day window (ModelScope, 2026; Figure 6). These unique-cloner proportions—74% and 58%—overlap the approximately 59%–63% range of the four high-traffic repositories in this study.

**Table 3**<br>
*Owner-Published GitHub Traffic Comparisons*

| Repository | Subject | Clone events | Unique cloners | Views | Unique visitors | Source |
|---|---|---:|---:|---:|---:|---|
| `QwenAudio/Fun-ASR` | Speech/model tooling | 1,029 | 766 | 6,332 | 2,106 | (ModelScope, 2026) |
| `QwenAudio/SenseVoice` | Speech/model tooling | 1,132 | 660 | 8,425 | 3,436 | (ModelScope, 2026) |
| `homeassistant-ai/ha-mcp` | MCP/AI-agent tooling | 43,876 | 10,193 | 27,178 | 12,130 | (Home Assistant AI, 2026) |
| `artokun/comfyui-mcp` | MCP/model tooling | 21,890 | 3,010 | 6,281 | 2,752 | (Artokun, 2026) |
| `NSPG13/agent-bounties` | Agent protocol/security | 4,820 | 444 | 425 | 89 | (NSPG13, 2026) |
| `zhurong2020/pyobfus` | AI/security tooling with MCP | 1,999 | 202 | 214 | 85 | (Zhurong2020, 2026) |
| `JNHFlow21/agent-switch` | Local AI-agent/MCP control plane | 12 | 11 | 0 | 0 | (JNHFlow21, 2026) |
| `eaglejyjh/UniverseCrystal` | Research documents/PDFs | 591 | 208 | 669 | 11 | (Eaglejyjh, 2026) |
| `artginzburg/PiPOSS` | Non-AI macOS utility | 7 | 5 | 0 | 0 | (Artginzburg, 2026) |
| `sn4k3/UVtools` | Mature non-AI utility | 1,367 | 348 | 4,455 | 1,732 | (Sn4k3, 2026) |

*Note.* The comparison cases were published by owners or maintainers and are not a random sample. Dates and source links appear in the References. Artokun (2026) explicitly attributed part of `comfyui-mcp` traffic to CI runners, mirrors, and package aggregators.

The comparison establishes that high clone counts and clone-heavy funnels occur in the relevant technical ecosystem. The unusual feature of the present case is the combination of approximately 1,200–1,260 top-level unique cloners per selected repository, zero or one page view, and a synchronized daily floor across four repositories.

## Discussion

### Best-Supported Explanation

The evidence best supports two overlapping automated processes: recurring scheduled collection and additional event-triggered collection. The shared baseline suggests that the same selection rule, fleet, or set of independent services repeatedly touches the four repositories. The repository-specific push spikes suggest a second trigger responsive to public updates. These may be components of one system or several services that react to the same public signals.

This interpretation explains all four central observations: scale, subject selectivity, recurrence, and zero-view access. It also explains why private repositories were mostly unaffected. Public event streams and anonymous Git access expose public repositories to collectors; private repositories require authorization and do not participate in the same anonymous discovery route.

The inclusion of `BackspaceTextRetention` strengthens rather than weakens the subject-selection inference. A repository need not be executable software to interest a dataset builder, archival system, security scanner, or model-behavior index. Its Codex, deletion-retention, surveillance, and model-behavior content falls within the same broad information environment as the software repositories. A published research-document repository has likewise shown clone traffic far exceeding unique page visitors (Eaglejyjh, 2026).

### Alternative Explanations

Repository-local CI is a partial explanation for `TrashTreasurePickup` on October 11 but fails for the three high-traffic repositories with no Actions runs. Ordinary human discovery is possible for an unknown fraction, yet the absence of page views, backlinks, stars, forks, and referrals does not support interpreting the top-level unique values as 1,200 independent readers.

A GitHub accounting effect may contribute. GitHub had a recent community-reported aggregation delay, and its unique-cloner deduplication rule is undisclosed. However, a universal counter artifact does not readily explain why the traffic selected four semantically related public repositories, ignored a conventional public utility, and rose specifically in repositories that received pushes.

Broad archival, dependency, dataset, and security-scanning systems remain plausible actor classes. Public tools exist that discover all repositories under a profile and clone or cache them for repeated scanning. The current evidence does not connect any named tool to these counts. Similarly, no evidence supports attributing the activity to a government agency. Government, corporate, academic, and hobbyist automation remain observationally indistinguishable in GitHub’s aggregate interface.

### Meaning of “Unique Cloner”

The unique-cloner number should be treated as a GitHub-defined aggregate, not a population count. GitHub publishes the response fields `count` and `uniques` but does not define `uniques` as humans, accounts, machines, or IP addresses (GitHub, 2026a). A distributed fleet, rotating cloud egress, independent services, or internal aggregation rules could inflate the apparent uniqueness relative to the number of organizations involved.

The optimistic interpretation that survives this limitation is narrower but still meaningful: the repositories were repeatedly selected by one or more technical collection systems. They were not treated like the low-traffic control. Some human attention may exist behind those systems, but the available metric cannot measure it.

### Limitations

The analysis has six principal limitations. First, GitHub retains only a rolling 14-day traffic window. Second, clone-source IP addresses, user agents, referrers, and accounts are unavailable. Third, cross-repository unique overlap is unknown. Fourth, the comparative sample is self-selected because repository traffic is private unless owners publish it. Fifth, date alignment is daily and cannot resolve the ordering of pushes and clones within a UTC day. Sixth, an observed temporal association cannot identify the number or ownership of the underlying collectors.

The screenshots and API reads preserve what GitHub displayed, but they do not validate GitHub’s private measurement implementation. Accordingly, the investigation supports mechanism-level inference rather than actor attribution.

## Conclusion

Exactly 8,372 GitHub-counted clone events occurred across six public repositories in the examined 14-day window, producing the title value of exactly 598 clone events per day. Four related repositories accounted for 8,271 events and shared a remarkably stable daily floor, while a conventional public utility received three clones. Public pushes aligned with large repository-specific increases, and the affected repositories recorded almost no page traffic.

The most defensible conclusion is that one or more automated systems selectively and repeatedly collected the AI-, agent-, model-behavior-, and security-adjacent repositories, with additional cloning triggered by public updates. Public event streams provide a documented discovery route, and an independent index demonstrably discovered the repository set through that ecosystem. No available evidence identifies the actor, establishes that top-level unique cloners are unique people or IP addresses, or supports a government attribution.

The anomaly is therefore real in the limited sense that matters: the traffic is structured, selective, recurring, and responsive to repository activity. What remains unknown is who operates the collectors and why.

## References

AcTePuKc. (n.d.). *repo-metrics* [Computer software]. GitHub. https://github.com/AcTePuKc/repo-metrics

Artginzburg. (2026). *PiPOSS metrics* [Data set]. GitHub. https://github.com/artginzburg/PiPOSS/blob/main/docs/metrics.md

Artokun. (2026). *From report to release: An honest footnote about our download numbers* [Project report]. GitHub. https://github.com/artokun/comfyui-mcp/blob/main/docs/blog/from-report-to-release.mdx

ecosyste.ms. (2026a). *How repositories stay up to date* [Source code documentation]. GitHub. https://github.com/ecosyste-ms/repos/blob/main/docs/syncing.md

ecosyste.ms. (2026b). *Repositories owned by tmccoy678* [Data set]. https://repos.ecosyste.ms/api/v1/hosts/GitHub/owners/tmccoy678/repositories

Eaglejyjh. (2026, July 29). *UniverseCrystal repository traffic discussion* [Online forum post]. GitHub Community. https://github.com/orgs/community/discussions/203384

GitHub. (2026a). *REST API endpoints for repository traffic*. GitHub Docs. https://docs.github.com/en/rest/metrics/traffic#get-repository-clones

GitHub. (2026b). *Viewing traffic to a repository*. GitHub Docs. https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository

GitHub. (2026c). *REST API endpoints for events*. GitHub Docs. https://docs.github.com/en/rest/activity/events

GitHub. (2026d). *GitHub event types*. GitHub Docs. https://docs.github.com/en/rest/using-the-rest-api/github-event-types

Home Assistant AI. (2026, October 6). *GitHub traffic: 14-day rolling window* [Data set]. GitHub. https://github.com/homeassistant-ai/stats/blob/master/2026-10-06.md

JNHFlow21. (2026, August 10). *Agent Switch project activity* [Data set]. GitHub. https://github.com/JNHFlow21/agent-switch#project-activity

ModelScope. (2026, July 14). *Community growth to 20K stars* [Project report]. GitHub. https://github.com/modelscope/FunASR/blob/main/docs/community_growth_20k.md

Moltbook. (2026, October 14). *TrashTreasurePickup post* [Social media post]. https://moltbook.com/post/62e124f5-6087-4c5f-87ad-e8f95fdae6a6

NSPG13. (2026, July 16). *Agent Bounties traffic snapshot* [GitHub issue]. GitHub. https://github.com/NSPG13/agent-bounties/issues/286

Sn4k3. (2026, September 19). *UVtools repository traffic discussion* [Online forum post]. GitHub. https://github.com/sn4k3/UVtools/discussions/1148

Software Heritage. (n.d.). *Archive API*. https://archive.softwareheritage.org/api/

Zhurong2020. (2026, September 2). *Pyobfus current plan* [Project document]. GitHub. https://github.com/zhurong2020/pyobfus/blob/main/docs/CURRENT_PLAN_ZH.md

## Figures

**Figure 1**<br>
*GitHub Traffic Overview for DEGS-v2.1, October 14, 2026*

![GitHub Traffic page showing 2,011 clones, 1,254 unique cloners, zero views, and zero unique visitors for DEGS-v2.1.](figures/figure-1-degs-traffic-overview-2026-10-14.png)

*Note.* Original owner screenshot of the GitHub Traffic page. The clone and unique-cloner graphs cover September 30–October 13, 2026.

**Figure 2**<br>
*Unique Cloners for DEGS-v2.1 During the Same 14-Day Window*

![Close view of the DEGS-v2.1 unique-cloner chart showing 1,254 unique cloners and a daily series near 131–145.](figures/figure-2-degs-unique-cloners-2026-10-14.png)

*Note.* Original owner screenshot. The tightly bounded daily series is consistent with a recurring collection process but does not identify its source.

**Figure 3**<br>
*GitHub’s Authenticated Repository-Clone Endpoint*

![GitHub documentation page for the Get repository clones endpoint.](figures/figure-3-github-clone-api-documentation.png)

*Note.* Primary-source documentation captured October 19, 2026. The page identifies the authenticated endpoint used to retrieve repository clone traffic (GitHub, 2026a).

**Figure 4**<br>
*GitHub’s Public-Events Endpoint*

![GitHub documentation page for the List public events endpoint, including the statement that no fine-grained permissions are required.](figures/figure-4-github-public-events-api.png)

*Note.* Primary-source documentation captured October 19, 2026. GitHub states that the endpoint requires no fine-grained repository permission and may lag by 30 seconds to 6 hours (GitHub, 2026c).

**Figure 5**<br>
*ecosyste.ms Documentation of Public-Event Repository Discovery*

![Raw ecosyste.ms synchronization documentation describing GitHub public-event discovery and periodic polling.](figures/figure-5-ecosystems-sync-documentation.png)

*Note.* Primary-source documentation captured October 19, 2026. The service states that its GitHub discovery route reflects the public-events firehose and that recently active repositories are polled periodically (ecosyste.ms, 2026a).

**Figure 6**<br>
*Published GitHub Traffic Comparison for Fun-ASR and SenseVoice*

![ModelScope FunASR report table showing views, visitors, clones, and unique cloners for four related repositories.](figures/figure-6-funasr-traffic-comparison.png)

*Note.* Primary-source owner-published comparison captured October 19, 2026. `QwenAudio/Fun-ASR` recorded 1,029 clones and 766 unique cloners; `QwenAudio/SenseVoice` recorded 1,132 and 660, respectively (ModelScope, 2026).

## Supplementary Material

The original source-comparison and attribution notes are retained in [`SUPPLEMENTARY_ANALYSIS.md`](SUPPLEMENTARY_ANALYSIS.md). Machine-readable repository totals are available in [`data/traffic-snapshot-2026-10-17.csv`](data/traffic-snapshot-2026-10-17.csv). Figure provenance is documented in [`figures/README.md`](figures/README.md).

## License

Citation metadata are available in [`CITATION.cff`](CITATION.cff). This manuscript is licensed under the [MIT License](LICENSE).

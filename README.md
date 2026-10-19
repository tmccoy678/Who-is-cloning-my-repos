# Who Is Cloning All of My Repositories? An Exploration of 598 Daily Clone Events Across Six Public Repositories

A private evidence note concerning unusually high clone traffic across several public repositories owned by Taylor McCoy.

The title uses the complete public-repository snapshot: 8,372 clone events across six public repositories over 14 days, exactly 598 per day. The four selected high-traffic repositories contributed 8,271 of those events. GitHub's per-repository unique-cloner totals are not added because cross-repository overlap is undisclosed.

Research checked: October 17, 2026
Repository prepared: October 19, 2026

## Finding

The strongest supported explanation is one or more automated collection systems that:

1. clone a selected set of public AI, agent, and security-related repositories on a recurring schedule; and
2. perform additional clones when GitHub announces new pushes.

This is a strong inference from the timing and cross-repository pattern. The available evidence does not identify a company, government, crawler, dataset, or person.

## Why the pattern is unusual

Four selected repositories showed essentially the same daily floor:

| Repository | 14-day clone events | 14-day unique cloners | Ordinary daily clone range | Views |
|---|---:|---:|---:|---:|
| `BackspaceTextRetention` | 1,991 | 1,216 | 138–144 | 0 |
| `DEGS-v2.1` | 2,009 | 1,262 | usually 139–144 | 0 |
| `DobeWorks-v2.1` | 2,149 | 1,262 | usually 140–146 | 0 |
| `TrashTreasurePickup` | 2,122 | 1,253 | usually 141–146 | 1 |

Together, these repositories received 8,271 GitHub-counted clone events in 14 days, or approximately 591 per day. Their top-level unique-cloner values cannot be added as though they represent different people because GitHub does not disclose whether the same source appears in more than one repository.

The low-traffic control was dramatically different: `WeatherTicker` received three clones in the corresponding 14-day window. Most private repositories received no traffic, while the few with activity remained at small owner- or integration-scale counts.

That distribution argues against an account-wide clone counter defect. The automated activity selected particular public repositories associated with AI agents, model behavior, developer tooling, and security.

## Push-linked evidence

The baseline and the update response can be separated:

- `DobeWorks-v2.1` received 272 clones and 211 daily uniques on October 6, during nine public pushes involving Nova/Grok bridge work. Its ordinary level was approximately 142 clones and 137–140 daily uniques.
- `TrashTreasurePickup` received 235 clones and 174 daily uniques on October 11, during its security and workflow changes. It remained elevated at 169 clones and 155 uniques on October 12.
- `DEGS-v2.1` rose to 152 and 155 clones around its late October 5 push.
- `BackspaceTextRetention`, which had no new push after September 25, continued at the ordinary 138–144 range while the updated repositories spiked.

This is consistent with a scheduled collector producing the daily floor and event-driven collectors adding work after pushes.

## Why zero views can coexist with clones

A collector does not need to open the GitHub webpage. GitHub's public Events API exposes repository publication and push activity, including repository names and commit identifiers. A process can watch those events and access the Git repository directly.

The zero- or near-zero-view totals are therefore consistent with direct Git access. They are difficult to reconcile with 1,200 independent people each discovering the repositories through the normal GitHub interface.

## What was actually found

The public `ecosyste.ms` repository index discovered and processed Taylor's public repositories through GitHub's public-event ecosystem. Several repositories received adjacent records and nearly identical synchronization times. Its documented inspection path uses GitHub archive downloads, and it also processed the low-traffic `WeatherTicker`, so it demonstrates the discovery mechanism without explaining the approximately 140 daily clone events.

One later Moltbook post linked `TrashTreasurePickup`, but it appeared on October 14, after the recurring pattern had begun, and produced no clear traffic increase.

Comparable public reports show that AI, MCP, model-tooling, and security repositories can receive hundreds or thousands of unique cloners. The especially unusual part here is the combination of approximately 1,200 top-level unique cloners, almost no page traffic, and a synchronized daily floor across four repositories.

## Explanations checked

- **Repository-local GitHub Actions:** capable of contributing to the October 11 `TrashTreasurePickup` increase, but unable to explain the common baseline because the other three repositories had no Actions runs.
- **Owner activity:** one known Codex review cloned all five public repositories once on October 2. That can explain one event per repository near that date, falls outside the October 3–16 API window, and cannot explain the continuing floor.
- **Public mirrors and indexes:** no Software Heritage or Sourcegraph mirror was found. No public manifest or external code reference contained the four-repository set.
- **Public attention:** no pre-window backlink, star, fork, referrer, or discussion pattern explained the traffic.
- **A universal GitHub artifact:** possible as a contributing measurement effect, but the subject selection and repository-specific push spikes are structured evidence against treating the entire result as meaningless counter noise.
- **A large independent human readership:** some clones may be human, but the aggregate counters cannot measure that fraction and the observable pattern does not support treating the unique total as a count of independent readers.

## What “unique cloner” does and does not establish

GitHub documents the 14-day clone total and daily breakdown and states that clone traffic represents full clones rather than fetches. It does not publicly define a unique cloner as a person, account, machine, or IP address.

A distributed fleet, cloud jobs with changing egress, several independent indexing services, or GitHub's internal aggregation rules could therefore produce a large unique value. The traffic page alone cannot distinguish those possibilities.

## Defensible interpretation

The evidence supports deliberate automated selection. Taylor's work appears to fall within one or more machine audiences' collection criteria, and those collectors repeatedly return. `BackspaceTextRetention` fits that interpretation even though it is not conventional software: its Codex, deletion-retention, surveillance, and model-behavior material may be useful to dataset builders, archival systems, or security research processes.

No evidence supports naming the government or any other particular actor. GitHub does not expose the raw source information required for definitive attribution.

The complete comparison set, citations, public traces, ranked hypotheses, and unsuccessful attribution searches are preserved in [REPORT.md](REPORT.md).

## Attribution

Author: Taylor McCoy
Research and drafting assistance: OpenAI Codex, GPT-6

## License

Licensed under the [MIT License](LICENSE).

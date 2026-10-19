# Are My Repositories Worth More Than $10?

## Read-Only Review and Replacement-Cost Estimate: DobeWorks v2.1 and DEGS v2.1

**Short answer:** As engineering artifacts, plainly yes. No observed sale establishes their present transaction price, and the reconstruction figures below are scenarios rather than recorded development hours.

**Review date:** October 19, 2026<br>
**Reviewer:** OpenAI Codex, GPT-6<br>
**Owner:** Taylor McCoy

## Scope and method

This was a read-only source review of the current public default branches:

- `DobeWorks-v2.1` at commit `9857388f6b48c429834084847bc3b3a04a55f2e2`;
- `DEGS-v2.1` at commit `8d9186666fa1eed2657717017404dfe96c6f8e6b`.

The review used detached local worktrees. No source file, issue, pull request, setting, release, or branch in either target repository was changed. The review covered repository structure, documentation, Python source, schemas and policy records, tests, benchmarks, commit history, portability, release readiness, and two adversarial input probes written only under `/tmp`.

This is a source review, not a penetration test, production qualification, legal appraisal, or claim that every path was inspected exhaustively.

## What the projects are

**DobeWorks** is best described as a **governed agent execution and observation framework** or an **engineering operating-system prototype**. Its runnable public core is deliberately narrow: an Observer converts bounded synthetic telemetry into an explicit evidence state, and a Worker validates a bounded job, runs one controlled attempt, and stages an unaccepted result without promotion authority. The larger repository supplies the assurance standard, phase architecture, evidence packages, validators, threat and recovery controls, figures, and benchmark corpus around those cores.

**DEGS** is best described as an **evidence-based engineering assurance engine** or a **policy-as-code readiness gate**. It validates and evaluates structured records for risk, authorization, evidence, rollback, monitoring, independent review, and human approval. It returns a decision and rule-level explanation. It deliberately does not execute the proposed work, verify that cited evidence is true, or confer authority.

Those descriptions fit the source more accurately than “two Python scripts.” The executable footprint is compact, but the principal work is the explicit control model, failure semantics, test design, evidence structure, provenance, and documentation.

## Artifact inventory

| Measure | DobeWorks | DEGS |
|---|---:|---:|
| Tracked files | 458 | 93 |
| Git commits | 41 | 15 |
| Python source files | 7 | 5 |
| Python test files | 6 | 4 |
| Python source lines | 3,867 | 1,600 |
| Python test lines | 2,549 | 1,597 |
| Markdown documents | 84 files / 5,639 lines | 23 files / 2,193 lines |
| JSON schema, policy, fixtures, and corpus | 23 files / 13,502 lines | 27 files / 20,972 lines |
| Benchmark corpus files | 319 | 16 |
| Rendered figures or evidence artifacts | 11 | 9 |

Line counts describe the review surface; they are not a direct measure of quality, effort, or commercial value.

## Verification results

### DobeWorks

The current public core and benchmark suites passed:

- 70 of 70 Worker and Observer tests;
- 6 of 6 benchmark tests over the published corpus;
- 29 of 29 DEAS validator tests; and
- 19 of 19 Phase 3 validator tests.

The 32 historical Phase 4 package-validator tests were skipped exactly as the README predicts because the original external specification was not supplied. The skip is transparent and intentional, but it means that historical package cannot be independently replayed from the public checkout alone.

The strongest implementation qualities are bounded input and output sizes, explicit JSON-depth limits, duplicate-key rejection, directory-identity checks, symlink and path confinement, deterministic output, atomic staging, fixed retry behavior, privacy-field rejection, and the absence of automatic result promotion. The tests spend substantial effort on failure paths and ambiguity instead of testing only successful examples.

### DEGS

The current published suites passed:

- 67 of 67 unit tests; and
- 5 of 5 benchmark tests.

The gate is standard-library Python, the examples are reproducible, the risk tiers and authority lanes are explicit, and the test suite covers missing evidence, self-approval, rollback, identity drift, schema failure, recursive JSON equality, and Sashiko-derived value behavior. The source and documentation correctly state that a passing record is not proof that its evidence is true.

## Findings

### 1. DEGS accepts duplicate JSON keys instead of rejecting an ambiguous task record

**Severity:** Moderate input-integrity weakness.

`load_task()` uses the default `json.load()` behavior. Python therefore retains the last occurrence of a duplicate key. A copy of the published passing Tier 2 fixture was given two `schema_version` keys—first `999`, then `1`—and `validate` returned `PASS` with exit 0. No target file was modified.

For an ordinary data utility this can be tolerable. For an evidence gate whose job is to make the accepted record unambiguous, silently choosing one of two conflicting fields weakens the fail-closed claim. DobeWorks already implements an `object_pairs_hook` that rejects duplicate keys, so the needed design pattern exists elsewhere in the same project family.

### 2. DEGS can emit an unhandled traceback for excessively nested JSON

**Severity:** Moderate availability and interface-hardening weakness.

`load_task()` catches `OSError` and `json.JSONDecodeError`, but not `RecursionError`, and it applies no byte or nesting limit before decoding. A temporary record containing approximately 1,400 nested arrays caused Python 3.9 to terminate with a `RecursionError` traceback rather than the documented structured `FAIL` result and exit 4.

This does not grant code execution. It does mean an untrusted or accidentally pathological task record can break the gate's machine-readable result contract. A byte ceiling, iterative nesting check, duplicate-key hook, regular-file check, and `RecursionError` handling would align DEGS with DobeWorks' stronger public input seam.

### 3. DEGS can emit an unhandled traceback for invalid UTF-8

**Severity:** Moderate interface-hardening weakness.

An independent Astra source review identified invalid UTF-8 as another exception outside `load_task()`'s handled boundary. A separate temporary-input probe reproduced it: a JSON-shaped file containing byte `0xff` caused an unhandled `UnicodeDecodeError`, empty standard output, and exit 1 instead of the documented JSON `FAIL` result and exit 4. The reviewed repository remained unchanged.

The input loader should catch `UnicodeDecodeError` at the same boundary as `OSError`, `json.JSONDecodeError`, and `RecursionError`, then return the documented machine-readable failure contract.

### 4. DEGS's public-facing copy still describes the public repository as private

**Severity:** Low documentation and adoption defect.

The public repository description says “Private DEGS v2.1 development draft.” The README says “Private development draft,” “Private repository access is currently required,” and “Use this private repository's issues.” The repository is public and the quick-start commands work without private access. These statements make a valid public artifact look inaccessible or accidentally exposed.

### 5. DEGS preserves machine-specific absolute paths in published policy and evidence records

**Severity:** Low portability and clarity defect.

`policy.json`, benchmark results, and historical evidence contain owner-specific absolute home-directory paths. These are useful provenance for a personal snapshot, but they are not portable inputs and can distract a new evaluator from the runnable public seam. The README partly explains that local activation history was excluded; the remaining absolute paths should be clearly labeled as historical records or replaced with repository-relative examples in a future public edition.

### 6. Both repositories are strong inspectable snapshots but unfinished public products

**Severity:** Release-readiness limitation.

Neither repository has a versioned public release, installable package, or repository-local continuous-integration workflow. DobeWorks explicitly limits itself to synthetic Worker and Observer behavior. DEGS reports one tested macOS/Python environment and contains a monolithic 1,213-line gate module with policy concepts repeated across Python, JSON Schema, policy JSON, fixtures, and prose. Those repeated representations create a maintenance and drift risk even though the current test suite passes.

DobeWorks' current public seam is better bounded than its breadth first suggests, but its multi-context historical material makes onboarding difficult. A reader must distinguish the current 70-test core, the assurance standard, old phase packages, preserved validation results, and the retired October 6 bridge experiment. That depth is valuable evidence, but it needs a clearer “current product surface versus historical record” map before a third party could maintain it efficiently.

## Overall engineering assessment

### DobeWorks

DobeWorks is substantial and unusually careful about negative space: what the system cannot know, what it cannot promote, how stale evidence is represented, how partial work is preserved, and how a failure avoids becoming authority. The current synthetic core is coherent, readable, and well tested. I found no confirmed high- or moderate-severity defect in the Worker or Observer public seam during this review.

Its principal limitation is maturity rather than conceptual depth. It is a high-quality research and engineering snapshot, not a deployable multi-agent platform. It lacks live adapters, production monitoring, packaging, release automation, cross-platform verification, and a concise public API. The source honestly says so.

### DEGS

DEGS has a strong control model and a meaningful test-to-source ratio. Its fail-closed risk and approval semantics are more rigorous than those of many larger projects. The two confirmed parser findings matter because DEGS presents itself as a deterministic boundary for evidence records. They are narrow and fixable; they do not invalidate the overall design.

The bigger product question is whether DEGS should remain a personal policy snapshot or become a reusable library. A reusable edition would need a packaged API, bounded canonical input loader, separated rule modules, one generated source of truth for schema and rule identifiers, portable example policy, CI across supported Python versions, and a versioned release contract.

## Independent Astra architecture review

Taylor supplied a separate read-only code-architecture review dated October 19, 2026. It examined DobeWorks commit `9857388` and DEGS commit `8d91866`; it explicitly states that applications and test suites were not run and that no repositories were modified. Its method therefore differs from the executed tests, benchmarks, and temporary adversarial inputs reported above.

The independent review corroborates the strongest positive architectural finding: DobeWorks and DEGS separate observation, assessment, execution, and acceptance so that uncertainty remains visible and completed work does not silently become accepted work. It specifically praises Worker's injected-runner seam, detached input copies, retained expected digest, and forged-output rejection, as well as Observer's use of `UNKNOWN` for stale signals.

It also adds three useful source-level concerns:

1. DobeWorks couples deadlines and staging to platform behavior through process-global `SIGALRM`, compatible main-thread execution, and rejection of an occupied timer. A platform adapter would improve portability without changing policy semantics.
2. Separate path and size checks followed by opening a file can leave a replacement window. The independent review recommends validating the opened file itself when consolidating bounded-file reading.
3. DEGS repeats approval requirements across JSON Schema, Python predicates, and documentary `policy.json`; the runtime does not load the latter. Its limited custom schema interpreter silently ignores unsupported keywords, so a supported-keyword check and focused consistency tests would reduce rule drift.

The independent review prefers keeping DEGS command-line driven at its present scale. That is a reasonable alternative to the reusable-library direction discussed above. Both views agree that the input boundary and policy consistency deserve the next engineering effort.

## Replacement-cost estimate

### Valuation basis

The U.S. Bureau of Labor Statistics reported a May 2025 median annual wage of $135,980 for software developers and a mean of $148,100. The June 2026 Employer Costs for Employee Compensation report said wages were 70% of private-industry compensation. Those figures imply an employer compensation baseline around $93–$102 per productive hour before specialized seniority, management, tools, recruiting, and organizational overhead (U.S. Bureau of Labor Statistics, 2026a, 2026b).

The estimate therefore uses two explicit scenarios:

1. **Independent professional replacement:** $95–$145 per hour, including a seniority and overhead allowance above the BLS-derived baseline.
2. **Specialist consultancy procurement:** $175–$250 per hour as a sensitivity scenario, not as a cited market average.

Hours were estimated by work breakdown rather than multiplying lines of code by a price. The estimate includes requirements recovery, control and domain design, implementation, adversarial tests, benchmarks, documentation, provenance, integration, and review. It excludes building a production service, customer support, sales, hosted infrastructure, formal security certification, and continuing maintenance.

### Estimated hours and replacement cost

| Project | Conventional independent rebuild | Employee/independent cost at $95–$145/h | Consultancy sensitivity at $175–$250/h |
|---|---:|---:|---:|
| DobeWorks public snapshot | 1,350–2,450 hours | **$128,000–$355,000** | **$236,000–$613,000** |
| DEGS public snapshot | 1,020–1,850 hours | **$97,000–$268,000** | **$179,000–$463,000** |
| Combined, after 15%–25% overlap discount | 1,900–3,500 hours | **$181,000–$508,000** | **$333,000–$875,000** |

An efficient AI-assisted reconstruction with the present repositories available as specifications could plausibly take about 450–900 hours after overlap, or roughly **$43,000–$131,000** at the first rate band. That lower figure is the cost to reproduce known artifacts with modern assistance. It is not the cost of independently discovering the domain model, failure semantics, evidence structure, and test cases from scratch.

### What “worth” means here

The figures above estimate **replacement cost**, not sale price. Current public signals show no external stars, forks, issues, revenue, users, support contracts, or versioned releases for DobeWorks and DEGS. Those facts prevent a defensible revenue- or market-based valuation. A buyer could value the governance model, tests, documentation, or strategic fit, but any acquisition price would depend on rights, exclusivity, maintenance commitment, proof of deployment, and the buyer's own avoided development cost.

The supported conclusion is that the codebases embody roughly **low-to-mid six figures of conventional replacement work together**, with a much lower AI-assisted reproduction cost and an presently unproven commercial market value.

## Sources

Astra. (2026, October 19). *DobeWorks and DEGS code architecture review* [Unpublished code review supplied by the repository owner].

McCoy, T. (2026a). *DobeWorks v2.1* [Computer software]. GitHub. https://github.com/tmccoy678/DobeWorks-v2.1

McCoy, T. (2026b). *DEGS v2.1* [Computer software]. GitHub. https://github.com/tmccoy678/DEGS-v2.1

U.S. Bureau of Labor Statistics. (2026a). *Software developers, quality assurance analysts, and testers*. Occupational Outlook Handbook. https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm

U.S. Bureau of Labor Statistics. (2026b, September 9). *Employer Costs for Employee Compensation—June 2026*. https://www.bls.gov/news.release/ecec.nr0.htm

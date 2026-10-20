# Comparable Systems and Cost Context for DobeWorks and DEGS

Prepared: October 19, 2026<br>
Scope: Replacement-cost context

## The candid answer about the $875,000 figure

The $875,000 figure is defensible only as a high-end procurement stress case. It is the result of multiplying both upper assumptions in the earlier model:

> 3,500 reconstruction hours × $250 per specialist-consultancy hour = $875,000

That is about 21.9 person-months at 160 billed hours per month, or 1.68 person-years at 2,080 hours per year. For two security- and governance-oriented systems reconstructed independently—requirements, domain model, implementation, negative-path tests, benchmark corpora, documentation, provenance, integration, and review—that amount of labor is possible. Actual sale price, actual development time, and agent-assisted reproduction effort remain unmeasured.

The ceiling combines the longest modeled schedule with the highest modeled billing rate. That deliberately compounds uncertainty. It is consequently too high to present as the most likely value of the current snapshots. The more informative readings of the same model are:

| Interpretation | Arithmetic | Modeled amount |
|---|---:|---:|
| Conventional independent rebuild, manuscript range | 1,900–3,500 h × $95–$145/h | $181,000–$508,000 |
| Specialist procurement, midpoint of both assumptions | 2,700 h × $212.50/h | $573,750 |
| Specialist procurement, upper stress case | 3,500 h × $250/h | $875,000 |
| AI-assisted reconstruction using the existing repositories as specifications | 450–900 h × $95–$145/h | $43,000–$131,000 |

The U.S. Bureau of Labor Statistics reported a May 2025 median software-developer wage of $135,980. BLS also reported that wages were 70% of private-industry compensation in June 2026. Those figures support the manuscript's approximately $93-per-hour employer-compensation baseline before senior specialization, management, tools, recruiting, and organizational overhead ([BLS, 2026a](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm); [BLS, 2026b](https://www.bls.gov/news.release/ecec.nr0.htm)).

GSA's CALC+ API places a specialist procurement rate near $250 per hour in the upper tail of observed labor-ceiling records. GSA describes CALC+ as a pricing-research source for cost estimates and competitive-price benchmarking and says that its labor-ceiling data are refreshed nightly (U.S. General Services Administration, 2026a). In the October 19, 2026 data, an exact search returned 177 `Senior Software Engineer` ceiling-rate records: the median was $154.65, the mean was $163.48, and the maximum was $318.92 (U.S. General Services Administration, 2026b). The nine `Principal Programmer` records had a median of $188.30 and a maximum of $263.01; one current record was $250.25 (U.S. General Services Administration, 2026c). These awarded labor-ceiling records characterize public procurement rates. The projects have no observed transaction price. Billing all 3,500 modeled hours at $250 remains an aggressive stress case.

| Public-rate illustration | Hourly rate | Cost for 1,900 h | Cost for 3,500 h |
|---|---:|---:|---:|
| Independent model, low endpoint | $95.00 | $180,500 | $332,500 |
| Independent model, high endpoint | $145.00 | $275,500 | $507,500 |
| GSA senior software-engineer median | $154.65 | $293,835 | $541,275 |
| GSA senior software-engineer mean | $163.48 | $310,612 | $572,180 |
| GSA principal-programmer example | $250.25 | $475,475 | $875,875 |

My practical reading is therefore: $181,000–$508,000 is the stronger conventional replacement-cost range; roughly $574,000 is a useful high-end specialist midpoint; and $875,000 is a possible ceiling that needs its assumptions printed beside it.

## What is actually being compared

The reviewed DobeWorks and DEGS snapshots together contain 551 tracked files, 5,467 Python source lines, 4,146 Python test lines, 7,832 Markdown lines, 34,474 lines of schema, policy, fixtures, and corpus material, 335 benchmark-corpus files, and 56 commits. Their cost drivers include explicit authority semantics, failure behavior, adversarial cases, audit evidence, test oracles, and explanatory material around 5,467 lines of executable Python.

The following systems make similar engineering visible. Published build costs are unavailable, so the comparison reports repository scope and maturity while labor and quality remain separately evaluated.

The comparison snapshot was taken October 19, 2026. Physical line counts were calculated from files tracked at the listed commits. Source and test counts cover Python, Go, Rust, C/C++, and Protocol Buffers; tests were classified by conventional test paths and filenames. “Structured material” covers JSON, YAML, TOML, and Rego. The categories are approximate across languages and should be read as scale indicators.

| System | What the official project says it does | Tracked files | Non-test source lines (files) | Test lines (files) | Markdown lines | Structured-material lines | History commits | Contributor records | Releases | Relationship to DobeWorks + DEGS |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DobeWorks + DEGS | Governed agent work/observation plus evidence-based engineering assurance | 551 | 5,467 (12) | 4,146 (10) | 7,832 | 34,474 | 56 | Not used | 0 | Reference pair |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent/tree/04d809ceab9df28f9adaed044884180159172930) | A minimal software-engineering agent with multiple execution environments, model adapters, benchmark runners, and a trajectory inspector | 221 | 5,123 (59) | 9,907 (54) | 3,901 | 2,526 | 1,022 | 39 | 65 | Same raw non-test Python line-count band. Capability, architecture, maturity, and value differ. |
| [in-toto](https://github.com/in-toto/in-toto/tree/e352b43ad7cb8915d84c36d791aa61346152a0a3) | Verifies that supply-chain tasks were performed as planned by authorized functionaries and that products were not altered in transit | 183 | 7,542 (25) | 7,806 (29) | 2,079 | 386 | 2,479 | 49 | 31 | Conceptually comparable; more mature and larger in runnable/test code. The reviewed pair contains much more documentary and corpus material. |
| [Conftest](https://github.com/open-policy-agent/conftest/tree/ca2dfd71a5c673d5f8c207c8788f18c69a6250c7) | Evaluates structured configuration against Rego policies and reports passes, warnings, failures, and exceptions | 344 | 6,686 (65) | 7,156 (49) | 2,083 | 3,217 | 1,310 | 139 | 102 | A close product-form comparator; modestly larger in code/tests and vastly more mature as a maintained public tool. |
| [SLSA verifier v2.7.1](https://github.com/slsa-framework/slsa-verifier/tree/ea584f4502babc6f60d9bc799dbbb13c1caa9ee6) | Verifies cryptographic provenance, expected builders, source repositories, refs, artifacts, containers, and attestations | 911 | 8,475 (58) | 12,514 (21) | 1,158 | 34,239 | 488 | 29 | 45 | The closest whole-repository scale anchor: about twice the reviewed pair's code/test surface, nearly the same structured-material volume, and fewer Markdown lines. Overall it is larger and productized. |
| [Cedar](https://github.com/cedar-policy/cedar/tree/bf15eb3718a291834c403f104aa56d064a72504e) | Implements a fine-grained authorization language, evaluator, validator, symbolic compiler, CLI, language server, formatter, and WebAssembly interface | 973 | 192,340 (311) | 39,729 (49) | 4,393 | 7,738 | 1,545 | 66 | 85 | Far larger. It supplies an upper scale anchor as a large policy-language ecosystem. |

Contributor records were counted from GitHub's first-party contributors endpoints; these records can include bots and omit unattributed contributions. Release and commit counts came from GitHub's first-party repository interfaces on the snapshot date ([mini-SWE-agent contributors](https://api.github.com/repos/SWE-agent/mini-swe-agent/contributors?anon=true&per_page=100), [in-toto contributors](https://api.github.com/repos/in-toto/in-toto/contributors?anon=true&per_page=100), [Conftest contributors](https://api.github.com/repos/open-policy-agent/conftest/contributors?anon=true&per_page=100), [SLSA verifier contributors](https://api.github.com/repos/slsa-framework/slsa-verifier/contributors?anon=true&per_page=100), [Cedar contributors](https://api.github.com/repos/cedar-policy/cedar/contributors?anon=true&per_page=100)).

## Why these systems are useful context

### mini-SWE-agent: similar raw source count, different system

At commit `04d809c`, mini-SWE-agent contains 5,123 physical lines across 59 tracked non-test Python files. DobeWorks and DEGS together contain 5,467 physical lines across 12 non-test Python files. Those totals occupy the same narrow raw line-count band. The comparison is confined to raw source volume because purpose, architecture, module granularity, assurance goals, and maturity differ substantially.

The surrounding artifacts make the difference visible. mini-SWE-agent has 9,907 Python test lines across 54 files, compared with 4,146 across 10 in the reviewed pair. DobeWorks and DEGS have 7,832 Markdown lines and 34,474 structured schema/policy/fixture/corpus lines, compared with mini-SWE-agent's 3,901 and 2,526 respectively. mini-SWE-agent has 1,022 commits at the pinned snapshot, a package, CI, 65 GitHub releases in the October 19 repository snapshot, multiple execution backends and model adapters, benchmark runners, and a documented trajectory inspector. The reviewed pair has more tracked files overall because its evidence and benchmark corpus is unusually large, but it lacks mini-SWE-agent's public product history.

The mini-SWE-agent README describes it as “some 100 lines of python for the agent class.” That statement refers to the central `DefaultAgent` class, followed immediately by the README's acknowledgment of additional environment, model, and run-script code. The complete repository contains 5,123 non-test Python lines beyond that central class ([SWE-agent, 2026](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/README.md)). A roughly 100-line central agent can therefore sit inside an engineering product containing thousands of source and test lines.

### in-toto: the closest conceptual comparison

in-toto separates a project owner's intended supply-chain layout from signed evidence produced by authorized functionaries. Verification checks authorization, expiration, materials, products, required commands, and inspections. That resembles DobeWorks and DEGS in a meaningful way: the artifact carries evidence, authority is explicit, and verification is separate from execution or acceptance. Its official repository also contains governance, security reporting, packaging, continuous integration, and a published installation path ([in-toto, 2026a](https://github.com/in-toto/in-toto/blob/e352b43ad7cb8915d84c36d791aa61346152a0a3/README.md); [in-toto specification](https://github.com/in-toto/specification/blob/master/in-toto-spec.md)).

in-toto has roughly 1.6 times the reviewed pair's combined code-and-test surface and more than 44 times the commit history. It is clearly more mature. DobeWorks and DEGS have almost four times its Markdown volume and far more fixture/corpus material in the reviewed snapshots. DobeWorks and DEGS occupy a recognizable secure-systems design space with substantial evidence and assurance artifacts.

### Conftest: what a mature policy gate looks like

Conftest tests Kubernetes, Terraform, pipelines, serverless definitions, and other structured configurations with Open Policy Agent's Rego language. Its sample output distinguishes passes, warnings, failures, and exceptions, while its `verify` command supports unit testing the policies themselves ([Open Policy Agent, 2026a](https://github.com/open-policy-agent/conftest/blob/ca2dfd71a5c673d5f8c207c8788f18c69a6250c7/README.md); [Open Policy Agent, 2026b](https://github.com/open-policy-agent/conftest/blob/ca2dfd71a5c673d5f8c207c8788f18c69a6250c7/docs/index.md)). This is close to DEGS's basic product shape: structured input, policy evaluation, an explainable result, a CLI contract, and tests for the policy boundary.

Its current source-and-test surface is only about 44% larger than the combined reviewed pair, while its 1,310-commit history, 102 releases, and broad contributor record place it firmly in maintained-public-product territory. DobeWorks and DEGS are substantial engineering snapshots whose present control model and evidence artifacts would require substantial labor to rediscover and reconstruct.

### SLSA verifier: the closest repository-shape comparison

The SLSA verifier's released CLI checks cryptographic provenance and expected builder, source, branch, tag, artifact, container, and attestation properties. Its official documentation exposes multiple verification modes, known limitations, technical design, and release installation paths ([SLSA, 2025](https://github.com/slsa-framework/slsa-verifier/blob/ea584f4502babc6f60d9bc799dbbb13c1caa9ee6/README.md); [SLSA verification specification](https://slsa.dev/spec/v1.2/verifying-artifacts)).

At release v2.7.1 it had about 2.18 times the reviewed pair's combined code-and-test lines and almost exactly the same measured volume of structured material. DobeWorks and DEGS had about 6.8 times more Markdown. SLSA verifier is the larger, productized system. Schemas, provenance samples, negative cases, and verification corpora add substantial engineering surface around a compact primary implementation. The current upstream README describes the project as inactive and directs GitHub Actions users toward newer attestation tooling, illustrating a transition in product status after substantial historical investment ([SLSA, 2026](https://github.com/slsa-framework/slsa-verifier)).

### Cedar: a clear boundary on the comparison

Cedar includes a parser, evaluator, typechecker, schema validator, symbolic compiler, formatter, CLI, language server, WebAssembly interface, integration tests, corpus tests, and fuzzing support. Its maintainers describe it as designed for automated reasoning and differential random testing ([Cedar Policy, 2026a](https://github.com/cedar-policy/cedar/blob/bf15eb3718a291834c403f104aa56d064a72504e/README.md); [Cedar Policy, 2026b](https://github.com/cedar-policy/cedar/blob/bf15eb3718a291834c403f104aa56d064a72504e/cedar-testing/README.md)).

Cedar has more than 24 times the reviewed pair's code-and-test lines and supplies an upper boundary for the policy-and-assurance family. DobeWorks and DEGS are substantial prototypes; Cedar is a mature language ecosystem with an undisclosed development cost. Cedar plays no role in the $875,000 ceiling.

## What the comparisons support

These comparisons support four conclusions:

1. The pair is much larger than its five main Python modules suggest. The executable core is the smallest visible layer of an evidence, test, and assurance artifact.
2. The pair has a real peer group. in-toto, Conftest, and SLSA verifier all spend engineering effort on explicit policy, provenance, authorization, failure semantics, structured records, and verification.
3. The pair is substantially less mature than those products. It has no public releases, package contract, production adapters, sustained contributor base, or comparable maintenance history. That limits present commercial value and argues against treating the consultancy ceiling as ordinary value.
4. A 1,900–3,500-hour clean-room range is plausible, but its top endpoint is judgmental. It becomes credible when “replacement” includes rediscovering the control model, writing the negative cases, constructing evidence corpora, and documenting the reasoning. It becomes too high if replacement means reproducing only the present executable behavior from the existing repositories.

For a single personal-context estimate, approximately $400,000–$575,000 is a more balanced conventional-to-specialist center of gravity for an independent clean-room reconstruction of both snapshots. The existing $875,000 remains a valid “expensive specialist engagement went all the way to both upper assumptions” ceiling. The $43,000–$131,000 range remains the more relevant estimate for a competent team using the current repositories, tests, and documents as a specification with modern AI assistance.

## References

Bureau of Labor Statistics. (2026a). *Software developers, quality assurance analysts, and testers*. U.S. Department of Labor. https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm

Bureau of Labor Statistics. (2026b, September 9). *Employer costs for employee compensation—June 2026*. U.S. Department of Labor. https://www.bls.gov/news.release/ecec.nr0.htm

Cedar Policy. (2026a). *Cedar* (commit `bf15eb3`) [Source code]. GitHub. https://github.com/cedar-policy/cedar/tree/bf15eb3718a291834c403f104aa56d064a72504e

Cedar Policy. (2026b). *Cedar testing* (commit `bf15eb3`) [Software documentation]. GitHub. https://github.com/cedar-policy/cedar/blob/bf15eb3718a291834c403f104aa56d064a72504e/cedar-testing/README.md

in-toto. (2026a). *in-toto* (commit `e352b43`) [Source code]. GitHub. https://github.com/in-toto/in-toto/tree/e352b43ad7cb8915d84c36d791aa61346152a0a3

Open Policy Agent. (2026a). *Conftest* (commit `ca2dfd7`) [Source code]. GitHub. https://github.com/open-policy-agent/conftest/tree/ca2dfd71a5c673d5f8c207c8788f18c69a6250c7

Open Policy Agent. (2026b). *Conftest documentation* (commit `ca2dfd7`) [Software documentation]. GitHub. https://github.com/open-policy-agent/conftest/blob/ca2dfd71a5c673d5f8c207c8788f18c69a6250c7/docs/index.md

SLSA. (2025). *SLSA verifier* (version 2.7.1, commit `ea584f4`) [Computer software]. GitHub. https://github.com/slsa-framework/slsa-verifier/tree/ea584f4502babc6f60d9bc799dbbb13c1caa9ee6

SLSA. (2026). *Verifying build artifacts*. https://slsa.dev/spec/v1.2/verifying-artifacts

SWE-agent. (2026). *mini-SWE-agent* (commit `04d809c`) [Computer software]. GitHub. https://github.com/SWE-agent/mini-swe-agent/tree/04d809ceab9df28f9adaed044884180159172930

U.S. General Services Administration. (2026a). *CALC+ Quick Rate API*. https://open.gsa.gov/api/dx-calc-api/

U.S. General Services Administration. (2026b, October 19). *CALC+ labor ceiling rates: Senior Software Engineer exact search* [Data set]. https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=labor_category:Senior%20Software%20Engineer&page=1&page_size=100&filter=price_range:15,500

U.S. General Services Administration. (2026c, October 19). *CALC+ labor ceiling rates: Principal Programmer exact search* [Data set]. https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=labor_category:Principal%20Programmer&page=1&page_size=100&filter=price_range:15,500

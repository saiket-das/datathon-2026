# R-G02 · B14 intermediary-collision generator alternatives (design, NOT FROZEN)

**Investigator:** G. **State:** independently specified research design; NO sponsor-data execution, NO outcome access, NO designated validation freeze. This file is not a claim of B14 replication. R-G01 remains frozen separately.

## Previously exposed information and independence limit
Other investigators' published aggregates report July intermediary collision 0.6229%, a May-weighted forecast 0.6088%, a uniform comparator 0.0242%, and country-joint TV 0.0164. These are prior exposure, not G's observations. Do not tune a threshold to these values, or present a same-dataset reproduction as external confirmation. Do not inspect D/E blind work.

## Mechanism alternatives
- M0: independent uniform intermediary selection from a prespecified eligible bank universe.
- M1: global May marginal intermediary frequencies, with replacement conditional on route length.
- M2: May intermediary frequencies conditional on source/destination country pair and route length; back off only via a prespecified hierarchy.
- M3: path-template or sender/receiver bank conditioned sampling, with a finite set of repeated intermediary motifs.
- M4: sampling without replacement (or explicit within-route deduplication), which predicts suppressed repeated intermediaries even under concentrated marginals.
- M5: latent batch/time mixture with bank concentration shifts, capable of producing similar overall collision rates without the proposed country generator.

## Identifiability threats
The collision indicator must be defined before inspecting rows: repeated intermediate BIC8 within one route is not the same as shared intermediary between distinct routes, and repeated full path templates are not independent draws. Conditioning on path length is mandatory because opportunities for collisions scale with intermediate-node count. A single scalar collision rate cannot identify the sampling mechanism; compare conditional collision, concentration, route motifs and temporal drift on the same eligible records. Bank overlap, template reuse and shared country pairs induce dependence.

## Prospective cohort and exclusions (to freeze after schema-only verification)
Training: UTC May 2023; designated validation: UTC July 2023, based solely on previously exposed EPOCH_SECONDS period support. Freeze the exact BIC8_PATH tokenizer, treatment of empty/invalid tokens, role of first/last endpoints, definition of intermediaries and route-length bins **before** any May feature counts or July outcomes. All payment types are initially in scope; report by TRANSACTION_TYPE_CODE as secondary stratification, not an opportunistic filter. Routes with fewer than two intermediary positions cannot contribute to within-route collisions; report their count as structurally ineligible, not as negatives. Unknown/malformed paths are a separate unsupported population. Exact denominators remain unknown.

## G-032 prospective May-only estimator and fallback contract (design amendment, NOT a freeze)

For each eligible May route, count each observed intermediary **position**, including repeated positions, rather than one vote per unique bank or route. Define the candidate universe U solely from distinct intermediary BIC8 tokens in eligible May routes. No July token may enlarge U. The uniform M0 comparator uses U and abstains if U is empty; unseen July intermediary identities affect observed collision labels but never model weights. The estimator is conditional on May support, not a claim that the synthetic generator draws from a fixed universe.

Define an intermediary count k as the number of positions strictly between the two visible endpoints. Proposed M1 global weight for category b in U: (n_b + alpha)/(N + alpha*|U|), with alpha=1 fixed *before* reading May counts. For M2 use the same Dirichlet-one smoothing in each supported stratum, retaining the global U for every stratum, not a stratum-specific bank universe. A stratum is a **directed** visible-endpoint country pair and exact k. No July-derived country-pair, route-length or bank-frequency statistic enters fitting. Candidate country attribution must come from a prespecified static BIC-country mapping verified separately; if no reliable mapping exists, M2 is **unsupported**, not inferred from July or silently replaced with M1.

Proposed deterministic backoff for M2, assessed using May **eligible route counts** (not intermediary-position counts): directed country pair + exact k if at least 100 May routes; otherwise directed country pair pooled across k if at least 100; otherwise global exact k if at least 100; otherwise global M1. Empty U or unavailable required country mapping produces explicit abstention. The fallback level and number of routes at each level must be reported privately for both May and July; this hierarchy is fixed in advance as a *candidate* and cannot be described as validated or tuned. M0/M1/M2 must be compared on the identical common eligible July route set, with a separate model-specific coverage table.

**Key identifiability caveat:** M1/M2's May intermediary-position marginals are estimated from routes that may already contain motifs or deduplication, so fitting these weights does not prove iid sampling. Dirichlet-one smoothing across a large U may substantially dilute sparse strata. Predeclare sensitivity analyses for alpha=0.5 and 2 as secondary only; no selection by July score. Never use published B14 percentages to tune alpha or fallback support.

**Still unresolved before scientific freeze:** verified static country mapping and path schema; exact M3 motif likelihood, M4/M5 estimators, train-only model selection, log-score clipping, July week boundaries, minimum cluster count, bootstrap seed/replicates, primary threshold and multiplicity adjustment. This amendment supplies a concrete estimator candidate, **not** a complete R-G02 frozen executable or permission to inspect July.

## Candidate discriminating tests (NOT YET AUTHORISED TO RUN)
1. Fit M0–M3 solely on May; compute July predicted collision probability by country pair and intermediate count, using the exact same July eligibility for all models. Use a prespecified hierarchical fallback for unseen country pairs and report fallback coverage separately.
2. Test M4 by comparing observed repeat probability with the with-replacement baseline on routes having at least two intermediate positions, retaining route-length strata.
3. Test M3 using a predeclared full-template recurrence statistic on July, with May-derived motif support only; separately quantify entirely new templates.
4. Test M5 by dividing May into chronological training blocks and July into prespecified weekly blocks; report temporal instability without selecting a favorable block.
5. Compare predictions with paired per-route log score and Brier score for collision probability; use cluster bootstrap by directed endpoint pair, and a conservative bank-overlap sensitivity analysis. A paired metric is only valid when both models predict the same route.

## Required pre-outcome freeze
Before July access, commit an executable, synthetic fixture tests, source schema contract, exact eligibility, M0–M5 formulas, smoothing/fallback, minimum support, validation weeks, primary metric, cluster bootstrap seed/replicates, rejection threshold and multiple-testing adjustment. Commit and record SHA of both protocol and executable. Designated validation must run on a separately approved, read-only, authenticated complete Parquet input with private output. Never repurpose the R-G01 validation approval.

## Report contract
Private report must include total July rows, parseable rows, eligible routes, structurally ineligible routes, unsupported/malformed paths, missing/other labels, per-length and country-pair support (small cells suppressed with complementary protection), exact observed collision numerator/denominator, model-wise paired coverage and error/loss, cluster counts and uncertainty, failure strata and alternative mechanisms still compatible. Report prior aggregate exposure and all deviations. No raw paths, BICs, accounts, identifiers or unreviewed small cells on public GitHub.

**Current verdict:** DESIGN ONLY, UNEXECUTED. No sponsor-data observations, no model fitting, no validation results, no code freeze. Next step is a dataset-independent synthetic tokenizer/eligibility fixture and a separate immutable R-G02 executable, not outcome inspection.

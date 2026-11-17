# H-F04 — Is bank-pair FX overlap limited by occupancy or state sorting?

- **Owner:** Investigator F. Scientific role: independent cross-mechanism synthetic payment generator discovery.
- **Status:** PROPOSED EXPLORATORY ONLY. No H-F04 execution, no freeze, no held-out validation or independent confirmation.
- **Confidentiality:** This public file contains ONLY prospective definitions. All results and private runner provenance from earlier H-F experiments are held outside GitHub. Do not quote/reproduce their observed counts, effects, hashes, job IDs, fingerprints or restricted reports.
- **Pre-existing exposure:** Investigator F received previously reviewed H-F01/H-F02 exploratory summaries and a complete private H-F03 report before proposing H-F04. H-F01's original invocation and executor record remain unknown. The earlier H-F02 parser failure and H-F03 local fixture/mount-depth failure remain preserved in the F ledger. No July outcome was opened in F's exploration.

## Explanatory alternatives

1. **Occupancy/sparsity null:** Directed bank pairs generally receive too few observations to meet a high support requirement in *both* FX categories, regardless of a bank-specific FX mechanism.
2. **Composition-constrained null:** Bank pairs may be located in coarse route/currency/party or country corridors with different FX-state frequencies. The apparent bank-pair overlap pattern could follow solely from those coarse category frequencies and pair occupancy.
3. **Bank-specific FX sorting:** Even conditional on coarse group FX marginals, the distribution of FX labels across directed bank pairs is more concentrated than an exchangeable assignment would predict.
4. **Repeated-account selection:** Stable originating/beneficiary account relationships may produce bank-level concentrations without a bank-level FX generator rule.

No one pattern establishes generator code, processing order or causal assignment.

## Predefined development data and controls

Use exclusively May–June 2023 UTC, `ANOMALY_TYPE IS NULL`, `USD_AMOUNT >= 0`, `TOTAL_DURATION >= 0`, `PARTICIPANT_COUNT BETWEEN 2 AND 5` and `CURRENCY_CONVERSION_COUNT IN (0,1)`, matching the H-F03 development universe. Verify source manifest, 26 columns, unique ROW_IDs and five file counts locally before any analysis; these source integrity checks are not permission to read July outcomes. Keep the exact ordered pair (`ORDERING_BIC8`, `BENEFICIARY_BIC8`) and null-safe grouping conventions from H-F03. Use exact same full eligible universe, then a separate H-F03-style S0 common-support population as a sensitivity, **not interchangeable populations**.

Fix **support thresholds t = 1, 5, 10, 25, 50, 100** payments per FX state. In every population and at each threshold:
- Count all distinct directed bank pairs, both-state pairs, FX0-only pairs and FX1-only pairs (local-only).
- Calculate the **capacity bound**: how many pairs have at least `2t` payments total and thus could possibly meet the threshold. This is a necessary, not sufficient condition.
- Calculate the actual both-state eligible pair count; state-specific retained payment totals and full-universe coverage, plus the fraction of capacity-eligible pairs actually supported.
- Report the full pair-size distribution only as private aggregate counts or prespecified quantiles, never a bank-pair identifier or a small cell in public output.
- Detect and preserve any arithmetic nonconservation, unsupported groups and differences from an H-F03 cohort replication.

## Explicit competing allocation benchmarks

All allocation benchmarks hold the observed payment rows, bank-pair occupancy, coarse stratum memberships and source eligibility fixed. Only hypothetical FX labels are reassigned. They do not constitute causal interventions or valid significance tests under reused accounts.

- **M0 global exchangeability:** assign exactly the overall observed FX1 count among eligible rows uniformly, to illustrate how much support is constrained by pair occupancy alone.
- **M1 S0-conditional exchangeability:** independently reassign FX labels within each route × participants × currency × B/C party pair × gap-count cell, preserving exact FX0/FX1 marginal counts in each cell.
- **M2 corridor-conditional exchangeability:** as M1, but additionally condition on ordering and beneficiary country. Cells with one state only remain one-state. Preserve NULL as a grouping value rather than removing it.
- For each benchmark, perform **32 deterministic exploratory replicate reallocations** using a fixed seed `20261117` plus replicate index; preserve exact within-stratum FX-state totals by ranking a deterministic pseudorandom score of unique row ID. Do not use naive independent Bernoulli assignment when it would alter marginals.
- Report private distributions of matched directed bank-pair support and retained-payment coverage at every threshold: **median, minimum, maximum, 10th and 90th empirical percentiles** from the 32 replicates; no nominal p-values or confidence intervals. Preserve all failed replicates; do not silently reduce the sample count.
- An implementation must guarantee no reuse of deterministic hash values as bank identifiers in output. Keep shuffled labels, per-row scores and partner bank/account IDs local, never in stdout or GitHub.

## Entity-reuse and path-selection diagnostics (local only)

Compare the bank-pair overlap pattern with the number of repeat payments per directed **account pair**, and the fraction of account pairs that appear in both FX states, only as large private aggregate totals/quantiles. This is an **exploratory diagnostic**, not an additional null model that assumes account independence. If account-pair signatures are overwhelmingly single-state, the account-mix mechanism remains plausible. Do not assume time ordering or that banks cause the account mix.

## Predetermined interpretations and counterexamples

- **Capacity-limited result:** near-zero capacity at a threshold means an observed near-zero overlap is primarily a sampling feasibility limitation; bank-specific FX sorting is not established.
- **Composition-only compatibility:** if observed overlap is inside broad distributions under M1/M2, the bank-specific sorting mechanism adds little *descriptive* evidence beyond the chosen conditioning.
- **Additional bank-pair sorting candidate:** if observed overlap is consistently below all M2 permutations at several thresholds **where occupancy capacity is appreciable**, pair-specific sorting remains a plausible generator component. But unmeasured account/repeated-path dependence and exchangeability violations remain alternatives.
- **Counterexamples:** unexpectedly high observed mixed-state support; expected support also disappearing under M0; severe differences between all eligible and S0-selected records; results reversing under M1 versus M2; strong repeated-account concentration; insufficient permutation replicates.
- **Control:** rerun only an *identical* H-F03 cohort definition and count the same universe to establish comparability, but do not rerun or reconstruct H-F03's private final report.
- **No inferential shortcuts:** permuted-null distributions under row exchangeability are diagnostic expectations, not uncertainty intervals accounting for correlated banks, accounts, or causal mechanisms.

## Execution and disclosure plan

- **Input:** a new F-only exploratory code commit after coordinator has reviewed implementation, resource/cutoff constraints and self-tests. This hypothesis is NOT a run authorization.
- **Sandbox:** existing offline, read-only five-Parquet local executor. No sponsor-data hosted GitHub Actions.
- **Output:** private git-ignored `dataset/private_reports/H-F04_occupancy_state_sorting.md`, and private runner metadata. Never publish full results without explicit independent disclosure approval; do not echo source fingerprint, report hash or private job identifier to GitHub.
- **Resource expectation:** permutations across millions of records can be expensive; seek an occupancy-only local dry run and a no-sponsor synthetic permutation test before approval. The coordinator should budget RAM and scratch disk empirically and enforce the fixed hard cutoff.
- **Cutoff:** 18 Nov 2026 at 20:00 MYT; a local supervisor must terminate in-flight runs, not only prevent new starts.
- **Schedule:** F's hourly ChatGPT automation remains gated until a genuine *scheduled* private recovery cycle verifies exact new job ID, execution commit and approved private results. Old task stays untouched.

## Status / validation register

- Exposures: earlier F exploratory work seen privately; not reproduced here.
- H-F04 source implementation: none.
- H-F04 synthetic test: none.
- H-F04 dataset run: none.
- H-F04 results: none.
- Frozen hypothesis/validation gate: none.
- Next step: coordinator review this independent mechanism-focused study and approve implementation before any local execution.


## Implementation addendum: phased, private-only exploratory source (17 Nov 2026 MYT)

This addendum records **prospective code preparation**, not experimental outcomes. None of H-F04's sponsor-data findings, supports, source fingerprints, private execution metadata or report hashes have been seen by Investigator F or published in this repository.

**Script:** `analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py`, initial implementation commit `dd0de73feef33105cd959426b4e6f41327efa635`; corrected source-and-fixture commit `03f55694b80f5bb2fe7c6b754296e34508f5e242`. The second commit explicitly counts records with missing directed BIC endpoints in the **private report** and makes the synthetic fixture assert **within-S0 and within-S1 exact FX marginals**, not only the overall FX total. Nulls remain valid stratum labels. All other threshold and benchmark definitions remain as predeclared above.

**Phased execution proposal, from repository root:**

1. Pure invented-fixture SQL check: `uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --self-test`.
2. Capacity, observed overlap, pair-size and repeated-account descriptive checks: `uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --data-dir /mnt/f-parquet --phase capacity`.
3. Only after resource review, independent full-universe conditional FX assignments: `uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --data-dir /mnt/f-parquet --phase permute --population dev`.
4. Separately, coarse common-support sensitivity: `uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --data-dir /mnt/f-parquet --phase permute --population P0`.

Every phase operates on the same *May–June only* source eligibility and read-only verified source paths; `P0` includes both FX states in every matched S0 group with >=100 observations per state. `P0` support joins use `IS NOT DISTINCT FROM`, matching the prior H-F03 semantics. The ordered bank-pair key is preserved, including null-containing keys for comparability; a separate local-only missing-BIC coverage audit warns if a grouped unknown endpoint could be mistaken for a genuine exact-bank pair.

**Private phase outputs** (all under Git-ignored `dataset/private_reports/`; no public output):

- `H-F04_occupancy_state_sorting_capacity.md`
- `H-F04_occupancy_state_sorting_perm_dev.md`
- `H-F04_occupancy_state_sorting_perm_p0.md`

The earlier single-file output proposal is superseded **only operationally** so long-running permutations can be reviewed independently and interrupted jobs cannot overwrite a prior report. Every final/partial report is fail-closed against overwriting. No result publication is authorised.

**Exact fixed-marginal implementation:** for benchmark `M0`, globally; `M1`, partitioned by S0; and `M2`, partitioned by S1, deterministically rank distinct source row IDs by `hash(row_id, seed)` with `row_id` tie-breaking and assign exactly the original number of FX1 labels within each partition. Fixed seeds `20261117` through `20261148` are used for **32** replicates per model per population. This tests row-exchangeability expectations only. The synthetic fixture includes null group keys, repeated account pairs and three separate bank-pair strata with sufficient FX0/FX1 support; both total and conditional marginals are asserted in the latest script. The revised source and fixture have **not been executed by Investigator F**. An offline coordinator must run fixture and perform an independent code/scale review before approving payment-data use.

**Resource and failure control:** each `--phase permute` run is potentially expensive (96 window sorts over an eligible population); schedule/review it independently after `--phase capacity` with at least 6–8 GiB available memory and 20–40 GiB private free scratch as planning allowances, **not measured peaks**. The DuckDB per-process memory limit is 3 GiB and thread count 2. Coordinator must enforce the absolute 18 November 2026 20:00 MYT termination externally; the script also checks the cutoff between operations. Any OOM, SQL test failure, incomplete replicate or missing fixed-margin conservation must be reported as a failed attempt, not silently omitted.

**Source-only and privacy constraints:** there is no `SELECT *`; the source view explicitly lists all 26 authorised columns. Source fingerprint values are computed only in the private local executor and must be checked against the local approved manifest. Account pair diagnostics exclude null account identifiers **only in that diagnostic** and report excluded volume privately; this does not redefine the payment universe. No bank/account names, observed pair sizes, transaction contents or report hashes are written to stdout/GitHub.

**H-F04 scientific state:** Proposed protocol + reviewed-source candidate, **NO execution, NO validation freeze, NO July exposure**. Source requires fixture/runtime approval, and coordinator must preserve each failure and private return before any interpretation.

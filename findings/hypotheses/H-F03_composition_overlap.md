# H-F03 — Fixed-support FX–duration composition decomposition and exact-bank overlap

- **Owner:** Investigator F, autonomous cross-mechanism generator discovery.
- **Status:** PROPOSED EXPLORATORY experiment; **not executed, not frozen**, no designated validation outcomes opened.
- **Script:** `analysis/40_cross_mechanisms/H-F03_composition_overlap.py`.
- **Output:** **LOCAL-PRIVATE ONLY**, `dataset/private_reports/H-F03_composition_overlap.md` (ignored by Git); no numerical results, fingerprints, output hashes, or run provenance may be copied to this public repository without separate, explicit disclosure approval.
- **Population:** May 1 inclusive through July 1 exclusive, 2023 UTC; `ANOMALY_TYPE IS NULL`, nonnegative amount/duration, 2–5 participants, FX step count **exactly 0 or 1**. Any overall count of other FX states is outside the estimand. Reproduce, do not redefine, prior H-F01/H-F02 eligibility for these two states. Source preflight checks full ten-million-row and 26-column structure but makes no July **outcome** queries.
- **No inference claim:** these are descriptions of selected, repeatedly observed account/bank populations, not a causal FX effect, exact generator implementation, independent confirmation or new held-out test.

## 1. Prior exposure and failed-run register

F has already privately received coordinator-reviewed exploratory summaries from H-F01 and H-F02 concerning route/FX/duration and payment mix, including the negative coarse association, tighter-country contrasts and the failure of strict exact-bank-pair matching to retain supported strata. **Deliberately omit all private amounts, denominators, hashes, dates/identifiers of offline jobs and other restricted execution metadata here.** The full H-F01 original remains locally held back due to complementary small-cell disclosure risk; its original invocation and runtime provenance are unknown and must not be reconstructed. H-F02's first local attempt failed while preparing its SQL development view due to ambiguous alias syntax; this failed attempt was preserved. A minimal explicit `AS` correction was separately committed, followed by a coordinator-reviewed successful *exploratory* S0–S3 run, with S4 disabled and without opening July outcomes. Neither H-F01 nor H-F02 is a frozen validation. Both prior experiments and this H-F03 plan may share banks, senders, beneficiaries, paths and already-exposed records. E's independent results remain unavailable; no E cross-pollination.

## 2. Falsifiable scientific questions and competing mechanisms

- **Composition-selection mechanism:** the FX state reallocates observed payments across slower/faster supported strata; an overall association can therefore arise without a uniform within-stratum processing difference.
- **Within-stratum association:** FX0/FX1 log durations differ even after conditioning on route, party pair, currency, gaps and observed country/amount groups. The association might still reflect hidden banks, accounts, amount or timing selection rather than FX processing.
- **Bank-pair positivity failure:** exact directed bank pairs seldom exhibit both FX states with meaningful support. The zero-supported result under an earlier strict threshold might represent insufficient sample size, near-deterministic FX assignment or a mixture of both.
- **Reference-distribution sensitivity:** an apparent within/selection allocation is sensitive to whether the comparator uses the FX0 distribution, FX1 distribution, symmetric average, or pooled-payment reference.
- **Counterexamples:** a stratum-level reversal; disappearance of the conditional difference after fixing the same population; negligible shared-bank coverage even at the lowest thresholds; or a decomposition that does not close numerically.

## 3. Cohorts and fixed-common-support comparisons (development only)

Represent `Y_d=ln(1+TOTAL_DURATION)` and `Y_a=ln(1+USD_AMOUNT)` with FX state 0 or 1, and discard neither state selectively after estimating strata.

Construct nested **common-support** populations (both states must have at least **100 payments** in every included stratum):

- `P0`: S0 support, where S0 = route × participant count × currency × B/C pair × gap count.
- `P1`: restriction of P0 to S1 support, where S1 = S0 plus ordering-bank country and beneficiary-bank country.
- `P3`: restriction of P1 to S3 support, where S3 = S1 plus `min(31,floor(log2(1+USD_AMOUNT)))` amount band.

Calculate S0 on P0; **both S0 and S1 on the exact same P1 records**; and **S0, S1 and S3 on the exact same P3 records**. Report population and state-specific denominators and coverage relative to the same original FX0/FX1 development universe. This deliberately prevents the fallacy of interpreting different support populations as a pure covariate adjustment.

For any specific fixed population and grouping, let `n_fs` and `mu_fs` be FX-specific stratum counts and mean log outcome; `p_fs=n_fs/sum_s(n_fs)`. Define `D=sum_s(p_1s mu_1s)-sum_s(p_0s mu_0s)`. Reproduce **exactly** three decompositions:

- **FX0 reference:** `W0 = sum_s p_0s (mu_1s-mu_0s)`, `C0=sum_s (p_1s-p_0s) mu_1s`, so `D=W0+C0`.
- **FX1 reference:** `W1 = sum_s p_1s (mu_1s-mu_0s)`, `C1=sum_s (p_1s-p_0s) mu_0s`, so `D=W1+C1`.
- **Symmetric reference:** `Wsym=(W0+W1)/2` and `Csym=(C0+C1)/2`, so `D=Wsym+Csym`.

Add the **pooled payment-weight** within coefficient `Wpool=sum_s((n_0s+n_1s)/(N0+N1)) (mu_1s-mu_0s)`, and the residual `D-Wpool` (interpret this as a reference-specific algebraic residual, not uniquely causal 'composition'). Also calculate the previously used minimum-state-count weighted contrast as a distinct estimand, together with group-distribution TV = `0.5*sum_s |p_1s-p_0s|`. Report weighted amount decompositions as a payment-mix diagnostic, **not** a null placebo. Check closure numerically; fail safely if any decomposition does not reproduce D within 1e-8.

## 4. Exact directed-bank FX-overlap audit

Within **all** development-eligible FX0/FX1 records and, separately, within the fixed S0 common-support P0 population, locally group by `(ORDERING_BIC8, BENEFICIARY_BIC8)`. For **preselected thresholds 1, 5, 10, 25, 50 and 100** payments per FX state, report only private aggregated pair counts, state-specific matched payment totals and coverage. Report total observed bank pairs, both-state pairs, state-only pairs, and state-specific overall denominators, all **private**. No bank strings, hashes of bank identities, row samples or path sequences leave DuckDB. No July data read.

If exact-bank overlap disappears at high but not low thresholds, support-driven non-identification remains plausible. If it is absent even at threshold 1, an FX state–bank-pair constraint becomes a stronger candidate, still not proof of the original rule. The audit must not collapse 'no support' into a zero effect.

## 5. Coverage, selection and robustness constraints

- Nested population retention `P0 ⊇ P1 ⊇ P3`, counts in both states and percentage coverage of the starting FX0/FX1 development universe must be reported.
- Within the **same population**, compare coarse/fine decomposition, not only the separate P0/P1/P3 estimates.
- Reference weighting must be varied as specified; stratum mix TV and min-count weighted estimates expose concentration and dependence on the target distribution.
- Explicitly report empty/missing support and smaller groups in the **local-only report**. Public disclosure requires a separate review, including prevention of complementary cell recovery from totals.
- No analytic confidence interval is asserted: payments share parties, banks, routes and prior exposures. Any later internal validation needs a separately frozen bank/account-aware uncertainty design, thresholds, code SHA and precise eligible cohort **before opening July outcomes**.
- Because amount may itself reflect selection or processing, conditioning on amount is a sensitivity analysis, not a clean intervention. Conditioning on country or bank may similarly block or induce associations.
- We cannot infer generator source code or temporal causal ordering from these identities or matching patterns alone.

## 6. Proposed local job (not yet approved/executed)

**Input:** latest reviewed F-only commit after adding this exact hypothesis and script.  
**Working directory:** `C:\\Users\\IRTIZA\\Projects\\datathon-2026-R2-F` on the coordinator's existing local runner, or its mapped offline Docker worktree.  
**Data directory:** `/mnt/f-parquet` in the existing offline Docker runner (as used by the coordinator).  
**Command:** `python analysis/40_cross_mechanisms/H-F03_composition_overlap.py --data-dir /mnt/f-parquet`.  
**Optional self-test:** `python analysis/40_cross_mechanisms/H-F03_composition_overlap.py --self-test`; requires no sponsor files.  
**Private output:** `dataset/private_reports/H-F03_composition_overlap.md` (under the worktree, git-ignored).  
**Run mode:** exploratory May–June only, read-only source; no validation and no S4 exact path analysis. Coordinator must approve the exact commit, audit untracked/private outputs and publication restrictions, check dataset checksums against its **local** approved manifest, and return an authenticated private run report/exit code and output hash. Do not upload this output to GitHub. Only a safe non-numeric status may be appended to the public F ledger after coordinator review.

**Expected resource needs:** DuckDB 3 GiB configured memory ceiling, two query threads and separate Python runtime overhead; coordinator should reserve **at least 5–6 GiB RAM and 10–20 GiB available private scratch disk** for local sorting/hash aggregation, with the full existing five Parquet partitions available read-only. These are planning provisions, not measured peaks. Use a local private DuckDB spill directory and terminate any in-flight research by the 20:00 MYT hard cutoff.

**Freeze:** NONE. **Validation:** NOT ATTEMPTED. **Scientific release:** private coordinator-reviewed aggregates only.

## 7. Execution / counterexample register

- Code and hypothesis submitted for review: pending GitHub commits.
- Local self-test: not run by F; coordinator must verify.
- Full-data H-F03 test: not executed.
- Supported population and effect estimates: **none observed by F**.
- Falsified mechanisms: **none established by H-F03**.
- Failed attempts: none yet under H-F03; prior H-F02 preparatory syntax failure explicitly retained above.
- Future: update this record only after a reviewed private job handoff, avoiding restricted details in GitHub.


## 17 Nov 2026 MYT — implementation and private queue proposal

- **Design document:** established in Git before any H-F03 payment outcome access.
- **Implementation:** `analysis/40_cross_mechanisms/H-F03_composition_overlap.py`, source commit **`d6303983012a7a4e6fed2e0af9d663486328a913`** (contains source-typed invented-fixture self-test; previous script commits were preparatory).
- **Frozen confirmation plan:** **NONE**. This Git commit captures an exploratory design; it is not a frozen validation plan and does not license access to July outcomes.
- **Data exposure by F during this design:** No H-F03 source rows, matched group outcomes, bank identities or validation data read. Existing H-F01/H-F02 exploratory evidence was disclosed privately and informs the design; its protected counts, report hashes and executor metadata are deliberately absent here. Prior H-F02 parser failure remains a recorded failed attempt without scientific outcomes, not a falsification of H-F02.
- **Local test:** Neither `--self-test` nor `uv run pytest` has been executed by F in this Chat because available local Python/container runtimes returned client errors. A Docker/Windows coordinator must execute them; no pass is claimed.
- **Approval candidate:** `python analysis/40_cross_mechanisms/H-F03_composition_overlap.py --self-test` followed, only if approved and fixture passed, by `python analysis/40_cross_mechanisms/H-F03_composition_overlap.py --data-dir /mnt/f-parquet`. No other flags are needed. The coordinator checks the computed local five-source SHA-256 digests against its reviewed private manifest and preserves the run command, environment, exit code and output hash **locally**, not in GitHub.
- **Expected private report:** `dataset/private_reports/H-F03_composition_overlap.md`; report is Git-ignored by the existing `/dataset/*` rule. Temporary private DuckDB scratch: `dataset/private_reports/.duckdb_tmp`.
- **Resource provision:** DuckDB memory limit 3GB, threads=2, minimum 5–6 GiB RAM allocated to the local runner with 10–20 GiB private scratch free. No source records may be uploaded to GitHub/hosted CI, and no report is public by default.
- **Cutoff:** Never start at or after 2026-11-18 20:00 Asia/Kuala_Lumpur; local supervisor must also terminate any in-flight process at cutoff.
- **Output interpretation:** no H-F03 empirical result until exact approved private execution/review is returned. Keep failed tests and unsuccessful controls as separate additions rather than replacing the original design.


## Exploratory implementation safety amendment (before any H-F03 data run)

The earlier H-F03 code-only implementation commit remains part of the immutable Git history. A subsequent **non-scientific** safeguard now refuses to overwrite an existing private report or incomplete `.partial` report. If either exists, the coordinator must preserve and review it before launching another attempt. New approved code SHA/commit is **`5bed769b022e62e4738bf82c1a4e29bab28147aa`** (code change only); this **supersedes the preceding code commit as the requested execution input**. Experimental populations, decomposition, thresholds, references and May–June restrictions have not changed. No source outcome was read and no H-F03 self-test was run by F while making this amendment. The coordinator must still run the invented-fixture self-test and review source integrity before payment-data execution.


## 17 November 2026 MYT — explicit projection and nullable matching review (pre-execution correction)

**Coordinator testing received:** The earlier H-F03 invented-source self-test passed both in the local Python environment and in offline Docker at the intended source-tree mounting depth. The initial Docker fixture setup failed because the script was mounted at insufficient directory depth; it subsequently passed after correcting the mount layout. Preserve this infrastructure failure, but do not attribute it to a scientific finding or mark the **revised** fixture as executed. No H-F03 real-data run has occurred.

**Source-review defect 1, view projection:** The prior full-source view used `SELECT *`, contrary to repository instructions, even though no source rows were displayed. Replaced it with an **explicit ordered 26-column projection** from the source Parquet reader. The existing exact 26-column view-schema assertion remains. The development projection retains the same original 13 analysis columns, exact date/state/eligibility predicates, and all previous metrics.

**Source-review defect 2, nullable group keys:** SQL `GROUP BY` treats NULL keys as part of a grouped stratum; a subsequent `INNER JOIN ... USING(keys)` uses ordinary equality and would not match supported NULL-containing strata to their source rows. This could silently shrink P0/P1/P3 even when a NULL stratum has adequate FX0 and FX1 support. Changed only the support rejoin to conjunctions of `d.key IS NOT DISTINCT FROM s.key` for all predefined grouping keys, and replaced `SELECT d.*` with the explicit thirteen-column development projection. The support table is grouped uniquely by those keys, preventing join-induced row multiplication. No NULL keys are preemptively dropped or imputed: doing so would redefine the planned population.

**Synthetic adversarial regression:** The expanded invented fixture contains a separately supported stratum with NULL values in route, currency, party type, gap count and both endpoint countries. It asserts that `dev`, P0, P1 and P3 each preserve the complete synthetic row count and every NULL-stratum row; also checks exact supported-stratum counts, FX-support conservation, both outcome decompositions, closure and directed-bank overlap. This fixture would fail under the old `USING` joins. The revised fixture has **not** yet been executed by F or independently retested by the coordinator.

**Scientific implication:** Whether real data contains such NULL matching keys is **unknown from this revision**, and no new sponsor data were queried. If none exist, the corrected join should yield the same supported rows as before; if any exist, the old code would have excluded them contrary to the predefined `GROUP BY` support rule. The proposed eligible development population, May–June dates, FX0/FX1 states, thresholds, nested-support definitions, decompositions, overlap audit and private output path are unchanged. Effects remain exploratory, no freeze/validation.

**Code-only correction commit:** `95f38fad635d99c995949861abe2c062a0d23463`. Supersedes earlier H-F03 source commits for execution approval. The coordinator must rerun `--self-test` using the exact final source commit before considering a private H-F03 payment-data run. Preserve any test failures, never publish detailed findings or source fingerprints to GitHub.


## Private coordinator handoff — exploratory execution reported, report not received

The coordinator privately notified Investigator F that the revised invented-source self-test passed and an offline read-only May–June H-F03 exploratory run completed. Its full report remains local and has **not been delivered** to this conversation. No H-F03 numerical outcomes, source fingerprints, report hashes, private job provenance or restricted execution metadata are reproduced in this public hypothesis file.

**Current scientific status:** Executed as reported by coordinator; detailed outcomes not recovered or independently reviewed by F. No frozen validation, July outcome access, interpretation or confirmation. Previous synthetic fixture mount-depth failure is preserved in the earlier addendum. Hold all scientific conclusions pending a complete *private* report handoff. The ordinary Chat hourly automation remains gated on demonstrated scheduled private recovery.

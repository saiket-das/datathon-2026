# H-F02 — Does bank/path selection account for the negative FX–duration contrast?

- **Owner:** Investigator F only.
- **Status:** New exploratory falsification plan; **not executed, not frozen**.
- **Code:** `analysis/40_cross_mechanisms/H-F02_bank_path_confounding.py` (tracked on F branch).
- **Run:** `uv run python analysis/40_cross_mechanisms/H-F02_bank_path_confounding.py --data-dir /absolute/local/parquet-directory`.
- **Result:** `analysis/40_cross_mechanisms/out/H-F02_bank_path_confounding.md`, aggregate-only, to be approved by coordinator before publication.
- **F temporal exposure:** F read reported H-F01 contrast from user on 17 Nov MYT; the original H-F01 aggregate report and local execution metadata were absent from GitHub. H-F02 is not a blind confirmation of H-F01.

## Scientific question

H-F01 reportedly gave a *negative* FX1-minus-FX0 mean `log(1+duration)` contrast of −0.146278 after coarse route/currency/party/gap matching; the corresponding amount contrast was −0.083975. These values are coordinator-reported exploration, not independently recovered by F. Could the negative duration difference result primarily from selection into different bank endpoints and correspondent paths rather than any reduction in duration **caused** by FX steps?

### Competing mechanisms

1. **Bank/path selection:** FX-step states have different endpoint banks, geographic corridors or route realizations with different latent duration baselines. Endpoint-country and bank-pair matching should attenuate the FX contrast if those explain it.
2. **Amount/payment mix:** FX-state groups differ by payment amount or customer segment; adding a pre-specified amount band may attenuate the duration contrast, even after bank-country matching.
3. **Within-route FX-associated processing:** A residual contrast remains among matched directed bank pairs/exact Direct paths; this would *still not identify causal FX processing*, because accounts, times and hidden conditions may differ.
4. **Positivity failure:** Nearly no bank pairs or paths support both FX=0 and FX=1 sufficiently. Tight matching does not identify the contrast, and comparisons of the surviving small subset cannot generalize.

## Development population (no validation read)

May 1–June 30 2023 UTC; `ANOMALY_TYPE IS NULL`; 0 ≤ `USD_AMOUNT`, 0 ≤ `TOTAL_DURATION`; `PARTICIPANT_COUNT` 2–5; `CURRENCY_CONVERSION_COUNT` 0–3. FX contrast uses only FX=0 and FX=1, with exact denominator for each.

The source preflight must verify 10,000,000 rows, 26 columns, unique ROW_ID and, when reading split files, all five manifest SHA-256 values. No July outcomes accessed.

## Exploratory analyses (not frozen gates)

Each of the following analyses computes **FX1−FX0** `log(1+duration)` and `log(1+USD_AMOUNT)` mean differences, weighted by the lesser of group counts. Require **at least 100 payments in each FX state per matched stratum**.

| Label | Exact matching keys | Purpose |
| --- | --- | --- |
| S0 | Route, participant count, currency, B/C party pair, gap count | H-F01 coarse diagnostic replication; no claim of exact numerical identity before executing |
| S1 | S0 + ordering and beneficiary BIC countries | Geographic-corridor selection control |
| S2 | S0 + exact directed ordering and beneficiary BIC8 identities (queried locally, never exported) | Bank endpoint selection control |
| S3 | S1 + fixed `floor(log2(1 + USD_AMOUNT))` amount band (clipped to 31) | Payment-size-mix sensitivity |
| S4 | S0 + exact `BIC8_PATH`, Direct payments only | Exact-ordered-path overlap feasibility; all path strings remain local |

Print only counts: number of eligible FX0/FX1 payments, qualifying strata, matched denominators, matched weight, positive/negative stratum signs and aggregate weighted contrasts. **No individual banks, account strings, or path strings**; no small cells. If no matched stratum qualifies, report `unsupported` rather than a zero effect.

## Interpretation and counterexamples

- Predeclared **negative control / confounding diagnostic:** amount contrast within each matched scheme. It is *not* assumed to be null under every genuine FX processing mechanism.
- Predeclared **adversarial control:** exact Directed path support (S4). No support means the within-path causal mechanism is **not identifiable**, not rejected.
- Coverage is a scientific outcome: report the n0/n1 matched counts and shares of total FX0/FX1; S2/S4 may be highly selected even if S0 is large.
- Compare signed effects across S0–S3, but an attenuation is only *compatible with* an observed-selection mechanism. Changing eligible populations means not all attenuation can be attributed to removing confounding. A future reweighted common-support sensitivity is needed.
- Dependency: shared sending/receiving banks and accounts; any row-level standard error would be invalid. No confidence interval is claimed in this exploratory pilot. Before any held-out confirmation, design cluster-aware or bank-block sensitivity and freeze code, population, controls, thresholds and outcome access guard.
- Failure to reproduce H-F01 coarse aggregates must be logged rather than hidden, because unmatched currency nulls, different source versions, or code mistakes may be responsible.

## Execution register

- **Local run:** pending coordinator-approved executor.
- **Source/checksum verification:** not performed by F.
- **Observed outcome:** none for H-F02.
- **Freeze commit:** none.
- **Validation set:** unopened by H-F02; prior shared aggregate exposures mean not independently blind.
- **Next:** inspect the reviewed H-F01 report, recover local `chat-F.md` operational handoff, obtain approval to execute H-F02 and preserve the resulting evidence and failures.


## 17 November 2026 MYT — approved exploratory queue failure and independent source correction

**Coordinator handoff (received verbatim in F Chat):** Approved queue job `hf02-explore-4615580` attempted H-F02 offline from input branch commit `4615580a6d9c7beb7b5db29b9ce42f185f523a52`. The coordinator reports all five source Parquet partitions verified, read-only execution, S4 disabled and no July outcomes examined. The run **exited 1 before creating the development view**, so **there are no H-F02 exploratory payment aggregates, no supported strata, no duration estimate and no validation result**. Its failure is preserved, not converted into a negative scientific finding.

**Reported failure:** DuckDB 2.0.0 parser rejects the development-view projection `TOTAL_DURATION seconds` on an empty source-typed fixture. Coordinator reports `TOTAL_DURATION AS seconds` binds and runs S0–S3 on that fixture. This is a coordinator-reported fixture result; F has independently inspected the source and confirmed the exact problematic text, but has not locally executed a fixture or the 10M-row dataset.

**F-only correction:** The one-line alias change to `TOTAL_DURATION AS seconds` was committed at `1d1cac7442d1e38d9ad0c4c50671452af880f905`. All other script bytes and hypothesis definitions were preserved. This is an *unfrozen bugfix* to an exploratory script, not a post-freeze retuning. No proof of a successful data run follows from the correction alone.

**Next coordinator approval request:** Sync the corrected F branch commit, rerun only the previously approved exploratory S0–S3 job using the local read-only executor with all five verified Parquet partitions; **do not enable S4**. Execute from the repository root with `uv run python analysis/40_cross_mechanisms/H-F02_bank_path_confounding.py --data-dir <local-data-directory>` (replace placeholder with the existing approved local dataset directory). Target local aggregate report: `analysis/40_cross_mechanisms/out/H-F02_bank_path_confounding.md`. Keep raw rows and identifying bank/path/account data local. Review exact denominators and complementary disclosure/reconstruction risk before any public repository publication; exact totals alone are *not* automatically safe, as H-F01 showed. Recover coordinator's job provenance, actual invocation, source/script hashes, exit status and approved sanitized report before claiming H-F02 execution success. Preserve this failed job and any subsequent failures.

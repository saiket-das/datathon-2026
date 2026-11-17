# H-F01: Does the FX-step–duration relationship survive coarse route and payment-mix matching?

- **Owner:** Investigator F, autonomous cross-mechanism generator discovery.
- **Status:** PROPOSED EXPLORATORY PILOT; unexecuted; **not frozen**.
- **Script:** `analysis/40_cross_mechanisms/H-F01_fx_route_duration.py`.
- **Exact command:** `uv run python analysis/40_cross_mechanisms/H-F01_fx_route_duration.py --data-dir /path/to/local/parquet`.
- **Output (when executed):** `analysis/40_cross_mechanisms/out/H-F01_fx_route_duration.md`, aggregate only.
- **Authorship:** F; no A/B/C/D/E/G claims adopted as F results.

## Scientific question and alternatives

Does an apparent additional FX-stage duration contrast remain after matching on route
type, visible participant count, payment currency, B/C party pair, and gap count?

Plausible explanations include (1) true FX-processing delays; (2) selection of slow
banks, paths or currencies that also tend to involve FX; (3) sender/receiver and amount
mix; (4) undocumented timing or simulation rules. No causal ordering is assumed.

## Exploratory population and exposure

May 1–June 30, 2023 UTC; anomaly label null; positive or zero USD amount and duration;
participant count 2–5; FX count 0–3. The script reads full dataset count, schema and
ROW_ID integrity for preflight but **only May–June development outcomes** for H-F01.
Raw bank/account identities remain local and are not printed.

Phase 0 and A/B/C aggregate evidence have already exposed full-dataset structural
facts, repeated banks/accounts and related FX/routing/duration outcomes. July is at
best a reused-entity internal validation candidate, not independent confirmation.
No designated H-F01 validation outcomes have yet been opened by Investigator F.

## Exploratory statistics (to be executed, no results yet)

1. Count the full data (`n=10,000,000` expected, **not yet directly verified**),
   check 26 columns, source checksums where five split files are used, and distinct ROW_IDs.
2. Count the May/June eligible denominator. Calculate only cells with at least 100
   rows for route × participants × FX category (0, 1, or 2+).
3. Match FX=0 versus FX=1 inside route × participants × currency × B/C pair × gap
   count. Require at least 100 records for each FX state. Report number of strata,
   both FX denominators and min-count weighted mean log(1+duration) contrast.
4. Calculate the analogous log(1+amount) contrast as a **payment-mix diagnostic**,
   not as a placebo with guaranteed null expectation.
5. Show unsupported cells and populations explicitly; do not generalise across them.
   No confidence interval is asserted by this exploratory script because rows share
   banks/accounts, and matched strata are dependent.

## Counterexamples and planned controls

- If the matched duration contrast vanishes, reject any **universal independent
  additive FX-delay** account at this coarseness; do not conclude zero effects in
  every bank/path segment.
- If the amount contrast remains large, payment-mix selection is still compatible
  with the duration contrast.
- Inspect whether support vanishes on exact directed paths and whether particular
  bank-country corridors drive the contrast. Aggregate only; suppress small cells.
- A future H-F01 freeze must specify a statistically honest cluster/sensitivity
  method, exact eligible account/bank support, all thresholds and code hash **before**
  reading any designated validation outcomes.

## Execution / freeze / validation register

- Executed source: **none**.
- Observed denominator: **none**.
- Discoveries: **none**.
- Failed hypotheses: **none tested**.
- Freeze SHA: **none**.
- Validation verdict: **not attempted**.
- Next: run the pilot on the complete local dataset via a verified read-only DuckDB
  executor; review actual aggregates and competing explanations before any freeze.


## 2026-11-17 MYT — coordinator-reported execution, publication pending

**Provenance:** direct report from the user about the coordinator's local Windows run; **not independently recovered by Investigator F**. At the time of this entry, the expected reviewed report `analysis/40_cross_mechanisms/out/H-F01_fx_route_duration.md` returned GitHub 404 and F branch head remained `c31ae3476ca6a8a12b637da40b6328b633f1b6b6`. No local execution record or coordinator's `chat-F.md` handoff has been supplied in this Chat conversation. Do not change the original script or treat these numbers as a validated result.

Reported source: five verified Parquet partitions, 10,000,000 rows, 26 columns and all five SHA-256 checksums passing. Reported May–June eligible population: **6,837,489**. Matched FX=0 versus FX=1 strata: **122**. Matched weighted log(1+duration) difference (FX1−FX0): **−0.146278**; log(1+amount) difference: **−0.083975**. Exact per-FX denominators, support/coverage, runtime version, execution SHA and uncertainty estimates are not recoverable yet; no confidence interval or causal interpretation is justified.

**Scientific status:** exploratory, coordinator-reported only, approved aggregate publication **PENDING**. **Frozen test:** none. **Designated confirmation opened by F:** none. **Next action:** coordinator should approve/publish the original aggregate-only H-F01 report and execution provenance to the existing F branch; F should recover the exact report commit and compare the report's script/version, counts, eligibility and contrasts before marking the report GitHub-verified.


## 17 November 2026 MYT — coordinator publication decision (preserve original result)

The F Chat received the coordinator's complete `chat-F.md` handoff and an operational update. The coordinator reports that **H-F01's original aggregate report is preserved locally but publication approval was withheld**: exact totals could allow reconstruction of a group below its disclosure threshold. Its five dataset fingerprints match the local manifest and the script bytes agree across the earlier and current branch heads. The original invocation, job ID and runtime provenance **could not be independently verified**. These are coordinator-reported checks, not GitHub-recovered execution evidence; the F Chat has not accessed the staged report. Do not reconstruct or fabricate it using the user-reported headline values, do not publish its disclosive totals and do not rerun or modify H-F01 simply to obtain a publishable replacement. **Status remains exploratory, locally reported, unpublished and not validated.**

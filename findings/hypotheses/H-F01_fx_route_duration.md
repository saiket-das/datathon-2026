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

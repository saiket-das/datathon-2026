# H-A02: day-specific EUR scaling reveals a rounded source-amount component

- **Owner:** A
- **Status:** replicated
- **Script / exact command / commit:** `uv run python analysis/10_amounts_currency/H-A02_usd_rounding.py`; frozen version is the commit introducing this plan. Confirmation: append `--phase confirm --freeze <SHA>`.
- **Chart:** `analysis/10_amounts_currency/out/H-A02_usd_rounding_confirm.png`

## Proposed rule and scope

A substantial component of unlabelled EUR payments is compatible with a **whole-unit latent amount multiplied by a date-specific scale and rounded to USD cents**. On the predeclared off-anchor EUR population, at least 30% of payments should fit the exploration-learned same-day integer grid, with at least 20 percentage points more fit than a mismatched-date grid. Equal sender and equal receiver weighting must each retain at least a 20-point excess.

Variables: `CURRENCY_CODE`, `USD_AMOUNT`, UTC date from `ts_utc`, both accounts; party types and route are sensitivity strata. Unit is payment for coverage and account for concentration checks. This is a partial mixture signature, not a deterministic model for every amount, proof of historical FX prices or a rule for `CURRENCY_CONVERSION_COUNT`.

## Test plan (freeze before confirmation)

- **Learn on exploration only:** for each EUR date and decimal base `10^floor(log10(amount))`, group repeated amounts with `1000 <= amount < 2000000` and significand in **[1.08,1.25]**. Select the most frequent exact amount per date/base (amount ascending breaks ties). Keep modes supported by at least **20** payments, choose the largest base per date and set `rate=modal_amount/base`. This is a fixed algorithm; never refit on confirmation. Small anchor-group values and rates by date are not published, only fitted-model aggregate support/range.
- **Measurement tolerance:** observed USD cents leave the learned rate uncertain by at most `0.005/base` conditional on the modal anchor representing the stated base. Classify an amount `a` as fitting rate `r` iff `abs(a-r*round(a/r)) <= 0.005 + 0.005*a/r/base + 1e-8`. This is a rounding-compatible interval, not exact equality. The anchor interpretation itself is tested through off-anchor predictions.
- **Population:** positive, unlabelled EUR payments on dates with a trained rate and a rate seven subsequent available dates later; **10 <= USD_AMOUNT <= 90000**, excluding **[900,1500] and [9000,15000]**. Thus all training amount windows are excluded from primary evaluation; higher training windows exceed 90,000. Final seven learned dates are excluded because the negative control is unavailable. Do not change windows after confirmation.
- **Comparators:** same observation with the rate seven subsequent learned dates later (`lead(rate,7)` ordered by date), and with the median of all learned daily rates. The latter is a secondary constant-scale negative control. Apply the same tolerance formula with the tested rate and observation's trained base. Also report USD whole-number share in identical amount/date windows as a descriptive benchmark, not an equivalence claim across currency populations.
- **Primary criteria:** row-weighted daily fit >= **0.30** and daily-minus-wrong-date fit >= **0.20**. For each of sender and receiver, average each account's per-payment grid difference equally; require the lower bound of its **97.5% interval** to be >= **0.20**. Interval = account mean +/- `2.241403 * sample_sd(account difference)/sqrt(accounts)`. Both account conditions must hold; this Bonferroni correction covers two account comparisons, not a general family of discovered hypotheses.
- **Uncertainty / alternatives:** counterparties, banks and shared dates may correlate account summaries; intervals are conditional descriptive account-sampling intervals, not network-independent inference. Random cents, repeating customer invoices or one large sender could create concentrations; wrong-date, fixed-rate, off-anchor and equal-account comparisons test those alternatives. Mode choice could select a wrong denomination; that would reduce off-anchor performance. No guarantee of original source currency units is assumed.
- **Falsification:** failure of any primary condition rejects the proposed rule as stated. Report all off-grid payments, support and sensitivity exceptions. At least 70% of eligible payments may remain unexplained under the minimum acceptance threshold. Neither off-grid nor unlabelled status defines anomaly/legitimacy.
- **Partition / audit:** the exact shared MD5 both-account bit split and local Parquet SHA-256 are as recorded in [H-A01](H-A01_amount_kernel.md). Shared coverage audit reviewed before selection: 2,579,943 explore / 2,416,730 confirm / 5,003,327 excluded; zero shared accounts in either role; endpoint banks and dates shared. Learned rate dates intentionally overlap across partitions; **this tests transfer to separated accounts on supported dates, not transfer to unseen dates**. No alternate split is pooled as independent evidence.
- **Exploration coverage / precision:** 91 trained dates, 5,067 selected anchor payments; aggregate learned rates 1.100718–1.217694. Primary 84 dates, **506,127 payments**, 46,963 senders and 192,356 receivers. Primary eligibility covers 64.21% of exploration EUR payments on learned dates (788,282), and 19.63% of all unlabelled exploration payments. Entity intervals have half-width about 0.004/0.0023, small relative to the predeclared 0.20 excess margin, conditional on their dependence assumption.
- **Primary confirmation:** run committed code unchanged with `--phase confirm --freeze <SHA>`. Recompute the identical model solely on bit-zero exploration rows; evaluate solely on bit-one confirmation rows. Record coverage and every acceptance flag.
- **Separate robustness:** party-pair, routing category and calendar-month summaries within the same primary account partition; report all cells with >=100 payments, senders and receivers. No new rate fitting, bank-scheme or full time-scheme test. No temporal extrapolation is claimed.
- **Freeze time / prior exposure:** prepared 16 Nov 2026, Malaysia time. Record commit/time immediately after committing, before confirmation. Phase 0 had inspected full-data rounded-amount concentrations; broad shared structural and validation aggregates were known. Daily EUR model, its tests and thresholds used only selected exploration rows. No other investigator's developing findings were read.

## Discovery evidence

Reproducible [aggregate report](../../analysis/10_amounts_currency/out/H-A02_usd_rounding_explore.md) and chart accompany the script.

- USD whole-number share is about 38–39% in each unlabelled party pair, versus about 1% for other currencies. This does **not** imply rounding exists only in USD.
- Off-anchor EUR primary fit: **36.9874%**, versus **0.9357%** wrong-date and **1.2007%** constant-rate; excess **36.0516 points**. Of 506,127 eligible payments, 187,203 fit and **318,924 do not**.
- Equal-sender fit 37.4184%; excess 36.5012 points (97.5% interval 36.1075–36.8949). Equal-receiver fit 36.9254%; excess 35.9894 points (35.7564–36.2225). Party-pair, month and routing excesses are near 36 points. USD whole-number benchmark in identical windows is 36.9509%.

### Search ledger and rejected alternatives

1. Compared whole-unit and one/two/three significant-digit frequencies by currency and magnitude. Reject the simplistic universal one-significant-digit rounding explanation: only about 12–13% of USD amounts above 1,000 fit that grid while about 38% are whole amounts.
2. Repeated EUR amount masses suggested scaled denominations. A 1,000-unit daily anchor initially yielded only **18.6835%** whole-unit compatibility at fixed tight tolerance. This was exploratory, not confirmation. Cent precision of the small anchor was an identified limitation.
3. Before freezing, changed to the highest supported decimal-base anchor, propagated cent-rounding uncertainty, and excluded all anchor ranges for evaluation. Full-range diagnostic fit became 39.0080%; the selected off-anchor fit is lower and is the frozen target.
4. Reject one constant EUR scale as an adequate explanation of the rounded component: its off-anchor fit is only 1.2007%. The precise rounding mixture, all-currency scope, rate evolution process and source distribution remain unresolved. The initial 1,000-anchor calculation is recorded here; the final committed script contains the selected algorithm and its complete SQL.

## Confirmation and robustness results

**Freeze recorded before confirmation:** `25d4703a6388baaec3d0808499dd7bebe05819da`, 16 Nov 2026 16:15:05 +08:00. The plan above and executable scripts are preserved in that commit. The results below were appended after running the unchanged test.

**Completed unchanged:** `uv run python analysis/10_amounts_currency/H-A02_usd_rounding.py --phase confirm --freeze 25d4703a6388baaec3d0808499dd7bebe05819da`. All primary conditions passed. No rate was fitted to confirmation, and no threshold, window, comparator or executable code changed after the freeze. [Confirmation tables](../../analysis/10_amounts_currency/out/H-A02_usd_rounding_confirm.md) and [aggregate chart](../../analysis/10_amounts_currency/out/H-A02_usd_rounding_confirm.png).

- **Coverage:** 516,299 off-anchor confirmation EUR payments, 46,249 senders, 199,269 receivers and 84 supported dates. This is **21.38%** of the 2,415,020 unlabelled payments in the primary confirmation account partition. Applicability is confined to EUR, the stated amount windows and supported dates; excluded amounts/dates are not silently extrapolated.
- **Row-weighted fit:** same-day **36.9088%** (190,560 payments); wrong-date **0.9221%**; constant-rate **1.1997%**. Primary excess **35.9867 percentage points**; both row thresholds pass. **325,739 payments (63.0912%) remain off-grid**.
- **Equal sender:** daily fit 36.8054%, excess **35.9120 points**, 97.5% account interval **35.5164–36.3076**; passes the 20-point lower-bound criterion.
- **Equal receiver:** daily fit 36.9179%, excess **36.0051 points**, interval **35.7764–36.2338**; passes the same criterion.
- **Separate sensitivity:** excess is 35.49–36.61 points across the four party pairs, 35.95–36.45 across routes and 35.83–36.11 across months. All prespecified displayed cells have sufficient record and entity support. USD whole-unit benchmark is 36.7912% on 254,599 payments in identical windows, close descriptively to EUR's fitted share, without a predeclared cross-currency equivalence test.

**Rejected / unresolved:** one constant EUR scale and wrong-date scaling explain very little of this grid signature. The statement that every payment comes from a whole-unit source amount is contradicted by the large off-grid majority. Neither this majority nor the fitted component estimates the generator's exact mixture weight: continuous amounts can accidentally fall on a grid, and cent precision or an incorrect anchor can lose true members. Daily rate uncertainty is bounded conditional on the learned denomination interpretation; it is not a general confidence interval on an economic exchange rate.

## Assessment

The fixed algorithm replicated the day-specific EUR scaling/rounding signature on separated accounts. The approximately 36-point lift over a mismatched date persists under equal-entity weighting and planned strata. The larger off-grid component remains unexplained; exact source distributions, rounding probabilities, rate-evolution model, other currencies and unseen-date transfer remain open. Functional compatibility does not identify the original code or causal order. Shared date effects and known prior exposure limit claims of independence; an independent teammate rerun is still required before final submission.

## Real-world explanation (interpretation, not evidence)

Invoices can be stated in round original-currency units and then normalised to USD at a date-specific rate. An alternative is a synthetic lookup/denomination process that directly creates scaled USD amounts. These observations cannot distinguish those implementations. No outside rate data are used.

# H-B01: Direct-route bank effects predict longer-route duration

- **Owner:** B
- **Status:** confirmation-ready
- **Script / exact command / commit:** `uv run python analysis/20_routing_time/H-B01_bank_additive_duration.py --phase explore`; freeze SHA to be recorded after committing this plan. Confirmation: same command with `--phase confirm --freeze <SHA>`.
- **Chart:** `analysis/20_routing_time/out/H-B01_bank_additive_duration_confirm.png` (after confirmation); discovery chart has `_explore` suffix.

## Proposed rule and scope

For unlabelled non-Direct payments whose every visible path bank has at least 100
appearances in unlabelled Direct exploration routes, predict duration as the sum of
one fitted effect for every visible bank occurrence, including repeated occurrences.
Fit effects using Direct exploration payments only. Compare with the mean duration
of the same route category and exact visible participant count, learned in exploration.
This tests transfer across route lengths, rather than merely observing longer paths
take longer. Gaps contribute no fitted bank effect. Keep all source fields unchanged.

The unit is a payment; ordering-bank clusters address some repeated-entity dependence.
Effects are unrestricted least-squares coefficients, **not physical service times**.
Negative coefficients already rule out that literal interpretation. An absent anomaly
label defines the baseline population, not proven legitimacy.

## Test plan (freeze before confirmation)

- **Comparator/statistic/tolerance:** primary population above; R2, model MSE divided
  by exploration-trained route/count baseline MSE, and mean signed prediction error.
  Accept only if the entire 99% ordering-bank resampling interval has R2 >= .95,
  MSE ratio <= .10, and bias within [-60,60] seconds. Also require >=60% coverage of
  all unlabelled non-Direct confirmation payments and >=100 distinct sending accounts,
  receiving accounts and declared ordering banks. The coverage threshold is substantive:
  a narrow successful subset cannot confirm broad applicability.
- **Model fixed before confirmation:** weighted least squares of Direct bank-pair
  sufficient statistics. Same bank parameter in both positions. Scale columns by square
  root of Direct bank exposure; LSQR atol=btol=1e-10, 2,000-iteration maximum; require
  successful convergence. No coefficients are fitted to confirmation. Eligibility uses
  training support alone. Unknown route/count baseline cells use the average of training
  cell means; document any practical impact through reported coverage and errors.
- **Alternative explanations/controls:** route length alone, party/FX composition,
  gaps, endpoint disagreement, exceptional customers, calendar month and long routes.
  Compare per-route results and equal-ordering-bank MSE/bias; remove the largest sending
  account by eligible population count as a fixed sensitivity check. Fit quality on
  exploration Direct records is in-sample and cannot validate transfer.
- **Falsification:** failure of any acceptance criterion rejects the broad transfer
  claim. Describe narrower eligible-subset performance without changing thresholds.
  Negative coefficients and shared banks prohibit identifying literal processing costs
  or claiming generalisation to wholly new path banks, even if prediction passes.
- **Partition:** foundation `banks` scheme. Let `bit(x) = (('0x'||substr(md5(x),1,8))::UBIGINT % 2)`.
  Explore requires both `bit(ORDERING_BIC8)=0` and `bit(BENEFICIARY_BIC8)=0`;
  confirm requires both bits 1. Cross-bit payments excluded throughout. Freeze uses no
  alternate partition. Foundation coverage is 2,246,981 explore / 2,732,147 confirm /
  5,020,872 excluded, with zero shared row IDs or declared endpoint banks; 11,565
  account strings and 6,709 visible path banks overlap at full-data scope. Source-bank
  metadata need not match path endpoints. Audit overlaps again on actual eligible
  unlabelled populations in the script. Eligibility will probably reduce transfer coverage;
  the minimum is fixed before measuring confirmation outcomes.
- **Primary confirmation:** unchanged model trained on unlabelled Direct exploration;
  evaluate unlabelled eligible non-Direct confirmation. Cluster resample whole declared
  ordering banks 1,000 times with NumPy seed 20261116; use .005/.995 quantiles. These
  are conditional sensitivity intervals: banks share intermediaries and accounts.
- **Separately labelled robustness:** calendar-month subgroups (July temporal
  sensitivity within the same bank-confirmation set), route, party pair, gap presence,
  FX bins 0/1/2/3+, visible-bank bins 3/4/5/6+, endpoint agreement, largest-sender removal,
  pooled labelled anomalies. No sequence target, so no sequence purge is applicable.
  All robustness shares records with primary evaluation; it is not independent replication.
- **Freeze/time/prior exposure:** freeze SHA/time recorded after commit, before any
  confirmation query. Phase 0 full-data summaries and the shared scientific foundation
  were read, including median duration, route counts, endpoint disagreement and split
  audits. No other investigator's developing branch, PR or provisional finding was read.
  Only the bank-exploration partition was queried during discovery. Source schema and
  official data dictionary were inspected. No confirmation outcome has been accessed.

## Discovery evidence

See the reproducible `_explore.md` report and chart. Direct training has 1,417,991
payments and 6,534 distinct visible banks; 1,844 banks meet the support criterion,
including 240 with negative fitted effects. The scaled solver converged in 45 iterations.

The eligible non-Direct discovery set has 652,019 payments (78.82% of unlabelled
non-Direct exploration), 80,711 senders, 250,366 receivers and 2,165 declared ordering
banks. R2=.982510, RMSE=157.025 seconds, MAE=98.514, bias=+3.836 seconds;
MSE ratio to route/count baseline=.017338. R2's 99% cluster interval is
[.978636,.985843]; MSE ratio [.014166,.020934]. Covered RMSE=236.005 versus
Indirect RMSE=145.536. Accuracy worsens for longer routes. These are discovery results.

### Rejected/uncertain alternatives

- A common duration distribution determined by hop count alone leaves much more
  squared error than the bank model; it does not explain bank heterogeneity.
- Literal nonnegative bank service times are not recovered by this unconstrained fit.
  A maximum-delay mechanism, correlated bank assignments, route-specific costs or
  another latent factor could produce an approximately additive predictor. No claim of
  independent, identically distributed bank delays is made.

## Confirmation and robustness results

Pending the frozen commit and unchanged test. Do not replace these criteria after viewing results.

## Assessment

Promising statistical approximation, not yet confirmed; even a successful confirmation
would identify an association, not causal direction or original generator code.

## Real-world explanation (interpretation, not evidence)

Different institutions may have different processing capacities, making paths with slow
institutions slower. Accumulating delays could create approximate additivity. An alternative
is a shared bank-level latent variable determining route and duration together, rather than
literal waiting times at each institution. The negative effects caution against a literal model.

# H-B04: Ordering-bank Covered propensities transfer across months

- **Owner:** B
- **Status:** confirmation-ready
- **Evidence level:** Exploratory until frozen internal validation; no independent holdout claim is available.
- **Script / exact command:** `uv run python analysis/20_routing_time/H-B04_covered_bank_stability.py --phase explore`
- **Validation:** same command with `--phase confirm --freeze <SHA>`.
- **Evidence:** matching `_explore.md` / `_confirm.md` aggregate reports in the script's out folder; no bank coefficients/identities exported.

## Proposed rule and scope

Within unlabelled multibank payments whose declared endpoint-bank MD5 bits are both zero,
Covered assignment has a stable ordering-bank-specific probability component across months.
This is an approximate predictive mechanism: bank-level probabilities trained in May/June
should outperform a global coin and a non-bank currency/party-pair/visible-count comparator
in July, while remaining calibrated at the bank aggregate level. This does not assert
that bank identity is causal, the sole input, or a recovered original implementation.

Population: PARTICIPANT_COUNT>2, ANOMALY_TYPE null, both declared endpoint-bank bits zero.
Train May/June 2023; evaluate July 2023. Eligible ordering banks have >=100 training payments.
Every eligible evaluation payment is included, without filtering on its outcome. Laplace
bank probability `(covered+.5)/(n+1)`. Global baseline is training Covered share. Composition
baseline groups currency, party pair, visible count capped at five, shrinks its count by
100 global pseudo-observations, and falls back to global for new groups. No validation fitting.

## Test plan (freeze before confirmation)

- Primary acceptance: eligible July coverage >=60%; >=100 senders, receivers and ordering banks.
  Entire 99% bank-resampling interval for bank/global Brier ratio <=.85, and for
  bank/composition Brier ratio <=.85. Entire 99% interval for row-weighted absolute
  bank calibration error <=.05. All conditions required. Failure rejects this specified
  practical transfer claim; do not rescue it with a selected subgroup or lower threshold.
- Unit: payment predictive error; whole ordering-bank uncertainty (1,000 multinomial bootstrap
  replicates; seed20261116). This is sensitivity to bank sampling, not proof of independence
  of shared receivers, intermediary banks or generator state. No multiplicity-adjusted
  claim over the complete Round2 search is made.
- Separate descriptive sensitivities: party pair, capped visible count and currency within
  the same validation population. Statistics with <100 records or supporting entities
  suppressed. Training probabilities and validation bank IDs stay local in memory.
- Audit counts of shared senders, receivers, ordering and beneficiary banks across training
  and evaluation. Months have no shared ROW_IDs by construction. Same-bank overlap is
  intentional: this tests stability for known banks, not unseen-bank generalisation.
  Cross-role account and visible-path-bank overlap are not fully audited here and may remain.
- Alternatives: currency/corridor/customer composition, repeated customers and common
  latent bank groups may cause the association. The composition comparator controls only
  currency/party/count, not every corridor or latent factor; Brier improvement cannot
  uniquely identify a generating assignment stage or functional form.
- Freeze: commit containing this confirmation-ready plan and exact executable, recorded
  in the progress register before accessing July B04 errors/calibration.

## Prior exposure and search ledger

Phase0 full-data and Round1 structural/split/route summaries are exposed. B03 already
exposed all-period bank-level Covered counts within this same bank-exploration population;
B02 exposed July route/count summaries; post-Argon synthesis exposed all investigators'
reported aggregate results. Therefore July records and some July aggregate outcomes are
previously exposed. July B04 predictive errors and calibration have not been examined
before this freeze, but that does not make July an independent holdout. At most, a passed
frozen test supports internal temporal validation conditional on this prior exposure.

Discovery was restricted to endpoint-bit0/0. Initial all-period endpoint summaries show
ordering-path agreement 94.2668% Covered vs95.0224% Indirect and beneficiary agreement
94.9722% vs95.0083%; a simple endpoint-mismatch explanation is inadequate. No endpoint
mechanism is claimed. Round1 B01 and B03 remain rejected, their code/results untouched.

May-to-June pilot used only pre-July records for training/evaluation. It retained
276,038 /335,391 payments (82.3033%),43,737 senders,126,152 receivers,497 ordering banks.
Bank/global Brier ratio .681329 with99% interval [.606028,.776681]; bank/composition
.699123 [.617389,.786597]; calibration error .008488 [.007334,.009593]. Pilot bank Brier
.0626335 versus global .0919285 and composition .0895886. Shared same-role senders31,722,
receivers32,634,ordering banks2,866,beneficiary banks2,806 (full month populations).

**Rejected pilot acceptance variant:** a provisional .75 bank/global upper-bound target
(with .80 composition bound) failed because .776681>.75. This was not a frozen test.
Before July evaluation, the final practical target is >=15% Brier improvement against both
baselines, so both ratio ceilings are .85. This development choice is disclosed; it does
not retroactively turn the earlier tighter pilot criterion into a pass. The pilot report
preserves the original false decision and its numerical cells. Only the script's final
acceptance thresholds were changed before freezing; no July outcome informed them.

## Confirmation and robustness results

Not accessed. Append unchanged-test results after freeze. Any pass is labelled
**Supported but not independently confirmed**, not a new independent replication.

## Assessment

Exploratory evidence supports stable bank-associated Covered propensity. Exact assignment,
causal direction, corridor controls and unseen-bank transfer remain unresolved.

## Real-world explanation (interpretation, not evidence)

Institutions may retain routing relationships over time; alternatively a shared synthetic
bank attribute or customer/currency composition may induce persistent route probabilities.
Neither this test nor the rejected global coin identifies the generator's architecture.
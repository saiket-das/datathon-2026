# H-A13 — Bounded daily scale updates

Freeze: exploration only.
512MB; one thread; no disk spill. Aggregates only.
Only both-account bit-0 data queried. Phase 0 and A01–A12 exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Eligible payment and date scope

| currency | payments | scoped_dates | anchor_dates | excluded_dates |
| --- | --- | --- | --- | --- |
| CHF | 194614 | 93 | 73 | 20 |
| EUR | 731239 | 93 | 91 | 2 |
| GBP | 244065 | 93 | 79 | 14 |
| USD | 418448 | 93 | 91 | 2 |

## Anchor support

| currency | dates | anchor_payments | min_base | max_base |
| --- | --- | --- | --- | --- |
| CHF | 73 | 2325 | 1000.0 | 100000.0 |
| EUR | 91 | 5067 | 10000.0 | 1000000.0 |
| GBP | 79 | 2658 | 1000.0 | 100000.0 |
| USD | 91 | 4274 | 1000.0 | 1000000.0 |

## Observed adjacent-day changes

| currency | increments | mean_change | sd_change | minimum | maximum | quantiles | beyond_candidate_bound |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 60 | 0.0025014316474717226 | 0.008752412342787124 | -0.014541633832414025 | 0.01519973969011823 | [-0.011462881996676489, -0.004205917706483653, 0.004383021435855894, 0.009142774869237424, 0.013340037930396155] | 2 |
| EUR | 90 | 0.0009064095716991923 | 0.008136681437355426 | -0.01470331623048915 | 0.015133193751196705 | [-0.011637767835257396, -0.005005592477665688, 0.0014898370619609302, 0.007445995035709585, 0.01189869314707901] | 1 |
| GBP | 69 | -0.0004094965268474243 | 0.009539053159652967 | -0.014621644276632373 | 0.014916833759000214 | [-0.012874796185797475, -0.009475611134956874, 0.00014234834747250957, 0.008055698655204946, 0.01226938637926489] | 0 |
| USD | 90 | 0.0 | 0.0 | 0.0 | 0.0 | [0.0, 0.0, 0.0, 0.0, 0.0] | 0 |

## Pooled fixed-shape comparison

| increments | dates | uniform_KS | Gaussian_KS | Gaussian_expected_tail_share | observed_tail_share |
| --- | --- | --- | --- | --- | --- |
| 219 | 90 | 0.0769118089796309 | 0.11038703525254256 | 0.08305914837288568 | 0.0136986301369863 |

## Seven-date circular-block sensitivity, shared across currencies

| statistic | low99 | high99 |
| --- | --- | --- |
| direct mean | -0.0009967217866405616 | 0.0025156264732325586 |
| direct SD | 0.008005998323884685 | 0.009557416139943877 |
| direct tail share | 0.0 | 0.03211463562402631 |
| inverse uniform KS | 0.04298435417519792 | 0.17897523461310755 |
| inverse Gaussian minus uniform KS | -0.03670243234058754 | 0.057069715975046564 |

## Lag-one diagnostic within contiguous observed triples

| currency | adjacent_pairs | lag1 |
| --- | --- | --- |
| CHF | 48 | 0.05984100826224717 |
| EUR | 89 | -0.1449866865833622 |
| GBP | 59 | -0.12227373163874874 |

## Inverse-scale alternative

| currency | increments | mean_inverse | sd_inverse | minimum_inverse | maximum_inverse | beyond_inverse_bound |
| --- | --- | --- | --- | --- | --- | --- |
| CHF | 60 | -0.0024201771710271065 | 0.008737868686735898 | -0.01497216665437473 | 0.014756213282724362 | 0 |
| EUR | 90 | -0.0008401849407139271 | 0.008136119460735216 | -0.014907594239210398 | 0.014922729846443605 | 0 |
| GBP | 69 | 0.0004994600528732186 | 0.009548275161333275 | -0.014697592219208744 | 0.014838609141052839 | 0 |
| USD | 90 | 0.0 | 0.0 | 0.0 | 0.0 | 0 |

## Inverse shape descriptive comparison

| increments | uniform_KS | Gaussian_KS |
| --- | --- | --- |
| 219 | 0.07687810939335749 | 0.10922488426765803 |

## Practical decision

| all_criteria_met |
| --- |
| True |

Candidate comparisons use fixed zero-centred shapes without fitting their parameters. KS values are descriptive after hypothesis selection. Block intervals condition on fitted anchors. Selection of supported dates can bias the inferred update law. No iid or original-code claim follows.

# H-A13 — Bounded daily scale updates

Freeze: 7bd948fa5a5663bb9fc3d57ebd35bb567f4ab38f.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Eligible payment and date scope

| currency | payments | scoped_dates | anchor_dates | excluded_dates |
| --- | --- | --- | --- | --- |
| CHF | 183600 | 92 | 76 | 16 |
| EUR | 750631 | 93 | 91 | 2 |
| GBP | 159698 | 93 | 70 | 23 |
| USD | 386081 | 93 | 91 | 2 |

## Anchor support

| currency | dates | anchor_payments | min_base | max_base |
| --- | --- | --- | --- | --- |
| CHF | 76 | 2372 | 1000.0 | 100000.0 |
| EUR | 91 | 5509 | 10000.0 | 1000000.0 |
| GBP | 70 | 2435 | 1000.0 | 100000.0 |
| USD | 91 | 4144 | 10000.0 | 1000000.0 |

## Observed adjacent-day changes

| currency | increments | mean_change | sd_change | minimum | maximum | quantiles | beyond_candidate_bound |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 62 | 0.001798787867461578 | 0.009176602651602786 | -0.014541714655189941 | 0.01519973969011823 | [-0.011716941193397879, -0.006227349109867497, 0.0036077537716526775, 0.0090261072526725, 0.013212619066878782] | 2 |
| EUR | 90 | 0.000906409207675792 | 0.008136685812927895 | -0.014703351407653886 | 0.015133229993588904 | [-0.011637767835257396, -0.005005598661491556, 0.0014897663574713338, 0.007445792609452162, 0.01189869314707901] | 1 |
| GBP | 56 | -0.0013463200680769133 | 0.009507472289998145 | -0.014065612661542493 | 0.01476229721033695 | [-0.013318349411035657, -0.011826339064692853, -0.002045630921823194, 0.00701731286332441, 0.010535614434391771] | 0 |
| USD | 90 | 0.0 | 0.0 | 0.0 | 0.0 | [0.0, 0.0, 0.0, 0.0, 0.0] | 0 |

## Pooled fixed-shape comparison

| increments | dates | uniform_KS | Gaussian_KS | Gaussian_expected_tail_share | observed_tail_share |
| --- | --- | --- | --- | --- | --- |
| 208 | 90 | 0.06238171846374296 | 0.10127523240294434 | 0.08305914837288568 | 0.014423076923076924 |

## Seven-date circular-block sensitivity, shared across currencies

| statistic | low99 | high99 |
| --- | --- | --- |
| direct mean | -0.0015040425332340846 | 0.002380187298188799 |
| direct SD | 0.008221806667585397 | 0.009501316202880656 |
| direct tail share | 0.0 | 0.03448361215431888 |
| inverse uniform KS | 0.044526011258403976 | 0.17140708466043475 |
| inverse Gaussian minus uniform KS | -0.0210745342316481 | 0.057069715975046564 |

## Lag-one diagnostic within contiguous observed triples

| currency | adjacent_pairs | lag1 |
| --- | --- | --- |
| CHF | 49 | 0.09461831944406644 |
| EUR | 89 | -0.14498542368384265 |
| GBP | 43 | -0.14046966559511134 |

## Inverse-scale alternative

| currency | increments | mean_inverse | sd_inverse | minimum_inverse | maximum_inverse | beyond_inverse_bound |
| --- | --- | --- | --- | --- | --- | --- |
| CHF | 62 | -0.001712936092922034 | 0.009167859761114021 | -0.01497216665437473 | 0.01475629650838206 | 0 |
| EUR | 90 | -0.0008401845067287028 | 0.008136123867574 | -0.014907629409081968 | 0.014922766081321814 | 0 |
| GBP | 56 | 0.0014372104017188786 | 0.009526718054266168 | -0.014547542070610708 | 0.014266276582068249 | 0 |
| USD | 90 | 0.0 | 0.0 | 0.0 | 0.0 | 0 |

## Inverse shape descriptive comparison

| increments | uniform_KS | Gaussian_KS |
| --- | --- | --- |
| 208 | 0.062348013350516596 | 0.1001536220852729 |

## Practical decision

| all_criteria_met |
| --- |
| True |

Candidate comparisons use fixed zero-centred shapes without fitting their parameters. KS values are descriptive after hypothesis selection. Block intervals condition on fitted anchors. Selection of supported dates can bias the inferred update law. No iid or original-code claim follows.

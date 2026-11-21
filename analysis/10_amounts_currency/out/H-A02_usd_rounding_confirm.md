# H-A02: confirm rounding and EUR scaling

Run: `uv run python analysis/10_amounts_currency/H-A02_usd_rounding.py --phase confirm --freeze 25d4703a6388baaec3d0808499dd7bebe05819da`

DuckDB 2.0.0; 2GB; two threads; no spill.
Both-account confirmation; EUR rates fitted only to exploration. Unlabelled does not imply legitimate.

## Exploration-trained rate support

| dates | anchor_payments | min_rate | max_rate | rate_sd |
| --- | --- | --- | --- | --- |
| 91 | 5067 | 1.10071766 | 1.2176939999999998 | 0.025665912055428272 |

## Primary off-anchor EUR coverage and row-weighted fit

| n | senders | receivers | dates | grid_payments | off_grid_payments | daily_grid | wrong_day_grid | constant_grid | excess_grid | passes_row_threshold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 516299 | 46249 | 199269 | 84 | 190560 | 325739 | 0.36908845455830824 | 0.009221400777456474 | 0.011996924262878681 | 0.3598670537808518 | True |

## Primary equal-account fit and excess

| weighting | accounts | daily_grid | wrong_day_grid | constant_grid | excess | account_SE | 97.5%_low | 97.5%_high | passes_excess |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sender | 46249 | 0.368054336800095 | 0.008933981859861644 | 0.011521754944034861 | 0.3591203549402337 | 0.0017650062346883171 | 0.3551642646707846 | 0.3630764452096828 | True |
| receiver | 199269 | 0.3691794699595091 | 0.009128518684459862 | 0.011982797414309796 | 0.36005095127504944 | 0.0010201515290213148 | 0.3577643805774465 | 0.3623375219726524 | True |

## Sensitivity by pair

| category | n | senders | receivers | daily_grid | wrong_day_grid | excess_grid |
| --- | --- | --- | --- | --- | --- | --- |
| BB | 94276 | 12784 | 41352 | 0.371706478849336 | 0.010426831855403284 | 0.3612796469939327 |
| BC | 301297 | 21264 | 118700 | 0.36725888409111274 | 0.009130525693916633 | 0.35812835839719614 |
| CB | 32034 | 10878 | 16946 | 0.36370731098208153 | 0.00880314665667728 | 0.3549041643254043 |
| CC | 88692 | 18606 | 43231 | 0.3744644387317909 | 0.008399855680331936 | 0.366064583051459 |

## Sensitivity by route

| category | n | senders | receivers | daily_grid | wrong_day_grid | excess_grid |
| --- | --- | --- | --- | --- | --- | --- |
| Covered | 24605 | 6493 | 15479 | 0.37398902662060557 | 0.009469619995935786 | 0.3645194066246698 |
| Direct | 321068 | 35128 | 136257 | 0.36845154297531985 | 0.008960718601666936 | 0.35949082437365293 |
| Indirect | 170626 | 28968 | 83285 | 0.3695802515443133 | 0.00967613376624899 | 0.3599041177780643 |

## Sensitivity by month(obs_date)

| category | n | senders | receivers | daily_grid | wrong_day_grid | excess_grid |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 173340 | 27162 | 84011 | 0.3683223722164532 | 0.010026537440867659 | 0.3582958347755856 |
| 6 | 231575 | 31462 | 105193 | 0.3689733347727518 | 0.008524236208571737 | 0.36044909856418006 |
| 7 | 111384 | 21489 | 58842 | 0.37052000287294407 | 0.009417869711987359 | 0.3611021331609567 |

## USD whole-unit benchmark in identical amount windows

| n | senders | receivers | integer_share |
| --- | --- | --- | --- |
| 254599 | 33276 | 114115 | 0.367911892819689 |

Account intervals assume independence of the account summaries; shared banks, counterparties and dates limit that interpretation. Negative controls use the same observation-specific rounding tolerance as the daily-rate rule.

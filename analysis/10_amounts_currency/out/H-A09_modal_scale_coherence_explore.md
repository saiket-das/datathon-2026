# H-A09: Daily modal-scale coherence

Exploration only, unlabelled both-account bit-0. Phase0/Round1/A03-A08 exposure applies.
A daily amount peak with at least 20 payments is chosen at the highest supported decade.
This generic peak is not an identified exchange rate. Changes over 10% can signal denominator switches.
No date-specific peak, currency-pair identity or transaction is exported.

## Daily peak support and stability

| currency | dates | peak_payments | log_scale_sd | adjacent_days | small_change_share | max_log_jump |
| --- | --- | --- | --- | --- | --- | --- |
| CHF | 73 | 2325 | 0.021384 | 60 | 1.0 | 0.015085 |
| EUR | 91 | 5067 | 0.022152 | 90 | 1.0 | 0.01502 |
| GBP | 79 | 2658 | 0.035312 | 69 | 1.0 | 0.014807 |
| SGD | 62 | 1603 | 0.158222 | 45 | 0.866667 | 0.704024 |
| USD | 91 | 4274 | 0.0 | 90 | 1.0 | 0.0 |

## Same-day currency-change agreement

| currency_pairs | min_days | max_days | median_correlation | minimum_correlation | maximum_correlation |
| --- | --- | --- | --- | --- | --- |
| 3 | 60 | 69 | 0.074893 | 0.069 | 0.083564 |

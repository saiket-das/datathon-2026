# H-A12: Conditional log-amount shape

Phase explore; freeze not frozen. Fit pre-July bit-0, score selected July population.
Locations and scales are training currency/party means and sample SDs.
At least 1,000 training payments per fitted group. Prior Phase 0, Round 1 and A03-A11 exposure applies.

## Training support

| groups | fit_payments | minimum_fit_sd | median_fit_sd | maximum_fit_sd |
| --- | --- | --- | --- | --- |
| 144 | 1726906 | 2.007335 | 2.111776 | 2.341894 |

## Score coverage

| scoped | eligible | senders | receivers |
| --- | --- | --- | --- |
| 749066 | 707232 | 77826 | 264363 |

## Standardised empirical cumulative probabilities

| party_pair | n | senders | receivers | mean_z | sd_z | z_le_minus3 | z_le_minus2 | z_le_minus1 | z_le_plus0 | z_le_plus1 | z_le_plus2 | z_le_plus3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 707232 | 77826 | 264363 | -0.000823 | 0.99913 | 0.001786 | 0.023509 | 0.155404 | 0.496024 | 0.841481 | 0.978327 | 0.998833 |
| BB | 158569 | 24024 | 62028 | -0.005914 | 1.005213 | 0.00198 | 0.024601 | 0.15807 | 0.497809 | 0.842006 | 0.978249 | 0.99877 |
| BC | 404207 | 38043 | 155517 | 0.000878 | 0.99756 | 0.001766 | 0.023104 | 0.154594 | 0.4961 | 0.841517 | 0.978402 | 0.998822 |
| CB | 38883 | 15147 | 19457 | 0.001442 | 0.999614 | 0.00162 | 0.022478 | 0.154515 | 0.493712 | 0.83957 | 0.977651 | 0.998894 |
| CC | 105573 | 29375 | 52181 | -0.000524 | 0.995777 | 0.001629 | 0.023794 | 0.154831 | 0.493905 | 0.841257 | 0.978404 | 0.998949 |

## Eight-bin shape and declared ordering-bank sensitivity

Gaussian / logistic / Laplace TV: 0.005811 / 0.040312 / 0.084731.
Ordering banks: 5435. Shared ordering banks with training: 5318.
Both-role literal account separation applies in validation. Related entities can overlap.
All practical criteria met: True.

| statistic | low99 | high99 |
| --- | --- | --- |
| Gaussian TV | 0.002735 | 0.019130 |
| logistic minus Gaussian TV | 0.022497 | 0.041651 |
| Laplace minus Gaussian TV | 0.066799 | 0.085424 |

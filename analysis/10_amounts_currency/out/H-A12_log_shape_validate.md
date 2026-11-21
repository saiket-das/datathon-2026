# H-A12: Conditional log-amount shape

Phase validate; freeze 36627f0. Fit pre-July bit-0, score selected July population.
Locations and scales are training currency/party means and sample SDs.
At least 1,000 training payments per fitted group. Prior Phase 0, Round 1 and A03-A11 exposure applies.

## Training support

| groups | fit_payments | minimum_fit_sd | median_fit_sd | maximum_fit_sd |
| --- | --- | --- | --- | --- |
| 144 | 1726906 | 2.007335 | 2.111776 | 2.341894 |

## Score coverage

| scoped | eligible | senders | receivers |
| --- | --- | --- | --- |
| 699603 | 658785 | 76234 | 256850 |

## Standardised empirical cumulative probabilities

| party_pair | n | senders | receivers | mean_z | sd_z | z_le_minus3 | z_le_minus2 | z_le_minus1 | z_le_plus0 | z_le_plus1 | z_le_plus2 | z_le_plus3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 658785 | 76234 | 256850 | 0.001937 | 0.993723 | 0.001608 | 0.022807 | 0.153777 | 0.494272 | 0.84273 | 0.978611 | 0.998869 |
| BB | 148002 | 23487 | 61324 | 0.001094 | 0.991962 | 0.001466 | 0.022986 | 0.154025 | 0.495905 | 0.845279 | 0.978784 | 0.998872 |
| BC | 383552 | 37602 | 152661 | 0.003914 | 0.991008 | 0.001603 | 0.02212 | 0.152587 | 0.49422 | 0.842496 | 0.978819 | 0.998889 |
| CB | 33142 | 14488 | 18020 | 0.002184 | 1.00288 | 0.00175 | 0.023776 | 0.153461 | 0.492517 | 0.83966 | 0.978245 | 0.998853 |
| CC | 94089 | 28635 | 48426 | -0.00488 | 1.004231 | 0.001796 | 0.024987 | 0.15835 | 0.492534 | 0.840757 | 0.977617 | 0.998788 |

## Eight-bin shape and declared ordering-bank sensitivity

Gaussian / logistic / Laplace TV: 0.007371 / 0.038275 / 0.082839.
Ordering banks: 5356. Shared ordering banks with training: 4156.
Both-role literal account separation applies in validation. Related entities can overlap.
All practical criteria met: True.

| statistic | low99 | high99 |
| --- | --- | --- |
| Gaussian TV | 0.005259 | 0.017461 |
| logistic minus Gaussian TV | 0.020742 | 0.034959 |
| Laplace minus Gaussian TV | 0.065301 | 0.079113 |

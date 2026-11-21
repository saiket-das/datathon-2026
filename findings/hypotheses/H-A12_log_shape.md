# H-A12: Approximate Gaussian shape for conditional log payment amounts

- **Owner:** A
- **Status at freeze:** confirmation-ready for reused-population internal transfer.
- **Command:** `uv run python analysis/10_amounts_currency/H-A12_log_shape.py`
- **Internal validation:** add `--phase validate --freeze SHA`.

## Proposed relationship

After standardizing log USD amount with a mean and sample standard deviation
learned per currency and ordering/beneficiary party-type pair, the pooled
positive, unlabelled July distribution should closely resemble a Gaussian
shape in eight predeclared bins. Unit-variance logistic and Laplace shapes
are practical alternatives with different shoulders and tails. The test
addresses predictive log-shape behavior and leaves the generator law open.

## Frozen test plan

- Train on both-account bit-0 unlabelled positive USD amounts before July.
  Use currency and the observed ordering/beneficiary party types. Require
  at least 1,000 training payments and positive sample SD per group.
  Fit the mean and SD of natural log USD amount without clipping or rounding.
- Internal validation is July only, both-account bit-1, positive amounts,
  no supplied anomaly label. Score only groups with a trained fit. Retain
  unsupported groups in coverage. Both-role literal account strings are
  disjoint by parity. Report shared declared ordering banks and acknowledge
  other dependencies. Report same-row strata by party pair descriptively.
- Use cutpoints -3, -2, -1, 0, 1, 2, 3 in frozen standardized units, with
  right-inclusive bins and both outer tails. Compare pooled relative bin
  frequencies by total variation (one half the sum of absolute differences)
  to analytic probabilities for standard Gaussian, centered logistic with
  scale sqrt(3)/pi and centered Laplace with scale 1/sqrt(2).
- Fit no score-side parameters. Resample declared ordering-bank clusters
  1,000 times with replacement, using NumPy seed 20261116 and .005/.995
  percentiles. These intervals condition on the fitted locations/scales and
  do not account for correlated bank/country or training estimates.
- Acceptance requires at least 90% scoring coverage, 100 eligible distinct
  senders, receivers and declared ordering banks each, upper 99% Gaussian
  TV at most .02, and lower 99% paired TV difference (alternative minus
  Gaussian) at least .02 for logistic and .05 for Laplace. Failure of any
  criterion rejects the full practical claim.
- Commit the executable and this plan before bit-1 scoring. The command
  verifies freeze ancestry and executable/helper equality. Frozen values
  remain unchanged after outcome exposure. No exact lognormal or mixture
  weight claim follows from a coarse pooled distribution.

## Development evidence and alternatives

Pre-July bit-0 training fitted 144 groups on 1,726,906 payments. Fitted group
SDs range 2.0073 to 2.3419. July bit-0 scores 707,232 of 749,066 payments and
covers 77,826 senders and 264,363 receivers. Standardized mean is -.000823,
and sample SD .99913. Gaussian, logistic and Laplace TVs are approximately
.005811, .040312 and .084731. The bank-cluster upper99 Gaussian TV is
.019130, and lower99 gains over logistic and Laplace are .022497 and
.066799. There are 5,435 scoring banks, 5,318 shared with training. The outer tails retain small asymmetry.
Currency/party mixtures, quantization, latent geography and bank/party
selection can create a similar pooled shape. Separate subgroup laws and
extreme-tail behavior remain open.

## Exposure

Phase 0 reported full-data amounts and party distributions. Round 1 A01
reported log-amount summaries and tested conditional mean shifts on the same
account-confirmation records. A02 and A10 exposed rounding/scale outcomes
from some of those currency/amount subsets. A03/A05/A11 exposed FX counts,
and A06/A08 exposed currency associations in July bit-1. Prior reports and
code do not expose this eight-bin standardized test, but the data and some
moments are reused. This test can support internal association, with no
independent-holdout label.

## Validation and robustness results

Pending at freeze.

## Assessment

A pass would support a pooled, conditional Gaussian approximation under
eight-bin resolution. Amount rounding and original amount generation order
remain unresolved.

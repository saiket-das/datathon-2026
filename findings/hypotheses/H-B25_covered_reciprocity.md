# H-B25 Reciprocal Covered labels after accounting for origin propensities

- **Status:** exploratory, uncertain after both bank-role sensitivity checks
- **Command:** `uv run python analysis/20_routing_time/H-B25_covered_reciprocity.py`

## Candidate mechanism

A common unordered-pair attribute could increase the probability of
Covered in both directions. Compare the observed both-Covered rate with
the product of two estimated direction probabilities. Conditional
independence is the comparator. Unmeasured endpoint or country effects,
repeat-corridor selection and imperfect origin calibration can also
make both labels co-occur.

## Development and evidence

Reuse B20's May and June unlabelled v3–5 paths with declared bank parity
0/0. Require a pure state and at least two June payments in both ordered
visible endpoint directions. Fit each origin's equal-pair rate from
pure May paths, with ten global pseudo-corridors. Remove the actual
scored ordered corridor from its origin's May totals if present. Require
at least 25 remaining directed training corridors per origin role.
Score canonical unordered pairs equally.

The raw asymmetric product is compared with a product after multiplying
both direction odds by a common factor fitted to June's pooled label rate.
This corrects one overall level, while potentially leaving role and bank
calibration differences. It uses the outcome and is descriptive. Also
compare the square of the overall June direction rate and examine the
product of residuals centered on fitted direction probabilities.

June has 5,502 eligible pairs and 88,634 payments. The direction Covered
rate is 7.02%, both-Covered is .800%, and the independent rates are .438%
with the pooled odds calibration, .236% without it, and .493% under the
equal-rate comparator. The 99% conditional bootstrap interval for the
observed minus calibrated rate is .090 to .724 percentage points with
316 canonical first banks, and −.116 to .946 points with 271 canonical
second banks. The centered residual product similarly has an interval
covering zero under second-bank resampling. These separate 1,000 resamples
use seed 20261116. Related opposite endpoints, repeated counterparties and
fixed fitted parameters limit their uncertainty interpretation.

## Assessment and exposure

The data suggest that a common-pair effect is worth testing under a
stronger balancing design. They leave excess reciprocity uncertain after
second-bank sensitivity. No frozen criterion or designated July outcome
follows from these exploratory results. Phase 0 and B01–B24 covered related
populations, including support-conditioned direction labels and origin
propensities. The cap and source history are given in the
[aggregate report](../../analysis/20_routing_time/out/H-B25_covered_reciprocity_explore.md).

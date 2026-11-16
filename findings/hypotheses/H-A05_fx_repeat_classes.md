# H-A05: A tighter upper bound for FX conversion counts

- **Owner:** A
- **Status at freeze:** confirmation-ready for a reused-population internal test.
- **Script:** `uv run python analysis/10_amounts_currency/H-A05_fx_repeat_classes.py`
- **Report:** `analysis/10_amounts_currency/out/H-A05_fx_repeat_classes_explore.md`

## Proposed rule and scope

For unlabelled payments with more than two visible banks, when all visible
countries are supported by the H-A03 bit-0 training graph, the reported FX
count never exceeds the number of adjacent changes between learned country
classes. The bound should be at least one count tighter than the visible
country-change count for at least 10% of eligible payments.

Classes are inferred from two-visible-bank bit-0 payments with at least 100
observations per country pair and agreement on zero conversion, exactly as in
H-A03. The change count can stay equal to or exceed the observed FX count.
This is a proposed bound on counted conversions. It does not reconstruct the
number of conversions exactly or prove that the classes are legal currencies.

## Test plan (freeze before validation)

- **Fit/output:** reuse the H-A03 fit and scoring code unchanged. Only
  `partition_sql('accounts')='explore'` rows train the graph. Primary score
  rows use `partition_sql('accounts')='confirm'` with both literal account
  MD5 parity bits 1. No cross-bit, labelled, or two-visible-bank score rows.
  All visible countries must have a mapping. Unsupported score rows enter
  the population denominator but cannot test the bound.
- **Comparator and controls:** count changes in literal BIC country rather
  than learned class. The latter is mechanically no greater than the former
  because one country maps to one class. Its success as an upper bound is
  empirical. Count violations of a seven-position shifted mapping with the
  same group sizes. This is a descriptive misspecification control. Also
  report the effect of removing repeat classes and the one-step decrement
  on prior residuals. These exploratory alternatives do not determine the
  primary decision.
- **Acceptance:** exactly zero eligible payments with FX above the class
  bound, at least 90% coverage, at least 10% of eligible payments strictly
  tighter than the country baseline, and at least 100 distinct senders,
  receivers and declared ordering banks in the tighter subset. Fail if any
  criterion fails. These are empirical population checks; a pass provides
  no statistical guarantee of zero violations on unseen payments.
- **Strata:** report eligible route, gap presence and class reentry summaries
  alongside pooled support. Display only groups with 1,000 payments and
  at least 100 senders and receivers. Mask positive event counts below 100.
  Report a failed aggregate threshold without relaxing any criterion.
- **Freeze:** commit this plan with the complete executable before reading
  bit-1 directional outcomes. Pass the SHA through `--phase validate --freeze SHA`.
  The script verifies the commit is an ancestor and compares the executable,
  H-A03 source, shared helper and the plan through the exposure section.
  Results can be appended after the frozen plan.

## Discovery evidence and alternatives

The pooled gap difference in A04 disappeared in the displayed same-length
Indirect comparisons. Covered gapped cells lacked event support. No broad
gap explanation follows. On 934,229 eligible bit-0 multibank payments,
the class bound had zero breaches, with 168,566 (18.04%) strictly tighter
than country changes and 3,594 counts strictly below the learned bound. The tighter
subset included 36,428 senders, 79,326 receivers and 4,316 declared ordering banks.
The shifted-class control was exceeded on 9,655 eligible payments.

Class reentry can create transitions without adding a new class. The
alternative of counting distinct classes minus one repairs 459 errors but
breaks 205,706 exact baseline predictions. Of 3,594 errors, 2,792 occur on
paths without class reentry, which that correction cannot repair. A constant
one-step decrement repairs 3,297 errors by construction of the candidate
comparator but cannot explain which exact matching paths should be decremented.
Both alternatives remain exploratory.

Missed joins from sparse two-bank support could make H-A03 class boundaries
too fine and its conversion counts too large. Wrong connected-component
merges could create violations in the other direction. A count suppression
or recording convention could also explain actual counts below the bound.
Shared bank, route mix and path gaps leave more than one possibility.

## Prior exposure and validation limits

Phase 0 already reported the visible country-change bound. Round 1 A01/A02
exposed both-account confirmation records and amount/rounding aggregates.
H-A03 then scored the same payments with the same prediction. Its bit-1
report exposed 876,388 eligible payments, 872,830 exact matches and route/month
agreement. It exposed the 3,558 total errors, mean absolute error 0.00436336,
maximum absolute error 3, and visible bank overlap of 6,530 of 7,110 banks.
Those values constrain the available error signs: any directional counts must
add to 3,558 and fit the known absolute-error magnitudes. They cannot identify
how many actual counts exceeded the fitted class bound. The stored H-A03
script and report contain exact, lifted and absolute error metrics, with no
signed tally. H-A04 and the H-A05 screening runs queried bit-0 signs only.
There is no claim of a fresh or independent holdout.

The H-A03 near-exact claim remains rejected. The H-A05 bound is a different
and strictly weaker claim about the prediction on the reused records.
Bank and country overlap can matter even with disjoint literal accounts.

## Validation and robustness results

Pending at freeze.

## Assessment

A passing test can support an empirical tighter bound on the reused
population. The original count algorithm and the cause of residuals remain
open.

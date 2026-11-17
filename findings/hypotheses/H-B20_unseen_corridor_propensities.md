# H-B20 Origin-bank propensities on previously unseen corridors

- **Status:** confirmation-ready
- **Command:** `uv run python analysis/20_routing_time/H-B20_unseen_corridor_propensities.py --phase explore`
- **Internal test:** replace the phase with `--phase confirm --freeze SHA`.

## Mechanism and alternative explanations

Known origin banks can retain a Covered propensity across their novel
counterparties. If this propensity is materially more informative than
receiver propensity or the directed country-pair rate, origin-specific
context is a better explanation than country-level composition alone.
Because B12 found stable directed labels, the target is an ordered
visible-endpoint corridor, with each unique corridor weighted once.
This is a probability approximation to a route state. An unobserved
source-specific choice of counterparties or corridor attributes could
produce it without an origin-specific random draw.

## Frozen design

- Source: unlabelled Covered or Indirect v3–5 payments with both declared
  endpoint-bank MD5 parity bits zero. Remove visible placeholders. Fit
  May 2023. Explore June, then evaluate July 2023 internal validation.
  Time intervals are half-open UTC calendar months.
- Sum labels per ordered first/last visible bank pair each month. Train
  on pure May pairs, including single observations. Score only pure
  repeated pairs (two or more observations) for which neither orientation
  appears in May. Require the origin to appear as origin and the receiver
  as receiver on at least 25 May pure corridors each.
- Predict the May proportion with equal corridor weights. Smooth all
  bank and country rates with ten global-rate pseudo-corridors. For a
  previously absent country pair, assign the global rate. Compare the
  origin-only Brier score with global, receiver-only and directed
  country-pair scores on identical rows. Descriptively combine the
  endpoint probabilities by multiplying their odds and dividing by
  global odds. Also report payment-weighted scores and calibration.
- Require at least 2,000 eligible corridors and 100 distinct banks per
  endpoint role, absolute origin calibration bias no greater than 2
  percentage points, and lower 99% relative Brier improvement at least
  3% versus each of global, receiver and country comparisons under
  *both* independent-by-role bank resampling sensitivity checks. These
  are paired 1,000-draw percentile intervals with seed 20261116. A
  favorable combined comparison or a subgroup cannot rescue a failed
  criterion. Cross-role bank overlap, repeated entities and shared
  countries limit interpretation of these sensitivity intervals.
- The combined model is a control for whether naive endpoint odds
  composition gains over the origin transfer by itself. It does not
  exhaust receiver-bank interactions or corridor classifiers.

## Exploration and exposure

May has 84,121 pure corridors and 239,427 payments. June has 100,498
corridors and 318,693 payments. Of 8,283 novel repeated June corridors
(19,957 payments), 2,796 lack endpoint role support. The remaining
5,487 corridors (13,459 payments) span 437 origins and 759 receivers.
Observed Covered share is 2.9707% versus 3.8606% predicted by origin.
Equal-corridor Brier is .025279 origin, .029172 global, .029314 receiver,
.029254 geography, and .025765 combined. The smallest 99% lower gains
over the three primary comparisons are .038272 under origin resampling
and .070316 under receiver resampling. The combined lift over origin has
intervals that cover zero in both checks.

Phase 0 and B01–B19 records and results were previously exposed. B04 used
payment-weighted bank propensities on reused July banks, B05 assessed
endpoint agreement, B12 tested known ordered corridors and B19 linked
known labels to Direct duration. None evaluated this May-unseen July
contrast or these fitted risks before the freeze. July reuses the bank
partition, records, currencies, banks, accounts and possible corridor
structure seen by other experiments. The novelty rule excludes both
literal orientations from this May training only. This is internal
validation and leaves new-bank transport and generator stage order open.

## Frozen internal result

The unchanged July test passed at freeze
`af07496a8a81d970bbb30531c1a4f484ec03fa55` (17 November 2026,
10:44:59 MYT). July had 81,372 directed corridors and 227,489
payments. Of 30,112 repeated pure corridors, 5,008 were absent in
both orientations from May (11,581 payments). After excluding 1,624
unsupported endpoint roles, 3,384 corridors and 7,907 payments remain.
These cover 408 origin banks and 732 receiver banks. The scorable
cohort represents 67.57% of novel repeated corridors and 3.48% of all
scoped July payments.

Origin-only Brier was .025336 versus .029565 global, .029831 receiver,
and .029426 directed country pair. Pooled Covered share was 3.0142%
versus 4.0149% estimated by origin. The origin-bank lower 99% gains
over the three controls were 6.005%, 6.373%, and 6.959%. The respective
receiver-bank bounds were 5.815%, 6.227%, and 5.377%. Combining
endpoint odds gave Brier .026256 and had a relative gain interval
over origin only spanning zero under either bank resample.

This supports persistent origin-associated variation in the population
of supported May-unseen corridors. It leaves the individual state
assignment, receiver interactions and new-bank transport unresolved.
These specific July outcomes are now exposed.
[Aggregate report](../../analysis/20_routing_time/out/H-B20_unseen_corridor_propensities_confirm.md).

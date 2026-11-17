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

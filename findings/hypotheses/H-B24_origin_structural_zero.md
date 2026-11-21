# H-B24 A binary origin gate for Covered states

- **Status:** exploratory rejection of a strict May-witness gate
- **Command:** `uv run python analysis/20_routing_time/H-B24_origin_structural_zero.py`

## Candidate mechanism

An origin bank either generates no Covered corridors or draws from a
common Covered rate. This coarse mechanism could explain the origin
signal in B20 if positive propensities do not vary appreciably among
origins. It predicts no Covered state for origins without May witnesses.
Compare this with graded B20 rates, which permit low positive probability.

## Discovery and falsification

Use exactly B20's May fit and June exploration population of May-novel
ordered visible corridors. Group supported origins by whether any May
directed corridor was Covered. Fit the two rates from the corresponding
May pure-corridor totals. Score all 5,487 June eligible directed corridors
with 437 origins and 759 receivers, equally weighting corridors.

Among 706 eligible corridors with no May Covered witness at their origin
(131 origins and 353 receivers), 1.13% are Covered in June. This contradicts
the strict observed-zero gate. These are counterexamples across a broad
group; positive event counts below 100 are suppressed in the report.
The data do not resolve whether a latent group really has zero probability,
since finite May samples can miss rare positive rates.

In the 4,781 corridors whose origin has a May Covered witness (306 origins),
graded Brier is .027361 versus .031778 for the two-rate model. Over the whole
population, graded Brier is .025279 versus .029147 for the two-rate model
and .029172 global. The graded relative gain's conditional 99% sensitivity
interval is 3.97% to 22.74% under origin resampling and 6.90% to 18.89%
under receiver resampling. These comparisons arise from the June
exploration data, with no separate confirmatory claim. The two-rate model
may also lose because the May groups have differing corridor coverage and
selection, rather than because grades are a generator input.

## Exposure

Phase 0 and B01–B23 expose all related structure, including the July B20
test on the same general population and this exact May/June exploration
cohort. This script opens only May and June. Repeated endpoint banks,
countries and payment entities remain possible dependencies. The observed
zero gate is too strong to pursue as a frozen candidate.
[Aggregate report](../../analysis/20_routing_time/out/H-B24_origin_structural_zero_explore.md).

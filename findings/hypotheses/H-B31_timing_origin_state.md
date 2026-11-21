# H-B31 Origin timing groups and Covered propensity

- **Status:** unsupported coarse timing explanation in exploration
- **Command:** `uv run python analysis/20_routing_time/H-B31_timing_origin_state.py`.

## Candidate and design

The bank-associated duration exclusion in B09 might mark the same origin
groups that explain Covered propensities in B20. Fit a May Direct timing
summary from paths starting at each visible bank with at least100 payments.
The features are the absence of sub-100-second observations and the
10th percentile of total duration. These are observed path summaries
conditioned on a source bank and can depend on receiver selection.

Estimate May Covered rates on pure directed visible v3–5 corridors
within the two observed timing classes, or duration percentile bands
below100,100–599 and600+seconds. For each target origin, exclude all its
own May corridor labels from the group estimator, requiring at least25
remaining training corridors. Smooth with ten pseudo-corridors at the
May global rate. Evaluate B20's June pure repeated corridors, with both
orientations absent from May and at least25 May corridors in each
endpoint role. All records are unlabelled and declared endpoint bits0/0.

## Results and assessment

The eligible intersection retains5,223/5,487 original June corridors,
12,857 payments,352 origins and758 receivers. Binary timing Brier is
.029345 and duration-band Brier .029348 versus .029318 global.
Own-origin rates give .025308. On370 May origins with at least25
training corridors, the correlation of log(1+p10 duration) and Covered
rate is−.116395, and absence-of-fast-witness correlation is−.135077.
The pooled description does not provide independent-bank uncertainty.
Small timing classes are used internally and no class identities or
small-group statistics are exported.

The particular timing-group predictors give no improvement over the
global rate. Graded bank attributes, within-group variation, partner
composition and interactions remain possible. This neither rejects all
joint timing/routing mechanisms nor turns the observed timing summaries
into intrinsic bank service parameters.

## Exposure and next question

Phase0 and B01–B30 outcomes were exposed, including the new B30 July
country contrast and the recovered B28 result. The script reads only
May and June. This is an exploratory screen without frozen validation
or a July outcome. The next question is whether country-matched partner
selection or a richer bank-level attribute can explain the residual
origin variation. [Safe report](../../analysis/20_routing_time/out/H-B31_timing_origin_state_explore.md).

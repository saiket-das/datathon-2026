# H-B06: Does timing differ on weekends within comparable payments?

- **Owner:** B
- **Status:** supported but not independently confirmed
- **Script:** `uv run python analysis/20_routing_time/H-B06_calendar_timing.py`
- **Evidence:** [initial aggregate report](../../analysis/20_routing_time/out/H-B06_calendar_timing_explore.md) and [exploratory challenge report](../../analysis/20_routing_time/out/H-B06_calendar_timing_sensitivity.md)

## Proposed rule and scope

On the May–June unlabelled endpoint-bit-0/0 population, weekend payments have a lower share in 06:00–17:59 UTC. Check whether that shift persists within ordering bank, route, party-type pair and month. The contrast compares shares among observed payments. It does not estimate an individual account's schedule or use a local time-zone lookup.

## Discovery evidence

Among 1,593,042 payments across 61 dates and 3,838 ordering banks, weekend daily volume averaged 9,807.06 compared with 31,913.98 on weekdays. Pooled UTC daytime share was 54.2453% on weekends and 62.0435% on weekdays.

Within 1,107 bank/route/party/month strata with at least 30 payments of each calendar type, the share difference was −6.9699 percentage points using each stratum's smaller count as weight, and −6.4776 points giving each stratum equal weight. The matching restriction retains 76,245 weekend and 680,435 weekday payments from 270 banks, about 49% and 47% of the respective calendar samples. About 76% of supported strata show a negative contrast. The supported Direct and Indirect summaries both fall around −7 points. Covered lacks 100 supported banks for the separate matched report.

An exploratory alignment screen finds minute and hour boundary shares close to uniform-second references. It offers no obvious large excess at those boundaries and does not establish that sub-minute timing is uniform. Calendar dates define the denominators. No holiday or workweek external data were used.

The May–June follow-up preserved the primary strata and statistic. Estimates were −7.2779 points in May and −6.7832 in June. Saturday and Sunday comparisons also went in the same direction, with independently recalculated 15-payments-per-arm support of 230 and 340 banks respectively. Their contrasts were −9.7148 and −5.9016 points, so treating the two days as interchangeable is not warranted. A Monday–Tuesday versus Wednesday–Friday placebo gave +0.0590 points on 658 banks. Raising the primary support cutoff to 50 gave −7.2551 points on 173 banks with lower coverage. Lowering it to 10 gave −6.5803 points on 658 banks. Among payments between declared bank countries the estimate was −7.0442 points on 254 banks. Same-country traffic and exact refinements by beneficiary country, country/currency, beneficiary bank and ordering account each lacked 100 supported banks. The primary result consequently leaves customer and geographic composition within ordering banks unresolved.

Recomputing support across nine leave-one-calendar-week-out samples gave contrasts between −7.5100 and −6.7388 points on 212–270 ordering banks. Each omission retained at least 42% of each remaining arm. This checks whether a single observed week dominates, without establishing sampling uncertainty across weeks.

## Test plan and exposure

Phase 0 conditional and full-data aggregates and the Round 1 B01–B03 outcomes are already exposed. Round 2 B04 and B05 use May–June and July within endpoint-bit-0/0, and the B05 ledger already notes a UTC hour/day pilot. This screen uses only May–June endpoint-bit-0/0. The exact July matched timing contrast remains unqueried in B06, but July records are reused and cannot be independent.

The frozen internal test uses July 2023 UTC, unlabelled rows and the same endpoint bit-0/0 predicate as May–June. July covers the half-open interval from July 1 to August 1. The exact July B06 outcome remains uninspected before freeze. Weekend is Saturday/Sunday UTC irrespective of local weekends. Preserve the original bank/route/party/month strata with 30 payments per arm and smaller-arm weighting. All four criteria must pass:

1. Retain at least 100 declared ordering banks and 30% of each calendar arm.
2. Weekend minus weekday UTC daytime share is at most −3 percentage points.
3. Recompute support and the same contrast after omitting each Monday-start UTC calendar block, including partial blocks at the boundaries. Require at least four omissions. Every omission must retain at least 100 banks and 20% of each remaining arm, and show a contrast of at most −1 percentage point.
4. Recompute with the weekday-only contrast of Monday–Tuesday versus Wednesday–Friday. Require at least 100 banks and an absolute difference strictly below 3 percentage points. This is a specificity challenge to a broad within-week composition explanation, not an exchangeable null.

The tolerances are practical discovery-informed requirements. The 3-point gate is materially smaller than the original 6.97-point contrast and its observed subgroup counterparts. The 1-point gate tests whether one week determines direction and practical size. Omission replicates share most dates and are a sensitivity range rather than a confidence interval. Same banks, customers and calendar dependence can recur. No row-level inference or independent temporal holdout claim is made. Covered stays descriptive and remains suppressed if too sparse.

Run `uv run python analysis/20_routing_time/H-B06_calendar_timing.py --phase confirm --freeze SHA` only after committing this confirmation-ready plan and exact executable. Save all outcomes as internal validation conditional on the recorded exposure. No threshold changes after inspecting July.

## Frozen internal validation result

Freeze `9e737f1d1e1e028b634b318624360902e3b99715`. All four criteria passed unchanged. The [aggregate report](../../analysis/20_routing_time/out/H-B06_calendar_timing_confirm.md) contains denominators and every week-omission result.

- The eligible July population contains 650,668 payments over 31 dates and 3,504 ordering banks. Matching retains 47,954 of 92,009 weekend payments (52.12%) and 285,728 of 558,659 weekday payments (51.15%) across 669 strata and 275 banks.
- Weekend minus weekday UTC daytime share is −5.3911 points with smaller-arm weights and −5.1850 points with equal stratum weights. The contrast is negative in 71.60% of supported strata. Direct and Indirect contrasts are −5.0749 and −5.8214 points. Covered does not meet the separate 100-bank reporting threshold.
- Omitting each of six UTC week blocks gives a range of −6.2506 to −4.8242 points. All omissions retain at least 213 ordering banks and at least 44% of each remaining calendar arm.
- The weekday-only placebo on 530 banks is −0.2520 points. This meets the specificity threshold without excluding confounding within weekend/weekday strata.

The exact B06 outcome was viewed only after freeze. B04 and B05 had already analysed July records, including repeated ordering banks and accounts, so this is internal validation on reused records. The sensitivity range does not measure independent sampling uncertainty.

## Assessment

The matched pattern makes a purely pooled ordering-bank/route/party/month composition explanation inadequate on the supported strata. Remaining explanations include within-bank account/corridor mix, geography, and differences among specific days. UTC aggregates cannot identify a local business-hours generator, scheduling order or exact weekday weights.

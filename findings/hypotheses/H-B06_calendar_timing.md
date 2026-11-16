# H-B06: Does timing differ on weekends within comparable payments?

- **Owner:** B
- **Status:** exploratory
- **Script:** `uv run python analysis/20_routing_time/H-B06_calendar_timing.py`
- **Evidence:** [aggregate report](../../analysis/20_routing_time/out/H-B06_calendar_timing_explore.md)

## Proposed rule and scope

On the May–June unlabelled endpoint-bit-0/0 population, weekend payments have a lower share in 06:00–17:59 UTC. Check whether that shift persists within ordering bank, route, party-type pair and month. The contrast compares shares among observed payments. It does not estimate an individual account's schedule or use a local time-zone lookup.

## Discovery evidence

Among 1,593,042 payments across 61 dates and 3,838 ordering banks, weekend daily volume averaged 9,807.06 compared with 31,913.98 on weekdays. Pooled UTC daytime share was 54.2453% on weekends and 62.0435% on weekdays.

Within 1,107 bank/route/party/month strata with at least 30 payments of each calendar type, the share difference was −6.9699 percentage points using each stratum's smaller count as weight, and −6.4776 points giving each stratum equal weight. The matching restriction retains 76,245 weekend and 680,435 weekday payments from 270 banks, about 49% and 47% of the respective calendar samples. About 76% of supported strata show a negative contrast. The supported Direct and Indirect summaries both fall around −7 points. Covered lacks 100 supported banks for the separate matched report.

An exploratory alignment screen finds minute and hour boundary shares close to uniform-second references. It offers no obvious large excess at those boundaries and does not establish that sub-minute timing is uniform. Calendar dates define the denominators. No holiday or workweek external data were used.

## Test plan and exposure

Phase 0 conditional and full-data aggregates and the Round 1 B01–B03 outcomes are already exposed. Round 2 B04 and B05 use May–June and July within endpoint-bit-0/0, and the B05 ledger already notes a UTC hour/day pilot. This screen uses only May–June endpoint-bit-0/0. The exact July matched timing contrast remains unqueried in B06, but July records are reused and cannot be independent.

This screen sets no validation criteria and reads no validation records. A later test should freeze the eligible population, effect-size and coverage requirements, a comparison sensitive to bank composition, and uncertainty accounting for calendar dates and correlated ordering banks before checking a further period. Check beneficiary geography and currency as composition alternatives only with a predeclared design. Weekend is defined as Saturday/Sunday UTC, irrespective of country-specific weekends.

## Assessment

The matched pattern makes a purely pooled ordering-bank/route/party/month composition explanation inadequate on the supported strata. Remaining explanations include within-bank account/corridor mix, geography, and differences among specific days. UTC aggregates cannot identify a local business-hours generator, scheduling order or exact weekday weights.

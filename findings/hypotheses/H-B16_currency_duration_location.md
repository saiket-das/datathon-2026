# H-B16 currency-conditioned Direct duration locations

- **Owner:** B
- **Status:** large currency shift rejected in exploration on supported paths
- **Command:** `uv run python analysis/20_routing_time/H-B16_currency_duration_location.py`
- **Evidence:** [safe report](../../analysis/20_routing_time/out/H-B16_currency_duration_location_explore.md).

## Candidate, controls and results

Candidate explanation for B13 asymmetry is a large currency-associated duration
location shift within the same directed visible bank pair. Screen whether changing
currency corresponds to a mean range exceeding 20 seconds on recurring paths.
Use unlabelled May–June UTC payments with two visible banks and declared endpoint
MD5 bits both zero. Keep currency cells with at least ten payments and require
two currencies for a path. Each path contributes one range between its largest
and smallest supported currency means.

There are 418 paths covering 113,279 payments and 249 first visible banks.
Zero ranges exceed 20 seconds. The median, 90th and 99th percentiles are
1.1644, 3.0687 and 5.4124 seconds. Increasing minimum currency-cell support
to 25 leaves inadequate path or bank support for the displayed gate. This
sensitivity is suppressed in the reproducible report.

As a reference, matching the same path and currency across months with at least
25 observations in each month gives 1,900 cells, 290,110 payments and 684 first
visible banks. Their median, 90th and 99th percentiles of absolute mean drift
are .8659, 2.3266 and 4.1543 seconds. Zero exceed 20 seconds.

The primary screen does not support a large currency-driven mean shift in this
recurrent subset. The within-path ranges can include sampling error and different
account or calendar compositions. Selection excludes most rare path/currency
combinations. Shared banks and paths limit independent evidence, and the screen
does not establish currency-independent generation everywhere.

## Exposure and validation

Phase 0 and B01–B14 duration/routing findings were already exposed. An initial
May–June probe at minimum support25 preceded this script and found limited
path support. The expanded ten-payment screen was exploration. B15 was frozen
before the B16 script was run and its July residual outcomes were still running.
No B16 July query, frozen internal evaluation or independent confirmation is
claimed. The candidate of a large mean shift was rejected on its eligible
exploration population. A precise equivalence or conditional rule needs a
new frozen design.

The remaining duration question is how directed route locations arise when
currency, endpoint identities and small within-path timing noise are held fixed.

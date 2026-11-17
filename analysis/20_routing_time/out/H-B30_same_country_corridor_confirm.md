# H-B30_same_country_corridor: confirm

Freeze: daf2979fc4c8017e557c0f555d19254295a8d041.
DuckDB 2.0.0; 512MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Receiver-supported target population

| n | payments | banks | receivers | same_country_corridors |
| --- | --- | --- | --- | --- |
| 63715 | 196947 | 3642 | 784 | 3875 |

## Primary retained matched population

| n | payments | banks | receivers | same_country | different_country |
| --- | --- | --- | --- | --- | --- |
| 28113 | 80657 | 167 | 784 | 2743 | 25370 |

## Equal-origin matched effects

| comparison | origins | effect | low99 | high99 |
| --- | --- | --- | --- | --- |
| Raw | 167 | 0.044937 | 0.028316 | 0.060484 |
| May receiver adjusted | 167 | 0.044518 | 0.027839 | 0.059786 |

## Hash-order placebo

| origins | mean_effect |
| --- | --- |
| 467 | 0.000423 |

## Frozen practical decision

| pass |
| --- |
| True |

# H-B30_same_country_corridor: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 512MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Receiver-supported target population

| n | payments | banks | receivers | same_country_corridors |
| --- | --- | --- | --- | --- |
| 76831 | 276082 | 3925 | 784 | 4700 |

## Primary retained matched population

| n | payments | banks | receivers | same_country | different_country |
| --- | --- | --- | --- | --- | --- |
| 35537 | 118059 | 201 | 784 | 3428 | 32109 |

## Equal-origin matched effects

| comparison | origins | effect | low99 | high99 |
| --- | --- | --- | --- | --- |
| Raw | 201 | 0.042490 | 0.029064 | 0.057195 |
| May receiver adjusted | 201 | 0.041821 | 0.028602 | 0.056466 |

## Hash-order placebo

| origins | mean_effect |
| --- | --- |
| 528 | -0.002440 |

## Frozen practical decision

| pass |
| --- |
| True |

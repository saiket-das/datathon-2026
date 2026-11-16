# H-B13_symmetric_direct_duration: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% canonical first-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Unlabelled two-visible-bank exploration population

| payments |
| --- |
| 1005689 |

## Directional mean gaps on matched Direct corridors

| group | cells | corridors | payments | share_gap_over_100s | share_means_straddle_100s | p50/p75/p90/p99 gap seconds |
| --- | --- | --- | --- | --- | --- | --- |
| All directed visible pairs | 905 | 905 | 117640 | 0.310497 | 0.304972 | [1.9061302681992274, 168.6679292929293, 440.57579591836736, 583.9958473105843] |
| Endpoints agree with declared fields | 832 | 832 | 107145 | 0.316106 | 0.310096 | [1.9079616461969398, 173.7338512860968, 434.663900914284, 585.0600352448955] |
| Matched currency and FX count | 161 | 161 | 22477 | 0.416149 | 0.385093 | [3.119540229885059, 251.12820512820514, 474.0557491289199, 554.5129797271452] |

## 99% sensitivity interval for directional gaps above 100 seconds

| group | canonical first bank clusters | low | high |
| --- | --- | --- | --- |
| All directed visible pairs | 152 | 0.256383 | 0.377412 |
| Endpoints agree with declared fields | 143 | 0.259090 | 0.385086 |

## Same directed path, May versus June placebo

| directed_paths | payments | banks | share_gap_over_100s | gap_seconds |
| --- | --- | --- | --- | --- |
| 2040 | 313040 | 715 | 0.000000 | [0.8639195107218427, 1.5393269082589454, 2.3708073522886646, 4.10956984126983] |

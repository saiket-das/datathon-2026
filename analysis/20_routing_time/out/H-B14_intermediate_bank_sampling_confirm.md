# H-B14_intermediate_bank_sampling: confirm

Freeze: b1dbe22f6712359081a4577de1643f032e9866ae.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Training and validation support

| May three-bank payments | fitted middle banks | target four-bank payments | first visible banks | senders | receivers | both middle banks seen in May | primary pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 159191 | 4138 | 55865 | 2908 | 20994 | 34153 | 0.985537 | True |

## Frozen collision tests (intervals are observed minus expected)

| event | observed_share | expected_share | low99 | high99 | uniform-bank baseline |
| --- | --- | --- | --- | --- | --- |
| Identical visible middle banks | 0.006229 | 0.006088 | -0.000641 | 0.000985 | 0.000242 |
| Same country in both middle positions | 0.064531 | 0.065458 | -0.003112 | 0.001605 | n/a |

## Joint distribution of pooled middle-slot countries

| model | TV | low99 | high99 |
| --- | --- | --- | --- |
| Two draws from May distribution | 0.016403 | 0.019099 | 0.027272 |

## Marginal TV by position versus May distribution

| position | TV |
| --- | --- |
| 2 | 0.003311 |
| 3 | 0.005508 |

## Route type

| cell | n | banks | senders | receivers | repeated | country_collision | observed_endpoint_repeat | expected_endpoint_repeat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 5405 | 623 | 3176 | 4203 | <100 | 0.065125 | 0.008696 | 0.009278 |
| Indirect | 50460 | 2793 | 19343 | 31355 | 317 | 0.064467 | 0.004915 | 0.004767 |

## Gap presence

| cell | n | banks | senders | receivers | repeated | country_collision | observed_endpoint_repeat | expected_endpoint_repeat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 48053 | 2771 | 19074 | 30056 | 305 | 0.064949 | 0.005411 | 0.005216 |
| true | 7812 | 1384 | 5144 | 6336 | <100 | 0.061956 | 0.004480 | 0.005124 |

## Endpoint countries agree

| cell | n | banks | senders | receivers | repeated | country_collision | observed_endpoint_repeat | expected_endpoint_repeat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 52058 | 2795 | 19917 | 32225 | 324 | 0.064524 | 0.005359 | 0.005270 |
| true | 3807 | 621 | 2515 | 3021 | <100 | 0.064618 | 0.004203 | 0.004291 |

# H-B14_intermediate_bank_sampling: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Training and validation support

| May three-bank payments | fitted middle banks | target four-bank payments | first visible banks | senders | receivers | both middle banks seen in May | primary pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 159191 | 4138 | 78427 | 3234 | 26199 | 45281 | 0.986867 | True |

## Frozen collision tests (intervals are observed minus expected)

| event | observed_share | expected_share | low99 | high99 | uniform-bank baseline |
| --- | --- | --- | --- | --- | --- |
| Identical visible middle banks | 0.005916 | 0.006088 | -0.000815 | 0.000475 | 0.000242 |
| Same country in both middle positions | 0.065067 | 0.065458 | -0.002440 | 0.001814 | n/a |

## Joint distribution of pooled middle-slot countries

| model | TV | low99 | high99 |
| --- | --- | --- | --- |
| Two draws from May distribution | 0.013471 | 0.015600 | 0.022428 |

## Marginal TV by position versus May distribution

| position | TV |
| --- | --- |
| 2 | 0.005553 |
| 3 | 0.005690 |

## Route type

| cell | n | banks | senders | receivers | repeated | country_collision | observed_endpoint_repeat | expected_endpoint_repeat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 7846 | 750 | 4235 | 5865 | <100 | 0.066403 | 0.009432 | 0.009293 |
| Indirect | 70581 | 3088 | 24141 | 41404 | 420 | 0.064918 | 0.004605 | 0.004768 |

## Gap presence

| cell | n | banks | senders | receivers | repeated | country_collision | observed_endpoint_repeat | expected_endpoint_repeat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 67264 | 3097 | 23745 | 39787 | 388 | 0.064894 | 0.005129 | 0.005233 |
| true | 11163 | 1643 | 6825 | 8648 | <100 | 0.066111 | 0.004837 | 0.005142 |

## Endpoint countries agree

| cell | n | banks | senders | receivers | repeated | country_collision | observed_endpoint_repeat | expected_endpoint_repeat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 73043 | 3133 | 24938 | 42702 | 434 | 0.065112 | 0.005189 | 0.005278 |
| true | 5384 | 723 | 3265 | 4117 | <100 | 0.064450 | 0.003715 | 0.004443 |

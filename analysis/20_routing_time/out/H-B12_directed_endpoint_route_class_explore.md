# H-B12_directed_endpoint_route_class: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 1280MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
The 99% upper bound assumes independent first-visible-bank units. Shared receiving banks and entities limit that assumption.

## Frozen decision and coverage

| passes | target_multibank_rows | novel_supported_share | 99% upper affected fraction | mixed May visible corridors |
| --- | --- | --- | --- | --- |
| True | 318693 | 0.734164 | 0.001611 | 0 |

## Primary on novel visible paths through known directed endpoints

| n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 233973 | 48808 | 106383 | 2856 | 45199 | 228880 | 27024 | 0 | 0.000000 |

## Paired comparison to declared-bank majority on jointly supported novel paths

| n | senders | receivers | banks | corridors | path_sequences | visible_rate | declared_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 223546 | 47045 | 101718 | 2659 | 43004 | 218745 | 0.000000 | 0.005967 |

## Reversing the directed endpoints on jointly supported novel paths

| n | senders | receivers | banks | corridors | path_sequences | forward_rate | reversed_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 102402 | 25271 | 48485 | 740 | 14802 | 100253 | 0.000000 | 0.197584 |

## Mixed-label endpoint groups within target month

| basis | repeated_groups | payments | mixed_groups | minimum_error |
| --- | --- | --- | --- | --- |
| Declared, directed | 39282 | 255049 | 1691 | 0.008508 |
| Visible, directed | 39655 | 257850 | 0 | 0.000000 |
| Visible, unordered | 35672 | 264612 | 1052 | 0.026654 |

## Scope exclusions and prior path repetition

| supported | novel | n | banks | corridors |
| --- | --- | --- | --- | --- |
| False | True | 70176 | 3814 | 55248 |
| True | False | 14544 | 916 | 3146 |
| True | True | 233973 | 2856 | 45199 |

## Direct payments on visible corridors also seen as multibank that month

| route | n | banks | corridors |
| --- | --- | --- | --- |
| Covered | 53601 | 976 | 3417 |
| Indirect | 409876 | 3093 | 57989 |

## Visible bank count

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 150722 | 38131 | 74928 | 2685 | 38662 | 145647 | 17102 | 0 | 0.000000 |
| 4 | 61068 | 21811 | 35302 | 2223 | 23785 | 61050 | 7225 | 0 | 0.000000 |
| 5 | 22183 | 11138 | 15085 | 1675 | 12593 | 22183 | 2697 | 0 | 0.000000 |

## Route

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 27024 | 9916 | 16534 | 817 | 2721 | 26223 | 27024 | 0 | 0.000000 |
| Indirect | 206949 | 44767 | 95746 | 2729 | 42478 | 202657 | 0 | 0 | 0.000000 |

## Gap present

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 206777 | 45507 | 96236 | 2813 | 43221 | 202571 | 23900 | 0 | 0.000000 |
| true | 27196 | 12957 | 18070 | 1814 | 14805 | 27135 | 3124 | 0 | 0.000000 |

## Currency absent from May corridor

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 218786 | 46608 | 100315 | 2775 | 42346 | 213940 | 25843 | 0 | 0.000000 |
| true | 15187 | 8558 | 11219 | 1633 | 10916 | 15168 | 1181 | 0 | 0.000000 |

## Both visible endpoints agree with declared fields

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 15933 | 9068 | 11661 | 1930 | 10008 | 15895 | 2077 | 0 | 0.000000 |
| true | 218040 | 46443 | 99776 | 2301 | 42174 | 213402 | 24947 | 0 | 0.000000 |

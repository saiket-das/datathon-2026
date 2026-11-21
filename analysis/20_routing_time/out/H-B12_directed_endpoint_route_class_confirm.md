# H-B12_directed_endpoint_route_class: confirm

Freeze: 9489c1a051237433c0a6fbbbd260e602b2e27521.
DuckDB 2.0.0; 1280MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
The 99% upper bound assumes independent first-visible-bank units. Shared receiving banks and entities limit that assumption.

## Frozen decision and coverage

| passes | target_multibank_rows | novel_supported_share | 99% upper affected fraction | mixed May visible corridors |
| --- | --- | --- | --- | --- |
| True | 227489 | 0.735003 | 0.001679 | 0 |

## Primary on novel visible paths through known directed endpoints

| n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 167205 | 39984 | 81171 | 2741 | 39761 | 164380 | 19173 | 0 | 0.000000 |

## Paired comparison to declared-bank majority on jointly supported novel paths

| n | senders | receivers | banks | corridors | path_sequences | visible_rate | declared_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 159706 | 38548 | 77780 | 2542 | 37861 | 157038 | 0.000000 | 0.006387 |

## Reversing the directed endpoints on jointly supported novel paths

| n | senders | receivers | banks | corridors | path_sequences | forward_rate | reversed_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 73504 | 20442 | 37163 | 706 | 13704 | 72320 | 0.000000 | 0.196384 |

## Mixed-label endpoint groups within target month

| basis | repeated_groups | payments | mixed_groups | minimum_error |
| --- | --- | --- | --- | --- |
| Declared, directed | 29933 | 174438 | 1154 | 0.008450 |
| Visible, directed | 30112 | 176229 | 0 | 0.000000 |
| Visible, unordered | 27348 | 181965 | 909 | 0.026450 |

## Scope exclusions and prior path repetition

| supported | novel | n | banks | corridors |
| --- | --- | --- | --- | --- |
| False | True | 50012 | 3425 | 41547 |
| True | False | 10272 | 833 | 2473 |
| True | True | 167205 | 2741 | 39761 |

## Direct payments on visible corridors also seen as multibank that month

| route | n | banks | corridors |
| --- | --- | --- | --- |
| Covered | 38004 | 856 | 2878 |
| Indirect | 280090 | 2849 | 45199 |

## Visible bank count

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 107590 | 31009 | 56995 | 2537 | 33110 | 104768 | 12273 | 0 | 0.000000 |
| 4 | 43622 | 17381 | 26726 | 2012 | 19589 | 43619 | 5004 | 0 | 0.000000 |
| 5 | 15993 | 8882 | 11342 | 1573 | 9863 | 15993 | 1896 | 0 | 0.000000 |

## Route

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 19173 | 7771 | 12437 | 760 | 2527 | 18727 | 19173 | 0 | 0.000000 |
| Indirect | 148032 | 36703 | 73047 | 2620 | 37234 | 145653 | 0 | 0 | 0.000000 |

## Gap present

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 147595 | 37218 | 73330 | 2693 | 37722 | 145247 | 16983 | 0 | 0.000000 |
| true | 19610 | 10213 | 13722 | 1624 | 11783 | 19584 | 2190 | 0 | 0.000000 |

## Currency absent from May corridor

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 156400 | 38166 | 76676 | 2651 | 37228 | 153712 | 18357 | 0 | 0.000000 |
| true | 10805 | 6579 | 8249 | 1464 | 8419 | 10796 | 816 | 0 | 0.000000 |

## Both visible endpoints agree with declared fields

| cell | n | senders | receivers | banks | corridors | path_sequences | Covered_n | exceptions | error_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 11437 | 7131 | 8595 | 1743 | 7675 | 11416 | 1593 | 0 | 0.000000 |
| true | 155768 | 38074 | 76290 | 2242 | 37143 | 153214 | 17580 | 0 | 0.000000 |

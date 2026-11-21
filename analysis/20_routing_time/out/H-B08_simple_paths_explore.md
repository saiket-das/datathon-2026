# H-B08: repeated visible banks in route paths

Exploration only. Unlabelled May–June endpoint-bit-0/0, 512MB, one thread, no spill.
All bank identities stay in memory. Positive event counts below 100 are masked.
Visible adjacency is computed after removing placeholders. It differs from literal path-entry adjacency.

| Visible occurrences | Payments | Ordering banks | Any repeat | Same first/last bank | Adjacent visible repeat |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 | 1,005,689 | 3,702 | 0 | 0 | 0 |
| 3 | 370,978 | 3,257 | 1,966 | 0 | 1,966 |
| 4 | 137,022 | 2,798 | 2,225 | 0 | 1,503 |
| 5 | 50,120 | 2,276 | 1,635 | 0 | 815 |
| 6 | 18,500 | 1,721 | 945 | 0 | 379 |
| 7 | 6,836 | 1,235 | 586 | 0 | 201 |
| 8 | 2,450 | 775 | 276 | 0 | <100 |
| 9 | 921 | 467 | 148 | 0 | <100 |
| 10 | 338 | 239 | <100 | 0 | <100 |

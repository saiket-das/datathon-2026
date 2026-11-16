# H-A04: FX residuals and path gaps

Freeze: exploration only.
512MB; one thread; no disk spill. Aggregates only.
Only both-account exploration records queried. Five visible banks denotes five or more.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Unlabelled multibank coverage

| payments | eligible | mismatches |
| --- | --- | --- |
| 947930 | 934229 | 3594 |

## Signed errors by gap and route-length group

| route | visible_banks | has_gap | n | senders | receivers | error_pct | overpredict | underpredict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | False | 819701 | 93456 | 297698 | 0.3817 | 3129 | 0 |
| All | All | True | 114528 | 33061 | 60912 | 0.406 | 465 | 0 |
| Covered | 3 | False | 63116 | 15528 | 32790 | 0.2551 | 161 | 0 |
| Covered | 3 | True | 6831 | 3361 | 5147 | <100 errors | <100 | 0 |
| Covered | 4 | False | 21750 | 7662 | 13853 | <100 errors | <100 | 0 |
| Covered | 4 | True | 3651 | 2130 | 2922 | <100 errors | <100 | 0 |
| Covered | 5 | False | 11765 | 5058 | 8266 | <100 errors | <100 | 0 |
| Covered | 5 | True | 3064 | 1839 | 2513 | <100 errors | <100 | 0 |
| Indirect | 3 | False | 470741 | 71847 | 191923 | 0.3201 | 1507 | 0 |
| Indirect | 3 | True | 50710 | 19872 | 31042 | 0.2978 | 151 | 0 |
| Indirect | 4 | False | 164530 | 40688 | 81230 | 0.4668 | 768 | 0 |
| Indirect | 4 | True | 27141 | 13161 | 18396 | 0.4642 | 126 | 0 |
| Indirect | 5 | False | 87799 | 28122 | 48836 | 0.6287 | 552 | 0 |
| Indirect | 5 | True | 23131 | 11849 | 16110 | 0.6269 | 145 | 0 |

# H-C05: scam endpoint agreement (validate)

Sender MD5 bit 1. Freeze: cc24a3820411f7ac0a28aca53975d5d5f13ecca0.
Phase 0 and prior Round 1 outcome exposure apply. Validation reuses Round 1 bit-1 records.
Cohorts with fewer than 100 senders are omitted. Positive event counts below 100 are masked.

## Target totals

| Label | Route | Payments | Senders | Orderer mismatches | Beneficiary mismatches | Affected senders | 98.75% upper bound |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ACCOUNT_REPLACEMENT_SCAM | All | 312 | 301 | <100 | 0 | 0 | 0.014453 |
| CEO_SCAM | All | 465 | 442 | <100 | 0 | 0 | 0.009865 |

## Within-route controls

| Label | Route | Payments | Senders | Orderer mismatches | Beneficiary mismatches | Affected senders | 98.75% upper bound |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ACCOUNT_REPLACEMENT_SCAM | Direct | 218 | 212 | <100 | 0 | 0 | 0.020458 |
| CEO_SCAM | Direct | 285 | 273 | <100 | 0 | 0 | 0.015923 |
| CEO_SCAM | Indirect | 177 | 175 | <100 | 0 | 0 | 0.024729 |
| UNLABELLED | Direct | 3096496 | 166153 | 154315 | 155012 | 40303 | 0.244931 |
| UNLABELLED | Indirect | 1605218 | 128648 | 80031 | 80277 | 27354 | 0.215196 |

Frozen practical criteria: FAIL.

| Criterion | Result |
| --- | --- |
| ACCOUNT_REPLACEMENT_SCAM: total support | PASS |
| ACCOUNT_REPLACEMENT_SCAM: beneficiary concordance and uncertainty | PASS |
| ACCOUNT_REPLACEMENT_SCAM: ordering mismatch at least 2% | PASS |
| CEO_SCAM: total support | PASS |
| CEO_SCAM: beneficiary concordance and uncertainty | PASS |
| CEO_SCAM: ordering mismatch at least 2% | PASS |
| Unlabelled Direct: support and beneficiary mismatch at least 2% | PASS |
| Unlabelled Indirect: support and beneficiary mismatch at least 2% | PASS |
| ACCOUNT_REPLACEMENT_SCAM Direct: support and zero beneficiary mismatch | PASS |
| ACCOUNT_REPLACEMENT_SCAM Indirect: support and zero beneficiary mismatch | FAIL |
| CEO_SCAM Direct: support and zero beneficiary mismatch | PASS |
| CEO_SCAM Indirect: support and zero beneficiary mismatch | PASS |

## Target overlap (same role and field)

| Field | Shared values |
| --- | ---: |
| ROW_ID | 0 |
| ORDERING_ACCOUNT | 0 |
| BENEFICIARY_ACCOUNT | 231 |
| ORDERING_BIC8 | 192 |
| BENEFICIARY_BIC8 | 194 |
| Account in either role | 232 |
| Endpoint bank in either role | 375 |

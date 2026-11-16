# H-C05: scam endpoint agreement (explore)

Sender MD5 bit 0. Freeze: exploration only.
Phase 0 and prior Round 1 outcome exposure apply. Validation reuses Round 1 bit-1 records.
Cohorts with fewer than 100 senders are omitted. Positive event counts below 100 are masked.

## Target totals

| Label | Route | Payments | Senders | Orderer mismatches | Beneficiary mismatches | Affected senders | 98.75% upper bound |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ACCOUNT_REPLACEMENT_SCAM | All | 337 | 321 | <100 | 0 | 0 | 0.013558 |
| CEO_SCAM | All | 480 | 449 | <100 | 0 | 0 | 0.009712 |

## Within-route controls

| Label | Route | Payments | Senders | Orderer mismatches | Beneficiary mismatches | Affected senders | 98.75% upper bound |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ACCOUNT_REPLACEMENT_SCAM | Direct | 225 | 214 | <100 | 0 | 0 | 0.020269 |
| ACCOUNT_REPLACEMENT_SCAM | Indirect | 111 | 109 | <100 | 0 | 0 | 0.039405 |
| CEO_SCAM | Direct | 307 | 290 | <100 | 0 | 0 | 0.014997 |
| CEO_SCAM | Indirect | 169 | 165 | <100 | 0 | 0 | 0.026208 |
| UNLABELLED | Direct | 3222389 | 167100 | 160582 | 160941 | 40553 | 0.245046 |
| UNLABELLED | Indirect | 1653076 | 129282 | 82728 | 82065 | 27354 | 0.214142 |

Exploration pilot criteria (before freeze): PASS.

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
| ACCOUNT_REPLACEMENT_SCAM Indirect: support and zero beneficiary mismatch | PASS |
| CEO_SCAM Direct: support and zero beneficiary mismatch | PASS |
| CEO_SCAM Indirect: support and zero beneficiary mismatch | PASS |

# H-C05: beneficiary endpoint concordance in two scam labels

- **Owner:** C
- **Status:** Frozen combined test failed on support. Receiving-endpoint pattern supported but not independently confirmed.
- **Reproduce:** `uv run python analysis/30_parties_anomalies/H-C05_scam_endpoint_agreement.py --phase explore`
- **Evidence:** [Exploration report](../../analysis/30_parties_anomalies/out/H-C05_scam_endpoint_agreement_explore.md)

## Proposed rule and scope

Both ACCOUNT_REPLACEMENT_SCAM and CEO_SCAM retain concordance between
BENEFICIARY_BIC8 and the final visible path entry. ORDERING_BIC8 disagreement can
still occur. Contrast same-route unlabelled payments, where beneficiary
disagreement is common. This is a rule about consistency of the observed fields.
A path endpoint mismatch is a literal inequality using the final semicolon-delimited
entry, including any final placeholder. Neither timing nor the direction of any
generator edit is assumed.

## Test plan (freeze before validation)

1. Use only sender MD5 UTF-8 parity. Interpret the first eight hex digits of
   MD5(ORDERING_ACCOUNT) as an unsigned hexadecimal integer modulo 2. Bit 0
   supplied discovery. Bit 1 supplies frozen internal validation. All payments
   in those partitions are eligible for the designated cohorts, including
   Covered payments in target totals. Keep the two labels separate.
2. Each target must have at least 100 payments and 100 distinct senders, zero
   beneficiary endpoint mismatches, and at least 2% ordering endpoint mismatches.
   The one-sided exact Clopper-Pearson upper bound on the probability a target
   sender has any beneficiary mismatch must be at most 1.5% for each label.
   Use per-label 98.75% bounds. Bonferroni gives simultaneous coverage of at
   least 97.5% under independent-sender assumptions. Shared accounts, banks and
   text can violate effective independence.
3. Both labels must retain zero beneficiary mismatch within Direct and Indirect,
   with at least 100 payments and 100 senders in each label/route cell. Both
   unlabelled within-route controls must have at least 100 payments and senders
   and at least 2% receiving mismatch. These diagnostic controls address route
   composition and the alternative that endpoint disagreement vanished for
   every field. They do not control for bank, geography, calendar or unknown
   construction regimes. Unlabelled does not imply legitimate.
4. Fail the combined practical criteria when any condition fails, including
   inadequate support. Preserve descriptive results even if the combined
   test fails. Do not weaken criteria after observing bit 1.
5. Audit exact target row ID, same-role ordering and beneficiary accounts,
   same-role endpoint banks, and either-role accounts/banks across splits.
   Report counts only and mask positive values under 100. Report target and
   supported comparator denominators. No bank/time robustness or further
   negative-class tests are planned for this frozen run.
6. Phase 0 exposed full-data endpoint disagreement, entity overlap and balance.
   Round 1 exposed label aggregates and C01/C02 validation outcomes for these
   same bit-1 records. The class-specific receiving mismatch outcome in bit 1
   was unexamined for this test before freezing. The reused population cannot
   support an independent holdout claim. A pass supports the observed pattern
   under frozen internal validation, with evidence level Supported but not
   independently confirmed.

## Discovery evidence

Bit 0 had zero receiving endpoint mismatches for 337 account-replacement records
across 321 senders and 480 CEO records across 449 senders. Supported Direct and
Indirect cells in both labels also had zero. Same-route unlabelled controls
showed about 5% beneficiary mismatch. Sender mismatches were present in both
target totals. This can arise from restricting or recomputing relevant fields,
from a shared bank-selection regime, or from another dependence. Sparse Covered
cohorts do not support a separate route-specific statement.

## Validation results

Freeze: `cc24a3820411f7ac0a28aca53975d5d5f13ecca0`, recorded before
any C05 bit-1 outcomes were queried.

```text
uv run python analysis/30_parties_anomalies/H-C05_scam_endpoint_agreement.py --phase validate --freeze cc24a3820411f7ac0a28aca53975d5d5f13ecca0
```

**Overall result: FAIL.** The account-replacement Indirect cell did not reach the
frozen support floor. The corresponding statistics remain suppressed. Both
target totals met their criteria: 0 receiving mismatches in 312 account-replacement
payments (301 senders) and 465 CEO payments (442 senders). Both targets passed
the 2% ordering mismatch floor. The exact simultaneous upper bounds for any
receiving mismatch at sender level were approximately 1.445% and 0.986%.
The Direct and Indirect unlabelled controls retained about 5% receiving mismatch.

Zero target row IDs or sending accounts overlap across sender bits. The audit
found 231 shared receiver accounts, 232 account strings in either role and 375
endpoint banks in either role. Shared receivers and banks limit the interpretation
of the sender intervals. These outcomes came from reused Round 1 records.

See the [frozen validation report](../../analysis/30_parties_anomalies/out/H-C05_scam_endpoint_agreement_validate.md)
for every criterion decision and supported count.

## Assessment

Retain the failure of the combined rule and the descriptive endpoint asymmetry.
Zero beneficiary endpoint mismatches in the two observed totals is a constraint
on output fields. It leaves causal ordering, account substitution and the
exact mechanism unresolved. Review its role as a secondary finding after
independent methodological review.
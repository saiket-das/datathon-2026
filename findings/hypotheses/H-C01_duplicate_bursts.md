# H-C01: Duplicate-labelled payments form exact-context, short copy bursts

- **Owner:** C
- **Status:** replicated
- **Script / exact command / commit:** `uv run python analysis/30_parties_anomalies/H-C01_duplicate_bursts.py --phase confirm --freeze-commit bd61bc32dc61f4985c757244051404fb6622a71b`.
- **Chart:** `analysis/30_parties_anomalies/out/H-C01_duplicate_bursts_confirm.png`

## Proposed rule and scope

Duplicate-labelled payments occur in families keyed by the exact tuple
`(ORDERING_ACCOUNT, BENEFICIARY_ACCOUNT, CURRENCY_CODE, USD_AMOUNT)`.
The proposed signature is: 2–5 family members, consecutive original `ROW_ID`s,
family timestamp range at most 7,200 seconds, and exact constancy of all 15
non-account, non-amount, non-time context fields (including full details and tokens).
The family key already fixes both accounts, currency and amount. Labels do not
participate in signature construction. Time order is deliberately unrestricted.

Unit: a payment, with uncertainty and equal weighting at the sender level. A family
can have an unrelated payment to the same receiver at a different amount; that is
why the key includes amount/currency. This is an empirical joint structure, not the
dictionary definition of an accidental duplicate and not proof of the source code.

## Test plan (freeze before confirmation)

- **Comparator, statistic and tolerance:** all unlabelled payments in the same
  partition, plus every other allowlisted anomaly class. Primary coverage is the
  share of duplicate-labelled rows satisfying the whole signature; also calculate
  equal-sender mean coverage. Both must be at least 95%. The observed unlabelled
  signature share must be at most 0.1%. No exclusivity against other labels is claimed.
- **Uncertainty and support:** 4,000 whole-sender bootstrap replicates, seed
  `20261116`, describe mean-coverage uncertainty. Also count senders with *all*
  target payments matching; its exact binomial one-sided 97.5% lower bound must
  be at least 90%. Two primary hypotheses allocate 0.025 each by Bonferroni.
  For all-success independent senders, 36 suffice for this lower-bound criterion;
  this is a precision design, not a claim that shared receivers are independent.
  Report sender/receiver/family support, mask counts below 100, and largest-sender
  and largest-receiver payment shares. Receiver-weighted coverage is a descriptive
  concentration control. Bootstrap intervals can degenerate at 100%; report the exact bound.
- **Alternatives and controls:** report broad same-key repetition without context,
  chronology or source-order requirements. Report coverage by party pair, month
  and original million-row file block
  within the same split. Ordinary repeat invoices, round amounts, hubs and common
  routes can explain simple repetition; joint context/source-order constancy is the
  stronger claim. Hashes only shortlist adjacent candidates; exact strings and
  exact keys determine equality, so hash collisions cannot create signature hits.
- **Falsification:** reject or limit the proposed near-universal signature if any
  acceptance condition fails. Preserve exact coverage and all exception counts.
  A wrong family size, field change, nonconsecutive source row or range >7,200s
  is an exception. A small unlabelled hit rate does not establish legitimate status.
- **Partition, predicate and coverage:** shared `partition_sql('sender')`, with
  `(('0x'||substr(md5(ORDERING_ACCOUNT),1,8))::UBIGINT % 2)=0` for exploration,
  `=1` for confirmation; no seed reroll, no excluded rows. The shared audit gives
  5,097,938 exploration and 4,902,062 confirmation rows, zero shared sender/row IDs,
  but 388,309 account strings across roles and 7,838 endpoint banks overlap.
  Currency TV distance 0.050678; party-pair 0.012068; route 0.003202. The preexisting
  label-support audit gives 312/367 target rows; exploration has fewer than 100
  relevant senders, confirmation 100. Both-role account separation was considered
  but drops half the payments and has limited rare-class support; sender-specific
  sequence replication is the chosen estimand, not global entity independence.
- **Primary confirmation:** run the same script with `--phase confirm --freeze-commit SHA`.
  The program checks that both investigation scripts match that commit before
  reading confirmation. No per-row stratification, tuned thresholds or seed changes.
- **Robustness:** the frozen month, file-block and party-pair tables are descriptive sensitivity
  checks within confirmation. Family membership uses the entire sender partition,
  so a month boundary does not truncate sequences. This is not a time holdout, and
  no bank holdout or alternative partition is pooled as independent evidence.
- **Freeze commit/time and prior exposure:** `bd61bc32dc61f4985c757244051404fb6622a71b`,
  2026-11-16 08:19:47 UTC (16:19:47 Malaysia time). Recorded before opening confirmation.
  Before freezing, only sender-bit-0 outcomes were queried by this investigator.
  Prior exposure includes the shared Phase 0 full-data structural, balance and
  label-support aggregates. No partition is wholly unseen. Other investigators'
  developing branches, PRs and provisional findings were not consulted.

## Discovery evidence

The exploration report contains the exact reproducible denominators. All 312
duplicate-labelled rows match the signature. Target-containing exact-key families
contain only duplicate labels, have 2–5 members, median span 3,959 seconds and
maximum span 7,043 seconds. Every family retains its complete context.
Equal-sender coverage is 100%; the one-sided 97.5% exact lower bound on the
all-success sender probability is 0.956529. Largest sender contributes 2.5641%.
There are no hits among 5,094,378 unlabelled rows. The signature also matches
0.605144% of romance-labelled rows: it cannot uniquely identify a duplicate label.

**Rejected initial variant:** an unlabelled original plus labelled copies. Exact-key
target families instead have every member labelled. Do not select an unlabelled
record as an invented original. **Unresolved:** chronology does not identify an
original transaction; only 18.8235% of these families have monotone timestamps.
No uniform-jitter distribution or exact number-of-copies distribution is asserted.

## Confirmation and robustness results

**PASS, unchanged frozen test.** The confirmation report is
[`H-C01_duplicate_bursts_confirm.md`](../../analysis/30_parties_anomalies/out/H-C01_duplicate_bursts_confirm.md).
Confirmation read 4,902,062 sender-bit-1 payments. All **367/367 duplicate-labelled
payments**, spanning **100 exact-key families, 100 senders and 100 receivers**,
match the signature, with zero target exceptions. Family size remains 2–5;
median span 4,028 seconds, maximum 6,980. Every target family has constant complete
context and every member is labelled duplicate. Only 15% have monotone timestamps;
chronology still cannot identify a pristine original.

Row-, sender- and receiver-weighted coverage are all 100%. Sender bootstrap interval
is [100%,100%] (degenerate, descriptive); exact one-sided 97.5% lower bound for the
all-success sender probability is **96.3783%**, exceeding the frozen 90% criterion.
Largest sender and largest receiver each contribute 1.3624% of target payments.
No signature hits occur among **4,898,616 unlabelled confirmation payments**.
Ordinary same-key repetition, without full context/source-order conditions, instead
occurs in 2,508 unlabelled payments (0.0511981%).

**Exceptions to exclusivity:** 1.03986% of romance-labelled confirmation payments
also match this exact-amount-family signature; there are no matches in the other
four labelled classes. This was anticipated by discovery and is not hidden or
treated as a new reason to change the key.

**Predeclared sensitivities:** the complete signature covers every target row in
each month, party pair and source block. Suppressed strata remain suppressed in
the report; apparent missing stratum estimates do not imply absence of cases.
The displayable business→consumer stratum (215 payments), June (165) and July
(105) each have 100% coverage; all corresponding unlabelled strata have zero
signature matches. These checks use overlapping sender-confirmation records and
are not independent calendar/bank holdouts. No post-freeze code or test change.

## Assessment

Replicated reconstruction within the selected sender split: make a small batch sharing the payment context and
amount, with timestamps lying within a two-hour range; retain all members' labels.
The source-row adjacency is a file-construction signature and would disappear
under row shuffling. Identical context also fits independent template reuse; its
joint clustering and label association support a copy-burst interpretation, not
the original implementation, causal direction or a deployable fraud detector.

## Real-world explanation (interpretation, not evidence)

A retry or back-office race can resend the same instruction without changing its
party details or value. A synthetic batch writer using the same sampled context
is an alternative and could itself explain the contiguous file rows. The timestamp
range is evidence about this dataset, not an operational two-hour rule.

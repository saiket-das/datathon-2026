# H-C02: Romance-labelled payments form chronological, variable-amount copy bursts

- **Owner:** C
- **Status:** replicated
- **Script / exact command / commit:** `uv run python analysis/30_parties_anomalies/H-C02_romance_bursts.py --phase confirm --freeze-commit bd61bc32dc61f4985c757244051404fb6622a71b`; implementation shared with H-C01.
- **Chart:** `analysis/30_parties_anomalies/out/H-C02_romance_bursts_confirm.png`

## Proposed rule and scope

Romance-labelled payments occur in exact sender–receiver pairs containing 2–8
payments. The signature requires a consumer sender, consecutive original `ROW_ID`s,
nondecreasing timestamps spanning at most 7,200 seconds, varying amounts, and
exact constancy of the other 15 context fields: currency, both banks, full route,
duration, continuity, FX count, participant count, route type, both detail strings,
both token strings and both party types. No receiver-type restriction is imposed.
All pair rows participate, regardless of amount/currency/label; unrelated payments
can falsify the whole-pair signature. Labels are used only after candidate scoring.

This predicts a specific batch structure, beyond the dictionary's repeated-transfer
description. Unit: payment; primary uncertainty and equal weighting: sender.
Family median adjacent amount growth is a prespecified descriptive statistic,
not an extra acceptance condition or a claim of an exact multiplier distribution.

## Test plan (freeze before confirmation)

- **Comparator, statistic and tolerance:** all unlabelled payments and every other
  anomaly class in the same partition; broad sender–receiver repetition is the
  deliberately weaker comparator. Target row coverage and equal-sender coverage
  must each be at least 95%; unlabelled signature share at most 0.1%.
- **Uncertainty:** identical H-C01 protocol: 4,000 sender bootstrap draws with seed
  `20261116`; one-sided 97.5% exact lower bound for the fraction of all-success
  senders must reach 90%, with Bonferroni allocation for two co-primary signatures.
  Report entity counts, family counts, largest sender/receiver shares and equal-receiver
  coverage as descriptive concentration controls. The bootstrap is
  descriptive and degenerates at all-success; the exact bound carries precision.
  Shared recipients can make both uncertainty summaries overconfident about a
  superpopulation, so treat confirmation as sender transfer in this dataset.
- **Alternatives and controls:** both consumer→business and consumer→consumer
  strata; all months and million-row source blocks; ordinary pair repetition; shared receiver/template reuse;
  source ordering; exact amount repetition versus varying amounts. Report complete
  family support and invariants, not only the rows selected by a final signature.
- **Falsification:** any violated acceptance condition rejects/limits the primary
  near-universal signature. Family size outside 2–8, constant amount, changed
  context, nonconsumer sender, backwards timestamp, source-row gap or >7,200s
  range counts as failure. Do not repair or relabel exceptions.
- **Partition and coverage:** MD5 sender bit 0 exploration, bit 1 confirmation,
  exactly the shared predicate and audit described in H-C01. Eligible rows:
  5,097,938 / 4,902,062, none excluded. Prior label-support audit: 1,322 romance
  exploration rows, 264 senders, 230 receivers; confirmation 1,154 rows, 236
  senders, 200 receivers. Sender IDs and rows are disjoint; receivers, cross-role
  identifiers, banks and text can overlap. Currency TV 0.050678, route TV 0.003202,
  party-pair TV 0.012068. Both-account splitting would lose half the rows and
  leave some target receiver support below 100; it is not substituted post hoc.
- **Primary confirmation:** `uv run python analysis/30_parties_anomalies/H-C02_romance_bursts.py --phase confirm --freeze-commit SHA`.
  The shared implementation must match the freeze commit. No thresholds, keys,
  exclusions or sender assignments change after confirmation is opened.
- **Robustness:** predeclared descriptive month, file-block and party-pair sensitivity tables
  inside the same sender confirmation partition. Whole families are scored before
  monthly summaries, avoiding artificial boundary failures. These are overlapping
  sensitivity checks, not independent temporal or bank replication.
- **Freeze commit/time and prior access:** `bd61bc32dc61f4985c757244051404fb6622a71b`,
  2026-11-16 08:19:47 UTC (16:19:47 Malaysia time), recorded before opening confirmation.
  Only sender-bit-0 outcomes were queried
  here before freeze. Shared Phase 0 full-data structural and split-support
  aggregates were already exposed. No other investigator's developing work read.

## Discovery evidence

All 1,322 romance-labelled exploration rows, representing 264 pairs/senders and
230 receiver identifiers, match the full signature. Pair size range 2–8;
median timestamp span 1,060.5 seconds, maximum 3,812; all timestamps are
nondecreasing in source order. All 15 context fields remain exactly unchanged
within every target-containing pair. Every such pair is fully labelled romance.
Amounts vary; the median across families of their median adjacent log amount
ratio, exponentiated, is 1.4954. This is not proof of a constant 1.5 multiplier.

No signature hits among 5,094,378 unlabelled rows or the other five classes.
Equal-sender coverage is 100%; exact lower bound 0.986124; largest sender share
0.605144%. See the script's comparison with ordinary pair repeats for specificity.

**Rejected initial variant:** consumer→consumer only, suggested by the official
dictionary's narrative. Business receivers occur in 27.4584% of romance-labelled
exploration payments (363/1,322), while every sender is a consumer. Party-type
fields are preserved; no assumption is made that a receiver label equals the
fraudster's true economic identity. **Rejected simplification:** exact amount copies
alone; every whole romance pair has varying amounts, although subgroups can repeat
an amount and therefore overlap H-C01's looser duplicate-family signature.

## Confirmation and robustness results

**PASS, unchanged frozen test.** Full safe evidence:
[`H-C02_romance_bursts_confirm.md`](../../analysis/30_parties_anomalies/out/H-C02_romance_bursts_confirm.md).
All **1,154/1,154 romance-labelled confirmation payments** match the signature,
with zero target exceptions, across **236 pairs/senders and 200 receivers**.
Every target-containing pair is fully romance-labelled; its 15 context fields
remain unchanged. Family size range is 2–8, median timestamp span 1,068 seconds,
maximum 4,191 seconds; timestamps are nondecreasing and amounts vary in every pair.
The frozen descriptive median-family geometric growth statistic is 1.4791 versus
1.4954 in exploration; no exact growth distribution or multiplier is inferred.

Row-, equal-sender- and equal-receiver-weighted coverage are all 100%. Sender
bootstrap interval [100%,100%] is degenerate; exact one-sided 97.5% lower bound for
the all-success sender probability is **98.4491%**, above the frozen 90% criterion.
Largest sender contributes 0.693241%, largest receiver 1.55979% of target payments.
No matches occur among **4,898,616 unlabelled confirmation payments**, or any of
the other five labels. By contrast, ordinary pair repetition occurs in 1,122,890
unlabelled payments (22.9226%): repeated transfers alone are a poor anomaly rule.

**Predeclared sensitivity:** all 302 consumer→business and 852 consumer→consumer
target payments match, preserving the rejection of a consumer-only receiver rule.
Business receivers account for 26.1698% of confirmation cases. May/June/July target
counts are 394/379/381, each with 100% signature coverage. All target cases again
occur in source-file million-row blocks 0–2 (465/533/156); no claim of file-order
generality is warranted. These are overlapping within-partition controls, not
independent temporal/bank holdouts. Small entity support remains masked in the
report; no criteria, key, threshold, code or partition changed after freeze.

## Assessment

Replicated reconstruction within the selected sender split: reuse a sampled consumer-origin payment context for a
short chronological sequence to one receiver, varying amounts while retaining
even duration and complete details/tokens. This supports a context-copy sequence
interpretation; it does not prove the exact random-number process, causality or
identity semantics. Bank/type independence and the original generator remain open.

## Real-world explanation (interpretation, not evidence)

Repeated requests for funds in a relationship scam can produce repeated transfers
and rising typical values. A synthetic scenario writer reusing a payment template
is an alternative explanation for exact route/duration/text persistence. Shared
counterparties and contiguous file batches weaken any claim of independent events.

# H-C04: literal LINEBREAK token count

- **Owner:** C
- **Status:** Rejected in exploration.
- **Reproduce:** `uv run python analysis/30_parties_anomalies/H-C04_literal_linebreak.py`
- **Evidence:** [Safe aggregate table](../../analysis/30_parties_anomalies/out/H-C04_literal_linebreak.md)

## Proposed rule and scope

Test a literal interpretation of the case study's line-break token example.
For each party role, count LF characters in the details and literal uppercase
LINEBREAK occurrences in the token string. The candidate predicts one marker per LF.

## Exploration design and results

On 5,097,938 sender-bit-0 payments, ordering details contain LF without any
marker in 4,977,524 cases. Beneficiary details do so in 4,971,004 cases.
The remaining exact-count cases have zero LF and zero literal markers.
Neither role uses the tested uppercase marker. This falsifies the literal
mapping. Formatting, a structured tag encoding, and a context-sensitive parser
remain possible. The official description does not prescribe literal token names.

## Validation and exposure

Rejected during discovery. The test has no validation run. Phase 0 exposed
same-details/different-tokens aggregates and Round 1 exposed grouped label/context
evidence. Only sender-bit-0 outcomes for this rule were queried. This result
supports a narrow caveat for the token dashboard, pending reconstruction of the
actual encoding.
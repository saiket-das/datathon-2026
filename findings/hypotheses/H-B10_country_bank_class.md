# H-B10: Is the B09 bank class fixed by visible-bank country?

- **Owner:** B
- **Status:** rejected in exploration
- **Script:** `uv run python analysis/20_routing_time/H-B10_country_bank_class.py`
- **Evidence:** [aggregate report](../../analysis/20_routing_time/out/H-B10_country_bank_class_explore.md)

## Candidate and exploration

The candidate says every supported visible bank in a country has the same B09 May duration-exclusion label. Use May Direct unlabelled endpoint-bit0/0 payments only, with at least100 appearances per bank. An exclusion label means zero appearances with duration<100. Country is the two-character visible BIC field. This concerns the observed witness-based bank classification, not a separately established latent bank type.

Among1,061 supported banks,440 are exclusion-labelled. They span142 countries, and71 countries contain both labels. Assigning each country its majority class misclassifies at least34.872762% of the same training banks. Among721 banks in countries with at least10 supported banks, the minimum error is39.528433%. No bank or country identifiers are exported.

The exact country-deterministic explanation of these observed labels is falsified. Geography can still correlate with probabilities, bank exposure, counterparties or duration. Errors in witness-based classification and within-country latent groups remain alternatives.

## Prior exposure and validation

Phase0, Round1 duration summaries, B04-B08, the B09 June pilot and its freeze were exposed before this May-only exploration. The first country-class aggregate was calculated while July B09 ran; the reproducible script was then run before reviewing the new B09 July output. There is no B10 validation, held-out country prediction or freeze. Any more detailed geographic or latent-class rule needs its own plan with the above outcomes disclosed.

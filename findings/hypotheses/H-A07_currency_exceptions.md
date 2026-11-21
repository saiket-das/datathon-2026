# H-A07: Receiver-country alternatives among currency exceptions

- **Owner:** A
- **Status:** exploratory
- **Command:** `uv run python analysis/10_amounts_currency/H-A07_currency_exceptions.py`
- **Evidence:** `analysis/10_amounts_currency/out/H-A07_currency_exceptions_explore.md`

## Question and scope

When the observed currency differs from the pre-July modal currency for the
first path-bank country, does receiving-country information account for the
exception? Compare a mode fitted by receiving country with the sending-country
map applied to the receiving country. Both are learned pre-July on unlabelled
bit-0 records. The latter uses one consistent country-to-mode map for both roles.
It is a learned local convention and uses no outside currency table.

The screen uses July bit-0 records where the sending and receiving country
maps are both supported by at least 100 training rows and currency differs
from the first-path-country prediction. Report only groups with at least
1,000 payments and 100 senders and receivers.

## Exploration evidence

The 49,548 residual payments span 20,435 senders and 29,718 receivers.
There are 27,778 EUR and 12,474 USD payments. Together EUR/USD account for
40,252 (81.24%) of this conditional population.

The mode fitted by receiving country agrees on 27,531 residuals. Among EUR
residuals it agrees on 98.83%, but among USD residuals only 0.59%. Its apparent
performance partly reflects the global prevalence of EUR in receiver groups,
so calling it the receiver's local currency would overstate the model.

Applying the sending-country map to the receiving country agrees on 28,220
residuals (56.96%). Agreement is 61.01% for EUR, 53.29% USD, 63.91% GBP,
57.00% CHF and 53.49% CNY in displayable currency groups.
In differing sender-versus-receiver modes fitted by their own roles, the
same-map receiving-country alternative agrees on 73.04% of Direct residuals,
42.93% Indirect and 39.51% Covered. The subset is chosen by modal errors,
and composition can explain this contrast.

## Prior exposure and validation

Phase 0 exposed global currency distributions. Round 1 A01/A02 and A03/A05/A06
exposed other outcomes on the both-account bit-1 population. This screen
queried bit-0 only and used no validation outcomes. It is development
conditioning after A06's endpoint-association result. No new acceptance rule
is frozen or independently confirmed.

A future test would need a prespecified endpoint/path currency-choice model,
a prevalence-preserving negative map or currency/route/country-mix control,
and frozen criteria before bit-1 scoring. Reusing those bit-1 records would
remain internal validation. The difference between maps shows why a
receiver-mode match cannot identify denomination selection by itself.

## Assessment and alternatives

No specific currency-selection mechanism is accepted. Possible next questions
include whether currency matches either endpoint's consistently learned mode
or the mode of an intermediate visible bank, and how that relation varies by
route. Recipient geography, path selection and the prevalence of EUR/USD can
produce these conditional summaries. The exact mixture, original denomination,
selection direction and original generator order remain unresolved.

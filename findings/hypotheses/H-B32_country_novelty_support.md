# H-B32 Geographic contrast on unseen pairs

- **Status:** insufficient matched-origin support for unseen-pair extension
- **Command:** `uv run python analysis/20_routing_time/H-B32_country_novelty_support.py`.

## Question and population

B30 permits previously observed corridors. Audit the same origin-matched
contrast on new June directed pairs when neither orientation appears
in May. Use unlabelled v3–5 bit0/0 pure pairs and at least25 May corridors
per receiver. Match same-country versus different-country groups within
each origin. Require five unique corridors per group, then repeat
with ten. Equal corridor weights define each group rate, followed by
equal origin weights in the matched contrast.

## Exploration results

Recurring pairs retain141 origins and21,011 corridors at support five.
The equal-origin Covered contrast is+.040475. At support ten there
are fewer than100 origins. May-unseen pairs retain6,487 corridors at
support five and2,993 at support ten, with fewer than100 origins under
both rules. Their effect sizes are suppressed. This limits what can
be claimed for the chosen matching design, without rejecting an
underlying geographic relationship. B30's actual population and
frozen result remain scoped as recorded.

## Exposure and uncertainty

Phase0 and B01–B31, including B30's July contrast, were already exposed.
This script reads only May–June and has no frozen validation claim.
A preliminary correlated anti-join completed slowly. The final query
uses canonical unordered bank-pair keys for either-orientation exclusion.
Shared banks, countries, accounts and observed labels remain dependencies.
The next question is whether a broader predeclared design can identify
the association on unseen corridors with adequate origin support.

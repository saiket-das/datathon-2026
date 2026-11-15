# H-000: <short title>

Copy this file to `H-<owner letter><number>_<short_name>.md`, for example `H-A01_amount_by_party_pair.md`. The owner letter keeps IDs from colliding.

- **Owner:** A / B / C
- **Status:** provisional | confirmed | rejected | uncertain
- **Script:** `analysis/<folder>/<script>.py`
- **Chart:** `analysis/<folder>/out/<file>.png`

## Guess
What we expect to see and why, in one or two sentences.

## Test
What we compare against what (the baseline), and which other factor we hold fixed.

## Result
The numbers. How many rows it covers (count and share). Where it does not hold.

## Confirmed on the other half of accounts?
Yes / No, with the numbers.

## Rule (only if confirmed)
When <condition>, <column> <changes how> by <how much>, covering <which rows>; it does not apply to <exceptions>.

## Real-world explanation (interpretation, not evidence)
Why a real payment system might behave like this, and one alternative explanation.

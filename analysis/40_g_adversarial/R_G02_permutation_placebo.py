"""G-039 exact conditional permutation placebo, synthetic-only.

Conditional on each observed intermediary multiset, randomly permuting its
positions uniformly is the null. No sponsor data, no RNG, no outcome access.
"""
from collections import Counter
from math import factorial, fsum, sqrt
from typing import Sequence


def _permutation_count(motif: tuple[str, ...]) -> int:
    counts = Counter(motif)
    denominator = 1
    for n in counts.values():
        denominator *= factorial(n)
    return factorial(len(motif)) // denominator


def permutation_placebo_exact(
    early_ordered: set[tuple[str, ...]],
    observed: Sequence[tuple[str, ...]],
) -> dict[str, float] | None:
    """Exact mean and marginal independent-route variance under uniform reordering.

    The observed routes' intermediary multisets are held fixed. For each route,
    success is whether its uniformly permuted ordered sequence belongs to the
    early ordered dictionary. Distinct routes are independent ONLY in this
    mathematical placebo, not necessarily in payment data. Return conditional
    expectation, variance of mean, and observed recall. Do not use z-tests or
    infer a sponsor p-value from this variance.
    """
    if not observed:
        return None
    k = len(observed[0])
    if k < 2 or any(len(x) != k for x in observed) or any(
        len(x) != k for x in early_ordered
    ):
        raise ValueError("all routes and early motifs require one k>=2 stratum")
    early_by_multiset: Counter[tuple[str, ...]] = Counter()
    for t in early_ordered:
        early_by_multiset[tuple(sorted(t))] += 1
    probs = []
    for t in observed:
        key = tuple(sorted(t))
        possible = _permutation_count(t)
        matches = early_by_multiset[key]
        if matches > possible:
            raise ValueError("early ordered dictionary exceeds possible permutations")
        probs.append(matches / possible)
    n = len(observed)
    observed_hits = sum(t in early_ordered for t in observed)
    expectation = fsum(probs) / n
    variance = fsum(p * (1.0 - p) for p in probs) / (n * n)
    return {
        "n": float(n),
        "observed_ordered_recurrence": observed_hits / n,
        "permutation_null_expected_recurrence": expectation,
        "observed_minus_null": observed_hits / n - expectation,
        "independent_route_null_sd": sqrt(variance),
        "multiset_supported_share": sum(p > 0 for p in probs) / n,
    }

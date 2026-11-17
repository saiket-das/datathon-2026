"""G-040 synthetic-only May-position-weighted permutation placebo.

Conditional on an observed multiset, assign each distinct permutation mass
proportional to product of early-May position-specific smoothed frequencies.
No sponsor dataset I/O, no July fitting, no inference p-value.
"""
from collections import Counter
from itertools import permutations
from math import fsum, log, exp
from typing import Sequence


def position_weighted_placebo(
    early_ordered: Sequence[tuple[str, ...]],
    observed: Sequence[tuple[str, ...]],
    alpha: float = 1.0,
    max_distinct_permutations: int = 40320,
) -> dict[str, float] | None:
    """Return exact May-position-weighted recurrence expectation for fixed multisets.

    A Dirichlet-alpha smoothed per-position categorical model is trained on
    early motifs only. Universe is precisely early-observed identities; novel
    identities have no support and are counted as abstentions, not successes.
    The target sample remains the entire observed set in returned shares.
    """
    if not observed:
        return None
    k = len(observed[0])
    if k < 2 or any(len(x) != k for x in observed) or any(len(x) != k for x in early_ordered):
        raise ValueError("one fixed k>=2 stratum required")
    if not (0 < alpha < float("inf")):
        raise ValueError("finite positive smoothing required")
    if max_distinct_permutations < 1:
        raise ValueError("positive enumeration cap required")
    universe = set(x for motif in early_ordered for x in motif)
    counts = [Counter(t[j] for t in early_ordered) for j in range(k)]
    denom = len(early_ordered) + alpha * len(universe)
    dictionary = set(early_ordered)
    probabilities: list[float | None] = []
    observed_hits = 0
    for motif in observed:
        if not set(motif).issubset(universe):
            probabilities.append(None)
            continue
        # Enumerate distinct orders only; repeated identities are not
        # artificially overrepresented by their factorial multiplicities.
        orders = set(permutations(motif))
        if len(orders) > max_distinct_permutations:
            probabilities.append(None)
            continue
        log_weights = [
            sum(log((counts[j][x] + alpha) / denom) for j, x in enumerate(order))
            for order in orders
        ]
        shift = max(log_weights)
        weights = [exp(v - shift) for v in log_weights]
        total = fsum(weights)
        expected = fsum(w for order, w in zip(orders, weights) if order in dictionary) / total
        probabilities.append(expected)
        observed_hits += motif in dictionary
    supported = [p for p in probabilities if p is not None]
    n = len(observed)
    if not supported:
        return {"n": float(n), "supported_n": 0.0, "support_share": 0.0,
                "observed_supported_recurrence": float("nan"),
                "weighted_null_recurrence": float("nan"),
                "observed_minus_weighted_null": float("nan")}
    supported_hits = sum(
        motif in dictionary for motif, p in zip(observed, probabilities) if p is not None
    )
    actual = supported_hits / len(supported)
    expected = fsum(supported) / len(supported)
    return {"n": float(n), "supported_n": float(len(supported)),
            "support_share": len(supported) / n,
            "observed_supported_recurrence": actual,
            "weighted_null_recurrence": expected,
            "observed_minus_weighted_null": actual - expected}

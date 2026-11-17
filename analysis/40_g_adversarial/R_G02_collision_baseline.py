"""R-G02: exact with-replacement collision probability, synthetic-only.

No sponsor data or BIC identities. Weights are nonnegative probabilities for
intermediary categories; k is the number of intermediary draws.
"""
from __future__ import annotations
import math


def collision_probability(weights: list[float], k: int) -> float:
    """P(at least one repeat among k iid categorical draws).

    Uses ordered-distinct dynamic programming directly: dp[j] is the\n    probability that j draws are all distinct using categories processed so far.\n    This avoids factorial overflow when k >= 171.
    This is an analytic baseline, NOT a fitted generator or validation.
    """
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    if not weights or any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError("weights must be nonempty, finite and nonnegative")
    total = math.fsum(weights)
    if total <= 0:
        raise ValueError("positive total mass required")
    if k < 2:
        return 0.0
    positive = [w / total for w in weights if w > 0]
    if k > len(positive):
        return 1.0
    dp = [0.0] * (k + 1)
    dp[0] = 1.0
    seen = 0
    for p in positive:
        seen += 1
        for j in range(min(k, seen), 0, -1):
            dp[j] += j * p * dp[j - 1]
    no_repeat = dp[k]
    return min(1.0, max(0.0, 1.0 - no_repeat))

"""Prospective R-G02 G-034 model primitives. SYNTHETIC-ONLY until frozen.

No sponsor-data loading, no entry point, no output with bank identities.
These functions are *not* a frozen validation executable and cannot establish
that any mechanism generated the sponsor data.
"""
from __future__ import annotations

from collections import Counter
from math import fsum, isfinite
from typing import Mapping, Sequence

from R_G02_collision_baseline import collision_probability

MIN_MAY_ROUTE_SUPPORT = 100
DIRICHLET_ALPHA = 1.0


def may_weights(
    position_counts: Mapping[str, int],
    universe: Sequence[str],
    *,
    alpha: float = DIRICHLET_ALPHA,
) -> dict[str, float]:
    """Fixed May-only candidate universe, *position* counts, Dirichlet smoothing."""
    keys = sorted(set(universe))
    if not keys or len(keys) != len(universe):
        raise ValueError("universe must be nonempty and contain unique categories")
    if not isfinite(alpha) or alpha <= 0:
        raise ValueError("alpha must be finite and positive")
    if any(k not in keys for k in position_counts):
        raise ValueError("counts contain categories outside May universe")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0
           for v in position_counts.values()):
        raise ValueError("position counts must be nonnegative integers")
    n = sum(position_counts.values())
    if n == 0:
        raise ValueError("no May intermediary positions: abstain")
    denom = n + alpha * len(keys)
    return {key: (position_counts.get(key, 0) + alpha) / denom
            for key in keys}


def iid_collision(weight_map: Mapping[str, float], k: int) -> float:
    """Exact within-route iid categorical collision probability."""
    return collision_probability(list(weight_map.values()), k)


def motif_recurrence_probability(
    known_motifs: set[tuple[str, ...]],
    weight_map: Mapping[str, float],
) -> float:
    """P(iid draw is in a fixed finite set of previously seen *ordered* motifs).

    The motifs are mutually exclusive events. Unseen categories have mass zero;
    they cannot be learned from July. Sum is bounded against float rounding.
    """
    mass = fsum(
        _motif_mass(t, weight_map) for t in known_motifs
    )
    return max(0.0, min(1.0, mass))


def _motif_mass(motif: tuple[str, ...], weights: Mapping[str, float]) -> float:
    p = 1.0
    for bank in motif:
        p *= weights.get(bank, 0.0)
    return p


def template_mixture(
    early_may_motifs: Sequence[tuple[str, ...]],
    late_may_motifs: Sequence[tuple[str, ...]],
    may_global_weights: Mapping[str, float],
    *,
    min_routes: int = MIN_MAY_ROUTE_SUPPORT,
) -> dict[str, float] | None:
    """M3b early-May template copying vs iid, calibrated on late May only.

    Both cohorts must consist of routes with the *same* intermediary count k.
    Returns None when May support or identifiability is inadequate.
    For July validation, callers MUST use default min_routes=100.
    """
    if isinstance(min_routes, bool) or min_routes < 1:
        raise ValueError("min_routes must be positive")
    if len(early_may_motifs) < min_routes or len(late_may_motifs) < min_routes:
        return None
    k = len(early_may_motifs[0])
    if k < 2 or any(len(t) != k for t in early_may_motifs) or any(
        len(t) != k for t in late_may_motifs
    ):
        raise ValueError("all motifs must have identical k>=2")
    if not may_global_weights:
        raise ValueError("May-only weights required")
    known = set(early_may_motifs)
    q = motif_recurrence_probability(known, may_global_weights)
    # At q=1, recurrence cannot distinguish a template draw from iid.
    if q >= 1.0 - 1e-12:
        return None
    r = sum(t in known for t in late_may_motifs) / len(late_may_motifs)
    lam = max(0.0, min(1.0, (r - q) / (1.0 - q)))
    c = sum(len(set(t)) < k for t in early_may_motifs)
    a = (c + 1.0) / (len(early_may_motifs) + 2.0)
    base = iid_collision(may_global_weights, k)
    return {
        "k": float(k),
        "lambda": lam,
        "iid_motif_mass": q,
        "late_may_motif_recurrence": r,
        "copied_template_collision": a,
        "iid_collision": base,
        "collision_probability": lam * a + (1.0 - lam) * base,
        "recurrence_probability": lam + (1.0 - lam) * q,
    }


def strict_no_replacement(k: int, universe_size: int) -> float | None:
    """M4 structural zero; None means no such sampling support."""
    if type(k) is not int or type(universe_size) is not int:
        raise ValueError("k and universe_size must be integers")
    if k < 2 or universe_size < 1:
        return None
    return 0.0 if k <= universe_size else None


def may_week_mixture(
    position_counts_by_week: Sequence[Mapping[str, int]],
    eligible_route_counts_by_week: Sequence[int],
    universe: Sequence[str],
    k: int,
    *,
    min_routes: int = MIN_MAY_ROUTE_SUPPORT,
) -> float | None:
    """M5 P(collision) from May-week ROUTE-level mixture, not pooled weights.

    Each five-block May week has a fixed May-only intermediary weight vector.
    A week with zero eligible routes contributes no mass. At least two weeks
    with >=100 eligible routes are necessary (fixed prospective support gate).
    """
    if len(position_counts_by_week) != 5 or len(eligible_route_counts_by_week) != 5:
        raise ValueError("exactly five fixed May calendar blocks required")
    if any(type(n) is not int or n < 0 for n in eligible_route_counts_by_week):
        raise ValueError("invalid route counts")
    if sum(n >= min_routes for n in eligible_route_counts_by_week) < 2:
        return None
    total = sum(eligible_route_counts_by_week)
    if total == 0:
        return None
    predictions = []
    for n, counts in zip(eligible_route_counts_by_week, position_counts_by_week):
        if n == 0:
            continue
        weights = may_weights(counts, universe)
        predictions.append((n / total) * iid_collision(weights, k))
    return fsum(predictions)


def brier(y: int, p: float) -> float:
    if y not in (0, 1) or not isfinite(p) or not 0 <= p <= 1:
        raise ValueError("invalid binary label or probability")
    return (y - p) ** 2


def unordered_motif_recurrence_probability(
    known_motifs: set[tuple[str, ...]],
    weight_map: Mapping[str, float],
) -> float:
    """Exact iid probability of matching a May-seen intermediary MULTISET.

    Deduplicate sorted tuples first: each multiset is one event. Its iid mass
    is multinomial(k; multiplicities) times the ordered tuple probability.
    This is a synthetic-only M3b placebo primitive, NOT an outcome test.
    """
    from math import factorial
    canonical = {tuple(sorted(t)) for t in known_motifs}
    total = 0.0
    for motif in canonical:
        counts = Counter(motif)
        # Calculate multinomial exactly, avoiding intermediate truncation.
        multiplicity = factorial(len(motif))
        denom = 1
        for n in counts.values():
            denom *= factorial(n)
        total += (multiplicity // denom) * _motif_mass(motif, weight_map)
    return max(0.0, min(1.0, total))


def ordered_vs_unordered_recurrence(
    known_motifs: set[tuple[str, ...]],
    observed_motifs: Sequence[tuple[str, ...]],
) -> dict[str, float] | None:
    """Separate exact-order recall from multiset recall on fixed observations."""
    if not observed_motifs:
        return None
    lengths = {len(t) for t in known_motifs | set(observed_motifs)}
    if len(lengths) != 1:
        raise ValueError("motif lengths must match within k stratum")
    ordered = sum(t in known_motifs for t in observed_motifs)
    unordered_set = {tuple(sorted(t)) for t in known_motifs}
    unordered = sum(tuple(sorted(t)) in unordered_set for t in observed_motifs)
    return {
        "ordered_recurrence": ordered / len(observed_motifs),
        "unordered_recurrence": unordered / len(observed_motifs),
        "order_sensitive_gap": (unordered - ordered) / len(observed_motifs),
    }

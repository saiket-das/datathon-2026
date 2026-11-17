"""G-041 synthetic-only dependence diagnostics for paired model comparisons.

Build connected components in the bipartite endpoint-bank graph. Every route
sharing either endpoint bank belongs to the same component, including
transitive links. This is conservative: components may be too large to support
meaningful independent-cluster inference. No sponsor-data adapter.
"""
from collections import defaultdict
from math import fsum, isfinite
import random


def bank_component_diagnostics(rows, *, seed=20261118, replicates=2000,
                               max_component_share=0.5, min_components=10):
    """Rows: (sender_bank, receiver_bank, paired_score_difference).

    A score difference is model_A_loss - model_B_loss on the SAME record.
    Bootstrap samples whole connected components, then ratio-normalizes by
    resampled record count. Refuse a CI if components are too few or giant.
    """
    if not rows:
        raise ValueError("nonempty paired cohort required")
    if replicates < 100 or not isinstance(seed, int):
        raise ValueError("replicates >=100 and integer seed required")
    if not (0 < max_component_share <= 1) or min_components < 2:
        raise ValueError("invalid independence gates")
    parent = {}

    def root(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = root(parent[x])
        return parent[x]

    def join(a, b):
        a, b = root(a), root(b)
        if a != b:
            parent[b] = a

    for a, b, d in rows:
        if not isinstance(a, str) or not a or not isinstance(b, str) or not b:
            raise ValueError("nonempty bank identifiers required")
        if not isinstance(d, (float, int)) or not isfinite(d):
            raise ValueError("finite paired differences required")
        join(("S", a), ("R", b))
    components = defaultdict(list)
    for a, b, d in rows:
        components[root(("S", a))].append(float(d))
    clusters = [(len(x), fsum(x)) for x in components.values()]
    n = len(rows)
    largest = max(c for c, _ in clusters)
    m = len(clusters)
    point = fsum(d for _, _, d in rows) / n
    supported = m >= min_components and largest / n <= max_component_share
    result = {"n": n, "components": m, "largest_share": largest/n,
              "point_difference": point, "ci_supported": supported,
              "ci_lower": None, "ci_upper": None}
    if not supported:
        return result
    rng = random.Random(seed)
    draws = []
    for _ in range(replicates):
        sample = [clusters[rng.randrange(m)] for _ in range(m)]
        draws.append(fsum(s for _, s in sample) / sum(c for c, _ in sample))
    draws.sort()
    result["ci_lower"] = draws[int(0.025 * replicates)]
    result["ci_upper"] = draws[min(replicates-1, int(0.975 * replicates))]
    return result

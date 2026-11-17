"""G-042 synthetic-only temporal common-shock falsifier; no sponsor data access.

A paired score contrast can be shared by a calendar block even when bank
identities are disjoint. This function compares fixed-cohort block summaries
with a seeded block bootstrap, abstaining when too few blocks exist.
"""
from collections import defaultdict
from math import fsum, isfinite
import random


def temporal_block_diagnostics(rows, *, seed=20261118, replicates=2000,
                               min_blocks=10, max_block_share=0.5):
    """rows: (predeclared_time_block, paired_loss_difference), same cohort.

    Resamples WHOLE blocks, ratio-normalized by payment count. Blocks are
    input-defined, not learned from outcomes. No CI if fewer than min_blocks
    or if the largest block contains more than max_block_share of records.
    """
    if not rows:
        raise ValueError("nonempty paired cohort required")
    if type(seed) is not int or type(replicates) is not int or replicates < 100:
        raise ValueError("integer seed and >=100 replicates required")
    if type(min_blocks) is not int or min_blocks < 2:
        raise ValueError("min_blocks must be integer >=2")
    if not isinstance(max_block_share, (int, float)) or not 0 < max_block_share <= 1:
        raise ValueError("invalid largest-block share")
    blocks = defaultdict(list)
    for block, difference in rows:
        if not isinstance(block, str) or not block:
            raise ValueError("nonempty prespecified time block required")
        if isinstance(difference, bool) or not isinstance(difference, (int, float)) or not isfinite(difference):
            raise ValueError("finite numeric paired loss required")
        blocks[block].append(float(difference))
    n = len(rows)
    clusters = [(len(v), fsum(v)) for v in blocks.values()]
    count = len(clusters)
    largest_share = max(k for k, _ in clusters) / n
    point = fsum(d for _, d in rows) / n
    supported = count >= min_blocks and largest_share <= max_block_share
    result = dict(n=n, blocks=count, largest_share=largest_share,
                  point_difference=point, ci_supported=supported,
                  ci_lower=None, ci_upper=None)
    if not supported:
        return result
    rng = random.Random(seed)
    draws = []
    for _ in range(replicates):
        sample = [clusters[rng.randrange(count)] for _ in range(count)]
        draws.append(fsum(s for _, s in sample) / sum(k for k, _ in sample))
    draws.sort()
    result["ci_lower"] = draws[int(0.025 * replicates)]
    result["ci_upper"] = draws[min(replicates - 1, int(0.975 * replicates))]
    return result

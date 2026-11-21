"""G-044: synthetic-only sparse crossed bank/time support audit.

This is a topology/identifiability diagnostic, not a variance estimator.
No sponsor data loading, inferential p values, or hidden holdout access.
"""
from collections import defaultdict
from math import isfinite


def crossed_support(rows, min_banks=10, min_times=10, max_share=0.5):
    """Rows are (bank_component, time_block, paired_loss_difference).

    Duplicate bank/time cells are allowed and counted as repeated observations.
    The bipartite incidence graph joins banks to observed time blocks.
    """
    if isinstance(min_banks, bool) or isinstance(min_times, bool) or min_banks < 2 or min_times < 2:
        raise ValueError("minimum cluster counts must be integers >=2")
    if not isinstance(min_banks, int) or not isinstance(min_times, int):
        raise ValueError("minimum cluster counts must be integers")
    if isinstance(max_share, bool) or not isinstance(max_share, (int, float)) or not 0 < max_share <= 1:
        raise ValueError("invalid max_share")
    if not rows:
        raise ValueError("empty observations")
    parent = {}
    weights = defaultdict(int)
    cells = defaultdict(list)
    bank_weights = defaultdict(int)
    time_weights = defaultdict(int)

    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for bank, time, value in rows:
        if not isinstance(bank, str) or not bank or not isinstance(time, str) or not time:
            raise ValueError("bank/time labels must be nonempty strings")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError("nonfinite or invalid paired loss")
        a, b = ("bank", bank), ("time", time)
        union(a, b)
        weights[a] += 1
        bank_weights[bank] += 1
        time_weights[time] += 1
        cells[(bank, time)].append(float(value))
    n = len(rows)
    component_counts = defaultdict(int)
    for bank, time, _ in rows:
        component_counts[find(("bank", bank))] += 1
    components = len(component_counts)
    max_component_share = max(component_counts.values()) / n
    cell_coverage = len(cells) / (len(bank_weights) * len(time_weights))
    # Two-way clustering needs both dimensions; incidence connectivity
    # is a diagnostic only, not a proof of lack of independent shocks.
    eligible = (len(bank_weights) >= min_banks and len(time_weights) >= min_times
                and max(bank_weights.values()) / n <= max_share
                and max(time_weights.values()) / n <= max_share)
    return {
        "observations": n, "banks": len(bank_weights), "times": len(time_weights),
        "observed_cells": len(cells), "possible_cells": len(bank_weights) * len(time_weights),
        "cell_coverage": cell_coverage, "incidence_components": components,
        "largest_incidence_component_share": max_component_share,
        "largest_bank_share": max(bank_weights.values()) / n,
        "largest_time_share": max(time_weights.values()) / n,
        "one_way_support_gates_pass": eligible,
        "joint_ci": None, "joint_ci_status": "NOT_IMPLEMENTED",
    }

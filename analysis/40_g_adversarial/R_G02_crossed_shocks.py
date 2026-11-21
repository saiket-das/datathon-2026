"""G-043 synthetic-only crossed bank/time dependence falsifier.

A balanced bank-component by time-block grid can contain two distinct common
shocks. These diagnostics are descriptive, not a confidence interval.
No sponsor-data reader, model fitting, or validation interface.
"""
from collections import defaultdict
from math import fsum, isfinite


def crossed_shock_diagnostics(rows):
    """Rows (bank_component, time_block, paired_loss_difference).

    Require a complete one-observation-per-cell rectangular grid so that
    bank, time, and interaction components are algebraically identifiable.
    Reject unbalanced grids rather than impute or silently pool records.
    Return centered ANOVA sums of squares and descriptive mean-square
    contributions. They are NOT independent-effect variance estimates.
    """
    if not rows:
        raise ValueError("nonempty grid required")
    cells = {}
    banks, times = set(), set()
    for bank, time, difference in rows:
        if not isinstance(bank, str) or not bank or not isinstance(time, str) or not time:
            raise ValueError("nonempty bank and time keys required")
        if isinstance(difference, bool) or not isinstance(difference, (int, float)) or not isfinite(difference):
            raise ValueError("finite numeric difference required")
        key = (bank, time)
        if key in cells:
            raise ValueError("duplicate bank/time cell")
        cells[key] = float(difference)
        banks.add(bank)
        times.add(time)
    b, t = len(banks), len(times)
    if b < 2 or t < 2 or len(cells) != b*t:
        raise ValueError("complete >=2 by >=2 crossed grid required")
    grand = fsum(cells.values()) / (b*t)
    bank_mean = {bank: fsum(cells[bank, time] for time in times)/t for bank in banks}
    time_mean = {time: fsum(cells[bank, time] for bank in banks)/b for time in times}
    ss_bank = t*fsum((x-grand)**2 for x in bank_mean.values())
    ss_time = b*fsum((x-grand)**2 for x in time_mean.values())
    ss_interaction = fsum((v-bank_mean[bank]-time_mean[time]+grand)**2
                          for (bank,time),v in cells.items())
    ss_total = fsum((v-grand)**2 for v in cells.values())
    return dict(banks=b, blocks=t, n=b*t, point_difference=grand,
                ss_bank=ss_bank, ss_time=ss_time,
                ss_interaction=ss_interaction, ss_total=ss_total,
                additive_residual_max=max(abs(v-bank_mean[bank]-time_mean[time]+grand)
                                          for (bank,time),v in cells.items()))

"""Test a bounded near-uniform directional gap on selected Direct corridors.

Run: uv run python analysis/20_routing_time/H-B18_bounded_directional_gap.py --phase explore
Frozen internal check: --phase confirm --freeze <SHA>.
"""

import sys
import duckdb
import numpy as np

from duration_reversals import estimate_reversals, load_reversals
from routing_common import OUT, arguments, cluster_draws, interval, report, table

STEM = "H-B18_bounded_directional_gap"
EDGES = np.array([20, 120, 240, 360, 480, 600])
COHORT = "short_center<100 AND abs(gap)>20"


def model_masses() -> tuple[np.ndarray, np.ndarray]:
    """Mass bins for a single uniform and the absolute difference of two uniforms."""
    single = (EDGES - 20) / 580
    difference = 1 - (1 - EDGES / 600) ** 2
    difference = (difference - difference[0]) / (1 - difference[0])
    return np.diff(single, append=1), np.diff(difference, append=1)


def controls(con: duckdb.DuckDBPyConnection, label: str) -> tuple:
    """Measure eligibility and gap shape for the selected conditional cohort."""
    return con.execute(f"""
      SELECT ?,count(*) eligible_pairs,sum(payments) payments,count(DISTINCT a) clusters,
        quantile_cont(abs(gap),[.1,.5,.9,.99]) gap_seconds,
        avg((abs(gap)>620)::INT) over620,
        count_if(drift IS NOT NULL) split_reference_pairs,
        quantile_cont(abs(drift),[.5,.9,.99]) split_reference_seconds
      FROM reversals WHERE {COHORT} HAVING count(*)>=100 AND clusters>=100
    """, [label]).fetchall()


def main() -> None:
    """Evaluate the fixed conditional distributions and report competing shapes."""
    opts = arguments(STEM)
    with duckdb.connect(config={"memory_limit": "768MB", "threads": 1, "temp_directory": ""}) as con:
        load_reversals(con, opts.phase, opts.freeze)
        estimate_reversals(con)
        coverage = table(con, f"""
          SELECT (SELECT count(*) FROM direct) all_direct,count(*) supported_pairs,
            sum(payments) supported_payments,count_if(short_center<100) short_pairs,
            count_if({COHORT}) eligible_pairs,
            count_if({COHORT})::DOUBLE/count(*) eligible_pair_share
          FROM reversals
        """)
        cutpoints = list(zip(EDGES[:-1], EDGES[1:]))
        columns = ",".join(f"count_if(abs(gap)>{lo} AND abs(gap)<={hi})" for lo, hi in cutpoints)
        stats = np.asarray(con.execute(f"""
          SELECT {columns},count_if(abs(gap)>600),count_if(abs(gap)>620)
          FROM reversals WHERE {COHORT} GROUP BY a ORDER BY a
        """).fetchall(), dtype=float)
        control_rows = controls(con, "Primary")
        estimate_reversals(con, agreements_only=True)
        control_rows.extend(controls(con, "Declared endpoints agree"))
    totals = stats.sum(axis=0)
    n = totals[:-1].sum()
    tables = {"Cohort coverage": coverage}
    passed = False
    if n >= 100 and len(stats) >= 100:
        observed = totals[:-1] / n
        boot = cluster_draws(stats)
        boot_n = boot[:, :-1].sum(axis=1)
        boot_shares = boot[:, :-1] / boot_n[:, None]
        uniform, triangular = model_masses()
        uniform_error = np.abs(boot_shares - uniform).sum(axis=1) / 2
        triangle_error = np.abs(boot_shares - triangular).sum(axis=1) / 2
        gain = interval(triangle_error - uniform_error)
        tv_up = interval(uniform_error)[1]
        tail_up = interval(boot[:, -1] / boot_n)[1]
        passed = n >= 150 and tv_up <= .15 and gain[0] >= .02 and tail_up <= .025
        tables["Fixed comparison with first-bank resampling"] = (
            ["n", "banks", "uniform_TV", "uniform_TV_upper99", "triangular_TV", "TV_gain_lower99",
             "TV_gain_upper99", "share_above620_upper99"],
            [(int(n), len(stats), abs(observed - uniform).sum()/2, tv_up,
              abs(observed - triangular).sum()/2, *gain, tail_up)],
        )
        tables["Gap histogram"] = (["interval_seconds", "count", "observed", "uniform", "triangular"], [
            (label, int(count) if count == 0 or count >= 100 else "<100",
             o if count == 0 or count >= 100 else "suppressed", u, t)
            for label, count, o, u, t in zip(
                ["(20,120]", "(120,240]", "(240,360]", "(360,480]", "(480,600]", ">600"],
                totals[:-1], observed, uniform, triangular)
        ])
    tables["Endpoint and split-period controls"] = (
        ["group", "eligible_pairs", "payments", "canonical_first_banks", "gap_p10_p50_p90_p99",
         "above620_share", "split_reference_pairs", "absolute_drift_p50_p90_p99"],
        [(row[:6] + ("<100", "suppressed") if 0 < row[6] < 100 else row) for row in control_rows],
    )
    tables["Frozen decision"] = (["pass"], [(passed,)])
    report(STEM, opts.phase, opts.freeze, tables)
    out = OUT / f"{STEM}_{opts.phase}.md"
    content = out.read_text(encoding="utf-8").replace("2GB; two threads", "768MB; one thread")
    content = content.replace("ordering-bank cluster", "canonical first-visible-bank cluster")
    out.write_text(content, encoding="utf-8")
    print(f"{opts.phase} B18 {'PASS' if passed else 'FAIL'}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        sys.exit(1)

"""Falsify a single directional bank score using Direct corridor triangles.

Run: uv run python analysis/20_routing_time/H-B17_directional_triangle.py --phase explore
Frozen internal check: --phase confirm --freeze <SHA>.
"""

import sys
import duckdb

from duration_reversals import estimate_reversals, load_reversals
from routing_common import OUT, arguments, report, table

STEM = "H-B17_directional_triangle"


def triangles(con: duckdb.DuckDBPyConnection, label: str) -> tuple[tuple, tuple]:
    """Return closure deviations and sensitivity to deleting any one bank."""
    con.execute("""
      CREATE OR REPLACE TEMP TABLE triangles AS
      SELECT x.a,x.b,y.b c,abs(x.gap+y.gap-z.gap) residual,
        abs(x.drift+y.drift-z.drift) temporal_reference
      FROM reversals x JOIN reversals y ON x.b=y.a
      JOIN reversals z ON z.a=x.a AND z.b=y.b
    """)
    columns, rows = table(con, """
      SELECT count(*) triangles,count_if(residual>100) breaks,
        avg((residual>100)::INT) break_fraction,quantile_cont(residual,[.5,.9,.99]) residual_s,
        count(temporal_reference) reference_triangles,
        count_if(temporal_reference>100) reference_breaks,
        quantile_cont(temporal_reference,[.5,.9,.99]) reference_s FROM triangles
    """)
    columns2, rows2 = table(con, """
      WITH total AS (SELECT count(*) n,count_if(residual>100) breaks FROM triangles),
      contributions AS (
        SELECT bank,count(*) n,count_if(residual>100) breaks
        FROM triangles,unnest([a,b,c]) t(bank) GROUP BY bank
      )
      SELECT count(*) banks,
        min((total.breaks-c.breaks)::DOUBLE/nullif(total.n-c.n,0)) low,
        max((total.breaks-c.breaks)::DOUBLE/nullif(total.n-c.n,0)) high,
        max(c.n)::DOUBLE/any_value(total.n) largest_triangle_share
      FROM contributions c CROSS JOIN total
    """)
    cols = ["group", *columns]
    results = list(rows[0])
    for i in (1, 4, 5):
        if 0 < results[i] < 100:
            results[i] = "<100"
    if results[4] == "<100":
        results[6] = "suppressed"
    return (cols, [(label, *results)]), (["group", *columns2], [(label, *rows2[0])])


def main() -> None:
    """Evaluate frozen algebraic contrast and its composition sensitivity."""
    opts = arguments(STEM)
    with duckdb.connect(config={"memory_limit": "768MB", "threads": 1, "temp_directory": ""}) as con:
        load_reversals(con, opts.phase, opts.freeze)
        estimate_reversals(con)
        coverage = table(con, """SELECT (SELECT count(*) FROM direct) all_direct,
          count(*) supported_bidirectional_pairs,sum(payments) supported_payments FROM reversals""")
        primary, influence = triangles(con, "All supported triangles")
        _, banks, low, _, _ = influence[1][0]
        n = primary[1][0][1]
        passed = n >= 500 and banks >= 100 and low >= .20
        estimate_reversals(con, agreements_only=True)
        control, control_influence = triangles(con, "Declared endpoints agree")
        primary[1].extend(control[1])
        influence[1].extend(control_influence[1])
    report(STEM, opts.phase, opts.freeze, {
        "Coverage before forming triangles": coverage,
        "Cycle sum and split-period reference": primary,
        "Leave out each bank across all triangle positions": influence,
        "Frozen criteria for rejecting the bank-score model": (["passes"], [(passed,)]),
    })
    out = OUT / f"{STEM}_{opts.phase}.md"
    content = out.read_text(encoding="utf-8").replace("2GB; two threads", "768MB; one thread")
    content = content.replace(
        "Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.",
        "Bank deletion ranges quantify concentration. Triangles share edges, banks, dates and payment entities.",
    )
    out.write_text(content, encoding="utf-8")
    print(f"{opts.phase} B17 {'PASS' if passed else 'FAIL'} for rejection criteria.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        sys.exit(1)

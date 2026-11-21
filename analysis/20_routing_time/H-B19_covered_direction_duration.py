"""Test whether multibank route labels locate the slower direction of Direct corridors.

Run: uv run python analysis/20_routing_time/H-B19_covered_direction_duration.py --phase explore
Frozen internal check: --phase confirm --freeze <SHA>.
"""

import sys
import duckdb
import numpy as np

from duration_reversals import estimate_reversals, load_reversals
from routing_common import OUT, arguments, cluster_draws, interval, report, table

STEM = "H-B19_covered_direction_duration"


def score(con: duckdb.DuckDBPyConnection) -> None:
    """Join Direct medians to separate May–June multibank labels."""
    con.execute("""
      CREATE OR REPLACE TEMP TABLE scored AS
      SELECT d.*,f.cover::INT+r.cover::INT classes,
        CASE WHEN f.cover THEN gap ELSE -gap END covered_minus_indirect
      FROM reversals d JOIN labels f ON d.a=f.a AND d.b=f.b
      JOIN labels r ON d.a=r.b AND d.b=r.a
      WHERE short_center<100
    """)


def summary(con: duckdb.DuckDBPyConnection) -> tuple:
    """Keep aggregate results only for supported label combinations."""
    return table(con, """
      SELECT classes covered_directions,count(*) n,count(DISTINCT a) banks,sum(payments) payments,
        avg((abs(gap)>20)::INT) large_gap_share,
        avg((covered_minus_indirect>20)::INT) FILTER(WHERE classes=1) covered_slower_share,
        quantile_cont(abs(gap),[.5,.9,.99]) absolute_gap_seconds
      FROM scored GROUP BY 1 HAVING n>=100 AND banks>=100 ORDER BY 1
    """)


def main() -> None:
    """Measure whether early multibank labels account for later Direct timing gaps."""
    opts = arguments(STEM)
    with duckdb.connect(config={"memory_limit": "768MB", "threads": 1, "temp_directory": ""}) as con:
        load_reversals(con, opts.phase, opts.freeze)
        estimate_reversals(con)
        con.execute("""
          CREATE TEMP TABLE labels AS
          WITH multibank AS (
            SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
              transaction_type_code='Covered' covered
            FROM read_parquet('dataset/payments.parquet')
            WHERE anomaly_type IS NULL AND participant_count BETWEEN 3 AND 5
              AND ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-07-01'
              AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
          )
          SELECT p[1] a,p[-1] b,min(covered) cover FROM multibank
          GROUP BY 1,2 HAVING min(covered)=max(covered)
        """)
        score(con)
        coverage = table(con, """
          SELECT (SELECT count(*) FROM direct) all_direct,
            (SELECT count(*) FROM reversals) supported_pairs,
            (SELECT count_if(short_center<100) FROM reversals) short_pairs,
            count(*) both_labels_known,count_if(classes=1) one_covered,
            count_if(classes=0) both_indirect FROM scored
        """)
        primary = summary(con)
        stats = np.asarray(con.execute("""
          SELECT count_if(classes=1),count_if(classes=1 AND covered_minus_indirect>20),
            count_if(classes=0),count_if(classes=0 AND abs(gap)>20),
            count_if(classes=1 AND abs(gap)>20),
            count_if(classes=1 AND covered_minus_indirect < -20)
          FROM scored WHERE classes IN (0,1) GROUP BY a ORDER BY a
        """).fetchall(), dtype=float).reshape(-1, 6)
        estimate_reversals(con, agreements_only=True)
        score(con)
        agreement = summary(con)
    tables = {"Eligibility": coverage, "Primary contrast": primary, "Declared endpoints agree": agreement}
    one, wins, neither, false_gaps, large, opposite = stats.sum(axis=0)
    passed = False
    if min(one, neither, len(stats)) >= 100:
        draws = cluster_draws(stats)
        covered_lo, _ = interval(draws[:, 1] / draws[:, 0])
        _, indirect_hi = interval(draws[:, 3] / draws[:, 2])
        passed = covered_lo >= .85 and indirect_hi <= .02
        tables["Primary practical gates and sign exceptions"] = (
            ["canonical_first_banks", "one_covered_slower_fraction", "one_covered_lower99",
             "both_indirect_large_gap_fraction", "both_indirect_upper99",
             "one_covered_large_gaps", "large_gap_points_toward_indirect"],
            [(len(stats), wins/one, covered_lo, false_gaps/neither, indirect_hi,
              int(large), "<100" if 0<opposite<100 else int(opposite))],
        )
    tables["Frozen decision"] = (["pass"], [(passed,)])
    report(STEM, opts.phase, opts.freeze, tables)
    out = OUT / f"{STEM}_{opts.phase}.md"
    content = out.read_text(encoding="utf-8").replace("2GB; two threads", "768MB; one thread")
    out.write_text(content.replace("ordering-bank cluster", "canonical first-visible-bank cluster"), encoding="utf-8")
    print(f"{opts.phase} B19 {'PASS' if passed else 'FAIL'}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        sys.exit(1)

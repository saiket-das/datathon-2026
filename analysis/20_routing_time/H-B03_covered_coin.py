"""Falsify an independent 10% Covered-label coin using exploration bank concentration.

Run from the repository root:
  uv run python analysis/20_routing_time/H-B03_covered_coin.py
Exploration only, no confirmation. Reads dataset/payments.parquet; exports safe aggregates.
"""

import sys

from routing_common import connect, report, selected, table

STEM = "H-B03_covered_coin"


def main() -> int:
    """Count extreme ordering-bank Covered shares against the candidate binomial law."""
    con = None
    try:
        con = connect()
        selected(con, "explore")
        tables = {"Banks with >=100 unlabelled multibank payments": table(con, """
          WITH b AS (SELECT ob,count(*) n,count(*) FILTER(WHERE route='Covered') c
            FROM sample WHERE NOT labelled AND v>2 GROUP BY ob HAVING count(*)>=100)
          SELECT count(*) banks,sum(n) rows,
            sum((c=0)::INT) banks_with_no_covered,
            sum((c=n)::INT) banks_with_only_covered,
            sum(pow(.9,n)) expected_no_covered_under_coin,
            sum(pow(.1,n)) expected_only_covered_under_coin,
            quantile_cont(c::DOUBLE/n,[.1,.5,.9]) bank_share_quantiles,
            sum(c)::DOUBLE/sum(n) row_weighted_covered_share FROM b
        """)}
        tables["Within-bank versus independent-coin variance"] = table(con, """
          WITH b AS (SELECT ob,count(*) n,count(*) FILTER(WHERE route='Covered') c
            FROM sample WHERE NOT labelled AND v>2 GROUP BY ob HAVING count(*)>=100)
          SELECT count(*) banks,avg((c::DOUBLE/n-.1)^2) mean_squared_share_deviation,
            avg(.1*.9/n) expected_under_independent_coin FROM b
        """)
        report(STEM, "explore", None, tables)
        print("Exploration-only Covered coin falsification aggregates written.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        return 1
    finally:
        if con is not None:
            con.close()


if __name__ == "__main__":
    sys.exit(main())

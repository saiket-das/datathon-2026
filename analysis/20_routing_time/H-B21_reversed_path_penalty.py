"""Compare reversed three-bank gaps with endpoint and adjacent Direct gaps.

Run: uv run python analysis/20_routing_time/H-B21_reversed_path_penalty.py --phase explore
Exploratory support screen only.
"""
from datetime import datetime, timezone
import sys

import duckdb
from routing_common import OUT, arguments, report, table

STEM = "H-B21_reversed_path_penalty"


def prepare(con: duckdb.DuckDBPyConnection, phase: str) -> None:
    """Estimate matched visible-path medians from separate direct and multibank rows."""
    start,end = (("2023-05-01","2023-07-01") if phase=="explore"
                 else ("2023-07-01","2023-08-01"))
    con.execute("""
      CREATE TEMP TABLE path_centers AS
      WITH payments AS (
        SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
          total_duration d,transaction_type_code route
        FROM read_parquet('dataset/payments.parquet')
        WHERE anomaly_type IS NULL AND participant_count IN (2,3) AND gap_count=0
          AND ts_utc>=?::TIMESTAMP AND ts_utc<?::TIMESTAMP
          AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
          AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
      )
      SELECT p[1] a,p[-1] b,CASE WHEN len(p)=3 THEN p[2] END middle,
        count(*) n,median(d) center,min(route) route
      FROM payments
      WHERE p[1]<>p[-1] AND (len(p)=2 OR (p[2]<>p[1] AND p[2]<>p[-1]))
      GROUP BY 1,2,3 HAVING n>=CASE WHEN middle IS NULL THEN 10 ELSE 3 END
        AND min(route)=max(route)
    """,[start,end])
    con.execute("""
      CREATE TEMP TABLE gaps AS
      SELECT f.a,f.b,f.middle,f.n+r.n payments,f.center-r.center gap,
        least(f.center,r.center) short_center,
        CASE WHEN f.route='Covered' AND r.route='Indirect' THEN 1
             WHEN r.route='Covered' AND f.route='Indirect' THEN -1
             WHEN f.route='Indirect' AND r.route='Indirect' THEN 0 END orient
      FROM path_centers f JOIN path_centers r ON f.a=r.b AND f.b=r.a
        AND f.middle IS NOT DISTINCT FROM r.middle WHERE f.a<f.b
    """)
    con.execute("""
      CREATE TEMP TABLE scored AS
      WITH matched AS (
        SELECT p.a,p.b,p.middle,p.payments,p.gap,p.orient,outer_edge.gap endpoint_gap,
          CASE WHEN p.a<p.middle THEN first_edge.gap ELSE -first_edge.gap END
          + CASE WHEN p.middle<p.b THEN last_edge.gap ELSE -last_edge.gap END adjacent_gap
        FROM gaps p
        JOIN gaps outer_edge ON p.a=outer_edge.a AND p.b=outer_edge.b AND outer_edge.middle IS NULL
        JOIN gaps first_edge ON first_edge.a=least(p.a,p.middle)
          AND first_edge.b=greatest(p.a,p.middle) AND first_edge.middle IS NULL
        JOIN gaps last_edge ON last_edge.a=least(p.b,p.middle)
          AND last_edge.b=greatest(p.b,p.middle) AND last_edge.middle IS NULL
        WHERE p.middle IS NOT NULL AND outer_edge.short_center<100
      )
      SELECT *,abs(gap-endpoint_gap) endpoint_error,abs(gap-adjacent_gap) adjacent_error,
        abs(gap-endpoint_gap-adjacent_gap) combined_error,abs(gap) symmetric_error
      FROM matched
    """)


def main() -> None:
    """Export only broad matched-path support and mechanism comparisons."""
    opts = arguments(STEM)
    if opts.phase!="explore":
        raise ValueError("B21 is exploration only")
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        prepare(con,opts.phase)
        coverage=table(con,"""
          SELECT (SELECT CASE WHEN count(*) BETWEEN 1 AND 99 THEN '<100' ELSE count(*)::VARCHAR END
                      FROM gaps WHERE middle IS NOT NULL) reversed_paths,
            (SELECT CASE WHEN count(*) BETWEEN 1 AND 99 THEN 'suppressed' ELSE sum(payments)::VARCHAR END
                      FROM gaps WHERE middle IS NOT NULL) reversed_payments,
            count(*) scored_paths,sum(payments) scored_payments,
            count(DISTINCT (a,b)) endpoints,count(DISTINCT middle) middle_banks
          FROM scored
        """)
        contrasts=table(con,"""
          WITH categorized AS (
            SELECT *,CASE WHEN abs(orient)=1 THEN 'One Covered'
                           WHEN orient=0 THEN 'Both Indirect' ELSE 'Other' END category
            FROM scored
          )
          SELECT CASE WHEN grouping(category)=1 THEN 'All' ELSE category END cohort,
            count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            count(DISTINCT (a,b)) endpoint_pairs,avg(endpoint_error) endpoint_mae,
            avg(adjacent_error) adjacent_mae,avg(combined_error) combined_mae,
            avg(symmetric_error) symmetric_mae,
            avg((endpoint_error<=20)::INT) endpoint_within20,
            avg((adjacent_error<=20)::INT) adjacent_within20,
            avg((gap*orient>20)::INT) FILTER(WHERE abs(orient)=1) covered_slower_share
          FROM categorized GROUP BY GROUPING SETS((),(category)) ORDER BY 1
        """)
        endpoint_equal=table(con,"""
          SELECT count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            avg(ee) endpoint_mae,avg(ae) adjacent_mae,avg(ce) combined_mae,avg(se) symmetric_mae
          FROM (
            SELECT a,b,avg(endpoint_error) ee,avg(adjacent_error) ae,
              avg(combined_error) ce,avg(symmetric_error) se
            FROM scored GROUP BY 1,2
          )
        """)
    report(STEM,opts.phase,opts.freeze,{"Eligibility":coverage,"Matched paths":contrasts,
          "Equal endpoint-pair weighting":endpoint_equal})
    result=OUT/f"{STEM}_{opts.phase}.md"
    result.write_text(result.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread"),
                      encoding="utf-8")
    print(f"OK: B21 {opts.phase} aggregate report.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

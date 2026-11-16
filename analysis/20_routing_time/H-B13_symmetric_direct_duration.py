"""Falsify a symmetric Direct-path duration center using May–June exploration.

From the repository root:
    uv run python analysis/20_routing_time/H-B13_symmetric_direct_duration.py
"""

from datetime import datetime, timezone
import sys

import duckdb
import numpy as np

from routing_common import OUT, cluster_draws, interval, report, table

STEM = "H-B13_symmetric_direct_duration"


def main() -> None:
    """Compare known bidirectional paths without exporting either bank name."""
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    tables = {}
    with duckdb.connect(config={"memory_limit": "768MB", "threads": 1, "temp_directory": ""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        con.execute("""
          CREATE TEMP TABLE paths AS
          WITH source AS (
            SELECT list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...') p,
              ORDERING_BIC8 ob,BENEFICIARY_BIC8 bb,month(ts_utc) mon,
              total_duration d,currency_code currency,currency_conversion_count fx
            FROM read_parquet('dataset/payments.parquet')
            WHERE ANOMALY_TYPE IS NULL AND participant_count=2 AND ts_utc>=TIMESTAMP '2023-05-01'
              AND ts_utc<TIMESTAMP '2023-07-01'
              AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
          )
          SELECT p[1] a,p[2] b,mon,d,currency,fx,ob=p[1] AND bb=p[2] AS agrees FROM source
        """)
        n_paths = con.execute("SELECT count(*) FROM paths").fetchone()[0]
        tables["Unlabelled two-visible-bank exploration population"] = (["payments"], [(n_paths,)])
        summary, intervals = [], []
        for label, control, group in (
            ("All directed visible pairs", "true", "''"),
            ("Endpoints agree with declared fields", "agrees", "''"),
            ("Matched currency and FX count", "true", "currency||':'||fx"),
        ):
            con.execute(f"""
              CREATE OR REPLACE TEMP TABLE directions AS
              SELECT a,b,{group} g,count(*) n,avg(d) mu FROM paths
              WHERE {control} GROUP BY 1,2,3 HAVING n>=25;
              CREATE OR REPLACE TEMP TABLE reversals AS
              SELECT x.a,x.b,x.n+y.n n,abs(x.mu-y.mu) delta,
                least(x.mu,y.mu)<100 AND greatest(x.mu,y.mu)>=100 opposite_thresholds
              FROM directions x JOIN directions y ON x.a=y.b AND x.b=y.a AND x.g=y.g
              WHERE x.a<x.b
            """)
            rows = con.execute("""
              SELECT count(*) cells,count(DISTINCT (a,b)) corridors,sum(n) payments,
                avg((delta>100)::INT),avg(opposite_thresholds::INT),
                quantile_cont(delta,[.5,.75,.9,.99])
              FROM reversals HAVING count(*)>=100
            """).fetchall()
            if rows:
                summary.append((label, *rows[0]))
            clusters = np.asarray(con.execute("""
              SELECT count(*),count_if(delta>100) FROM reversals GROUP BY a ORDER BY a
            """).fetchall(), dtype=float)
            if len(clusters) >= 100:
                draws = cluster_draws(clusters)
                intervals.append((label, len(clusters), *interval(draws[:, 1] / draws[:, 0])))
        tables["Directional mean gaps on matched Direct corridors"] = (
            ["group", "cells", "corridors", "payments", "share_gap_over_100s",
             "share_means_straddle_100s", "p50/p75/p90/p99 gap seconds"], summary)
        tables["99% sensitivity interval for directional gaps above 100 seconds"] = (
            ["group", "canonical first bank clusters", "low", "high"], intervals)
        tables["Same directed path, May versus June placebo"] = table(con, """
          WITH m AS (SELECT a,b,mon,count(*) n,avg(d) mu FROM paths
            GROUP BY 1,2,3 HAVING n>=25)
          SELECT count(*) directed_paths,sum(x.n+y.n) payments,count(DISTINCT a) banks,
            avg((abs(x.mu-y.mu)>100)::INT) share_gap_over_100s,
            quantile_cont(abs(x.mu-y.mu),[.5,.75,.9,.99]) gap_seconds
          FROM m x JOIN m y USING(a,b) WHERE x.mon=5 AND y.mon=6
          HAVING count(*)>=100 AND banks>=100
        """)
    report(STEM, "explore", None, tables)
    out = OUT / f"{STEM}_explore.md"
    metadata = out.read_text(encoding="utf-8").replace("2GB; two threads", "768MB; one thread")
    metadata = metadata.replace("ordering-bank cluster", "canonical first-bank cluster")
    out.write_text(metadata, encoding="utf-8")
    print("B13 exploration aggregates saved.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        sys.exit(1)

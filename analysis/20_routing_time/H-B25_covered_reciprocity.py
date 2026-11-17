"""Screen whether reciprocal Covered states co-occur more than origin rates predict.

Run: uv run python analysis/20_routing_time/H-B25_covered_reciprocity.py
Only May training and June exploration are opened.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import duckdb
import numpy as np

from routing_common import OUT, cluster_draws, interval, report, table

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("b20",HERE/"H-B20_unseen_corridor_propensities.py")
b20=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b20)
STEM=Path(__file__).stem


def main() -> None:
    """Compare reciprocal label counts to calibrated independent directions."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        b20.load(con,"explore")
        con.execute("""
          CREATE TEMP TABLE reciprocal AS
          WITH training AS (
            SELECT a,b,class FROM pairs WHERE train AND pure
          ), totals AS (
            SELECT a,count(*) n,sum(class) covered FROM training GROUP BY a
          ), fit AS (
            SELECT avg(class) global_p FROM training
          ), observed AS (
            SELECT x.a,x.b,x.class ca,y.class cb,x.payments+y.payments payments
            FROM pairs x JOIN pairs y ON x.a=y.b AND x.b=y.a AND x.a<x.b
            WHERE NOT x.train AND NOT y.train AND x.pure AND y.pure
              AND x.payments>=2 AND y.payments>=2
          )
          SELECT o.*,
            (x.covered-coalesce(f.class,0)+10*global_p)
              /(x.n-(f.class IS NOT NULL)::INT+10) pa,
            (y.covered-coalesce(r.class,0)+10*global_p)
              /(y.n-(r.class IS NOT NULL)::INT+10) pb
          FROM observed o JOIN totals x ON o.a=x.a JOIN totals y ON o.b=y.a
          LEFT JOIN training f ON o.a=f.a AND o.b=f.b
          LEFT JOIN training r ON o.a=r.b AND o.b=r.a CROSS JOIN fit
          WHERE x.n-(f.class IS NOT NULL)::INT>=25 AND y.n-(r.class IS NOT NULL)::INT>=25
        """)
        label_share=con.execute("SELECT avg((ca+cb)/2.0) FROM reciprocal").fetchone()[0]
        # Pooled intercept calibration makes this a same-month diagnostic.
        low,high=.001,1000.0
        for _ in range(30):
            mult=(low+high)/2
            estimated=con.execute("""
              SELECT avg((pa*?/(1-pa+pa*?)+pb*?/(1-pb+pb*?))/2) FROM reciprocal
            """,[mult]*4).fetchone()[0]
            if estimated<label_share:
                low=mult
            else:
                high=mult
        mult=(low+high)/2
        con.execute("""
          CREATE TEMP VIEW comparison AS
          WITH calibrated AS (
            SELECT *,pa*?/(1-pa+pa*?) qa,pb*?/(1-pb+pb*?) qb FROM reciprocal
          )
          SELECT *,ca*cb observed,qa*qb prediction,pa*pb raw_prediction,
            (ca-qa)*(cb-qb) centered_product FROM calibrated
        """.replace("?",str(mult)))
        results=table(con,f"""
          SELECT count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            sum(payments) payments,{label_share} direction_label_share,
            avg((ca+cb=1)::INT) one_covered_share,
            avg(observed) both_covered_share,
            avg(prediction) independent_calibrated,avg(raw_prediction) independent_raw,
            {label_share**2} independent_equal_rate,
            avg(centered_product) residual_product
          FROM comparison
        """)
        bounds=[]
        for role,key in (("Canonical first bank","a"),("Canonical second bank","b")):
            stats=np.asarray(con.execute(f"""
              SELECT count(*),sum(observed-prediction),sum(centered_product)
              FROM comparison GROUP BY {key} ORDER BY {key}
            """).fetchall(),dtype=float)
            if len(stats)>=100:
                draws=cluster_draws(stats)
                bounds.append((role,len(stats),*interval(draws[:,1]/draws[:,0]),
                               *interval(draws[:,2]/draws[:,0])))
    report(STEM,"explore",None,{"Reciprocal outcomes and origin-only alternatives":results,
       "Separate bank sensitivity":[
         ["cluster_role","clusters","both_covered_gap_low99","both_covered_gap_high99",
          "residual_product_low99","residual_product_high99"],bounds]})
    result=OUT/f"{STEM}_explore.md"
    result.write_text(result.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread")
      .replace("99% ordering-bank","99% separate bank-role"),encoding="utf-8")
    print("OK: B25 exploratory aggregate report.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

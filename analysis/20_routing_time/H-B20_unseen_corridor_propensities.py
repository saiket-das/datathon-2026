"""Test whether endpoint propensities explain Covered states on unseen corridors.

Run: uv run python analysis/20_routing_time/H-B20_unseen_corridor_propensities.py --phase explore
After committing the plan, use --phase confirm --freeze SHA for the July internal test.
"""
from datetime import datetime, timezone
import sys

import duckdb
import numpy as np

from routing_common import OUT, arguments, cluster_draws, interval, report, table

STEM = "H-B20_unseen_corridor_propensities"


def load(con: duckdb.DuckDBPyConnection, phase: str) -> None:
    """Summarise directed visible bank pairs with May and score-period support."""
    score_start, score_end = (("2023-06-01", "2023-07-01") if phase == "explore"
                              else ("2023-07-01", "2023-08-01"))
    con.execute("""
      CREATE TEMP TABLE pairs AS
      WITH visible AS (
        SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
          ts_utc<'2023-06-01'::TIMESTAMP train,
          transaction_type_code='Covered' covered
        FROM read_parquet('dataset/payments.parquet')
        WHERE anomaly_type IS NULL AND participant_count BETWEEN 3 AND 5
          AND transaction_type_code IN ('Covered','Indirect')
          AND ts_utc>='2023-05-01'::TIMESTAMP
          AND (ts_utc<'2023-06-01'::TIMESTAMP OR
               (ts_utc>=?::TIMESTAMP AND ts_utc<?::TIMESTAMP))
          AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
          AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
      )
      SELECT p[1] a,p[-1] b,train,count(*) payments,
        count_if(covered) positives,min(covered)::INT class,
        min(covered)=max(covered) pure
      FROM visible GROUP BY 1,2,3
    """,[score_start,score_end])


def score(con: duckdb.DuckDBPyConnection) -> None:
    """Hold out both orientations and compare equal-corridor probability risks."""
    con.execute("""
      CREATE TEMP VIEW novel AS
      SELECT t.* FROM pairs t
      WHERE NOT t.train AND t.pure AND t.payments>=2
        AND NOT EXISTS (
          SELECT 1 FROM pairs m WHERE m.train AND
            ((m.a=t.a AND m.b=t.b) OR (m.a=t.b AND m.b=t.a))
        )
    """)
    con.execute("""
      CREATE TEMP TABLE scored AS
      WITH training AS (
        SELECT a,b,class FROM pairs WHERE train AND pure
      ), mass AS (
        SELECT avg(class) global_p FROM training
      ), origins AS (
        SELECT a,sum(class) k,count(*) n FROM training GROUP BY a
      ), receivers AS (
        SELECT b,sum(class) k,count(*) n FROM training GROUP BY b
      ), countries AS (
        SELECT substr(a,5,2) ca,substr(b,5,2) cb,sum(class) k,count(*) n
        FROM training GROUP BY 1,2
      ), priors AS (
        SELECT t.a,t.b,t.class,t.payments,global_p,
          (o.k+10*global_p)/(o.n+10) origin_p,
          (r.k+10*global_p)/(r.n+10) receiver_p,
          (coalesce(c.k,0)+10*global_p)/(coalesce(c.n,0)+10) country_p
        FROM novel t CROSS JOIN mass
        JOIN origins o ON t.a=o.a AND o.n>=25
        JOIN receivers r ON t.b=r.b AND r.n>=25
        LEFT JOIN countries c ON substr(t.a,5,2)=c.ca AND substr(t.b,5,2)=c.cb
      ), products AS (
        SELECT *,origin_p/(1-origin_p)*receiver_p/(1-receiver_p)
          / (global_p/(1-global_p)) odds
        FROM priors
      )
      SELECT *,pow(class-global_p,2) global_error,
        pow(class-origin_p,2) origin_error,pow(class-receiver_p,2) receiver_error,
        pow(class-country_p,2) country_error,pow(class-odds/(1+odds),2) combined_error,
        odds/(1+odds) combined_p
      FROM products
    """)


def main() -> None:
    """Run a local exploration or the unchanged frozen time-transfer check."""
    opts = arguments(STEM)
    if datetime.now(timezone.utc) >= datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        load(con,opts.phase)
        score(con)
        coverage = table(con,"""
          SELECT CASE WHEN train THEN 'May training' ELSE 'Score month' END cohort,
            count(*) corridors,sum(payments) payments,
            count_if(NOT pure) mixed_corridors,
            count_if(pure AND payments>=2) pure_repeat_corridors
          FROM pairs GROUP BY train ORDER BY train DESC
        """)
        novelty = table(con,"""
          SELECT count(*) novel_repeated_corridors,sum(payments) payments,
            count(*)-(SELECT count(*) FROM scored) without_role_support
          FROM novel
        """)
        primary = table(con,"""
          SELECT count(*) n,sum(payments) payments,count(DISTINCT a) banks,
            count(DISTINCT b) receivers,avg(class) covered_share,avg(global_p) global_p,
            avg(origin_p) origin_p,avg(receiver_p) receiver_p,avg(country_p) country_p,
            avg(combined_p) combined_p,avg(global_error) global_brier,
            avg(origin_error) origin_brier,avg(receiver_error) receiver_brier,
            avg(country_error) country_brier,avg(combined_error) combined_brier,
            sum(combined_error*payments)/sum(payments) payment_weighted_combined,
            sum(origin_error*payments)/sum(payments) payment_weighted_origin
          FROM scored
        """)
        calibration = table(con,"""
          SELECT CASE WHEN origin_p<.01 THEN '0–1%' WHEN origin_p<.05 THEN '1–5%'
                      WHEN origin_p<.20 THEN '5–20%' ELSE '20%+' END probability_band,
            count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            avg(origin_p) predicted_share,avg(class) observed_share
          FROM scored GROUP BY 1 ORDER BY 1
        """)
        sensitivities = []
        combined_sensitivities = []
        for label, grouping in (("Origin bank","a"),("Receiver bank","b")):
            stats = np.asarray(con.execute(f"""
              SELECT count(*),sum(global_error),sum(origin_error),sum(receiver_error),
                sum(country_error),sum(combined_error)
              FROM scored GROUP BY {grouping} ORDER BY {grouping}
            """).fetchall(),dtype=float)
            if len(stats)>=100:
                draws=cluster_draws(stats)
                baselines=draws[:,[1,3,4,5]]
                lifts=(baselines-draws[:,2:3])/baselines
                low, high=np.quantile(lifts,[.005,.995],axis=0)
                sensitivities.append((label,len(stats),*low,*high))
                combined_sensitivities.append(
                    (label,*interval((draws[:,2]-draws[:,5])/draws[:,2]))
                )
        n,_,origins,receivers,observed,_,predicted,*_ = primary[1][0]
        passed = (n>=2000 and min(origins,receivers)>=100 and len(sensitivities)==2
                  and abs(observed-predicted)<=.02
                  and all(min(row[2:5])>=.03 for row in sensitivities))
    tables={"Record coverage":coverage,"Previously unseen corridor coverage":novelty,
            "Equal corridor comparisons":primary,"Origin calibration":calibration,
            "Bank resampling sensitivity":[
              ["cluster_role","clusters","global_low99","receiver_low99","country_low99","combined_low99",
               "global_high99","receiver_high99","country_high99","combined_high99"],sensitivities],
            "Secondary both-bank lift over origin only":(
              ["cluster_role","low99","high99"],combined_sensitivities),
            "Frozen decision":(["all_criteria_met"],[(passed,)])}
    report(STEM,opts.phase,opts.freeze,tables)
    destination=OUT/f"{STEM}_{opts.phase}.md"
    destination.write_text(destination.read_text(encoding="utf-8").replace(
      "2GB; two threads","512MB; one thread").replace(
      "99% ordering-bank cluster","99% separate origin- or receiver-bank cluster"),encoding="utf-8")
    print(f"OK: B20 {opts.phase} aggregate report.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

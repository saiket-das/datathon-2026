"""Test whether Covered direction marks an additional delay on long Direct corridors.

Run: uv run python analysis/20_routing_time/H-B22_covered_long_corridors.py --phase explore
Exploratory support screen only.
"""
from datetime import datetime, timezone
import sys

import duckdb
import numpy as np

from duration_reversals import estimate_reversals, load_reversals
from routing_common import OUT, arguments, cluster_draws, interval, report, table

STEM = "H-B22_covered_long_corridors"


def main() -> None:
    """Separate the B19 directional association from the short-baseline criterion."""
    opts = arguments(STEM)
    if opts.phase!="explore":
        raise ValueError("B22 is exploration only")
    if datetime.now(timezone.utc) >= datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as con:
        load_reversals(con,opts.phase,opts.freeze)
        estimate_reversals(con)
        con.execute("""
          CREATE TEMP TABLE labels AS
          WITH multibank AS (
            SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
              transaction_type_code='Covered' covered
            FROM read_parquet('dataset/payments.parquet')
            WHERE anomaly_type IS NULL AND participant_count BETWEEN 3 AND 5
              AND transaction_type_code IN ('Covered','Indirect')
              AND ts_utc>='2023-05-01'::TIMESTAMP AND ts_utc<'2023-07-01'::TIMESTAMP
              AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
          )
          SELECT p[1] a,p[-1] b,min(covered)::INT cover FROM multibank
          GROUP BY 1,2 HAVING min(covered)=max(covered)
        """)
        con.execute("""
          CREATE TEMP VIEW joined AS
          SELECT d.*,CASE WHEN short_center<100 THEN 'Short' ELSE 'Long' END regime,
            f.cover+r.cover covered_directions,
            CASE WHEN f.cover=1 THEN gap ELSE -gap END signed_covered_gap
          FROM reversals d LEFT JOIN labels f ON d.a=f.a AND d.b=f.b
          LEFT JOIN labels r ON d.a=r.b AND d.b=r.a
        """)
        coverage=table(con,"""
          SELECT regime,count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            sum(payments) direct_payments,count(covered_directions) known_both_labels
          FROM joined GROUP BY 1 ORDER BY 1
        """)
        primary=table(con,"""
          SELECT regime,covered_directions,count(*) n,count(DISTINCT a) banks,
            count(DISTINCT b) receivers,sum(payments) payments,
            avg((abs(gap)>20)::INT) large_gap_share,
            avg((signed_covered_gap>20)::INT) FILTER(WHERE covered_directions=1) covered_slower_share,
            avg((signed_covered_gap < -20)::INT) FILTER(WHERE covered_directions=1) covered_faster_share,
            quantile_cont(abs(gap),[.10,.50,.90]) absolute_gap_quantiles,
            avg((abs(gap)>620)::INT) outside_gap_range,
            avg((abs(drift)>20)::INT) drift_reference_share,count(drift) drift_supported
          FROM joined WHERE covered_directions IS NOT NULL
          GROUP BY 1,2 ORDER BY 1,2
        """)
        banks=np.asarray(con.execute("""
          SELECT count_if(covered_directions=1),count_if(covered_directions=1 AND signed_covered_gap>20),
            count_if(covered_directions=0),count_if(covered_directions=0 AND abs(gap)>20)
          FROM joined WHERE regime='Long' AND covered_directions IN (0,1)
          GROUP BY a ORDER BY a
        """).fetchall(),dtype=float).reshape(-1,4)
        stats=banks.sum(axis=0)
        bounds=[]
        if len(banks)>=100 and min(stats[0],stats[2])>=100:
            draws=cluster_draws(banks)
            covered_low,covered_high=interval(draws[:,1]/draws[:,0])
            indirect_low,indirect_high=interval(draws[:,3]/draws[:,2])
            bounds.append((len(banks),covered_low,covered_high,indirect_low,indirect_high))
            passed=(covered_low>=.80 and indirect_high<=.03)
        else:
            passed=False
    report(STEM,opts.phase,opts.freeze,{"Pair and payment coverage":coverage,
      "Contrasts by observed duration regime":primary,
      "Canonical first bank resampling":(
        ["clusters","covered_slower_low99","covered_slower_high99","indirect_large_low99","indirect_large_high99"],bounds),
      "Frozen decision":(["all_criteria_met"],[(passed,)])})
    result=OUT/f"{STEM}_{opts.phase}.md"
    result.write_text(result.read_text(encoding="utf-8").replace(
      "2GB; two threads","512MB; one thread").replace("99% ordering-bank","99% canonical first bank"),
      encoding="utf-8")
    print(f"OK: B22 {opts.phase} aggregate report.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

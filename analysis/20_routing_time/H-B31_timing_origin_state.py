"""Screen whether observed May Direct timing groups explain origin Covered propensity.

Run: uv run python analysis/20_routing_time/H-B31_timing_origin_state.py
Exploration only, May training and June B20 unseen-corridor population.
"""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util
import sys
import duckdb
from routing_common import report,table,OUT

STEM=Path(__file__).stem


def main() -> None:
    """Fit timing-group rates without using the target origin's route labels."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Cutoff reached")
    spec=importlib.util.spec_from_file_location("b20",Path(__file__).with_name("H-B20_unseen_corridor_propensities.py"))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET enable_progress_bar=false")
        module.load(c,"explore")
        module.score(c)
        c.execute("""
          CREATE TEMP TABLE speed AS
          WITH visible AS (
            SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,total_duration d
            FROM read_parquet('dataset/payments.parquet')
            WHERE anomaly_type IS NULL AND participant_count=2
              AND ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-06-01'
              AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
          )
          SELECT p[1] a,count(*) witnesses,quantile_cont(d,.1) q,count_if(d<100)=0 no_fast
          FROM visible GROUP BY 1 HAVING witnesses>=100;
          CREATE TEMP TABLE bank_rates AS
          SELECT a,count(*) n,sum(class) k FROM pairs WHERE train AND pure GROUP BY 1;
          CREATE TEMP TABLE fitted AS
          SELECT o.*,s.q,s.no_fast,CASE WHEN q<100 THEN 0 WHEN q<600 THEN 1 ELSE 2 END band
          FROM bank_rates o JOIN speed s USING(a)
        """)
        c.execute("""
          CREATE TEMP TABLE evaluated AS
          WITH groups AS (SELECT no_fast,sum(n) n,sum(k) k FROM fitted GROUP BY 1),
          bands AS (SELECT band,sum(n) n,sum(k) k FROM fitted GROUP BY 1)
          SELECT t.*,(g.k-f.k+10*global_p)/(g.n-f.n+10) group_p,
            (b.k-f.k+10*global_p)/(b.n-f.n+10) band_p
          FROM scored t JOIN fitted f USING(a) JOIN groups g USING(no_fast)
          JOIN bands b USING(band) WHERE g.n-f.n>=25 AND b.n-f.n>=25
        """)
        tables={
            "Held-out-origin timing grouping on June unseen corridors":table(c,"""
              SELECT (SELECT count(*) FROM scored) original_corridors,count(*) n,sum(payments) payments,
                count(DISTINCT a) banks,count(DISTINCT b) receivers,
                avg(class) observed,avg(pow(class-group_p,2)) binary_timing_brier,
                avg(pow(class-band_p,2)) timing_band_brier,avg(global_error) global_brier,
                avg(origin_error) own_origin_brier FROM evaluated
            """),
            "Supported origin rates versus timing; May-only description":table(c,"""
              SELECT count(*) banks,sum(n) corridors,corr(ln(1+q),k::DOUBLE/n) log_duration_rate_correlation,
                corr(no_fast::INT,k::DOUBLE/n) no_fast_rate_correlation
              FROM fitted WHERE n>=25
            """)}
    report(STEM,"explore",None,tables)
    out=OUT/f"{STEM}_explore.md"
    out.write_text(out.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread"),encoding="utf-8")
    print("B31 safe exploration report saved.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

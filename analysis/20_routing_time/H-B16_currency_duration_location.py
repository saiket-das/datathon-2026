"""Screen currency-dependent duration locations within recurring Direct visible paths.

Run from root: uv run python analysis/20_routing_time/H-B16_currency_duration_location.py
May–June exploration only. No July outcomes or entity identities are exported.
"""
from datetime import datetime, timezone
from pathlib import Path
import sys
import duckdb


def main() -> None:
    """Compare currency-cell means with month drift at fixed directed endpoints."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET enable_progress_bar=false")
        c.execute("""
          CREATE TEMP TABLE e AS SELECT total_duration d,currency_code currency,month(ts_utc) mon,
            ordering_account oa,beneficiary_account ba,
            list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p
          FROM read_parquet('dataset/payments.parquet')
          WHERE anomaly_type IS NULL AND participant_count=2
            AND ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-07-01'
            AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
            AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
        """)
        lines=["# B16 currency and Direct duration location", "",
               "May–June unlabelled endpoint-bit-0/0.512MB, one thread, no spill.",
               "Exploration only. Shared paths, accounts and banks limit independence.",
               "", "| Minimum currency-cell payments | Paths | Payments | First path banks | p50/p90/p99 currency mean range, seconds | Ranges over20s |",
               "| --- | --- | --- | --- | --- | --- |"]
        for support in (10,25):
            row=c.execute(f"""
              WITH g AS (SELECT p,currency,count(*) n,avg(d) mu FROM e
                GROUP BY 1,2 HAVING n>={support}),
              x AS (SELECT p,sum(n) n,max(mu)-min(mu) delta FROM g GROUP BY 1 HAVING count(*)>=2)
              SELECT count(*) paths,sum(n),count(DISTINCT p[1]) banks,
                quantile_cont(delta,[.5,.9,.99]),count_if(delta>20) FROM x
            """).fetchone()
            paths,n,banks,q,ex=row
            if paths>=100 and banks>=100:
                lines.append(f"| {support} | {paths} | {n} | {banks} | {q} | {'<100' if 0<ex<100 else ex} |")
            else:
                lines.append(f"| {support} | Limited path or bank support | Suppressed | Suppressed | Suppressed | Suppressed |")
        row=c.execute("""
          WITH g AS (SELECT p,currency,mon,count(*) n,avg(d) mu FROM e
            GROUP BY 1,2,3 HAVING n>=25)
          SELECT count(*),sum(a.n+b.n),count(DISTINCT p[1]),quantile_cont(abs(a.mu-b.mu),[.5,.9,.99]),
            count_if(abs(a.mu-b.mu)>20)
          FROM g a JOIN g b USING(p,currency) WHERE a.mon=5 AND b.mon=6
        """).fetchone()
        lines+=["", "Same-path/same-currency month reference, with>=25 observations per month.",
                "| Cells | Payments | First path banks | p50/p90/p99 drift seconds | Drift over20s |",
                "| --- | --- | --- | --- | --- |",
                f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {'<100' if 0<row[4]<100 else row[4]} |"]
    (Path(__file__).parent/"out/H-B16_currency_duration_location_explore.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Saved B16 safe exploration aggregates.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.",file=sys.stderr)
        sys.exit(1)

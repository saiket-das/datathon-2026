"""Test whether B09's May bank-duration classes are country-deterministic.

Run from repository root:
    uv run python analysis/20_routing_time/H-B10_country_bank_class.py
"""
from datetime import datetime, timezone
from pathlib import Path
import sys
import duckdb


def main() -> None:
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        row=c.execute("""
            WITH paths AS (
                SELECT TOTAL_DURATION AS duration,
                list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...') AS path
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND PARTICIPANT_COUNT=2
                  AND ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-06-01'
                  AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
                  AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
            ), banks AS (
                SELECT bank,count(*) n,count_if(duration<100)=0 AS exclusion
                FROM paths,unnest(path)t(bank) GROUP BY bank HAVING n>=100
            ), countries AS (
                SELECT substring(bank,5,2) AS country,count(*) AS banks,
                       count_if(exclusion) AS exclusions
                FROM banks GROUP BY country
            )
            SELECT sum(banks),sum(exclusions),count(*),
                   count_if(exclusions>0 AND exclusions<banks),
                   sum(least(exclusions,banks-exclusions))::DOUBLE/sum(banks),
                   sum(least(exclusions,banks-exclusions)) FILTER(WHERE banks>=10)::DOUBLE/
                     sum(banks) FILTER(WHERE banks>=10),
                   sum(banks) FILTER(WHERE banks>=10)
            FROM countries
        """).fetchone()
    assert row and row[0]>=100
    banks, exclusions, countries, mixed, error, supported_error, supported_banks=row
    lines=[
        "# H-B10: country-determined duration-class falsification","",
        "May Direct endpoint-bit0/0, unlabelled. Bank support requires100 payment appearances.",
        "The class is zero May durations<100; countries come from visible BIC characters5–6.",
        "No bank or country identity is exported. Aggregates only,512MB,one thread,no spill.","",
        "| Supported banks | Exclusion banks | Countries | Mixed-class countries | Minimum country-only classification error |",
        "| ---: | ---: | ---: | ---: | ---: |",
        f"| {banks:,} | {exclusions:,} | {countries} | {mixed} | {error:.6%} |","",
        "Minimum error assigns each country its more frequent bank class, on the same training set.",
        f"For countries with at least10 supported banks, {supported_banks:,} banks give {supported_error:.6%} error.",
        "No held-out classification was run. Purely country-deterministic class membership is falsified on these observed labels.",
    ]
    (Path(__file__).parent/"out"/"H-B10_country_bank_class_explore.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Saved country-class aggregate falsification.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.",file=sys.stderr)
        sys.exit(1)

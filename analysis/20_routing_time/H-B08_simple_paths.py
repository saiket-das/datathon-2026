"""Reject unique-bank path generation on the May–June B exploration partition.

Run from repository root:
    uv run python analysis/20_routing_time/H-B08_simple_paths.py
"""
from datetime import datetime, timezone
from pathlib import Path
import sys
import duckdb


def main() -> None:
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise ValueError("Exploration cutoff reached")
    with duckdb.connect(config={"memory_limit": "512MB", "threads": 1, "temp_directory": ""}) as conn:
        rows = conn.execute("""
            WITH paths AS (
                SELECT PARTICIPANT_COUNT AS v, ORDERING_BIC8 AS bank,
                       ORDERING_ACCOUNT AS sender, BENEFICIARY_ACCOUNT AS receiver,
                       list_filter(string_split(BIC8_PATH,';'),lambda x: x<>'...') AS path
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND ts_utc>=TIMESTAMP '2023-05-01'
                  AND ts_utc<TIMESTAMP '2023-07-01'
                  AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
                  AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
            )
            SELECT v, count(*) AS n, count(DISTINCT bank) AS banks,
                   count_if(len(list_distinct(path))<v) AS repeated,
                   count_if(path[1]=path[-1]) AS endpoint_repeat,
                   count_if(len(list_filter(range(1,v),lambda j: path[j]=path[j+1]))>0) AS adjacent
            FROM paths GROUP BY v HAVING n>=100 AND banks>=100
              AND count(DISTINCT sender)>=100 AND count(DISTINCT receiver)>=100 ORDER BY v
        """).fetchall()
    lines = [
        "# H-B08: repeated visible banks in route paths", "",
        "Exploration only. Unlabelled May–June endpoint-bit-0/0, 512MB, one thread, no spill.",
        "All bank identities stay in memory. Positive event counts below 100 are masked.",
        "Visible adjacency is computed after removing placeholders. It differs from literal path-entry adjacency.",
        "", "| Visible occurrences | Payments | Ordering banks | Any repeat | Same first/last bank | Adjacent visible repeat |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for v, n, banks, *events in rows:
        safe = ["<100" if 0<count<100 else f"{count:,}" for count in events]
        lines.append(f"| {v} | {n:,} | {banks:,} | " + " | ".join(safe) + " |")
    (Path(__file__).parent/"out"/"H-B08_simple_paths_explore.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Saved supported exploration cohorts only.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

"""Screen whether four unresolved anomaly labels retain an adjacent source account.

Run from repository root:
    uv run python analysis/30_parties_anomalies/H-C03_adjacent_edit.py
"""
from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "out/H-C03_adjacent_edit.md"


def main() -> None:
    source = (ROOT / "dataset/payments.parquet").as_posix().replace("'", "''")
    with duckdb.connect() as con:
        con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
        con.execute(f"""CREATE VIEW e AS SELECT ROW_ID, ANOMALY_TYPE, ORDERING_ACCOUNT,
            BENEFICIARY_ACCOUNT FROM read_parquet('{source}')
            WHERE ('0x'||substr(md5(ORDERING_ACCOUNT),1,8))::UBIGINT%2=0""")
        rows = con.execute("""WITH target AS (
            SELECT * FROM e WHERE ANOMALY_TYPE IN
              ('ACCOUNT_REPLACEMENT_SCAM','CEO_SCAM','FAT_FINGER_MISTAKE','CUSTOMER_RECALL')
        ), wanted AS (
            SELECT ROW_ID target_row, unnest([ROW_ID-1,ROW_ID+1]) ROW_ID FROM target
        )
        SELECT t.ANOMALY_TYPE, n.ROW_ID-t.ROW_ID direction, count(*) n,
            count(DISTINCT t.ORDERING_ACCOUNT) senders,
            count_if(t.ORDERING_ACCOUNT=n.ORDERING_ACCOUNT) same_sender,
            count_if(t.BENEFICIARY_ACCOUNT=n.BENEFICIARY_ACCOUNT) same_receiver
        FROM wanted w JOIN e n USING (ROW_ID) JOIN target t ON t.ROW_ID=w.target_row
        GROUP BY 1,2 ORDER BY 1,2""").fetchall()
    report = ["# H-C03: adjacent source edit screen", "",
              "Exploration only: both rows have sender MD5 bit 0.",
              "Positive counts with fewer than 100 pairs or sending accounts are suppressed.", "",
              "| Label | Neighbour offset | Pairs | Senders | Same sender | Same receiver |",
              "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for label, direction, n, senders, same_sender, same_receiver in rows:
        values = (n, senders, same_sender, same_receiver) if min(n, senders) >= 100 else ("suppressed",)*4
        report.append("| " + " | ".join(map(str, (label, direction, *values))) + " |")
    OUT.write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"ERROR: {type(exc).__name__}. Source details suppressed.")
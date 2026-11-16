"""Test whether literal LINEBREAK strings encode every detail LF.

Run from repository root:
    uv run python analysis/30_parties_anomalies/H-C04_literal_linebreak.py
"""
from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "out/H-C04_literal_linebreak.md"


def main() -> None:
    source = (ROOT / "dataset/payments.parquet").as_posix().replace("'", "''")
    report = ["# H-C04: literal LINEBREAK count screen", "",
              "Exploration only: sender MD5 bit 0.", "",
              "| Role | Payments | Exact counts | LF present, marker absent | LF absent, marker present |",
              "| --- | ---: | ---: | ---: | ---: |"]
    with duckdb.connect() as con:
        con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''")
        for role in ("ORDERING", "BENEFICIARY"):
            row = con.execute(f"""WITH t AS (
                SELECT length({role}_DETAILS)-length(replace({role}_DETAILS,chr(10),'')) lf,
                    (length({role}_TOKENS)-length(replace({role}_TOKENS,'LINEBREAK','')))/9 marker
                FROM read_parquet('{source}') WHERE ('0x'||substr(md5(ORDERING_ACCOUNT),1,8))::UBIGINT%2=0
            ) SELECT count(*),count_if(lf=marker),count_if(lf>0 AND marker=0),count_if(lf=0 AND marker>0) FROM t""").fetchone()
            assert row is not None and row[0] >= 100
            cells = [str(value) if value == 0 or value >= 100 else "<100" for value in row]
            report.append("| " + " | ".join([role, *cells]) + " |")
    OUT.write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"ERROR: {type(exc).__name__}. Source details suppressed.")
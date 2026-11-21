"""Shared duration-centre query for B17/B18, run via their hypothesis scripts."""

from datetime import datetime, timezone
from pathlib import Path
import subprocess

import duckdb


def load_reversals(con: duckdb.DuckDBPyConnection, phase: str, freeze: str | None) -> None:
    """Build one ordered contrast per supported unordered visible bank pair."""
    if phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    if phase == "confirm":
        root = Path(__file__).resolve().parents[2]
        subprocess.run(
            ["git", "diff", "--exit-code", "--quiet", freeze, "--", str(Path(__file__).resolve())],
            cwd=root, check=True,
        )
    start, end, boundary = (
        ("2023-05-01", "2023-07-01", "2023-06-01") if phase == "explore"
        else ("2023-07-01", "2023-08-01", "2023-07-16")
    )
    con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
    con.execute("""
      CREATE TEMP TABLE direct AS
      WITH visible AS (
        SELECT total_duration d,ts_utc<?::TIMESTAMP early,
          list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
          ordering_bic8 ob,beneficiary_bic8 bb
        FROM read_parquet('dataset/payments.parquet')
        WHERE anomaly_type IS NULL AND participant_count=2
          AND ts_utc>=?::TIMESTAMP AND ts_utc<?::TIMESTAMP
          AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
          AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
      )
      SELECT p[1] a,p[2] b,d,early,ob=p[1] AND bb=p[2] agrees FROM visible
    """, [boundary, start, end])


def estimate_reversals(con: duckdb.DuckDBPyConnection, agreements_only: bool = False) -> None:
    """Estimate direction medians with ten payments and changes with five per half."""
    con.execute(f"""
      CREATE OR REPLACE TEMP TABLE reversals AS
      WITH edges AS (
        SELECT a,b,count(*) n,median(d) center,
          median(d) FILTER(WHERE early) - median(d) FILTER(WHERE NOT early) drift,
          least(count_if(early),count_if(NOT early)) block_support
        FROM direct WHERE {'agrees' if agreements_only else 'true'}
        GROUP BY 1,2 HAVING n>=10
      )
      SELECT f.a,f.b,f.n+r.n payments,f.center-r.center gap,
        least(f.center,r.center) short_center,
        CASE WHEN least(f.block_support,r.block_support)>=5 THEN f.drift-r.drift END drift
      FROM edges f JOIN edges r ON f.a=r.b AND f.b=r.a WHERE f.a<f.b
    """)

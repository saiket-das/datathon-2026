"""Audit country-contrast support after excluding both orientations of known pairs.

Run: uv run python analysis/20_routing_time/H-B32_country_novelty_support.py
May–June exploration only.
"""
from datetime import datetime,timezone
from pathlib import Path
import importlib.util
import sys
import duckdb
from routing_common import OUT,report,table

STEM=Path(__file__).stem


def main() -> None:
    """Use canonical unordered keys to exclude either May orientation."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Cutoff reached")
    spec=importlib.util.spec_from_file_location("b20",Path(__file__).with_name("H-B20_unseen_corridor_propensities.py"))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET enable_progress_bar=false")
        module.load(c,"explore")
        columns,rows=table(c,"""
          WITH receivers AS (SELECT b,count(*) n FROM pairs WHERE train AND pure GROUP BY b),
          seen AS (SELECT DISTINCT least(a,b) lo,greatest(a,b) hi FROM pairs WHERE train),
          target AS (
            SELECT t.*,s.lo IS NULL novel FROM pairs t
            JOIN receivers r ON r.b=t.b AND r.n>=25
            LEFT JOIN seen s ON least(t.a,t.b)=s.lo AND greatest(t.a,t.b)=s.hi
            WHERE NOT t.train AND t.pure
          ), groups AS (
            SELECT a,novel,substr(a,5,2)=substr(b,5,2) domestic,count(*) n,avg(class) p
            FROM target GROUP BY 1,2,3
          ), matched AS (
            SELECT a,novel,min(n) support,sum(n) corridors,
              max(p) FILTER(WHERE domestic)-max(p) FILTER(WHERE NOT domestic) effect
            FROM groups GROUP BY 1,2 HAVING count(*)=2
          )
          SELECT novel,threshold,count(*) origins,sum(corridors) corridors,avg(effect) effect
          FROM matched CROSS JOIN (VALUES (5),(10)) gate(threshold)
          WHERE support>=threshold GROUP BY 1,2 ORDER BY 1,2
        """)
        safe=[(novel,gate,origins if origins>=100 else "<100",n,
               effect if origins>=100 else "suppressed") for novel,gate,origins,n,effect in rows]
    report(STEM,"explore",None,{"Novelty and origin support":(columns,safe)})
    out=OUT/f"{STEM}_explore.md"
    out.write_text(out.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread"),encoding="utf-8")
    print("B32 safe support audit saved.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)

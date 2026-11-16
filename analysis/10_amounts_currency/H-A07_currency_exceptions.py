"""Explore exceptions to first-path-country modal currency association.

Run: uv run python analysis/10_amounts_currency/H-A07_currency_exceptions.py
Only both-account bit-0 July development outcomes and pre-July training are read.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import duckdb

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("currency_endpoint", HERE / "H-A06_currency_endpoint.py")
endpoint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(endpoint)


def main() -> int:
    if datetime.now(timezone.utc) >= datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''")
            source = endpoint.SOURCE.format(split=endpoint.foundation.partition_sql("accounts"),phase="explore")
            con.execute(f"CREATE VIEW scope AS {source}")
            for role in ("send","receive"):
                con.execute(f"""CREATE TEMP TABLE mode_{role} AS
                    SELECT path_{role} country,currency FROM scope WHERE training
                    GROUP BY path_{role},currency
                    QUALIFY sum(count(*)) OVER(PARTITION BY path_{role})>=100
                    AND row_number() OVER(PARTITION BY path_{role}
                        ORDER BY count(*) DESC,currency)=1""")
            con.execute("""CREATE VIEW residual AS
                SELECT s.*,a.currency sender_mode,b.currency receiver_mode,r.currency receiver_local_mode
                FROM scope s JOIN mode_send a ON path_send=a.country
                JOIN mode_receive b ON path_receive=b.country
                LEFT JOIN mode_send r ON path_receive=r.country
                WHERE NOT training AND s.currency<>a.currency""")
            queries = {
                "Coverage and receiver alternative": """SELECT count(*) n,
                    count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                    sum((currency=receiver_mode)::INT) matches_receiver,
                    sum((currency=receiver_local_mode)::INT) matches_receiver_sendertrained,
                    sum((currency IN ('USD','EUR'))::INT) usd_or_eur
                    FROM residual""",
                "Residual currencies with broad entity support": """SELECT currency,count(*) n,
                    count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                    round(avg((currency=receiver_mode)::INT),6) receiver_match_share,
                    round(avg(coalesce((currency=receiver_local_mode)::INT,0)),6) receiver_sendertrained_share
                    FROM residual GROUP BY currency
                    HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
                        AND count(DISTINCT receiver)>=100 ORDER BY n DESC""",
                "Route and shared endpoint-mode controls": """SELECT route,
                    sender_mode=receiver_mode same_endpoint_mode,count(*) n,
                    count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                    round(avg((currency=receiver_mode)::INT),6) receiver_match_share,
                    round(avg(coalesce((currency=receiver_local_mode)::INT,0)),6) receiver_sendertrained_share,
                    round(avg((currency IN ('USD','EUR'))::INT),6) usd_or_eur_share
                    FROM residual GROUP BY route,sender_mode=receiver_mode
                    HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
                        AND count(DISTINCT receiver)>=100 ORDER BY route,same_endpoint_mode""",
            }
            lines = ["# H-A07: Currency exceptions", "",
                "Exploration only. Both-account bit-0 July; modes trained pre-July on bit-0.",
                "Only rows where both endpoint-country maps are supported enter this conditional screen.",
                "Phase 0, Round 1 and A03-A06 exposure applies. This is new exploratory conditioning.", ""]
            for title,query in queries.items():
                result=con.execute(query)
                columns=[c[0] for c in result.description]
                rows=result.fetchall()
                lines += ["## "+title,"","| "+" | ".join(columns)+" |",
                          "| "+" | ".join(["---"]*len(columns))+" |"]
                lines += ["| "+" | ".join(map(str,row))+" |" for row in rows]
                lines.append("")
        (HERE/"out/H-A07_currency_exceptions_explore.md").write_text("\n".join(lines),encoding="utf-8")
        print("OK: aggregate currency-exception exploration report saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

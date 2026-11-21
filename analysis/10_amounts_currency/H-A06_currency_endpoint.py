"""Explore currency choice and endpoints on both-account bit-0 payments.

Run: uv run python analysis/10_amounts_currency/H-A06_currency_endpoint.py
Train modal currency maps before July and score July inside bit 0. This is
development evidence. Only grouped results leave DuckDB.
"""
import argparse
import subprocess
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import duckdb
import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "foundation", HERE.parent / "00_prep/scientific_checks.py"
)
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)

SOURCE = """SELECT CURRENCY_CODE currency, ORDERING_ACCOUNT sender,
       BENEFICIARY_ACCOUNT receiver, ORDERING_BIC8 bank, TRANSACTION_TYPE_CODE route,
       substr(ORDERING_BIC8,5,2) declared_send,
       substr(BENEFICIARY_BIC8,5,2) declared_receive,
       substr(split_part(BIC8_PATH,';',1),5,2) path_send,
       substr(list_extract(string_split(BIC8_PATH,';'),-1),5,2) path_receive,
       ts_utc < TIMESTAMP '2023-07-01' training
FROM read_parquet('dataset/payments.parquet')
WHERE ANOMALY_TYPE IS NULL AND {split} = '{phase}'"""

# Semantic fields only. Country and currency values stay in database joins.
FEATURES = ("declared_send", "declared_receive", "path_send", "path_receive")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["explore", "validate"], default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        print("Research cutoff reached. Exploration closed.", file=sys.stderr)
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Freeze SHA required")
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"],
                cwd=HERE.parents[1], check=True, capture_output=True,
            )
            for path in [Path(__file__).resolve(), Path(foundation.__file__)]:
                relative = path.relative_to(HERE.parents[1]).as_posix()
                frozen = subprocess.check_output(
                    ["git", "show", f"{args.freeze}:{relative}"],
                    cwd=HERE.parents[1], stderr=subprocess.DEVNULL,
                )
                if frozen.replace(b"\r\n",b"\n") != path.read_bytes().replace(b"\r\n",b"\n"):
                    raise ValueError("Frozen source mismatch")
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''")
            con.execute("SET preserve_insertion_order=false")
            sql = SOURCE.format(split=foundation.partition_sql("accounts"), phase="explore")
            con.execute(f"CREATE VIEW scope AS {sql}")
            con.execute("""CREATE TEMP TABLE mode_global AS
                SELECT currency FROM scope WHERE training GROUP BY currency
                ORDER BY count(*) DESC, currency LIMIT 1""")
            for feature in FEATURES:
                con.execute(f"""CREATE TEMP TABLE {feature}_mode AS
                    SELECT {feature} country, currency FROM scope
                    WHERE training AND length({feature})=2 GROUP BY {feature},currency
                    QUALIFY sum(count(*)) OVER (PARTITION BY {feature})>=100
                    AND row_number() OVER (
                        PARTITION BY {feature} ORDER BY count(*) DESC,currency
                    )=1""")
            joins = " ".join(
                f"LEFT JOIN {feature}_mode {feature}_fit ON s.{feature}={feature}_fit.country"
                for feature in FEATURES
            )
            predictions = ", ".join(
                f"coalesce({feature}_fit.currency,g.currency) AS {feature}_prediction"
                for feature in FEATURES
            )
            scoring = SOURCE.format(
                split=foundation.partition_sql("accounts"),
                phase="confirm" if args.phase == "validate" else "explore",
            )
            con.execute(f"CREATE VIEW evaluation AS {scoring}")
            con.execute(f"""CREATE VIEW scored AS
                SELECT s.*, g.currency global_prediction, {predictions}
                FROM evaluation s CROSS JOIN mode_global g {joins} WHERE NOT training""")
            accuracy = ", ".join(
                f"round(100*avg((currency={feature}_prediction)::INT),3) {feature}_pct"
                for feature in ("global", *FEATURES)
            )
            support = '''count(*) payments, count(DISTINCT sender) senders,
                         count(DISTINCT receiver) receivers'''
            result = con.execute(f"""WITH groups AS (
                SELECT *, declared_send=path_send sender_country_agrees,
                          declared_receive=path_receive receiver_country_agrees
                FROM scored
            )
            SELECT CASE WHEN grouping(route)=1 THEN 'All' ELSE route END route,
                   CASE WHEN grouping(sender_country_agrees)=1 THEN 'All'
                        ELSE sender_country_agrees::VARCHAR END sender_agrees,
                   CASE WHEN grouping(receiver_country_agrees)=1 THEN 'All'
                        ELSE receiver_country_agrees::VARCHAR END receiver_agrees,
                   {support}, {accuracy}
            FROM groups
            GROUP BY GROUPING SETS ((),(route),(sender_country_agrees,receiver_country_agrees))
            HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
                AND count(DISTINCT receiver)>=100
            ORDER BY route,sender_agrees,receiver_agrees""")
            cols = [col[0] for col in result.description]
            rows = result.fetchall()
            assert rows and rows[0][:3] == ("All","All","All")
            stat_rows = con.execute("""SELECT bank, count(*) n,
                sum((currency=path_send_prediction)::INT) correct,
                sum((currency=path_send_prediction)::INT -
                    (currency=declared_send_prediction)::INT) lift_sender,
                sum((currency=path_send_prediction)::INT -
                    (currency=path_receive_prediction)::INT) lift_receiver
                FROM scored GROUP BY bank ORDER BY bank""").fetchall()
            numeric = np.asarray([row[1:] for row in stat_rows], dtype=float)
            rng = np.random.default_rng(20261116)
            draws = []
            for _ in range(1000):
                sample = numeric[rng.integers(0,len(numeric),len(numeric))].sum(axis=0)
                draws.append(sample[1:] / sample[0])
            interval = np.quantile(draws,[.005,.995],axis=0)
            primary = [
                ("path sender accuracy", *interval[:,0]),
                ("lift vs declared sender", *interval[:,1]),
                ("lift vs path receiver", *interval[:,2]),
            ]
            decision = (min(rows[0][3:6]) >= 100 and len(numeric)>=100
                        and interval[0,0]>=.90 and interval[0,1]>=.02
                        and interval[0,2]>=.50)
            support = con.execute("""SELECT count(DISTINCT sender),
                count(DISTINCT receiver),count(DISTINCT bank) FROM scored""").fetchone()
            # Separate overlap queries keep entity sets below the memory cap.
            overlaps = []
            for entity in ("sender", "receiver", "bank"):
                overlap = con.execute(f"""SELECT count(DISTINCT {entity}) FROM scored
                    WHERE {entity} IN (
                        SELECT DISTINCT {entity} FROM scope WHERE training
                    )""").fetchone()[0]
                overlaps.append(overlap)
            training_overlap = tuple(overlaps)
        output = HERE / f"out/H-A06_currency_endpoint_{args.phase}.md"
        lines = [
            "# H-A06: Endpoint currency association",
            "",
            f"May/June and earlier bit-0 training; July {args.phase} scoring. Freeze: {args.freeze or chr(39)+chr(39)}.",
            "Prior Phase 0, Round 1 and A03/A05 reused-population exposure applies.",
            "Modal categorical currency predictor. A country with fewer than 100 training payments falls back to the global mode.",
            "Each percentage uses all rows in the displayed July subgroup, including fallbacks.",
            "",
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join(["---"] * len(cols)) + " |",
        ]
        lines.extend("| " + " | ".join(map(str, row)) + " |" for row in rows)
        lines += ["", "## 99% ordering-bank cluster sensitivity intervals", "",
                  "| statistic | low | high |", "| --- | --- | --- |"]
        lines += ["| " + " | ".join(map(str,row)) + " |" for row in primary]
        lines += ["", f"All practical criteria met: {decision}.",
                  f"Eligible senders / receivers / declared ordering banks: {support}.",
                  f"Same-role sender / receiver / ordering-bank overlap with training: {training_overlap}.",
                  "Other cross-role accounts and path banks may overlap; no independent-holdout inference."]
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"OK: aggregate {args.phase} report written. Criteria met: {decision}.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

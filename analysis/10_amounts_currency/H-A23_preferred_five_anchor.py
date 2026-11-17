"""Test a preferred USD mantissa-five point mass against local density controls.

Run: uv run python analysis/10_amounts_currency/H-A23_preferred_five_anchor.py
Freeze before --phase validate --freeze SHA. Aggregate output only.
This tests an output-distribution constraint, not a particular rounding operator.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import duckdb
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("foundation", HERE.parent / "00_prep/scientific_checks.py")
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)


def ratios(counts: np.ndarray) -> np.ndarray:
    """Compare anchor5 with4/6 and anchor7 with6/8, using point/background odds."""
    values = counts.reshape(5, 2)
    five = (values[1, 0] / values[1, 1]) / (
        (values[0, 0] + values[2, 0]) / (values[0, 1] + values[2, 1]))
    seven = (values[3, 0] / values[3, 1]) / (
        (values[2, 0] + values[4, 0]) / (values[2, 1] + values[4, 1]))
    return np.asarray([five, seven])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["explore", "validate"], default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Freeze required")
            subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"], cwd=ROOT, check=True, capture_output=True)
            for path in [Path(__file__).resolve(), Path(foundation.__file__)]:
                frozen = subprocess.check_output(["git", "show", f"{args.freeze}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT)
                if frozen.replace(b"\r\n", b"\n") != path.read_bytes().replace(b"\r\n", b"\n"):
                    raise ValueError("Freeze mismatch")
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
            split = foundation.partition_sql("accounts")
            phase = "explore" if args.phase == "explore" else "confirm"
            con.execute(f"""CREATE TEMP TABLE scope AS SELECT USD_AMOUNT amount,
                ORDERING_ACCOUNT sender,BENEFICIARY_ACCOUNT receiver,ORDERING_BIC8 bank,
                floor(log10(USD_AMOUNT))::INT magnitude,
                pow(10,floor(log10(USD_AMOUNT))) place
                FROM read_parquet('dataset/payments.parquet')
                WHERE {split}='{phase}' AND CURRENCY_CODE='USD'
                    AND ANOMALY_TYPE IS NULL AND USD_AMOUNT>0
                    AND ts_utc>=TIMESTAMP '2023-07-01'
                    AND ts_utc<TIMESTAMP '2023-08-01'""")
            con.execute("""CREATE TEMP TABLE selected AS SELECT *,
                round(amount/place)::INT digit,
                abs(amount-round(amount/place)*place)<1e-6 point,
                CASE WHEN magnitude=3 THEN '3' ELSE '4-5' END decade_group
                FROM scope WHERE magnitude BETWEEN 3 AND 5
                    AND round(amount/place) BETWEEN 4 AND 8
                    AND abs(amount/place-round(amount/place))<=.4""")
            support = con.execute("""SELECT (SELECT count(*) FROM scope),count(*),
                count(DISTINCT sender),count(DISTINCT receiver),count(DISTINCT bank),
                (SELECT count(*) FROM scope)-count(*)
                FROM selected""").fetchone()
            rows = con.execute("""SELECT CASE WHEN grouping(decade_group)=1 THEN 'All' ELSE decade_group END decade_group,
                digit,count(*) n,count(*) FILTER(WHERE point) point_n,
                count(DISTINCT sender) FILTER(WHERE point) point_senders,
                count(DISTINCT receiver) FILTER(WHERE point) point_receivers,
                count(*) FILTER(WHERE NOT point) background_n,
                count(DISTINCT sender) FILTER(WHERE NOT point) background_senders,
                count(DISTINCT receiver) FILTER(WHERE NOT point) background_receivers
                FROM selected GROUP BY GROUPING SETS ((digit),(decade_group,digit))
                HAVING grouping(decade_group)=1 OR digit<=6
                ORDER BY decade_group,digit""").fetchall()
            if len(rows) != 11 or any(min(row[3:]) < 100 for row in rows):
                raise ValueError("Unsafe anchor family")
            bank_rows = con.execute("""SELECT bank,digit,count(*) FILTER(WHERE point),
                count(*) FILTER(WHERE NOT point) FROM selected GROUP BY bank,digit ORDER BY bank,digit""").fetchall()
            banks: dict[str, np.ndarray] = {}
            for bank, digit, point, background in bank_rows:
                banks.setdefault(bank, np.zeros(10))[(digit-4)*2:(digit-4)*2+2] = point, background
            stats = np.asarray(list(banks.values()))
            estimate = ratios(stats.sum(axis=0))
            rng = np.random.default_rng(20261117)
            samples = np.asarray([ratios(stats[rng.integers(0,len(stats),len(stats))].sum(axis=0)) for _ in range(1000)])
            intervals = np.quantile(samples, [.005,.995], axis=0)
            strata = []
            for name in ["3", "4-5"]:
                counts = np.asarray([[row[3],row[6]] for row in rows if row[0]==name])
                odds = (counts[1,0]/counts[1,1])/((counts[0,0]+counts[2,0])/(counts[0,1]+counts[2,1]))
                strata.append((name,odds))
            passed = (support[1]>=15000 and min(support[2:])>=100
                and intervals[0,0]>=3 and intervals[0,1]>=.5 and intervals[1,1]<=2
                and all(row[1]>=3 for row in strata))
        lines = ["# H-A23 — Preferred USD mantissa-five anchor", "",
            f"Phase {args.phase}; freeze {args.freeze or 'exploration only'}.",
            "Positive unlabelled July USD, selected both-account bit. Magnitudes3–5; symmetric decimal-mantissa windows ±.4 around4–8.",
            "Phase0/Round1 and A02/A10/A18/A22 exposure; A19 UTC and A09/A13 rates exposed. Reused bit-1 records are internal validation only.",
            "512MB, one thread, no spill. Point mass tolerance USD1e-6; background is the rest of the same local window.", "",
            "| scoped | selected | senders | receivers | banks | excluded |", "| --- | --- | --- | --- | --- | --- |",
            "| " + " | ".join(map(str,support)) + " |", "",
            "| decade_group | digit | n | point_n | point_senders | point_receivers | background_n | background_senders | background_receivers |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        lines += ["| " + " | ".join(map(str,row)) + " |" for row in rows]
        lines += ["", "| contrast | odds_ratio | low99 | high99 |", "| --- | --- | --- | --- |"]
        lines += [f"| {name} | {estimate[i]} | {intervals[0,i]} | {intervals[1,i]} |" for i,name in enumerate(["5 vs4/6","7 vs6/8 control"])]
        lines += ["", "| decade_group | 5 vs4/6 |", "| --- | --- |"]
        lines += ["| " + " | ".join(map(str,row)) + " |" for row in strata]
        lines += ["", f"All frozen criteria met: {passed}.", "",
            "Whole declared ordering-bank bootstrap1000, seed20261117, .005/.995 percentiles. Shared countries/corridors, receivers and previous exposure remain. Preferred fixed values, rounding anchors and different latent mixtures are observational alternatives; this test does not recover a rounding operator or mixture probability.", ""]
        (HERE / f"out/H-A23_preferred_five_anchor_{args.phase}.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"OK: aggregate preferred-anchor {args.phase} saved. Criteria met: {passed}.")
        return 0
    except Exception as exc:
        if isinstance(exc, duckdb.ParserException):
            print(str(exc).splitlines()[0], file=sys.stderr)
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

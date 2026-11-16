"""Test a fixed joint endpoint-disagreement law using only local Parquet aggregates.

Run from repository root:
    uv run python analysis/20_routing_time/H-B05_endpoint_mismatch.py --phase explore
After freezing, replace --phase explore with --phase confirm --freeze SHA.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
STEM = Path(__file__).stem
FIXED = np.array([.9025, .0475, .0475, .0025])
NAMES = ("ordering mismatch", "beneficiary mismatch", "both mismatch", "joint excess", "fixed-law TV")


def metrics(stats: np.ndarray) -> np.ndarray:
    """Map [n, ordering, beneficiary, both] event counts to pooled diagnostics."""
    ordering, beneficiary, both = (stats[..., 1:] / stats[..., :1]).T
    distribution = np.stack((1 - ordering - beneficiary + both, ordering - both,
                             beneficiary - both, both), axis=-1)
    tv = np.abs(distribution - FIXED).sum(axis=-1) / 2
    return np.stack((ordering, beneficiary, both, both - ordering * beneficiary, tv), axis=-1)


def evaluate(connection: duckdb.DuckDBPyConnection, phase: str, freeze: str | None) -> str:
    """Produce cohort-level evidence with a fixed cluster resampling procedure."""
    n, senders, receivers, banks, invalid = connection.execute("""
        SELECT count(*), count(DISTINCT sender), count(DISTINCT receiver),
               count(DISTINCT ob), count_if(o IS NULL OR b IS NULL)
        FROM sample
    """).fetchone()
    if min(senders, receivers, banks) < 100:
        raise ValueError("insufficient entity support")
    by_bank = np.asarray(connection.execute("""
        SELECT count(*), count_if(o), count_if(b), count_if(o AND b)
        FROM sample WHERE o IS NOT NULL AND b IS NOT NULL GROUP BY ob ORDER BY ob
    """).fetchall(), dtype=float)
    if len(by_bank) < 100:
        raise ValueError("insufficient scorable ordering banks")
    point = metrics(by_bank.sum(axis=0))
    rng = np.random.default_rng(20261116)
    weights = rng.multinomial(len(by_bank), np.full(len(by_bank), 1 / len(by_bank)), size=1000)
    low, high = np.quantile(metrics(weights @ by_bank), [.005, .995], axis=0)
    passed = (invalid == 0 and low[0] >= .045 and high[0] <= .055 and low[1] >= .045
              and high[1] <= .055 and low[3] >= -.00075 and high[3] <= .00075 and high[4] <= .0075)
    _, _, _, joint_count = by_bank.sum(axis=0)
    lines = [
        f"# {STEM}: {phase}", "",
        f"Freeze: {freeze or 'not yet frozen'}", "",
        "Endpoint bit0/0, unlabelled payments. 512MB, one thread, no spill, UTC.",
        "Phase 0 and Round 1 priors are exposed. July is internal temporal validation.",
        "",
        f"Payments: {n:,}. Senders: {senders:,}. Receivers: {receivers:,}. Ordering banks: {banks:,}.",
        f"Unscorable comparisons: {invalid:,}. Both mismatch: {int(joint_count):,}.",
        "A disjoint single-endpoint error comparator predicts zero joint cases.",
        f"Fixed-law practical criteria pass: {passed}.", "",
        "| Statistic | Pooled estimate | 99% lower | 99% upper |",
        "| --- | ---: | ---: | ---: |",
    ]
    lines.extend(f"| {name} | {value:.8f} | {lo:.8f} | {hi:.8f} |"
                 for name, value, lo, hi in zip(NAMES, point, low, high))
    for title, group in [("Route", "route"), ("Party pair", "party")]:
        lines.extend(["", f"## {title} sensitivity",
                      "| Group | Payments | Ordering mismatch | Beneficiary mismatch | Joint rate | Excess joint | TV |",
                      "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"])
        rows = connection.execute(f"""
            SELECT {group}, count(*), count_if(o), count_if(b), count_if(o AND b)
            FROM sample WHERE o IS NOT NULL AND b IS NOT NULL
            GROUP BY 1 HAVING count(*) >= 100 AND count(DISTINCT sender) >= 100
                 AND count(DISTINCT receiver) >= 100 ORDER BY 1
        """).fetchall()
        for name, *counts in rows:
            formatted = " | ".join(f"{value:.8f}" for value in metrics(np.array(counts)))
            lines.append(f"| {name} | {counts[0]:,} | {formatted} |")
    lines.extend(["", "## Mismatch comparisons",
                  "| Role | Mismatches | Same country share | Equals opposite path endpoint share |",
                  "| --- | ---: | ---: | ---: |"])
    for role, flag, declared, path_end, opposite in [
        ("ordering", "o", "ob", "po", "pb"), ("beneficiary", "b", "bb", "pb", "po")
    ]:
        result = connection.execute(f"""
            SELECT count(*), avg((substr({declared},5,2)=substr({path_end},5,2))::INT),
                   avg(({declared}={opposite})::INT)
            FROM sample WHERE {flag} HAVING count(*)>=100 AND count(DISTINCT sender)>=100
                 AND count(DISTINCT receiver)>=100
        """).fetchone()
        if result:
            count, same_country, swapped = result
            lines.append(f"| {role} | {count:,} | {same_country:.8f} | {swapped:.8f} |")
    if phase == "confirm":
        lines.extend(["", "## Distinct entities shared with May–June",
                      "| Entity set | Shared count |", "| --- | ---: |"])
        membership = {
            "sender": "SELECT DISTINCT sender entity FROM {}",
            "receiver": "SELECT DISTINCT receiver entity FROM {}",
            "accounts across both roles": "SELECT sender entity FROM {0} UNION SELECT receiver FROM {0}",
            "declared endpoint banks": "SELECT ob entity FROM {0} UNION SELECT bb FROM {0}",
            "visible path banks": """SELECT DISTINCT unnest(list_filter(path, lambda entry: entry <> '...'))
                                      entity FROM {}""",
        }
        for label, template in membership.items():
            july = template.format("sample")
            prior = template.format("earlier")
            count = connection.execute(f"SELECT count(*) FROM (({july}) INTERSECT ({prior}))").fetchone()[0]
            lines.append(f"| {label} | {'<100' if 0 < count < 100 else f'{count:,}'} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "confirm"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        parser.error("research cutoff passed")
    if args.phase == "confirm":
        if not args.freeze:
            parser.error("confirmation requires --freeze")
        subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"], cwd=ROOT, check=True)
        subprocess.run(["git", "diff", "--quiet", args.freeze, "--",
                        f"analysis/20_routing_time/{STEM}.py"], cwd=ROOT, check=True)
        plan = subprocess.check_output(
            ["git", "show", f"{args.freeze}:findings/hypotheses/{STEM}.md"], cwd=ROOT, text=True)
        if "**Status:** confirmation-ready" not in plan:
            raise ValueError("freeze must contain validation criteria")
    source = (ROOT / "dataset/payments.parquet").as_posix().replace("'", "''")
    begin, end = ("2023-05-01", "2023-07-01") if args.phase == "explore" else ("2023-07-01", "2023-08-01")
    with duckdb.connect(config={"memory_limit": "512MB", "threads": 1, "temp_directory": ""}) as connection:
        connection.execute("SET TimeZone='UTC'")
        connection.execute(f"""
            CREATE VIEW bank_zero AS
            SELECT ORDERING_BIC8 ob, BENEFICIARY_BIC8 bb, string_split(BIC8_PATH,';') path,
                ORDERING_ACCOUNT sender, BENEFICIARY_ACCOUNT receiver, TRANSACTION_TYPE_CODE route,
                ORDERING_TYPE||BENEFICIARY_TYPE party, ts_utc
            FROM read_parquet('{source}')
            WHERE ANOMALY_TYPE IS NULL AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
                AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
        """)
        connection.execute(f"""
            CREATE VIEW sample AS SELECT *, path[1] po, path[-1] pb,
                ob<>nullif(path[1],'...') o, bb<>nullif(path[-1],'...') b
            FROM bank_zero WHERE ts_utc>=TIMESTAMP '{begin}' AND ts_utc<TIMESTAMP '{end}'
        """)
        if args.phase == "confirm":
            connection.execute("""
                CREATE VIEW earlier AS SELECT * FROM bank_zero
                WHERE ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-07-01'
            """)
        report = evaluate(connection, args.phase, args.freeze)
    output = Path(__file__).parent / "out" / f"{STEM}_{args.phase}.md"
    output.write_text(report, encoding="utf-8")
    print("Endpoint mismatch aggregate report saved.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}. Source details hidden.", file=sys.stderr)
        sys.exit(1)

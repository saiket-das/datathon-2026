"""Test beneficiary-endpoint concordance for two scam labels on sender splits.

Run from repository root:
    uv run python analysis/30_parties_anomalies/H-C05_scam_endpoint_agreement.py --phase explore
    uv run python analysis/30_parties_anomalies/H-C05_scam_endpoint_agreement.py --phase validate --freeze SHA
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

import duckdb
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STEM = "H-C05_scam_endpoint_agreement"
TARGETS = ("ACCOUNT_REPLACEMENT_SCAM", "CEO_SCAM")
TARGET_SQL = ", ".join(f"'{label}'" for label in TARGETS)


def verify_freeze(sha: str) -> None:
    """Require the full recorded freeze commit and unchanged script and test plan."""
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("validation requires the full freeze SHA")
    subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                   check=True, capture_output=True)
    for path in (Path(__file__).resolve(), ROOT / f"findings/hypotheses/{STEM}.md"):
        name = path.relative_to(ROOT).as_posix()
        frozen = subprocess.run(["git", "show", f"{sha}:{name}"], cwd=ROOT, check=True,
                                capture_output=True).stdout.decode("utf-8")
        current = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            section = "## Test plan (freeze before validation)"
            frozen = frozen.split(section, 1)[1].split("\n## ", 1)[0]
            current = current.split(section, 1)[1].split("\n## ", 1)[0]
        if frozen.splitlines() != current.splitlines():
            raise ValueError("script or acceptance plan differs from freeze")


def aggregate(con: duckdb.DuckDBPyConnection, where: str, *, by_route: bool = False) -> list[tuple]:
    """Count discordance without ever returning a source record."""
    route = "TRANSACTION_TYPE_CODE" if by_route else "'All'"
    return con.execute(f"""SELECT coalesce(label,'UNLABELLED'), route, sum(n)::BIGINT n,
            count(*) senders, sum(orderer_bad)::BIGINT, sum(beneficiary_bad)::BIGINT,
            count_if(beneficiary_bad>0) affected_senders
        FROM (
            SELECT ANOMALY_TYPE label, {route} route, ORDERING_ACCOUNT,
                count(*) n,
                count_if(ORDERING_BIC8 IS DISTINCT FROM split_part(BIC8_PATH,';',1)) orderer_bad,
                count_if(BENEFICIARY_BIC8 IS DISTINCT FROM list_last(string_split(BIC8_PATH,';'))) beneficiary_bad
            FROM e WHERE {where} GROUP BY 1,2,3
        ) GROUP BY 1,2 ORDER BY 1,2""").fetchall()


def render(rows: list[tuple]) -> list[str]:
    lines = ["| Label | Route | Payments | Senders | Orderer mismatches | Beneficiary mismatches | Affected senders | 98.75% upper bound |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for label, route, n, senders, orderer_bad, beneficiary_bad, affected in rows:
        if min(n, senders) < 100:
            continue
        bound = float(beta.ppf(.9875, affected+1, senders-affected)) if affected < senders else 1.0
        counts = [str(value) if value == 0 or value >= 100 else "<100"
                  for value in (orderer_bad, beneficiary_bad, affected)]
        bound_text = "suppressed" if 0 < affected < 100 else f"{bound:.6f}"
        lines.append(f"| {label} | {route} | {n} | {senders} | "
                     + " | ".join(counts) + f" | {bound_text} |")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "validate"), required=True)
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "validate":
        verify_freeze(args.freeze or "")
    source = (ROOT / "dataset/payments.parquet").as_posix().replace("'", "''")
    bit = int(args.phase == "validate")
    report = [f"# H-C05: scam endpoint agreement ({args.phase})", "",
              f"Sender MD5 bit {bit}. Freeze: {args.freeze or 'exploration only'}.",
              "Phase 0 and prior Round 1 outcome exposure apply. Validation reuses Round 1 bit-1 records.",
              "Cohorts with fewer than 100 senders are omitted. Positive event counts below 100 are masked.", ""]
    with duckdb.connect() as con:
        con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
        con.execute(f"""CREATE VIEW e AS SELECT ANOMALY_TYPE, TRANSACTION_TYPE_CODE, ORDERING_ACCOUNT,
                ORDERING_BIC8, BENEFICIARY_BIC8, BIC8_PATH
            FROM read_parquet('{source}')
            WHERE ('0x'||substr(md5(ORDERING_ACCOUNT),1,8))::UBIGINT%2={bit}""")
        # Group broad controls in independent scans to avoid holding all strings in memory.
        targets = aggregate(con, f"ANOMALY_TYPE IN ({TARGET_SQL})")
        controls = aggregate(con, "ANOMALY_TYPE IS NULL AND TRANSACTION_TYPE_CODE IN ('Direct','Indirect')", by_route=True)
        routes = aggregate(con, f"ANOMALY_TYPE IN ({TARGET_SQL}) AND TRANSACTION_TYPE_CODE IN ('Direct','Indirect')", by_route=True)
        assert len(targets) == len(controls) == 2
        decisions = {}
        for label, _, n, senders, obad, bbad, affected in targets:
            decisions[f"{label}: total support"] = min(n, senders) >= 100
            decisions[f"{label}: beneficiary concordance and uncertainty"] = (
                bbad == 0 and float(beta.ppf(.9875, affected+1, senders-affected)) <= .015
            )
            decisions[f"{label}: ordering mismatch at least 2%"] = obad/n >= .02
        for _, route, n, senders, _, bbad, _ in controls:
            decisions[f"Unlabelled {route}: support and beneficiary mismatch at least 2%"] = (
                min(n, senders) >= 100 and bbad/n >= .02
            )
        for label in TARGETS:
            for route in ("Direct", "Indirect"):
                decisions[f"{label} {route}: support and zero beneficiary mismatch"] = any(
                    r[0] == label and r[1] == route and min(r[2], r[3]) >= 100 and r[5] == 0
                    for r in routes
                )
        passed = all(decisions.values())
        decision_label = "Frozen practical criteria" if bit else "Exploration pilot criteria (before freeze)"
        report += ["## Target totals", "", *render(targets), "", "## Within-route controls", "",
                   *render(routes + controls), "", f"{decision_label}: {'PASS' if passed else 'FAIL'}.", "",
                   "| Criterion | Result |", "| --- | --- |",
                   *(f"| {name} | {'PASS' if result else 'FAIL'} |" for name, result in decisions.items())]
        if bit == 1:
            # Read only target entities for the overlap audit. Never export identities.
            con.execute(f"""CREATE TEMP TABLE audit AS SELECT ROW_ID, ORDERING_ACCOUNT, BENEFICIARY_ACCOUNT,
                    ORDERING_BIC8, BENEFICIARY_BIC8,
                    ('0x'||substr(md5(ORDERING_ACCOUNT),1,8))::UBIGINT%2 bit
                FROM read_parquet('{source}') WHERE ANOMALY_TYPE IN ({TARGET_SQL})""")
            report += ["", "## Target overlap (same role and field)", "",
                       "| Field | Shared values |", "| --- | ---: |"]
            for field in ("ROW_ID", "ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT", "ORDERING_BIC8", "BENEFICIARY_BIC8"):
                row = con.execute(f"""SELECT count(*) FROM (
                    SELECT {field} FROM audit WHERE bit=0 INTERSECT SELECT {field} FROM audit WHERE bit=1
                )""").fetchone()
                assert row is not None
                n = row[0]
                report.append(f"| {field} | {n if n == 0 or n >= 100 else '<100'} |")
            for name, fields in (("Account in either role", ("ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT")),
                                 ("Endpoint bank in either role", ("ORDERING_BIC8", "BENEFICIARY_BIC8"))):
                a, b = fields
                row = con.execute(f"""WITH entities AS (
                    SELECT bit, value FROM audit, unnest([{a},{b}]) u(value)
                ) SELECT count(*) FROM (
                    SELECT value FROM entities WHERE bit=0 INTERSECT SELECT value FROM entities WHERE bit=1
                )""").fetchone()
                assert row is not None
                n = row[0]
                report.append(f"| {name} | {n if n == 0 or n >= 100 else '<100'} |")
    out = HERE / "out" / f"{STEM}_{args.phase}.md"
    out.write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"ERROR: {type(exc).__name__}. Source details suppressed.")
"""Test conditional placement of one or two internal placeholders.

Run from repository root:
    uv run python analysis/20_routing_time/H-B07_gap_placement.py --phase explore
Frozen internal validation:
    uv run python analysis/20_routing_time/H-B07_gap_placement.py --phase confirm --freeze SHA
"""
import argparse
from datetime import datetime, timezone
from itertools import combinations_with_replacement
from pathlib import Path
import subprocess
import sys

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def shape_probabilities(visible: int, gaps: int) -> tuple[list[tuple[int, int]], np.ndarray, np.ndarray]:
    """Enumerate legal internal shapes and the two competing probability laws."""
    slots = visible - 1
    cells = [(i, i) for i in range(1, slots + 1)] if gaps == 1 else list(combinations_with_replacement(range(1, slots + 1), 2))
    uniform = np.full(len(cells), 1 / len(cells))
    iid = uniform.copy() if gaps == 1 else np.array([(1 if a == b else 2) / slots**2 for a, b in cells])
    assert np.isclose(uniform.sum(), 1) and np.isclose(iid.sum(), 1)
    return cells, uniform, iid


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "confirm"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    low, high = "2023-05-01", "2023-07-01"
    if args.phase == "confirm":
        if not args.freeze or len(args.freeze) != 40 or any(ch not in "0123456789abcdef" for ch in args.freeze):
            raise ValueError("Full freeze SHA required")
        subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"], cwd=ROOT, check=True)
        frozen = subprocess.check_output(["git", "show", f"{args.freeze}:analysis/20_routing_time/H-B07_gap_placement.py"], cwd=ROOT)
        plan = subprocess.check_output(["git", "show", f"{args.freeze}:findings/hypotheses/H-B07_gap_placement.md"], cwd=ROOT)
        if frozen != Path(__file__).read_bytes().replace(b"\r\n", b"\n") or b"**Status:** confirmation-ready" not in plan:
            raise ValueError("Frozen executable and confirmation-ready plan required")
        low, high = "2023-07-01", "2023-08-01"
    with duckdb.connect(config={"memory_limit": "512MB", "threads": 1, "temp_directory": ""}) as conn:
        conn.execute("SET TimeZone='UTC'")
        conn.execute(f"""
            CREATE VIEW paths AS
            SELECT PARTICIPANT_COUNT AS v, ORDERING_BIC8 AS bank,
                   ORDERING_ACCOUNT AS sender, BENEFICIARY_ACCOUNT AS receiver,
                   TRANSACTION_TYPE_CODE AS route, string_split(BIC8_PATH,';') AS p,
                   month(ts_utc) AS month
            FROM read_parquet('dataset/payments.parquet')
            WHERE ANOMALY_TYPE IS NULL AND ts_utc >= TIMESTAMPTZ '{low} 00:00:00+00'
              AND ts_utc < TIMESTAMPTZ '{high} 00:00:00+00'
              AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
        """)
        conn.execute("""
            CREATE VIEW sample AS
            SELECT *, length(p)-v AS g, list_position(p,'...') AS first_gap,
                   length(p)-list_position(list_reverse(p),'...')+1 AS last_gap
            FROM paths WHERE v BETWEEN 3 AND 5 AND length(p)-v IN (1,2)
        """)
        audit = conn.execute("""
            SELECT count(*),count_if(first_gap=1 OR last_gap=length(p)),
                   count_if(len(list_filter(p,lambda item: item<>'...'))<>v)
            FROM sample
        """).fetchone()
        coverage = conn.execute("""
            SELECT count(*),count_if(v>=3),count_if(length(p)>v)
            FROM paths
        """).fetchone()
        lines = [
            f"# H-B07 conditional gap placement: {args.phase}", "",
            f"UTC period [{low}, {high}); unlabelled endpoint bit 0/0; 512MB, one thread, no spill.",
            f"Freeze: {args.freeze or 'exploration only'}. Prior Phase 0/Round 1/Round 2 exposure applies.",
            "The July population has prior outcome exposure and shared entities. Only new shape outcomes were sealed.",
            f"Selected shape population: {audit[0]:,}; endpoint placeholders: {audit[1]}; visible-count mismatches: {audit[2]}.",
            f"Source population: {coverage[0]:,}; multibank: {coverage[1]:,}; paths with any gaps: {coverage[2]:,}.",
            "", "| Visible | Gaps | Payments | Banks | Senders | Receivers | TV uniform shapes | 99% upper | TV iid-slot | TV ratio | Ratio 99% upper | Adjacency share | Uniform adjacency | Iid adjacency |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        passed = audit[1] == 0 and audit[2] == 0
        for visible in range(3, 6):
            for gaps in (1, 2):
                primary = gaps == 1 or visible <= 4
                n, banks, senders, receivers = conn.execute("""
                    SELECT count(*),count(DISTINCT bank),count(DISTINCT sender),count(DISTINCT receiver)
                    FROM sample WHERE v=? AND g=?
                """, [visible, gaps]).fetchone()
                cells, uniform, iid = shape_probabilities(visible, gaps)
                rows = conn.execute("""
                    SELECT bank, first_gap-1 AS a,
                           CASE WHEN g=1 THEN first_gap-1 ELSE last_gap-2 END AS z,count(*)
                    FROM sample WHERE v=? AND g=? GROUP BY ALL ORDER BY bank,a,z
                """, [visible, gaps]).fetchall()
                matrix = np.zeros((banks, len(cells)))
                index = {bank: i for i, bank in enumerate(sorted({row[0] for row in rows}))}
                positions = {cell: i for i, cell in enumerate(cells)}
                for bank, a, z, count in rows:
                    matrix[index[bank], positions[(a, z)]] += count
                assert matrix.sum() == n
                if n < 250 or min(banks, senders, receivers) < 100:
                    lines.append(f"| {visible} | {gaps} | Suppressed | — | — | — | — | — | — | — | — | — | — | — |")
                    passed &= not primary
                    continue
                point = matrix.sum(axis=0)/n
                tv = np.abs(point-uniform).sum()/2
                control_tv = np.abs(point-iid).sum()/2
                rng = np.random.default_rng(20261116 + visible*10 + gaps)
                draws = rng.multinomial(banks, np.full(banks, 1/banks), size=1000) @ matrix
                draws /= draws.sum(axis=1, keepdims=True)
                distance = np.abs(draws-uniform).sum(axis=1)/2
                upper = float(np.quantile(distance, .99))
                if gaps == 2:
                    ratio = tv/control_tv
                    ratios = distance/(np.abs(draws-iid).sum(axis=1)/2)
                    ratio_upper = float(np.quantile(ratios, .99))
                    adjacent = sum(point[i] for i, (a,z) in enumerate(cells) if a==z)
                    model_adjacent = 2/visible
                    iid_adjacent = 1/(visible-1)
                    if primary:
                        passed &= upper <= .06 and ratio_upper <= .50
                    tail = f"{ratio:.6f} | {ratio_upper:.6f} | {adjacent:.6f} | {model_adjacent:.6f} | {iid_adjacent:.6f}"
                else:
                    passed &= upper <= .03
                    tail = "— | — | — | — | —"
                lines.append(f"| {visible} | {gaps} | {n:,} | {banks:,} | {senders:,} | {receivers:,} | {tv:.6f} | {upper:.6f} | {control_tv:.6f} | {tail} |")
        lines.extend([
            "", "## Descriptive shape controls", "",
            "Two-gap conditional shapes only. Require 250 payments and 100 banks, senders and receivers per cohort.",
            "These controls share primary records and do not replace failed primary criteria.",
            "", "| Control | Group | Visible | Payments | Banks | TV uniform | TV iid-slot | Adjacency |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ])
        for control in ("route", "month"):
            groups = conn.execute(f"SELECT DISTINCT {control} FROM sample ORDER BY 1").fetchall()
            for (group,) in groups:
                for visible in range(3, 6):
                    n, banks, senders, receivers = conn.execute(f"""
                        SELECT count(*),count(DISTINCT bank),count(DISTINCT sender),count(DISTINCT receiver)
                        FROM sample WHERE v=? AND g=2 AND {control}=?
                    """, [visible, group]).fetchone()
                    if n < 250 or min(banks, senders, receivers) < 100:
                        lines.append(f"| {control} | {group} | {visible} | Suppressed | — | — | — | — |")
                        continue
                    cells, uniform, iid = shape_probabilities(visible, 2)
                    count_map = dict(((a,z),count) for a,z,count in conn.execute(f"""
                        SELECT first_gap-1, last_gap-2,count(*)
                        FROM sample WHERE v=? AND g=2 AND {control}=?
                        GROUP BY first_gap-1,last_gap-2
                    """, [visible, group]).fetchall())
                    distribution = np.array([count_map.get(cell,0)/n for cell in cells])
                    tv_uniform = np.abs(distribution-uniform).sum()/2
                    tv_iid = np.abs(distribution-iid).sum()/2
                    adjacent = sum(distribution[i] for i,(a,z) in enumerate(cells) if a==z)
                    lines.append(
                        f"| {control} | {group} | {visible} | {n:,} | {banks:,} | "
                        f"{tv_uniform:.6f} | {tv_iid:.6f} | {adjacent:.6f} |"
                    )
        lines.extend([
            "", f"Practical criteria {'PASS' if passed else 'FAIL'} ({'pilot only' if args.phase=='explore' else 'unchanged frozen internal test'}).",
            "Uniform weak compositions give equal probability to each legal sorted gap-slot pattern conditional on counts.",
            "Primary strata: one gap and 3–5 visible banks, or two gaps and 3–4 visible banks. Two gaps with five banks is descriptive.",
            "This also follows from exchangeable ordered visible/placeholder sequences conditional on counts.",
            "It distinguishes iid per-gap slot allocation without identifying unique source implementation or exact probabilities.",
            "Ordering-bank bootstrap intervals measure sensitivity with dependence and prior exposure limitations.",
        ])
    out = Path(__file__).parent / "out" / f"H-B07_gap_placement_{args.phase}.md"
    out.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(f"Wrote aggregate gap-placement report; criteria {'PASS' if passed else 'FAIL'}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        sys.exit(1)

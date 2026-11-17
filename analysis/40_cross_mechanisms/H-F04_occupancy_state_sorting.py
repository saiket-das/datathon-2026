"""H-F04: directed bank-pair FX overlap versus occupancy and state sorting.

EXPLORATORY ONLY. Do not use July outcomes, publish private reports, or infer
causality/hidden generator code from simulated exchangeability benchmarks.

From the repository root with the approved offline DuckDB/Python environment:
    uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --self-test
    uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --data-dir /mnt/f-parquet --phase capacity
    uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --data-dir /mnt/f-parquet --phase permute --population dev
    uv run python analysis/40_cross_mechanisms/H-F04_occupancy_state_sorting.py --data-dir /mnt/f-parquet --phase permute --population P0

All payment-derived output, intermediate tables and spill files remain inside
the local git-ignored dataset/private_reports directory. Source Parquets are
read-only. Every operation uses only May–June 2023 FX0/1 development outcomes;
whole-source metadata-only preflight is permitted. No SQL SELECT-star previews.
Private report files refuse overwrite; preserve failed attempts separately.
Permutations reassign FX within fixed groups, not observed outcome values.
The coordinator must independently check source digests against its private
approved manifest, review disclosure risk, and enforce an external hard cutoff.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import math
import os
from pathlib import Path
import statistics
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dataset" / "private_reports"
REPORT_STEM = "H-F04_occupancy_state_sorting"
CUTOFF_UTC = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
THRESHOLDS = (1, 5, 10, 25, 50, 100)
REPLICATES = 32
BASE_SEED = 20261117
S0 = ("route", "participants", "currency", "party_pair", "gaps")
S1 = S0 + ("ord_country", "ben_country")
DEV_COLUMNS = (
    "row_id", "fx", "route", "participants", "currency", "party_pair",
    "gaps", "ord_country", "ben_country", "ord_bank", "ben_bank",
    "ord_account", "ben_account",
)
SOURCE_COLUMNS = (
    "ROW_ID", "EPOCH_SECONDS", "CURRENCY_CODE", "USD_AMOUNT",
    "ORDERING_BIC8", "BENEFICIARY_BIC8", "BIC8_PATH", "TOTAL_DURATION",
    "CONTINUITY_QFLAG", "CURRENCY_CONVERSION_COUNT", "PARTICIPANT_COUNT",
    "TRANSACTION_TYPE_CODE", "ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT",
    "ORDERING_DETAILS", "ORDERING_TOKENS", "BENEFICIARY_DETAILS",
    "BENEFICIARY_TOKENS", "ORDERING_TYPE", "BENEFICIARY_TYPE",
    "ANOMALY_TYPE", "ts_utc", "ord_country", "ben_country", "path_len",
    "gap_count",
)
MODE_KEYS: dict[str, tuple[str, ...]] = {"M0": (), "M1": S0, "M2": S1}
METRIC_NAMES = ("supported_pairs", "retained_fx0", "retained_fx1",
                "coverage_fx0_pct", "coverage_fx1_pct")


def cutoff() -> None:
    if datetime.now(timezone.utc) >= CUTOFF_UTC:
        raise TimeoutError("Scientific research cutoff reached")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            cutoff()
            chunk = stream.read(8 * 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def parquet_sources(data_dir: Path) -> list[Path]:
    paths = [data_dir / f"payments_part_{i:02d}_of_05.parquet"
             for i in range(1, 6)]
    if any(not p.is_file() for p in paths):
        raise FileNotFoundError("Five complete local Parquet parts required")
    return paths


def literal(paths: list[Path]) -> str:
    return "[" + ", ".join(
        "'" + p.as_posix().replace("'", "''") + "'" for p in paths
    ) + "]"


def configure(con: duckdb.DuckDBPyConnection, scratch: Path) -> None:
    scratch.mkdir(parents=True, exist_ok=True)
    con.execute("SET threads=2")
    con.execute("SET memory_limit='3GB'")
    con.execute("SET TimeZone='UTC'")
    con.execute("SET preserve_insertion_order=false")
    con.execute("SET temp_directory='" +
                scratch.resolve().as_posix().replace("'", "''") + "'")


def setup_dev(con: duckdb.DuckDBPyConnection) -> None:
    """Project exactly the H-F03 development eligibility and necessary IDs."""
    cutoff()
    con.execute("""
        CREATE TEMP TABLE dev AS
        SELECT ROW_ID AS row_id,
               CURRENCY_CONVERSION_COUNT AS fx,
               TRANSACTION_TYPE_CODE AS route,
               PARTICIPANT_COUNT AS participants,
               CURRENCY_CODE AS currency,
               ORDERING_TYPE || BENEFICIARY_TYPE AS party_pair,
               gap_count AS gaps,
               ord_country AS ord_country,
               ben_country AS ben_country,
               ORDERING_BIC8 AS ord_bank,
               BENEFICIARY_BIC8 AS ben_bank,
               ORDERING_ACCOUNT AS ord_account,
               BENEFICIARY_ACCOUNT AS ben_account
        FROM payments_source
        WHERE ts_utc >= TIMESTAMP '2023-05-01'
          AND ts_utc < TIMESTAMP '2023-07-01'
          AND ANOMALY_TYPE IS NULL
          AND TOTAL_DURATION >= 0 AND USD_AMOUNT >= 0
          AND PARTICIPANT_COUNT BETWEEN 2 AND 5
          AND CURRENCY_CONVERSION_COUNT IN (0,1)
    """)


def setup_p0(con: duckdb.DuckDBPyConnection) -> None:
    cutoff()
    keys = ", ".join(S0)
    on = " AND ".join(f"d.{key} IS NOT DISTINCT FROM s.{key}" for key in S0)
    projections = ", ".join("d." + key for key in DEV_COLUMNS)
    con.execute(f"""
        CREATE TEMP TABLE support_p0 AS
        SELECT {keys} FROM dev
        GROUP BY {keys}
        HAVING count(*) FILTER (WHERE fx=0) >= 100
           AND count(*) FILTER (WHERE fx=1) >= 100
    """)
    con.execute(f"""
        CREATE TEMP VIEW p0 AS
        SELECT {projections}
        FROM dev AS d INNER JOIN support_p0 AS s ON {on}
    """)


def pop_counts(con: duckdb.DuckDBPyConnection,
               population: str) -> tuple[int, int, int]:
    if population not in ("dev", "p0"):
        raise ValueError("Unexpected population")
    cutoff()
    n, n0, n1 = con.execute(f"""
        SELECT count(*), count(*) FILTER (WHERE fx=0),
               count(*) FILTER (WHERE fx=1)
        FROM {population}
    """).fetchone()
    if n != n0 + n1:
        raise ArithmeticError("FX count conservation failed")
    return int(n), int(n0), int(n1)


def pair_counts(con: duckdb.DuckDBPyConnection,
                population: str, table: str) -> None:
    if population not in ("dev", "p0") or table not in ("bank_dev", "bank_p0"):
        raise ValueError("Unexpected bank pair population/table")
    cutoff()
    con.execute(f"""
        CREATE TEMP TABLE {table} AS
        SELECT ord_bank, ben_bank, count(*) AS n,
               count(*) FILTER (WHERE fx=0) AS n0,
               count(*) FILTER (WHERE fx=1) AS n1
        FROM {population}
        GROUP BY ord_bank, ben_bank
    """)


def private_bank_summary(con: duckdb.DuckDBPyConnection,
                         table: str) -> dict[str, object]:
    cutoff()
    result = con.execute(f"""
        SELECT count(*) AS pairs,
               count(*) FILTER (WHERE n0 > 0 AND n1 > 0) AS mixed,
               count(*) FILTER (WHERE n0 > 0 AND n1 = 0) AS fx0_only,
               count(*) FILTER (WHERE n0 = 0 AND n1 > 0) AS fx1_only,
               min(n), max(n), avg(n), quantile_cont(n, 0.50),
               quantile_cont(n, 0.90), quantile_cont(n, 0.99)
        FROM {table}
    """).fetchone()
    keys = ("pairs", "mixed", "fx0_only", "fx1_only",
            "pair_size_min", "pair_size_max", "pair_size_mean",
            "pair_size_p50", "pair_size_p90", "pair_size_p99")
    output = dict(zip(keys, result, strict=True))
    if output["pairs"] != (output["mixed"]+output["fx0_only"]+
                            output["fx1_only"]):
        raise ArithmeticError("Pair state partition failed")
    return output


def support_thresholds(con: duckdb.DuckDBPyConnection, table: str,
                       n0: int, n1: int,
                       with_capacity: bool) -> list[tuple]:
    """Only aggregate threshold rows leave this SQL statement."""
    cutoff()
    levels = ",".join(map(str, THRESHOLDS))
    capacity_sql = ("""count(*) FILTER (WHERE n >= 2*t.min_state) AS capacity_pairs,"""
                    if with_capacity else """cast(NULL AS BIGINT) AS capacity_pairs,""")
    rows = con.execute(f"""
        WITH levels AS (SELECT unnest([{levels}]) AS min_state)
        SELECT t.min_state, {capacity_sql}
               count(*) FILTER (WHERE n0 >= t.min_state AND n1 >= t.min_state)
                    AS supported_pairs,
               coalesce(sum(n0) FILTER (WHERE n0 >= t.min_state
                                       AND n1 >= t.min_state),0)
                    AS retained_fx0,
               coalesce(sum(n1) FILTER (WHERE n0 >= t.min_state
                                       AND n1 >= t.min_state),0)
                    AS retained_fx1
        FROM {table} AS p CROSS JOIN levels AS t
        GROUP BY t.min_state ORDER BY t.min_state
    """).fetchall()
    if tuple(int(row[0]) for row in rows) != THRESHOLDS:
        raise ArithmeticError("Missing prespecified threshold")
    output = []
    for (t, capacity, mixed, keep0, keep1) in rows:
        if keep0 > n0 or keep1 > n1:
            raise ArithmeticError("Retained population exceeds source")
        if with_capacity and mixed > capacity:
            raise ArithmeticError("Support exceeds occupancy capacity")
        output.append((int(t),capacity,int(mixed),int(keep0),int(keep1),
                       100*keep0/n0 if n0 else None,
                       100*keep1/n1 if n1 else None,
                       100*mixed/capacity if capacity else None))
    for before,after in zip(output,output[1:]):
        if any(after[k] > before[k] for k in (2,3,4)):
            raise ArithmeticError("Nonmonotonic threshold retention")
    return output


def account_diagnostic(con: duckdb.DuckDBPyConnection,
                       population: str) -> dict[str, object]:
    """Aggregate only; NULL account keys excluded from this diagnostic alone."""
    cutoff()
    if population not in ("dev","p0"):
        raise ValueError("Unexpected account population")
    missing = con.execute(f"""
        SELECT count(*) FILTER (WHERE ord_account IS NULL
                                 OR ben_account IS NULL)
        FROM {population}
    """).fetchone()[0]
    con.execute(f"""
        CREATE TEMP TABLE account_{population} AS
        SELECT ord_account, ben_account, count(*) AS n,
               count(*) FILTER (WHERE fx=0) AS n0,
               count(*) FILTER (WHERE fx=1) AS n1
        FROM {population}
        WHERE ord_account IS NOT NULL AND ben_account IS NOT NULL
        GROUP BY ord_account, ben_account
    """)
    values = con.execute(f"""
        SELECT count(*) AS pairs,
               count(*) FILTER (WHERE n >= 2) AS repeated_pairs,
               coalesce(sum(n) FILTER (WHERE n >= 2),0) AS rows_repeated,
               count(*) FILTER (WHERE n0>0 AND n1>0) AS mixed_pairs,
               coalesce(sum(n) FILTER (WHERE n0>0 AND n1>0),0)
                   AS mixed_pair_rows,
               quantile_cont(n,0.5), quantile_cont(n,0.9),
               quantile_cont(n,0.99)
        FROM account_{population}
    """).fetchone()
    con.execute(f"DROP TABLE account_{population}")
    keys = ("account_pairs", "repeated_pairs", "rows_repeated",
            "mixed_pairs", "mixed_pair_rows", "size_p50","size_p90","size_p99")
    return {"excluded_null_account_rows":int(missing),
            **dict(zip(keys,values,strict=True))}


def allocate(con: duckdb.DuckDBPyConnection, population: str,
             mode: str, seed: int) -> None:
    """Generate exact fixed-marginal simulated assignments as bank counts."""
    cutoff()
    if mode not in MODE_KEYS or population not in ("dev","p0"):
        raise ValueError("Invalid exploratory allocation mode")
    if not (BASE_SEED <= seed < BASE_SEED + REPLICATES):
        raise ValueError("Unregistered permutation seed")
    keys = MODE_KEYS[mode]
    partition = ("PARTITION BY " + ", ".join(keys)) if keys else ""
    order_by = "ORDER BY hash(row_id, " + str(seed) + "), row_id"
    con.execute("""
        CREATE TEMP TABLE perm_pairs AS
        WITH ranked AS (
            SELECT ord_bank, ben_bank,
                   fx, row_number() OVER (""" + partition + " " + order_by + """)
                       AS rank_within_group,
                   sum(fx) OVER (""" + partition + """) AS fx1_in_group
            FROM """ + population + """
        ), assigned AS (
            SELECT ord_bank, ben_bank,
                   CASE WHEN rank_within_group <= fx1_in_group
                        THEN 1 ELSE 0 END AS assigned_fx
            FROM ranked
        )
        SELECT ord_bank, ben_bank, count(*) AS n,
               count(*) FILTER (WHERE assigned_fx=0) AS n0,
               count(*) FILTER (WHERE assigned_fx=1) AS n1
        FROM assigned
        GROUP BY ord_bank, ben_bank
    """)


def quantile(values: list[float], p: float) -> float:
    values = sorted(values)
    if len(values) != REPLICATES:
        raise ValueError("Missing simulation replicates")
    x = (len(values) - 1) * p
    lo,hi = math.floor(x),math.ceil(x)
    return values[lo] + (x-lo)*(values[hi]-values[lo])


def fmt(x: object) -> str:
    if x is None:
        return "unsupported"
    if isinstance(x,float):
        return f"{x:.9f}"
    return str(x)


def markdown_table(fields: tuple[str,...], rows: list[tuple]) -> list[str]:
    return ["| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |"] + [
            "| " + " | ".join(fmt(c) for c in row) + " |" for row in rows]


def report_filename(phase: str, population: str | None) -> Path:
    suffix = "capacity" if phase == "capacity" else "perm_" + str(population)
    return PRIVATE / (REPORT_STEM + "_" + suffix + ".md")


def save_exclusive(target: Path, lines: list[str]) -> None:
    """No stale report overwrite; .partial preserved on interrupted runs."""
    cutoff()
    stage = target.with_suffix(".md.partial")
    if target.exists() or stage.exists():
        raise FileExistsError("Previous private report/partial must be preserved")
    with stage.open("x",encoding="utf-8") as stream:
        stream.write("\n".join(lines) + "\n")
    cutoff()
    os.replace(stage,target)


def report_header(phase: str, population: str | None,
                  script_sha: str, source_sha: list[str]) -> list[str]:
    return [
        "# H-F04 — PRIVATE exploratory " + phase + " diagnostics",
        "",
        "**Never commit, publish or quote this restricted report publicly.**",
        "**No frozen validation, causal inference, independent replication or July outcomes.**",
        "Produced UTC: " + datetime.now(timezone.utc).isoformat(),
        "Phase: " + phase + "; population: " + str(population),
        "Script SHA-256: " + script_sha,
        "Local source SHA-256 (coordinator must match to approved private manifest):",
        *["- Part " + str(i+1) + ": " + x for i,x in enumerate(source_sha)],
        "",
    ]


def capacity_phase(con: duckdb.DuckDBPyConnection,
                   header: list[str]) -> list[str]:
    lines = header + [
        "## Occupancy feasibility and directed-bank support",
        "",
        "Cap(t) = number of bank pairs with at least 2*t payments total.",
        "Cap is necessary but not sufficient for >=t payments per FX state.",
        "NULL directed bank BIC keys are grouped, never imputed.",
        "",
    ]
    for population in ("dev","p0"):
        cutoff()
        total,n0,n1=pop_counts(con,population)
        table = "bank_"+population
        pair_counts(con,population,table)
        summary = private_bank_summary(con,table)
        rows = support_thresholds(con,table,n0,n1,True)
        lines.extend(["### "+population,"",f"Development population n={total}, FX0={n0}, FX1={n1}",
                      ""])
        lines.extend([f"- {k}: {fmt(v)}" for k,v in summary.items()])
        lines.extend(markdown_table(
            ("t","capacity_pairs","supported_pairs","retained_fx0",
             "retained_fx1","FX0 coverage %","FX1 coverage %","supported/capacity %"),
            rows))
        lines.extend(["","### Repeated account-pair diagnostic: "+population,""])
        account=account_diagnostic(con,population)
        lines.extend([f"- {k}: {fmt(v)}" for k,v in account.items()])
        lines.append("")
        con.execute("DROP TABLE "+table)
    lines += [
        "## Limitations",
        "- Capacity may be small even without bank-specific FX constraints.",
        "- Account-pair concentration is not a bank causal test.",
        "- Repeated accounts and bank dependence invalidate naive row-level uncertainty.",
        "- No bank, account, hash identifier or raw record is exported.",
        "- All findings remain private, exploratory and previously exposed to F.",
        "",
    ]
    return lines


def permutation_phase(con: duckdb.DuckDBPyConnection, population: str,
                      header: list[str]) -> list[str]:
    cutoff()
    n,n0,n1=pop_counts(con,population)
    lines=header+[
        "## Fixed-marginal permutation benchmarks",
        "",
        f"Population {population}: n={n}, FX0={n0}, FX1={n1}",
        "M0=global; M1=S0-conditioned; M2=S1/corridor-conditioned.",
        "32 deterministic seeds per mode; exact within-group FX totals.",
        "These are descriptive exchangeability benchmarks, NOT inferential CIs.",
        "The same observed rows and directed-bank occupancy are fixed per mode.",
        "",
    ]
    for mode in ("M0","M1","M2"):
        cutoff()
        captured=[]
        for rep in range(REPLICATES):
            cutoff()
            seed=BASE_SEED+rep
            allocate(con,population,mode,seed)
            try:
                total_0,total_1=con.execute(
                    "SELECT coalesce(sum(n0),0), coalesce(sum(n1),0) "
                    "FROM perm_pairs"
                ).fetchone()
                if int(total_0)!=n0 or int(total_1)!=n1:
                    raise ArithmeticError("Permutation FX marginals changed")
                thresholds=support_thresholds(con,"perm_pairs",n0,n1,False)
                captured.append((rep,thresholds))
            finally:
                con.execute("DROP TABLE IF EXISTS perm_pairs")
        if len(captured)!=REPLICATES:
            raise ArithmeticError("Fewer than fixed 32 replicate allocations")
        lines.extend(["### "+mode,""])
        dist=[]
        for i,t in enumerate(THRESHOLDS):
            for j,label in ((2,"supported_pairs"),(5,"FX0 coverage %"),
                            (6,"FX1 coverage %")):
                values=[float(rows[i][j]) for _,rows in captured]
                dist.append((t,label,min(values),quantile(values,0.10),
                             statistics.median(values),quantile(values,0.90),
                             max(values)))
        lines.extend(markdown_table(
            ("threshold","metric","min","q10","median","q90","max"),dist))
        lines.append("")
        # Preserve all single-run aggregates privately. This is not a
        # publication-safe table, and is never exposed to model stdout.
        lines.extend(["#### Private per-replicate audit", ""])
        audit=[]
        for rep,thresholds in captured:
            for level in thresholds:
                audit.append((rep,level[0],level[2],level[3],level[4]))
        lines.extend(markdown_table(
            ("replicate","threshold","supported_pairs",
             "retained_fx0","retained_fx1"),audit))
        lines.append("")
    lines+= [
        "## Interpretation constraints",
        "- If all benchmarks have little capacity, a bank-specific rule is not identified.",
        "- M0/M1/M2 are alternative, often implausible label-exchangeability models.",
        "- A difference from permutations can reflect repeated accounts or unmodelled",
        "  paths, schedules or conditioned country/amount mix.",
        "- No permutation p-values, valid row-independent CIs, or causal conclusions.",
        "- H-F01's original invocation remains unknown; H-F03 is not rerun here.",
        "",
    ]
    return lines


def self_test() -> None:
    """Synthetic source-typed test of SQL, nullable keys and exact label margins."""
    con=duckdb.connect()
    try:
        con.execute("""
            CREATE TEMP TABLE payments_source (
                ROW_ID BIGINT, CURRENCY_CONVERSION_COUNT INTEGER,
                TRANSACTION_TYPE_CODE VARCHAR, PARTICIPANT_COUNT INTEGER,
                CURRENCY_CODE VARCHAR, ORDERING_TYPE VARCHAR,
                BENEFICIARY_TYPE VARCHAR, gap_count INTEGER,
                ord_country VARCHAR, ben_country VARCHAR,
                ORDERING_BIC8 VARCHAR, BENEFICIARY_BIC8 VARCHAR,
                ORDERING_ACCOUNT VARCHAR, BENEFICIARY_ACCOUNT VARCHAR,
                ts_utc TIMESTAMP, ANOMALY_TYPE VARCHAR,
                TOTAL_DURATION DOUBLE, USD_AMOUNT DOUBLE
            )
        """)
        rows=[]
        row_id=0
        for route,currency,cc,bn in (
            ("Direct","USD","US","BANK_A"),
            ("Indirect","EUR","GB","BANK_B"),
            (None,None,None,"BANK_NULL"),
        ):
            for fx in (0,1):
                for j in range(120):
                    row_id+=1
                    rows.append((row_id,fx,route,2,currency,
                                 None if route is None else "B","C",
                                 0 if route is not None else None,cc,
                                 None if route is None else "SG",
                                 bn,"BANK_TARGET","ACC_"+str(j%11),
                                 "BEN_"+str(j%7),datetime(2023,5,15),
                                 None, float(10+j), float(100+j)))
        con.executemany(
            "INSERT INTO payments_source VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            rows)
        setup_dev(con)
        setup_p0(con)
        if pop_counts(con,"dev") != (720,360,360):
            raise ArithmeticError("Synthetic development cohort mismatch")
        if pop_counts(con,"p0") != (720,360,360):
            raise ArithmeticError("Supported synthetic NULL strata lost")
        for pop in ("dev","p0"):
            table="bank_"+pop
            pair_counts(con,pop,table)
            if private_bank_summary(con,table)["pairs"]!=3:
                raise AssertionError("Unexpected fixture pair count")
            summary=support_thresholds(con,table,360,360,True)
            if summary[0][2]!=3 or summary[-1][2]!=3:
                raise AssertionError("Unexpected fixture support across thresholds")
            con.execute("DROP TABLE "+table)
            diagnostic=account_diagnostic(con,pop)
            if diagnostic["account_pairs"]<=0:
                raise AssertionError("Missing synthetic repeated account pairs")
            for mode in ("M0","M1","M2"):
                allocate(con,pop,mode,BASE_SEED)
                try:
                    p0,p1=con.execute(
                        "SELECT sum(n0), sum(n1) FROM perm_pairs"
                    ).fetchone()
                    if (p0,p1)!=(360,360):
                        raise AssertionError("FX marginals not conserved")
                    support_thresholds(con,"perm_pairs",360,360,False)
                finally:
                    con.execute("DROP TABLE IF EXISTS perm_pairs")
    finally:
        con.close()
    print("OK: H-F04 invented-fixture calculations passed; no sponsor data accessed.")


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--data-dir",type=Path,default=ROOT/"dataset")
    ap.add_argument("--phase",choices=("capacity","permute"))
    ap.add_argument("--population",choices=("dev","P0"))
    args=ap.parse_args()
    try:
        cutoff()
        if args.self_test:
            self_test()
            return 0
        if not args.phase or (args.phase=="permute")!=bool(args.population):
            raise ValueError("Select capacity, or permute with a population")
        population = None if args.population is None else args.population.lower()
        PRIVATE.mkdir(parents=True,exist_ok=True)
        target=report_filename(args.phase,population)
        if target.exists() or target.with_suffix(".md.partial").exists():
            raise FileExistsError("Preserve prior private report; refuse overwrite")
        paths=parquet_sources(args.data_dir.resolve())
        local_hashes=[sha256_file(p) for p in paths]
        cutoff()
        con=duckdb.connect()
        try:
            configure(con,PRIVATE/".duckdb_tmp")
            projection=", ".join(SOURCE_COLUMNS)
            con.execute("CREATE TEMP VIEW payments_source AS SELECT "+
                        projection+" FROM read_parquet("+literal(paths)+")")
            actual={x[0] for x in con.execute(
                "DESCRIBE payments_source").fetchall()}
            if actual!=set(SOURCE_COLUMNS):
                raise ValueError("Expected exact 26-column source schema")
            n,unique=con.execute(
                "SELECT count(*), count(DISTINCT ROW_ID) FROM payments_source"
            ).fetchone()
            if n!=10_000_000 or unique!=n:
                raise ValueError("Expected 10M unique source IDs")
            for path in paths:
                cutoff()
                part_n=con.execute("SELECT count(*) FROM read_parquet("+
                                   literal([path])+")").fetchone()[0]
                if part_n!=2_000_000:
                    raise ValueError("Split partition count mismatch")
            setup_dev(con)
            setup_p0(con)
            all_counts=pop_counts(con,"dev")
            common_counts=pop_counts(con,"p0")
            if any(x<y for x,y in zip(all_counts,common_counts)):
                raise ArithmeticError("P0 exceeds May–June development universe")
            cutoff()
            local_script_hash=sha256_file(Path(__file__))
            header=report_header(args.phase,population,local_script_hash,
                                 local_hashes)
            if args.phase=="capacity":
                lines=capacity_phase(con,header)
            else:
                lines=permutation_phase(con,population,header)
            cutoff()
            save_exclusive(target,lines)
            print("OK: H-F04 PRIVATE exploratory phase completed; coordinator review required.")
            return 0
        finally:
            con.close()
    except Exception as err:
        # Keep potentially sensitive DuckDB error messages and paths private.
        print("ERROR: "+type(err).__name__+
              "; specifics intentionally withheld to protect sponsor data.",
              file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())

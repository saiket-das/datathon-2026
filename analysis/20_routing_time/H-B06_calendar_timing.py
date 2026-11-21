"""Screen timing and calendar composition on the B exploration partition.

Run from the repository root:
    uv run python analysis/20_routing_time/H-B06_calendar_timing.py
Frozen internal validation:
    uv run python analysis/20_routing_time/H-B06_calendar_timing.py --phase confirm --freeze SHA
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]


def sensitivity(connection: duckdb.DuckDBPyConnection, explore: bool) -> tuple[list[str], tuple]:
    """Compute cohort summaries for the original B06 contrast and pre-validation challenges."""
    primary = "bank, route, parties, mon"
    cases = [
        ("Primary", primary, "weekend", "TRUE", 30),
        ("May", primary, "weekend", "mon=5", 30),
        ("June", primary, "weekend", "mon=6", 30),
        ("Saturday vs weekdays", primary, "weekday=6", "weekday<>7", 15),
        ("Sunday vs weekdays", primary, "weekday=7", "weekday<>6", 15),
        ("Placebo: Mon-Tue vs Wed-Fri", primary, "weekday<=2", "weekday<=5", 30),
        ("Minimum support 10", primary, "weekend", "TRUE", 10),
        ("Minimum support 50", primary, "weekend", "TRUE", 50),
        ("Also match beneficiary country", primary + ", beneficiary_country", "weekend", "TRUE", 30),
        ("Also match beneficiary country and currency", primary + ", beneficiary_country, currency", "weekend", "TRUE", 30),
        ("Also match beneficiary bank", primary + ", beneficiary_bank", "weekend", "TRUE", 30),
        ("Also match ordering account", primary + ", sender", "weekend", "TRUE", 30),
        ("Same declared bank country", primary, "weekend", "same_country", 30),
        ("Different declared bank countries", primary, "weekend", "NOT same_country", 30),
    ]
    if not explore:
        cases = [case for case in cases if case[0] in ("Primary", "Placebo: Mon-Tue vs Wed-Fri")]
    placebo: tuple = ()
    lines = [
        "## Pre-validation challenges" if explore else "## Primary and weekday placebo contrasts", "",
        "Positive contrast means a higher UTC daytime share in the first calendar group.",
        "All estimates use smaller-group weights. Matched rows require 100 ordering banks.",
        "Coverage denominators are the corresponding calendar groups before support filtering.",
        "Suppressed rows have inadequate bank support. Date, bank and account composition can still differ.",
        "",
        "| Contrast | Banks | Strata | Group 1 payments | Group 2 payments | Group 1 coverage | Group 2 coverage | Difference (pp) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label, strata, first, cohort, minimum in cases:
        row = connection.execute(f"""
            WITH counts AS (
                SELECT {strata}, count_if({first}) n1, count_if(NOT ({first})) n2,
                       count_if(({first}) AND daytime) y1,
                       count_if(NOT ({first}) AND daytime) y2
                FROM timing WHERE {cohort} GROUP BY {strata}
            ), scored AS (
                SELECT *, least(n1,n2) AS weight, y1/n1-y2/n2 AS delta
                FROM counts WHERE n1 >= ? AND n2 >= ?
            ), denominators AS (
                SELECT sum(n1) AS all1, sum(n2) AS all2 FROM counts
            )
            SELECT count(DISTINCT bank), count(*), sum(n1), sum(n2),
                   sum(n1)/any_value(all1), sum(n2)/any_value(all2),
                   sum(delta*weight)/sum(weight)
            FROM scored CROSS JOIN denominators
        """, [minimum, minimum]).fetchone()
        assert row is not None
        if label.startswith("Placebo"):
            placebo = row
        banks, groups, n1, n2, coverage1, coverage2, gap = row
        if banks < 100:
            lines.append(f"| {label} | Suppressed | — | — | — | — | — | — |")
            continue
        lines.append(
            f"| {label} | {banks:,} | {groups:,} | {n1:,} | {n2:,} | "
            f"{coverage1:.2%} | {coverage2:.2%} | {gap*100:.4f} |"
        )
    return lines, placebo


def omit_calendar_week(connection: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Recompute original eligibility and contrast after omitting each UTC week."""
    return connection.execute("""
        WITH week_counts AS (
            SELECT bank, route, parties, mon, date_trunc('week', day) AS week,
                   count_if(weekend) AS n_we, count_if(NOT weekend) AS n_wd,
                   count_if(weekend AND daytime) AS y_we,
                   count_if(NOT weekend AND daytime) AS y_wd
            FROM timing GROUP BY ALL
        ), totals AS (
            SELECT bank, route, parties, mon, sum(n_we) AS n_we, sum(n_wd) AS n_wd,
                   sum(y_we) AS y_we, sum(y_wd) AS y_wd
            FROM week_counts GROUP BY ALL
        ), weeks AS (
            SELECT week, sum(n_we) AS n_we, sum(n_wd) AS n_wd
            FROM week_counts GROUP BY week
        ), others AS (
            SELECT t.bank, w.week, t.n_we-coalesce(k.n_we,0) AS n_we,
                   t.n_wd-coalesce(k.n_wd,0) AS n_wd,
                   t.y_we-coalesce(k.y_we,0) AS y_we,
                   t.y_wd-coalesce(k.y_wd,0) AS y_wd
            FROM totals t CROSS JOIN weeks w
            LEFT JOIN week_counts k
              ON (t.bank,t.route,t.parties,t.mon,w.week) = (k.bank,k.route,k.parties,k.mon,k.week)
        ), scored AS (
            SELECT bank, week, n_we, n_wd, least(n_we,n_wd) AS wt, y_we/n_we-y_wd/n_wd AS gap
            FROM others WHERE n_we >= 30 AND n_wd >= 30
        ), population AS (
            SELECT sum(n_we) AS n_we, sum(n_wd) AS n_wd FROM weeks
        )
        SELECT w.week, count(DISTINCT s.bank), count(s.bank), sum(s.n_we), sum(s.n_wd),
               sum(s.n_we)/any_value(p.n_we-w.n_we), sum(s.n_wd)/any_value(p.n_wd-w.n_wd),
               sum(wt*gap)/sum(wt)
        FROM weeks w CROSS JOIN population p LEFT JOIN scored s ON w.week=s.week
        GROUP BY w.week ORDER BY w.week
    """).fetchall()


def main() -> None:
    """Read local Parquet and write only supported aggregate statistics."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "confirm"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    explore = args.phase == "explore"
    if explore and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise RuntimeError("Research cutoff reached")
    lower, upper = "2023-05-01", "2023-07-01"
    if not explore:
        if not args.freeze or len(args.freeze) != 40 or any(char not in "0123456789abcdef" for char in args.freeze):
            parser.error("Confirmation requires a full 40-character Git freeze SHA")
        subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"], cwd=ROOT, check=True)
        plan_path = "findings/hypotheses/H-B06_calendar_timing.md"
        code_path = Path(__file__).relative_to(ROOT).as_posix()
        freeze_plan = subprocess.check_output(["git", "show", f"{args.freeze}:{plan_path}"], cwd=ROOT)
        freeze_code = subprocess.check_output(["git", "show", f"{args.freeze}:{code_path}"], cwd=ROOT)
        if b"**Status:** confirmation-ready" not in freeze_plan:
            raise ValueError("Freeze must contain a confirmation-ready plan")
        if freeze_code != Path(__file__).read_bytes().replace(b"\r\n", b"\n"):
            raise ValueError("Executable does not match the freeze")
        lower, upper = "2023-07-01", "2023-08-01"
    with duckdb.connect(config={"memory_limit": "512MB", "threads": "1", "temp_directory": ""}) as connection:
        connection.execute("SET TimeZone='UTC'")
        connection.execute(f"""
            CREATE TEMP VIEW timing AS
            SELECT EPOCH_SECONDS AS epoch, hour(ts_utc) BETWEEN 6 AND 17 AS daytime,
                   isodow(ts_utc) > 5 AS weekend, CAST(ts_utc AS DATE) AS day,
                   month(ts_utc) AS mon, isodow(ts_utc) AS weekday, TRANSACTION_TYPE_CODE AS route,
                   ORDERING_TYPE || BENEFICIARY_TYPE AS parties, ORDERING_BIC8 AS bank,
                   BENEFICIARY_BIC8 AS beneficiary_bank,
                   substring(BENEFICIARY_BIC8, 5, 2) AS beneficiary_country,
                   substring(ORDERING_BIC8, 5, 2) = substring(BENEFICIARY_BIC8, 5, 2) AS same_country,
                   CURRENCY_CODE AS currency, ORDERING_ACCOUNT AS sender
            FROM read_parquet('dataset/payments.parquet')
            WHERE ANOMALY_TYPE IS NULL AND ts_utc >= TIMESTAMPTZ '{lower} 00:00:00+00'
              AND ts_utc < TIMESTAMPTZ '{upper} 00:00:00+00'
              AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
        """)
        boundaries = connection.execute("""
            SELECT count(*), count(DISTINCT day), count(DISTINCT bank),
                   avg((epoch%5=0)::int), avg((epoch%60=0)::int), avg((epoch%3600=0)::int)
            FROM timing
        """).fetchone()
        daily = connection.execute("""
            SELECT weekend, count(*), count(DISTINCT day), count(DISTINCT bank), avg(daytime::int)
            FROM timing GROUP BY weekend ORDER BY weekend
        """).fetchall()
        matched = connection.execute("""
            WITH counts AS (
                SELECT bank, route, parties, mon,
                       count_if(weekend) AS n_we, count_if(NOT weekend) AS n_wd,
                       avg(daytime::int) FILTER (WHERE weekend) AS p_we,
                       avg(daytime::int) FILTER (WHERE NOT weekend) AS p_wd
                FROM timing GROUP BY bank, route, parties, mon
            ), eligible AS (
                SELECT bank, route, n_we, n_wd, p_we-p_wd AS delta, least(n_we,n_wd) AS weight
                FROM counts WHERE n_we >= 30 AND n_wd >= 30
            )
            SELECT coalesce(route, 'All'), count(*), count(DISTINCT bank), sum(n_we), sum(n_wd),
                   sum(delta*weight)/sum(weight), avg(delta), avg((delta<0)::int)
            FROM eligible GROUP BY GROUPING SETS ((route), ())
            HAVING count(DISTINCT bank) >= 100 ORDER BY 1
        """).fetchall()
        if boundaries is None or min(boundaries[:3]) <= 0 or len(daily) != 2:
            raise ValueError("Incomplete timing population")
        n, days, banks, second5, minute, hour = boundaries
        lines = [
            f"# H-B06: UTC calendar timing {args.phase}", "",
            f"UTC period [{lower}, {upper}). Unlabelled endpoint bit 0/0.",
            ("Exploration only. No validation was opened." if explore else
             f"Frozen internal validation: {args.freeze}. July records have earlier aggregate exposure."),
            "512MB, one thread, no spill. Daytime denotes 06:00–17:59 UTC.", "",
            f"{n:,} payments, {days} dates and {banks:,} ordering banks.", "",
            "| Alignment | Observed share | Uniform within-hour reference |",
            "| --- | ---: | ---: |",
        ]
        for name, observed, denominator in [("5 seconds", second5, 5), ("Minute", minute, 60), ("Hour", hour, 3600)]:
            lines.append(f"| {name} | {observed:.6%} | {1/denominator:.6%} |")
        lines.extend(["", "| Calendar | Payments | Dates | Ordering banks | Mean payments/day | UTC daytime share |",
                      "| --- | ---: | ---: | ---: | ---: | ---: |"])
        for weekend, count, dates, support, daytime in daily:
            lines.append(f"| {'Weekend' if weekend else 'Weekday'} | {count:,} | {dates} | {support:,} | {count/dates:,.2f} | {daytime:.4%} |")
        lines.extend([
            "", "Matched calendar contrast within ordering bank, route, party pair and month.",
            "Each stratum has at least 30 payments of each calendar type. Weights are the smaller count.",
            "Route rows with fewer than 100 supported ordering banks are suppressed.", "",
            "| Route | Strata | Banks | Weekend payments | Weekday payments | Weighted delta (pp) | Equal-stratum delta (pp) | Strata with negative delta |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for route, strata, support, we, wd, weighted, equal, negative in matched:
            lines.append(f"| {route} | {strata:,} | {support:,} | {we:,} | {wd:,} | {weighted*100:.4f} | {equal*100:.4f} | {negative:.4%} |")
        challenges, placebo = sensitivity(connection, explore)
        challenges.extend([
            "", "## Leave-one-UTC-week-out sensitivities", "",
            "Remove all included dates in each Monday-start block, then recompute matching and support.",
            "This range measures sensitivity to observed calendar blocks, without a confidence interval.", "",
            "| Omitted week starting | Banks | Strata | Weekend payments | Weekday payments | Weekend coverage | Weekday coverage | Difference (pp) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        weeks = omit_calendar_week(connection)
        for week, banks, strata, we, wd, we_coverage, wd_coverage, gap in weeks:
            if banks < 100:
                challenges.append(f"| {week} | Suppressed | — | — | — | — | — | — |")
                continue
            challenges.append(
                f"| {week} | {banks:,} | {strata:,} | {we:,} | {wd:,} | "
                f"{we_coverage:.2%} | {wd_coverage:.2%} | {gap*100:.4f} |"
            )
    out = Path(__file__).parent / "out"
    if explore:
        (out / "H-B06_calendar_timing_sensitivity.md").write_text(
            "# H-B06: May–June exploratory composition checks\n\n" + "\n".join(challenges) + "\n",
            encoding="utf-8",
        )
    else:
        primary = next((row for row in matched if row[0] == "All"), None)
        criteria = {
            "Primary support": (primary is not None and primary[3] / daily[1][1] >= .30
                                and primary[4] / daily[0][1] >= .30),
            "Primary contrast at most −3 points": primary is not None and primary[5] <= -.03,
            "Week omission support and direction": (len(weeks) >= 4 and all(
                banks >= 100 and we_cov >= .20 and wd_cov >= .20 and gap <= -.01
                for _, banks, _, _, _, we_cov, wd_cov, gap in weeks
            )),
            "Placebo within 3 points": placebo[0] >= 100 and abs(placebo[-1]) < .03,
        }
        lines.extend(["", "## Frozen decision", ""])
        lines.extend(f"- {name}: {'PASS' if passed else 'FAIL'}" for name, passed in criteria.items())
        lines.extend(["", f"Overall: {'PASS' if all(criteria.values()) else 'FAIL'}.", "", *challenges])
        (out / "H-B06_calendar_timing_confirm.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote H-B06 {args.phase} aggregates.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}. Details hidden to protect sponsor values.", file=sys.stderr)
        sys.exit(1)

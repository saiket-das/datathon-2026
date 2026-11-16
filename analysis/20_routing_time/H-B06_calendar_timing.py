"""Screen timing and calendar composition on the B exploration partition.

Run from the repository root:
    uv run python analysis/20_routing_time/H-B06_calendar_timing.py
"""
from datetime import datetime, timezone
from pathlib import Path
import sys

import duckdb


def main() -> None:
    """Read local Parquet and write only supported aggregate statistics."""
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise RuntimeError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit": "512MB", "threads": "1", "temp_directory": ""}) as connection:
        connection.execute("SET TimeZone='UTC'")
        connection.execute("""
            CREATE TEMP VIEW timing AS
            SELECT EPOCH_SECONDS AS epoch, hour(ts_utc) BETWEEN 6 AND 17 AS daytime,
                   isodow(ts_utc) > 5 AS weekend, CAST(ts_utc AS DATE) AS day,
                   month(ts_utc) AS mon, TRANSACTION_TYPE_CODE AS route,
                   ORDERING_TYPE || BENEFICIARY_TYPE AS parties, ORDERING_BIC8 AS bank
            FROM read_parquet('dataset/payments.parquet')
            WHERE ANOMALY_TYPE IS NULL AND ts_utc >= TIMESTAMPTZ '2023-05-01 00:00:00+00'
              AND ts_utc < TIMESTAMPTZ '2023-07-01 00:00:00+00'
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
            "# H-B06: UTC calendar timing exploration", "",
            "May and June unlabelled endpoint bit 0/0. No validation was opened.",
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
    output = Path(__file__).parent / "out" / "H-B06_calendar_timing_explore.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote H-B06 exploration aggregates.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}. Details hidden to protect sponsor values.", file=sys.stderr)
        sys.exit(1)

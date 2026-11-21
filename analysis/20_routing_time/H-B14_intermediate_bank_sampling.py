"""Compare four-bank paths with two draws from a May middle-bank distribution.

Run from the repository root:
    uv run python analysis/20_routing_time/H-B14_intermediate_bank_sampling.py --phase explore
For the frozen July internal test, use --phase confirm --freeze <SHA>.
"""

from datetime import datetime, timezone
import sys

import duckdb
import numpy as np

from routing_common import OUT, arguments, cluster_draws, interval, report, table

STEM = "H-B14_intermediate_bank_sampling"
COUNTRIES = 11  # Top 10 country codes in May, then pooled remainder.


def load_samples(con: duckdb.DuckDBPyConnection, target_month: int) -> None:
    """Fit from May three-bank paths and score the target month's four-bank paths."""
    con.execute("""
      CREATE TEMP TABLE sample AS
      SELECT month(ts_utc) mon,participant_count v,transaction_type_code route,
        gap_count>0 gap,ordering_account oa,beneficiary_account ba,
        list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...') p
      FROM read_parquet('dataset/payments.parquet')
      WHERE ANOMALY_TYPE IS NULL
        AND ((ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-06-01' AND participant_count=3)
         OR (ts_utc>=TIMESTAMP '2023-05-01'+(?-5)*INTERVAL '1 month'
             AND ts_utc<TIMESTAMP '2023-06-01'+(?-5)*INTERVAL '1 month' AND participant_count=4))
        AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
        AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
    """, [target_month, target_month])
    con.execute("""
      CREATE TEMP TABLE fit AS
      SELECT p[2] bank,substr(p[2],5,2) country,count(*) n, n::DOUBLE/sum(n) OVER() pr
      FROM sample WHERE v=3 GROUP BY 1,2;
      CREATE TEMP TABLE fit_country AS
      SELECT country,sum(pr) pr,
        least(row_number() OVER(ORDER BY sum(pr) DESC,country)-1,10) bin
      FROM fit GROUP BY 1;
      CREATE TEMP TABLE target AS
      SELECT p[1] cluster,p[-1] last_bank,p[2] m1,p[3] m2,route,gap,oa,ba,
        substr(p[2],5,2)=substr(p[3],5,2) same_country,
        coalesce(c1.bin,10)*11+coalesce(c2.bin,10) cell,
        f1.bank IS NOT NULL AND f2.bank IS NOT NULL both_in_catalogue,
        coalesce(a.pr,0)+coalesce(b.pr,0) endpoint_probability,
        substr(p[1],5,2)=substr(p[-1],5,2) domestic
      FROM sample LEFT JOIN fit_country c1 ON substr(p[2],5,2)=c1.country
      LEFT JOIN fit_country c2 ON substr(p[3],5,2)=c2.country
      LEFT JOIN fit f1 ON p[2]=f1.bank LEFT JOIN fit f2 ON p[3]=f2.bank
      LEFT JOIN fit a ON p[1]=a.bank LEFT JOIN fit b ON p[-1]=b.bank
      WHERE v=4
    """)


def analyse(con: duckdb.DuckDBPyConnection) -> tuple[dict, bool]:
    """Measure joint country fit, bank collisions and support with bank resampling."""
    fit_banks, training, bank_pred = con.execute("SELECT count(*),sum(n),sum(pr^2) FROM fit").fetchone()
    country_pred = con.execute("SELECT sum(pr^2) FROM fit_country").fetchone()[0]
    bins = np.zeros(COUNTRIES)
    for bucket, probability in con.execute("SELECT bin,sum(pr) FROM fit_country GROUP BY 1").fetchall():
        bins[bucket] = probability
    expected_joint = np.outer(bins, bins).ravel()
    assert abs(expected_joint.sum() - 1) < 1e-10

    n_stats = 3
    count_columns = ",".join(f"count_if(cell={i})" for i in range(COUNTRIES**2))
    stats = np.asarray(con.execute(f"""
      SELECT count(*),count_if(m1=m2),count_if(same_country),{count_columns}
      FROM target GROUP BY cluster ORDER BY cluster
    """).fetchall(), dtype=float)
    counts = stats.sum(axis=0)
    draws = cluster_draws(stats)
    observed_joint = counts[n_stats:] / counts[0]
    empirical = draws[:, n_stats:] / draws[:, :1]
    tv, *tv_ci = [float(np.abs(observed_joint - expected_joint).sum() / 2),
                  *interval(np.abs(empirical - expected_joint).sum(axis=1) / 2)]
    error = draws[:, 1:n_stats] / draws[:, :1] - [bank_pred, country_pred]
    bank_ci, country_ci = interval(error[:, 0]), interval(error[:, 1])
    support = con.execute("""
      SELECT count(DISTINCT oa),count(DISTINCT ba),avg(both_in_catalogue::INT) FROM target
    """).fetchone()
    passed = (counts[0] >= 10000 and min(*support[:2], len(stats)) >= 100
              and support[-1] >= .98 and bank_ci[0] >= -.0015 and bank_ci[1] <= .0015
              and country_ci[0] >= -.006 and country_ci[1] <= .006 and tv_ci[1] <= .035)
    tables = {
        "Training and validation support": (
            ["May three-bank payments", "fitted middle banks", "target four-bank payments", "first visible banks",
             "senders", "receivers", "both middle banks seen in May", "primary pass"],
            [(training, fit_banks, int(counts[0]), len(stats), *support, passed)]),
        "Frozen collision tests (intervals are observed minus expected)": (
            ["event", "observed_share", "expected_share", "low99", "high99", "uniform-bank baseline"],
            [("Identical visible middle banks", counts[1] / counts[0], bank_pred, *bank_ci, 1 / fit_banks),
             ("Same country in both middle positions", counts[2] / counts[0], country_pred, *country_ci, "n/a")]),
        "Joint distribution of pooled middle-slot countries": (
            ["model", "TV", "low99", "high99"], [("Two draws from May distribution", tv, *tv_ci)]),
    }
    test_joint = observed_joint.reshape(COUNTRIES, COUNTRIES)
    tables["Marginal TV by position versus May distribution"] = (
        ["position", "TV"], [(pos, np.abs(test_joint.sum(axis=axis) - bins).sum() / 2)
                              for pos, axis in [(2, 1), (3, 0)]])
    for dimension, category in (("Route type", "route"), ("Gap presence", "gap::VARCHAR"),
                                ("Endpoint countries agree", "domestic::VARCHAR")):
        columns, rows = table(con, f"""
          SELECT {category} cell,count(*) n,count(DISTINCT cluster) banks,
            count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
            count_if(m1=m2) repeated,avg(same_country::INT) country_collision,
            avg((m1 IN (cluster,last_bank))::INT) observed_endpoint_repeat,
            avg(endpoint_probability) expected_endpoint_repeat
          FROM target GROUP BY 1 HAVING least(n,banks,senders,receivers)>=100 ORDER BY 1
        """)
        tables[dimension] = (columns, [
            (*row[:5], "<100" if 0 < row[5] < 100 else row[5], *row[6:]) for row in rows
        ])
    return tables, passed


def run(phase: str, freeze: str | None) -> None:
    """Use May fit for both phases and write only aggregated comparisons."""
    with duckdb.connect(config={"memory_limit": "768MB", "threads": 1, "temp_directory": ""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        load_samples(con, 6 if phase == "explore" else 7)
        tables, passed = analyse(con)
    report(STEM, phase, freeze, tables)
    out = OUT / f"{STEM}_{phase}.md"
    metadata = out.read_text(encoding="utf-8").replace("2GB; two threads", "768MB; one thread")
    metadata = metadata.replace("ordering-bank cluster", "first-visible-bank cluster")
    out.write_text(metadata, encoding="utf-8")
    print(f"{phase} B14 primary {'PASS' if passed else 'FAIL'}; safe aggregate report saved.")


if __name__ == "__main__":
    try:
        options = arguments(STEM)
        if options.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
            raise ValueError("Research cutoff reached")
        run(options.phase, options.freeze)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        sys.exit(1)

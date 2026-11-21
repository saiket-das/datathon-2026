"""Test whether visible directed endpoints determine Covered versus Indirect.

Run from repository root:
    uv run python analysis/20_routing_time/H-B12_directed_endpoint_route_class.py --phase explore
For the frozen July internal test, use --phase confirm --freeze <SHA>.
"""

from datetime import datetime, timezone
import sys

import duckdb
from scipy.stats import beta

from routing_common import OUT, arguments, report, table

STEM = "H-B12_directed_endpoint_route_class"


def event_count(count: int) -> int | str:
    """Mask positive exception cells below 100."""
    return "<100" if 0 < count < 100 else count


def evaluation(con: duckdb.DuckDBPyConnection, month: int) -> None:
    """Build May labels and compare with unseen full visible paths in a later month."""
    con.execute("""
      CREATE TEMP TABLE observed AS
      SELECT month(ts_utc) mon,participant_count v,transaction_type_code route,
        ordering_bic8 ob,beneficiary_bic8 bb,ordering_account oa,beneficiary_account ba,
        currency_code currency,gap_count>0 gap,
        list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p
      FROM read_parquet('dataset/payments.parquet')
      WHERE ANOMALY_TYPE IS NULL AND ts_utc>=TIMESTAMP '2023-05-01'
        AND ts_utc<TIMESTAMP '2023-06-01'+(?-5)*INTERVAL '1 month'
        AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
        AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
    """, [month])
    con.execute("""
      CREATE TEMP TABLE sample AS
      SELECT *, p[1] a,p[-1] b,route='Covered' covered
      FROM observed WHERE v BETWEEN 3 AND 5
    """)
    con.execute("""
      CREATE TEMP TABLE visible_labels AS
      SELECT a,b,min(covered) label,min(covered)<>max(covered) ambiguous
      FROM sample WHERE mon=5 GROUP BY a,b
    """)
    con.execute("""
      CREATE TEMP TABLE declared_labels AS
      SELECT ob,bb,avg(covered::INT)>.5 label FROM sample WHERE mon=5 GROUP BY ob,bb
    """)
    con.execute("""
      CREATE TEMP TABLE exact_paths AS SELECT DISTINCT p FROM sample WHERE mon=5
    """)
    con.execute("""
      CREATE TEMP TABLE currency_cells AS SELECT DISTINCT a,b,currency FROM sample WHERE mon=5
    """)
    con.execute("""
      CREATE TEMP TABLE scored AS
      SELECT s.*,f.label prediction,r.label reverse_prediction,d.label declared_prediction,
        x.p IS NULL novel,c.currency IS NULL novel_currency,
        f.label IS NOT NULL AND NOT f.ambiguous supported
      FROM sample s LEFT JOIN visible_labels f ON f.a=s.a AND f.b=s.b
      LEFT JOIN visible_labels r ON r.b=s.a AND r.a=s.b AND NOT r.ambiguous
      LEFT JOIN declared_labels d USING(ob,bb)
      LEFT JOIN exact_paths x ON x.p=s.p
      LEFT JOIN currency_cells c ON c.a=s.a AND c.b=s.b AND c.currency=s.currency
      WHERE mon=?
    """, [month])


def summaries(con: duckdb.DuckDBPyConnection) -> tuple[dict, bool]:
    """Return safe totals and the frozen exact-match decision."""
    core = "supported AND novel"
    support_columns = ["n", "senders", "receivers", "banks", "corridors", "path_sequences"]
    stat_columns = support_columns + ["Covered_n", "exceptions", "error_rate"]
    support_sql = """count(*) n,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                     count(DISTINCT a) banks,count(DISTINCT (a,b)) corridors,count(DISTINCT p) path_sequences"""
    stats_sql = f"""{support_sql},count_if(covered),count_if(prediction<>covered),
                    avg((prediction<>covered)::DOUBLE)"""
    row = con.execute(f"SELECT {stats_sql} FROM scored WHERE {core}").fetchone()
    n, senders, receivers, banks, corridors, _, covered, errors, rate = row
    total = con.execute("SELECT count(*) FROM scored").fetchone()[0]
    affected = con.execute(f"""
      SELECT count(DISTINCT a) FROM scored WHERE {core} AND prediction<>covered
    """).fetchone()[0]
    upper = 1.0 if affected == banks else float(beta.ppf(.99, affected + 1, banks - affected))
    training_mixed = con.execute("SELECT count_if(ambiguous) FROM visible_labels").fetchone()[0]
    passed = (training_mixed == 0 and n >= 5000 and n / total >= .50
              and min(senders, receivers, banks, corridors, covered, n - covered) >= 100
              and rate <= .001 and upper <= .02)
    tables = {
        "Frozen decision and coverage": (
            ["passes", "target_multibank_rows", "novel_supported_share", "99% upper affected fraction",
             "mixed May visible corridors"], [(passed, total, n / total, upper, event_count(training_mixed))]),
        "Primary on novel visible paths through known directed endpoints": (
            stat_columns, [(*row[:7], event_count(errors), rate if not 0 < errors < 100 else "suppressed")]),
        "Paired comparison to declared-bank majority on jointly supported novel paths": table(con, f"""
          SELECT {support_sql},avg((prediction<>covered)::DOUBLE) visible_rate,
            avg((declared_prediction<>covered)::DOUBLE) declared_rate
          FROM scored WHERE {core} AND declared_prediction IS NOT NULL
        """),
        "Reversing the directed endpoints on jointly supported novel paths": table(con, f"""
          SELECT {support_sql},avg((prediction<>covered)::DOUBLE) forward_rate,
            avg((reverse_prediction<>covered)::DOUBLE) reversed_rate
          FROM scored WHERE {core} AND reverse_prediction IS NOT NULL
        """),
        "Mixed-label endpoint groups within target month": table(con, """
          WITH kinds AS (
            SELECT 'Visible, directed' AS basis,a x,b y,covered FROM scored
            UNION ALL SELECT 'Declared, directed',ob,bb,covered FROM scored
            UNION ALL SELECT 'Visible, unordered',least(a,b),greatest(a,b),covered FROM scored
          ), counts AS (
            SELECT basis,x,y,count(*) n,count_if(covered) c FROM kinds GROUP BY 1,2,3 HAVING n>=2
          )
          SELECT basis,count(*) repeated_groups,sum(n) payments,
            CASE WHEN count_if(c>0 AND c<n) BETWEEN 1 AND 99 THEN '<100'
              ELSE count_if(c>0 AND c<n)::VARCHAR END mixed_groups,
            sum(least(c,n-c))::DOUBLE/sum(n) minimum_error FROM counts GROUP BY 1 ORDER BY 1
        """),
        "Scope exclusions and prior path repetition": table(con, """
          SELECT supported,novel,count(*) n,count(DISTINCT a) banks,count(DISTINCT (a,b)) corridors
          FROM scored GROUP BY 1,2 ORDER BY 1,2
        """),
        "Direct payments on visible corridors also seen as multibank that month": table(con, """
          WITH m AS (SELECT DISTINCT a,b,route FROM scored),
               d AS (SELECT p[1] a,p[2] b FROM observed WHERE v=2 AND mon=(SELECT min(mon) FROM scored))
          SELECT route,count(*) n,count(DISTINCT a) banks,count(DISTINCT (a,b)) corridors
          FROM m JOIN d USING(a,b) GROUP BY 1 ORDER BY 1
        """),
    }
    for label, category in (
        ("Visible bank count", "v::VARCHAR"), ("Route", "route"), ("Gap present", "gap::VARCHAR"),
        ("Currency absent from May corridor", "novel_currency::VARCHAR"),
        ("Both visible endpoints agree with declared fields", "(a=ob AND b=bb)::VARCHAR"),
    ):
        _, rows = table(con, f"""
          SELECT {category} cell,{stats_sql} FROM scored WHERE {core}
          GROUP BY 1 HAVING least(n,senders,receivers,banks)>=100 ORDER BY 1
        """)
        tables[label] = (["cell", *stat_columns], [
            (*r[:8], event_count(r[8]), r[9] if not 0 < r[8] < 100 else "suppressed") for r in rows
        ])
    return tables, passed


def run(phase: str, freeze: str | None) -> None:
    """Execute the locked split and discard all bank keys with the connection."""
    with duckdb.connect(config={"memory_limit": "1280MB", "threads": 1, "temp_directory": ""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        evaluation(con, 6 if phase == "explore" else 7)
        tables, passed = summaries(con)
    report(STEM, phase, freeze, tables)
    out = OUT / f"{STEM}_{phase}.md"
    metadata = out.read_text(encoding="utf-8").replace("2GB; two threads", "1280MB; one thread")
    metadata = metadata.replace(
        "Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.",
        "The 99% upper bound assumes independent first-visible-bank units. Shared receiving banks and entities limit that assumption.",
    )
    out.write_text(metadata, encoding="utf-8")
    print(f"{phase} B12 primary {'PASS' if passed else 'FAIL'}; safe aggregate report saved.")


if __name__ == "__main__":
    try:
        options = arguments(STEM)
        if options.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
            raise ValueError("Research cutoff reached")
        run(options.phase, options.freeze)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        sys.exit(1)

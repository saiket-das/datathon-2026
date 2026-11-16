"""Probe how the selected payment currency enters the path FX count.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A15_payment_currency_insertion.py
Only unlabelled bit-zero exploration. No path, bank or account identities are output.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx",HERE/"H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Compare endpoint replacement and initial conversion against the geography count."""
    if datetime.now(timezone.utc) >= datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        with fx.connect() as con:
            con.execute("""CREATE TEMP TABLE modes AS
              WITH country_currencies AS (
                SELECT substr(path[1],5,2) country,currency,count(*) n
                FROM source WHERE split='explore' AND ANOMALY_TYPE IS NULL
                  AND ts_utc<TIMESTAMP '2023-07-01'
                GROUP BY 1,2
                QUALIFY sum(count(*)) OVER(PARTITION BY country)>=100
                  AND row_number() OVER(PARTITION BY country ORDER BY count(*) DESC,currency)=1
              )
              SELECT map(list(country),list(currency)) currency_map FROM country_currencies""")
            con.execute("""CREATE VIEW evaluation AS
              SELECT oa,ba,ob,fx,route,currency,list_transform(path,
                lambda b:currency_map[substr(b,5,2)]) modes
              FROM source CROSS JOIN modes
              WHERE split='explore' AND ANOMALY_TYPE IS NULL AND len(path)>=2
                AND ts_utc>=TIMESTAMP '2023-07-01'""")
            scope = fx.query(con,"""SELECT count(*) scoped,
              count(*) FILTER(WHERE NOT list_contains(list_transform(modes,lambda m:m IS NULL),true)) eligible
              FROM evaluation""")
            report = fx.query(con,"""WITH predictions AS (
              SELECT *,list_sum(list_transform(range(1,len(modes)),
                lambda i:(modes[i]<>modes[i+1])::INT)) geography
              FROM evaluation WHERE NOT list_contains(list_transform(modes,lambda m:m IS NULL),true)
                 AND currency<>modes[1]
              ), comparisons AS (
              SELECT *,geography-(modes[1]<>modes[2])::INT+(currency<>modes[2])::INT replace_first,
                geography-(modes[-1]<>modes[-2])::INT+(currency<>modes[-2])::INT replace_last,
                geography+1 prepend_currency
              FROM predictions
              ), g AS (
              SELECT CASE WHEN grouping(route)=1 THEN 'All' ELSE route END route,
                count(*) n,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                count(DISTINCT ob) banks,
                count(*) FILTER(WHERE fx<>geography) geographic_errors,
                count(*) FILTER(WHERE fx<>replace_first) first_replacement_errors,
                count(*) FILTER(WHERE fx<>replace_last) last_replacement_errors,
                count(*) FILTER(WHERE fx<>prepend_currency) prepend_errors,
                count(*) FILTER(WHERE fx<>geography AND fx=replace_first) first_repairs
              FROM comparisons GROUP BY GROUPING SETS((),(route))
              HAVING count(*)>=1000 AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100)
              SELECT route,n,senders,receivers,banks,
                CASE WHEN geographic_errors BETWEEN 1 AND 99 THEN '<100' ELSE geographic_errors::VARCHAR END geography_errors,
                CASE WHEN first_replacement_errors BETWEEN 1 AND 99 THEN '<100' ELSE first_replacement_errors::VARCHAR END first_replacement_errors,
                CASE WHEN last_replacement_errors BETWEEN 1 AND 99 THEN '<100' ELSE last_replacement_errors::VARCHAR END last_replacement_errors,
                CASE WHEN prepend_errors BETWEEN 1 AND 99 THEN '<100' ELSE prepend_errors::VARCHAR END prepend_errors,
                CASE WHEN first_repairs BETWEEN 1 AND 99 THEN '<100' ELSE first_repairs::VARCHAR END first_repairs
              FROM g ORDER BY route""")
        output = fx.render("H-A15 — Payment currency and path FX-state alternatives",
            {"July scope":scope,"First-country currency exceptions":report},"exploration only")
        output = output.replace(
            "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
            "Both-account bit-0 exploration only. Phase 0 and A01–A14 exposure applies.")
        output += ("\nAll candidates share a pre-July first-visible-country mode map. "
                   "Route groups overlap the pooled result. Positive small cells are masked.\n")
        (HERE/"out/H-A15_payment_currency_insertion_explore.md").write_text(output,encoding="utf-8")
        print("OK: aggregate payment-currency insertion screen saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())

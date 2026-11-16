"""Check frozen amount calculations on invented data, without sponsor data.

Run from repository root: uv run pytest analysis/10_amounts_currency/test_value_mechanisms.py
"""

import importlib.util
from pathlib import Path

import duckdb
import pytest

spec = importlib.util.spec_from_file_location("value_kernel", Path(__file__).with_name("H-A01_amount_kernel.py"))
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)


def test_account_contrasts_recover_invented_business_effect() -> None:
    """Known two-log-unit effects survive repeated accounts and currency matching."""
    con = duckdb.connect()
    try:
        con.execute("""CREATE TABLE e AS SELECT s::VARCHAR sender,r::VARCHAR receiver,
          'X' currency,CASE WHEN s%2=0 THEN 'B' ELSE 'C' END ||
            CASE WHEN r%2=0 THEN 'B' ELSE 'C' END pair,
          false labelled,exp(6+2*(s%2=0)::INT+2*(r%2=0)::INT
            +0.01*(s%7-3)*(r%2=0)::INT+0.01*(r%11-5)*(s%2=0)::INT) a
          FROM range(200) x(s) CROSS JOIN range(200) y(r)""")
        table = kernel.contrasts(con)
        for row in table[1]:
            assert row[1] == 200
            assert row[2] == 40000
            assert row[3] == pytest.approx(2,abs=0.002)
            assert row[11] is True
    finally:
        con.close()


def test_rate_tolerance_accounts_for_cent_rounded_anchor() -> None:
    """A held-out amount fits a correctly scaled grid and fails a wrong rate."""
    true_rate,base = 1.12345678,100000
    rate = round(true_rate*base,2)/base
    for source in (17,237,2378,43781):
        amount = round(true_rate*source,2)
        tolerance = 0.005+0.005*amount/rate/base+1e-8
        assert abs(amount-rate*round(amount/rate)) <= tolerance
        wrong = 1.17777
        assert abs(amount-wrong*round(amount/wrong)) > tolerance


def test_confirmation_requires_a_freeze_commit() -> None:
    with pytest.raises(ValueError):
        kernel.freeze_guard(None)

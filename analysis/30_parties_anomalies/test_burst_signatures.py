"""Check exact burst logic and confidentiality on invented data only.

Run from the repository root:
    uv run pytest
"""

import importlib.util
from pathlib import Path

import duckdb
import pytest

spec = importlib.util.spec_from_file_location("c_bursts", Path(__file__).with_name("H-C01_duplicate_bursts.py"))
bursts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bursts)


@pytest.fixture
def con():
    connection = duckdb.connect()
    connection.execute("""CREATE TABLE e AS SELECT i::BIGINT ROW_ID,
      (1000+i*60)::BIGINT EPOCH_SECONDS,'USD' CURRENCY_CODE,100.0 USD_AMOUNT,
      '1111AA00' ORDERING_BIC8,'2222BB00' BENEFICIARY_BIC8,
      '1111AA00;2222BB00' BIC8_PATH,20 TOTAL_DURATION,'Y' CONTINUITY_QFLAG,
      0 CURRENCY_CONVERSION_COUNT,2 PARTICIPANT_COUNT,'Direct' TRANSACTION_TYPE_CODE,
      '_PRIVATE_TEST_SENDER_' ORDERING_ACCOUNT,'_PRIVATE_TEST_RECEIVER_' BENEFICIARY_ACCOUNT,
      '_PRIVATE_TEST_DETAILS_' ORDERING_DETAILS,'TOKEN' ORDERING_TOKENS,
      '_PRIVATE_TEST_DETAILS_' BENEFICIARY_DETAILS,'TOKEN' BENEFICIARY_TOKENS,
      'C' ORDERING_TYPE,'B' BENEFICIARY_TYPE,'DUPLICATE_PAYMENT' ANOMALY_TYPE,
      TIMESTAMP '2023-05-10' ts_utc FROM range(1,4) r(i)""")
    yield connection
    connection.close()


def test_duplicate_exact_context_and_label_blindness(con):
    # A whole duplicate family can be labelled; no unlabelled original is required.
    bursts.build_features(con, "duplicate")
    assert con.execute("SELECT count(*) FROM assessed WHERE signature").fetchone()[0] == 3
    assert con.execute("SELECT family_n,span FROM scored").fetchone() == (3, 120)


@pytest.mark.parametrize("mutation", [
    "UPDATE e SET ORDERING_TOKENS='DIFFERENT' WHERE ROW_ID=2",
    "UPDATE e SET ROW_ID=9 WHERE ROW_ID=3",
    "UPDATE e SET EPOCH_SECONDS=10000 WHERE ROW_ID=3",
])
def test_duplicate_rejects_context_changes_gaps_and_long_spans(con, mutation):
    con.execute(mutation)
    bursts.build_features(con, "duplicate")
    assert con.execute("SELECT count(*) FROM assessed WHERE signature").fetchone()[0] == 0


def test_duplicate_key_separates_unrelated_invoice_to_same_receiver(con):
    con.execute("INSERT INTO e SELECT * REPLACE(20 AS ROW_ID,9000 AS EPOCH_SECONDS,999.0 AS USD_AMOUNT,NULL AS ANOMALY_TYPE) FROM e WHERE ROW_ID=1")
    bursts.build_features(con, "duplicate")
    assert con.execute("SELECT count(*) FROM assessed WHERE signature").fetchone()[0] == 3
    assert con.execute("SELECT signature FROM assessed WHERE ROW_ID=20").fetchone()[0] is False


@pytest.mark.parametrize("mutation,expected", [
    ("UPDATE e SET ANOMALY_TYPE='ROMANCE_SCAM',USD_AMOUNT=ROW_ID*100", 3),
    ("UPDATE e SET ANOMALY_TYPE='ROMANCE_SCAM',USD_AMOUNT=ROW_ID*100,EPOCH_SECONDS=4000-ROW_ID*60", 0),
    ("UPDATE e SET ANOMALY_TYPE='ROMANCE_SCAM',USD_AMOUNT=ROW_ID*100,ORDERING_TYPE='B'", 0),
    ("UPDATE e SET ANOMALY_TYPE='ROMANCE_SCAM'", 0),
])
def test_romance_requires_consumer_chronology_and_varying_amount(con, mutation, expected):
    con.execute(mutation)
    bursts.build_features(con, "romance")
    assert con.execute("SELECT count(*) FROM assessed WHERE signature").fetchone()[0] == expected


def test_small_cohort_suppression():
    report = bursts.markdown_table(["label", "n", "senders", "coverage"], [("TEST", 3, 2, .123456)])
    assert "suppressed" in report and ".123456" not in report
    assert "| 2 |" not in report


def test_sender_weighting_counts_accounts_not_payments(con):
    con.execute("CREATE VIEW assessed AS SELECT *,ROW_ID<3 signature FROM e")
    result = bursts.entity_summary(con, "duplicate")
    assert result["senders"] == 1 and result["row_coverage"] == pytest.approx(2/3)
    assert result["sender_mean_coverage"] == pytest.approx(2/3)
    assert result["receivers"] == 1 and result["receiver_mean_coverage"] == pytest.approx(2/3)

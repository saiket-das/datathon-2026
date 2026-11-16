"""Test scientific checks on invented data, including deliberate leakage and exceptions.

Run from the repository root:
    uv run pytest
No sponsor data is required or opened.
"""

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys

import duckdb
import pytest

SCRIPT = Path(__file__).with_name("scientific_checks.py")
spec = importlib.util.spec_from_file_location("scientific_checks", SCRIPT)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
SECRET = "_TEST_PRIVATE_SENTINEL_"


@pytest.fixture
def con():
    connection = duckdb.connect()
    connection.execute(f"""CREATE TABLE t AS SELECT i::BIGINT ROW_ID,
      1684540800::BIGINT EPOCH_SECONDS,'USD' CURRENCY_CODE,i*1.11 USD_AMOUNT,
      '1111AA01' ORDERING_BIC8,'2222BB02' BENEFICIARY_BIC8,
      '1111AA01;...;2222BB02' BIC8_PATH,i::BIGINT TOTAL_DURATION,'N' CONTINUITY_QFLAG,
      1::INTEGER CURRENCY_CONVERSION_COUNT,2::INTEGER PARTICIPANT_COUNT,
      'Direct' TRANSACTION_TYPE_CODE,
      '{SECRET}s_'||(i%12) ORDERING_ACCOUNT,'{SECRET}r_'||(i%10) BENEFICIARY_ACCOUNT,
      '{SECRET}d_'||(i%7) ORDERING_DETAILS,'TOKEN_'||(i%7) ORDERING_TOKENS,
      '{SECRET}b_'||(i%7) BENEFICIARY_DETAILS,'TOKEN_'||(i%7) BENEFICIARY_TOKENS,
      'B' ORDERING_TYPE,'C' BENEFICIARY_TYPE,
      CASE WHEN i%3=0 THEN 'ROMANCE_SCAM' ELSE NULL END ANOMALY_TYPE,
      CASE i%4 WHEN 0 THEN TIMESTAMP '2023-05-20' WHEN 1 THEN TIMESTAMP '2023-06-20'
        WHEN 2 THEN TIMESTAMP '2023-07-20' ELSE TIMESTAMP '2023-07-31' END ts_utc,
      'AA' ord_country,'BB' ben_country,3::BIGINT path_len,1::BIGINT gap_count
      FROM range(1,401) r(i)""")
    connection.execute("UPDATE t SET EPOCH_SECONDS=epoch(ts_utc)::BIGINT")
    yield connection
    connection.close()


def metrics(table):
    return dict(zip(table[0], table[1][0]))


@pytest.fixture
def bank_routes(con):
    # Select invented endpoint banks independently of the SQL partition implementation.
    banks = {bit: [f"{i:04d}ZZ00" for i in range(32)
                   if int(hashlib.md5(f"{i:04d}ZZ00".encode()).hexdigest()[:8], 16) % 2 == bit]
             for bit in (0, 1)}
    e0, e1 = banks[0][:2]
    c0, c1 = banks[1][:2]
    pairs = [(e0, e1), (e1, e0), (c0, c1), (c1, c0), (e0, c0), (c0, e0)]
    con.execute("DELETE FROM t WHERE ROW_ID>6")
    for row_id, (ordering, beneficiary) in enumerate(pairs, 1):
        # Only crossing records use the second intermediary; it must not enter the active audit.
        intermediary = "9999ZZ99" if row_id <= 4 else "8888ZZ88"
        con.execute("""UPDATE t SET ORDERING_BIC8=?,BENEFICIARY_BIC8=?,BIC8_PATH=?,
          ORDERING_ACCOUNT='SHARED_TEST_SENDER',BENEFICIARY_ACCOUNT='SHARED_TEST_RECEIVER',
          ord_country='ZZ',ben_country='ZZ',path_len=3,gap_count=0,PARTICIPANT_COUNT=3,
          TRANSACTION_TYPE_CODE='Indirect',CONTINUITY_QFLAG='Y',CURRENCY_CONVERSION_COUNT=0
          WHERE ROW_ID=?""", [ordering, beneficiary,
                               f"{ordering};{intermediary};{beneficiary}", row_id])
    return con


def test_banks_partition_with_crossing_routes_and_shared_intermediaries(bank_routes):
    result = checks.validation_checks(bank_routes)
    coverage = result["banks: coverage and baseline stability"][1]
    assert {row[0]: row[1] for row in coverage} == {"explore": 2, "confirm": 2, "excluded": 2}
    audit = metrics(result["banks: overlap audit"])
    assert audit == {"row_ids": 0, "sender_ids": 1, "account_ids_either_role": 2,
                     "endpoint_bank_ids": 0, "visible_path_bank_ids": 1}
    bank_routes.execute(f"CREATE OR REPLACE TEMP VIEW p AS SELECT *,{checks.partition_sql('banks')} split FROM t")
    wrong = bank_routes.execute("""SELECT count(*) FROM p WHERE split <> CASE
      WHEN ROW_ID IN (1,2) THEN 'explore' WHEN ROW_ID IN (3,4) THEN 'confirm'
      ELSE 'excluded' END""").fetchone()[0]
    assert wrong == 0


def test_definitions_and_deliberate_violations(con):
    baseline = metrics(checks.query(con, checks.STRUCTURE_SQL))
    assert baseline["records"] == 400
    assert baseline["participants_vs_entries"] == 400
    assert baseline["participants_vs_visible"] == 0
    assert all(baseline[key] == 0 for key in (
        "direct_iff_two_bad", "continuity_bad", "fx_vs_country_changes",
        "ordering_endpoint_mismatch", "helper_time_bad",
    ))
    con.execute("""UPDATE t SET TRANSACTION_TYPE_CODE='Indirect',CONTINUITY_QFLAG='Y',
      CURRENCY_CONVERSION_COUNT=4,ORDERING_BIC8='9999CC03',path_len=9 WHERE ROW_ID=1""")
    changed = metrics(checks.query(con, checks.STRUCTURE_SQL))
    for key in ("direct_iff_two_bad", "continuity_bad", "fx_exceeds_links",
                "fx_exceeds_country_changes", "ordering_endpoint_mismatch", "helper_path_bad"):
        assert changed[key] == 1


def test_account_roles_and_exact_detail_counterexamples(con):
    con.execute("""UPDATE t SET ORDERING_TYPE='C',BENEFICIARY_BIC8='9999CC03',
      ORDERING_TOKENS='CHANGED',BENEFICIARY_TOKENS='CHANGED' WHERE ROW_ID=1""")
    con.execute("UPDATE t SET BENEFICIARY_ACCOUNT=ORDERING_ACCOUNT WHERE ROW_ID=2")
    result = checks.structural_checks(con)
    assert metrics(result["Account consistency: ORDERING"])["multi_type"] == 1
    assert metrics(result["Account consistency: BENEFICIARY"])["multi_bank"] == 1
    assert metrics(result["Cross-role identity consistency"])["type_disagreement"] == 1
    for role in ("ORDERING", "BENEFICIARY"):
        found = metrics(result[f"Visible details to tokens: {role}"])
        assert found["inconsistent_detail_groups"] == 1
        assert found["affected_rows"] > 1


@pytest.mark.parametrize("value", ["same-account", "different-bank", "caf\u00e9", ""])
def test_md5_parity_is_stable_across_python_and_sql(con, value):
    actual = con.execute(f"SELECT {checks.bucket('?')}", [value]).fetchone()[0]
    assert actual == int(hashlib.md5(value.encode()).hexdigest()[:8], 16) % 2


def test_partition_coverage_overlap_balance_and_repeatability(con):
    result = checks.validation_checks(con)
    for scheme in ("sender", "accounts", "banks", "time"):
        rows = result[f"{scheme}: coverage and baseline stability"][1]
        assert sum(row[1] for row in rows) == 400
        assert {row[0] for row in rows} == {"explore", "confirm", "excluded"}
        assert metrics(result[f"{scheme}: overlap audit"])["row_ids"] == 0
    assert metrics(result["sender: overlap audit"])["sender_ids"] == 0
    assert metrics(result["sender: overlap audit"])["account_ids_either_role"] > 0
    assert metrics(result["accounts: overlap audit"])["account_ids_either_role"] == 0
    assert metrics(result["banks: overlap audit"])["endpoint_bank_ids"] == 0
    time_rows = result["time: coverage and baseline stability"][1]
    assert {row[0]: row[1] for row in time_rows} == {"explore": 200, "confirm": 100, "excluded": 100}
    con.execute(f"CREATE VIEW first_assignment AS SELECT ROW_ID,{checks.partition_sql('accounts')} split FROM t")
    first = con.execute("SELECT bit_xor(hash(ROW_ID,split)) FROM first_assignment").fetchone()[0]
    second = con.execute(f"SELECT bit_xor(hash(ROW_ID,{checks.partition_sql('accounts')})) FROM t").fetchone()[0]
    assert first == second
    assert all(0 <= table[1][0][0] <= 1 for name, table in result.items()
               if "composition distance" in name and table[1][0][0] is not None)
    con.execute(f"UPDATE t SET CURRENCY_CODE=CASE WHEN {checks.bucket('ORDERING_ACCOUNT')}=0 THEN 'USD' ELSE 'EUR' END")
    shifted = checks.validation_checks(con)
    assert metrics(shifted["sender: composition distance for CURRENCY_CODE"])["total_variation"] == 1


def test_overlap_detects_cross_role_identity_and_duplicate_membership(con):
    con.execute("""CREATE VIEW p AS SELECT *,CASE WHEN ROW_ID%2=0 THEN 'explore'
      ELSE 'confirm' END split FROM t""")
    assert checks.overlap(con, ["ORDERING_ACCOUNT"])[1][0][0] == 0
    con.execute("UPDATE t SET BENEFICIARY_ACCOUNT=(SELECT ORDERING_ACCOUNT FROM t WHERE ROW_ID=2) WHERE ROW_ID=1")
    assert checks.overlap(con, ["ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT"])[1][0][0] > 0
    con.execute("UPDATE t SET ROW_ID=2 WHERE ROW_ID=1")
    # Construct an adversarial overlapping assignment independent of ROW_ID parity.
    con.execute("CREATE OR REPLACE VIEW p AS SELECT *,CASE WHEN TOTAL_DURATION%2=0 THEN 'explore' ELSE 'confirm' END split FROM t")
    assert checks.overlap(con, ["ROW_ID"])[1][0][0] == 1


def test_small_subgroups_and_small_entity_support_are_suppressed():
    text = checks.render({"support": (["split", "label", "n", "senders", "amount_median", "support"], [
        ("confirm", "ROMANCE_SCAM", 3, 2, 999999.123, "limited"),
        ("explore", "ROMANCE_SCAM", 200, 2, 25.0, "limited"),
    ])})
    assert "999999.123" not in text
    assert "| 2 |" not in text
    assert "<100" in text and "suppressed" in text


def test_cli_only_writes_safe_aggregates_and_hides_errors(con, tmp_path):
    source, output = tmp_path / "invented.parquet", tmp_path / "report.md"
    con.execute(f"COPY t TO '{source.as_posix()}' (FORMAT parquet)")
    run = subprocess.run([sys.executable, str(SCRIPT), "--src", str(source), "--out", str(output)],
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert SECRET not in run.stdout + run.stderr + output.read_text(encoding="utf-8")
    con.execute("UPDATE t SET ROW_ID=1 WHERE ROW_ID=2")
    con.execute(f"COPY t TO '{source.as_posix()}' (FORMAT parquet)")
    before = output.read_bytes()
    failed = subprocess.run([sys.executable, str(SCRIPT), "--src", str(source), "--out", str(output)],
                            capture_output=True, text=True)
    assert failed.returncode != 0 and "details hidden" in failed.stderr
    assert SECRET not in failed.stdout + failed.stderr
    assert output.read_bytes() == before
    source_before = source.read_bytes()
    overwrite = subprocess.run([sys.executable, str(SCRIPT), "--src", str(source),
                                "--out", str(source)], capture_output=True, text=True)
    assert overwrite.returncode != 0 and source.read_bytes() == source_before


def test_missing_source_fails_without_creating_report(tmp_path):
    output = tmp_path / "report.md"
    run = subprocess.run([sys.executable, str(SCRIPT), "--src", str(tmp_path / "absent.parquet"),
                          "--out", str(output)], capture_output=True, text=True)
    assert run.returncode != 0 and not output.exists()

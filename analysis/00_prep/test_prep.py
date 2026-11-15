"""Fast, dataset-independent checks of the repository setup.

Tests that the preparation and profile scripts work, fail loudly, and print no
records, using a tiny made-up CSV written to a temporary folder (no sponsor data),
and that Git refuses data-shaped files.

Run from the repo root (about 5 seconds, no dataset needed):
    uv run pytest
"""
import csv
import pathlib
import shutil
import subprocess
import sys

import duckdb
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = ROOT / "analysis" / "00_prep" / "build_parquet.py"
PROFILE = ROOT / "analysis" / "00_prep" / "profile.py"

HEADER = ["DISCLAIMER", "EPOCH_SECONDS", "CURRENCY_CODE", "USD_AMOUNT", "ORDERING_BIC8", "BENEFICIARY_BIC8",
          "BIC8_PATH", "TOTAL_DURATION", "CONTINUITY_QFLAG", "CURRENCY_CONVERSION_COUNT", "PARTICIPANT_COUNT",
          "TRANSACTION_TYPE_CODE", "ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT", "ORDERING_DETAILS",
          "ORDERING_TOKENS", "BENEFICIARY_DETAILS", "BENEFICIARY_TOKENS", "ORDERING_TYPE", "BENEFICIARY_TYPE",
          "ANOMALY_TYPE"]
SECRET = "_TEST_ACCT_"  # marker that must never appear in script output


def fixture_rows(n=6):
    """Invented records exercising quotes, commas, embedded line breaks and path gaps."""
    rows = []
    for i in range(n):
        gap = i == 2
        rows.append([
            "made-up test data" if i == 0 else "", 1700000000 + 3600 * i, ["AAA", "BBB"][i % 2], 100.5 * (i + 1),
            "TESTAA11", "TESTBB22", "TESTAA11;...;TESTBB22" if gap else "TESTAA11;TESTBB22",
            60 + i, "N" if gap else "Y", i % 2, 3 if gap else 2, "Indirect" if gap else "Direct",
            f"{SECRET}{i}", f"{SECRET}B{i}", f'NAME {i}, "QUOTED"\nSTREET {i}\nCITY', "NAME LINEBREAK STREET",
            f"OTHER {i}\nROAD", "NAME LINEBREAK", "BC"[i % 2], "CB"[i % 2], "TEST_LABEL" if i == 4 else "",
        ])
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADER)
        writer.writerows(rows)


def run(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)


@pytest.fixture
def built(tmp_path):
    src, out = tmp_path / "in.csv", tmp_path / "payments.parquet"
    write_csv(src, fixture_rows())
    result = run(BUILD, "--src", src, "--out", out)
    assert result.returncode == 0, result.stderr
    return src, out, result


def test_build_keeps_every_record_in_order(built):
    _, out, _ = built
    con = duckdb.connect()
    cols = [r[0] for r in con.sql(f"DESCRIBE SELECT * FROM '{out.as_posix()}'").fetchall()]
    assert len(cols) == 26 and "DISCLAIMER" not in cols
    rows = con.sql(f"""SELECT ROW_ID, EPOCH_SECONDS, path_len, gap_count, ord_country, ben_country,
        ANOMALY_TYPE, ORDERING_DETAILS, epoch(ts_utc)::BIGINT FROM '{out.as_posix()}' ORDER BY ROW_ID""").fetchall()
    assert [r[0] for r in rows] == [1, 2, 3, 4, 5, 6]
    assert [r[1] for r in rows] == [1700000000 + 3600 * i for i in range(6)]  # original order kept
    assert [r[2] for r in rows] == [2, 2, 3, 2, 2, 2] and [r[3] for r in rows] == [0, 0, 1, 0, 0, 0]
    assert {(r[4], r[5]) for r in rows} == {("AA", "BB")}
    assert [r[6] for r in rows] == [None, None, None, None, "TEST_LABEL", None]
    assert rows[1][7] == 'NAME 1, "QUOTED"\nSTREET 1\nCITY'  # line breaks and quotes survive
    assert all(r[8] == r[1] for r in rows)  # ts_utc is EPOCH_SECONDS in UTC


def test_build_prints_aggregates_only(built):
    _, out, result = built
    assert "records            6" in result.stdout
    assert SECRET not in result.stdout + result.stderr
    assert not out.with_name(out.name + ".partial").exists()


def test_build_fails_clearly_without_input(tmp_path):
    out = tmp_path / "payments.parquet"
    result = run(BUILD, "--src", tmp_path / "missing.csv", "--out", out)
    assert result.returncode != 0 and "not found" in result.stderr
    assert not out.exists()


def test_failed_build_keeps_previous_output(built, tmp_path):
    _, out, _ = built
    before = out.read_bytes()
    bad = fixture_rows()
    bad[3][3] = "not-a-number"
    write_csv(tmp_path / "bad.csv", bad)
    result = run(BUILD, "--src", tmp_path / "bad.csv", "--out", out)
    assert result.returncode != 0 and "left untouched" in result.stderr
    assert "not-a-number" not in result.stderr and SECRET not in result.stderr  # error text quotes no data
    assert "not-a-number" in run(BUILD, "--src", tmp_path / "bad.csv", "--out", out, "--show-error-detail").stderr
    assert out.read_bytes() == before
    assert not out.with_name(out.name + ".partial").exists()


def test_verify_only_accepts_a_good_file(built):
    src, out, _ = built
    for flags in ([], ["--independent"]):
        result = run(BUILD, "--verify-only", "--src", src, "--out", out, *flags)
        assert result.returncode == 0, result.stderr
        assert "matches the CSV" in result.stdout and SECRET not in result.stdout


# Each case damages a copy of a correct Parquet in a way the earlier aggregate checks
# (record count, integer sums, amount sum, total text length per column) could not see.
TAMPERS = {
    "control: rewritten unchanged": ("*", None),
    "one text field changed, same length": (
        "* REPLACE (CASE WHEN ROW_ID = 2 THEN replace(ORDERING_DETAILS, 'STREET', 'STREEX') ELSE ORDERING_DETAILS END AS ORDERING_DETAILS)",
        "fingerprint"),
    "two amounts changed, same sum": (
        "* REPLACE (USD_AMOUNT + CASE ROW_ID WHEN 1 THEN 0.5 WHEN 2 THEN -0.5 ELSE 0 END AS USD_AMOUNT)", "fingerprint"),
    "two integers changed, same sum": (
        "* REPLACE (TOTAL_DURATION + CASE ROW_ID WHEN 3 THEN 7 WHEN 6 THEN -7 ELSE 0 END AS TOTAL_DURATION)", "fingerprint"),
    "one value swapped between two rows": (
        "* REPLACE (CASE ROW_ID WHEN 1 THEN 'BBB' WHEN 2 THEN 'AAA' ELSE CURRENCY_CODE END AS CURRENCY_CODE)", "fingerprint"),
    "label moved to another row": (
        "* REPLACE (CASE ROW_ID WHEN 4 THEN 'TEST_LABEL' WHEN 5 THEN NULL ELSE ANOMALY_TYPE END AS ANOMALY_TYPE)", "fingerprint"),
    "two records exchanged positions": (
        "* REPLACE (CASE ROW_ID WHEN 1 THEN 2 WHEN 2 THEN 1 ELSE ROW_ID END AS ROW_ID)", "fingerprint"),
    "helper column wrong": ("* REPLACE (gap_count + (ROW_ID = 1)::INT AS gap_count)", "helper columns"),
    "last record missing": ("* EXCLUDE (keep) FROM (SELECT *, ROW_ID < 6 AS keep", "record counts differ"),
}


@pytest.mark.parametrize("case", TAMPERS)
def test_verification_detects_damage(built, tmp_path, case):
    src, out, _ = built
    select, expected = TAMPERS[case]
    good, damaged = f"read_parquet('{out.as_posix()}')", tmp_path / "damaged.parquet"
    query = f"SELECT {select} FROM {good}" + (") WHERE keep" if "keep" in select else "")
    duckdb.connect().execute(f"COPY ({query}) TO '{damaged.as_posix()}' (FORMAT parquet)")
    result = run(BUILD, "--verify-only", "--src", src, "--out", damaged)
    assert SECRET not in result.stdout + result.stderr
    if expected is None:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0 and "does NOT match" in result.stderr and expected in result.stderr


def test_verification_detects_a_partly_written_file(built, tmp_path):
    src, out, _ = built
    data = bytearray(out.read_bytes())
    cut, zeroed = tmp_path / "cut.parquet", tmp_path / "zeroed.parquet"
    cut.write_bytes(data[: len(data) // 2])
    data[200:1200] = bytes(1000)  # same size, a block of zeros inside the column data
    zeroed.write_bytes(data)
    for damaged in (cut, zeroed):
        result = run(BUILD, "--verify-only", "--src", src, "--out", damaged)
        assert result.returncode != 0 and "does NOT match" in result.stderr


def test_python_fingerprint_equals_duckdb_fingerprint(built):
    """The independent check is only meaningful if both implementations agree on good data."""
    src, out, _ = built
    module = load_build_module()
    con = duckdb.connect()
    fields = [f"{c}::VARCHAR" for c in module.COLUMNS]
    from_parquet = con.sql(module.fingerprint_sql(f"read_parquet('{out.as_posix()}')", "ROW_ID", fields)).fetchall()[0]
    assert module.python_fingerprint(src) == from_parquet


def test_failed_verification_never_replaces_output(built, monkeypatch):
    src, out, _ = built
    before = out.read_bytes()
    module = load_build_module()
    monkeypatch.setattr(module, "verify", lambda *a, **k: (["forced failure"], {}))
    with pytest.raises(SystemExit) as exit_info:
        module.build(src, out)
    assert "left untouched" in str(exit_info.value) and "forced failure" in str(exit_info.value)
    assert out.read_bytes() == before
    assert not out.with_name(out.name + ".partial").exists()


def load_build_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_parquet_under_test", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_profile_runs_and_prints_no_records(built):
    _, out, _ = built
    result = run(PROFILE, "--src", out)
    assert result.returncode == 0, result.stdout[-2000:] + result.stderr
    assert "## overall" in result.stdout and "OK: all profile queries ran." in result.stdout
    assert "ERR" not in result.stdout and SECRET not in result.stdout


def test_profile_fails_without_parquet(tmp_path):
    result = run(PROFILE, "--src", tmp_path / "missing.parquet")
    assert result.returncode != 0 and "not found" in result.stderr


def test_profile_fails_when_a_query_breaks(built, tmp_path):
    _, out, _ = built
    broken = tmp_path / "broken.parquet"
    duckdb.connect().execute(
        f"COPY (SELECT * EXCLUDE (TOTAL_DURATION) FROM '{out.as_posix()}') TO '{broken.as_posix()}' (FORMAT parquet)")
    result = run(PROFILE, "--src", broken)
    assert result.returncode != 0 and "FAILED" in result.stderr


needs_git = pytest.mark.skipif(shutil.which("git") is None or not (ROOT / ".git").exists(), reason="not a git clone")


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


@needs_git
@pytest.mark.parametrize("path", [
    "dataset/swift_umdac_datathon_2026_fictitious_payment_data.csv", "dataset/payments.parquet",
    "dataset/sample.xlsx", "dataset/extract.json", "dataset/rows.txt", "dataset/sub/rows.txt",
    "dataset/.duckdb_tmp/x.tmp", "analysis/10_amounts_currency/out/rows.csv",
    "analysis/20_routing_time/out/rows.json", "analysis/30_parties_anomalies/out/rows.xlsx",
    "analysis/10_amounts_currency/sample.parquet", "extract.jsonl", "docs/rows.pkl", ".env",
    "notebook.ipynb", "docs/research-notes.ipynb", "analysis/10_amounts_currency/work.ipynb",
    "analysis/30_parties_anomalies/out/exploration.ipynb",
])
def test_gitignore_blocks_data_shaped_files(path):
    assert git("check-ignore", "-q", "--no-index", path).returncode == 0, f"{path} is NOT ignored"


@needs_git
@pytest.mark.parametrize("path", [
    "dataset/README.md", "uv.lock", "pyproject.toml", "analysis/10_amounts_currency/out/H-A01_x.png",
    "analysis/20_routing_time/out/H-B01_x.md", "analysis/30_parties_anomalies/out/.gitkeep",
    "analysis/10_amounts_currency/H-A01_x.py", "findings/hypotheses/H-A01_x.md", "deliverables/slides.pdf",
])
def test_gitignore_allows_intended_files(path):
    assert git("check-ignore", "-q", "--no-index", path).returncode == 1, f"{path} is wrongly ignored"


@needs_git
def test_no_data_files_are_tracked():
    tracked = git("ls-files").stdout.split("\n")
    bad_ext = (".csv", ".tsv", ".parquet", ".xlsx", ".xls", ".jsonl", ".ndjson", ".pkl", ".ipynb", ".duckdb", ".db", ".zip", ".gz")
    offenders = [f for f in tracked if f.lower().endswith(bad_ext) or (f.startswith("dataset/") and f != "dataset/README.md")]
    assert not offenders, f"data-shaped files are tracked in Git: {offenders}"

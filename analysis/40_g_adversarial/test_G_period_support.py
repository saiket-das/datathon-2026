"""G periods-only connector: synthetic fixtures, never sponsor payment data."""
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import duckdb
import pytest

SPEC = spec_from_file_location(
    "g_periods", Path(__file__).with_name("G_period_support.py")
)
assert SPEC and SPEC.loader
g = module_from_spec(SPEC)
SPEC.loader.exec_module(g)


def fixture(path: Path, epochs: list[int]) -> None:
    db = duckdb.connect(":memory:")
    try:
        db.execute("CREATE TABLE fixture(EPOCH_SECONDS BIGINT)")
        db.executemany("INSERT INTO fixture VALUES (?)", [(x,) for x in epochs])
        db.execute(f"COPY fixture TO '{str(path).replace(chr(39), chr(39)*2)}' (FORMAT parquet)")
    finally:
        db.close()


def sec(year: int, month: int, day: int) -> int:
    return int(datetime(year, month, day, tzinfo=timezone.utc).timestamp())


def test_single_source_only_utc_calendar_counts(tmp_path: Path) -> None:
    source = tmp_path / "payments.parquet"
    fixture(source, [sec(2025, 4, 30), sec(2025, 5, 1),
                     sec(2025, 5, 2), sec(2025, 7, 1)])
    mode, paths = g.resolve_sources(source, None)
    assert mode == "single_parquet"
    assert g.period_counts(paths) == [
        {"utc_month": "2025-04", "count": 1},
        {"utc_month": "2025-05", "count": 2},
        {"utc_month": "2025-07", "count": 1},
    ]
    a = g.source_fingerprint(paths)
    b = g.source_fingerprint(paths)
    assert a == b and len(a[0]["sha256_private"]) == 64


def test_five_parts_and_partial_input_rejection(tmp_path: Path) -> None:
    for i, basename in enumerate(g.PARTS):
        fixture(tmp_path / basename, [sec(2025, 5 + i, 1)])
    mode, paths = g.resolve_sources(None, tmp_path)
    assert mode == "five_parquet_parts"
    assert len(paths) == 5
    assert sum(x["count"] for x in g.period_counts(paths)) == 5
    (tmp_path / g.PARTS[-1]).unlink()
    with pytest.raises(ValueError, match="exactly five"):
        g.resolve_sources(None, tmp_path)


def test_reject_ambiguous_sources_and_git_trackable_outputs(tmp_path: Path) -> None:
    fixture(tmp_path / "payments.parquet", [sec(2025, 5, 1)])
    fixture(tmp_path / g.PARTS[0], [sec(2025, 5, 1)])
    with pytest.raises(ValueError, match="Ambiguous"):
        g.resolve_sources(None, tmp_path)
    with pytest.raises(ValueError, match="exactly one"):
        g.resolve_sources(None, None)

    with pytest.raises(ValueError, match="Git-trackable"):
        g.write_private_atomic(
            g.ROOT / "analysis/40_g_adversarial/out/periods-private.json",
            {"fake": 1},
        )
    out = tmp_path / "private-output.json"
    g.write_private_atomic(out, {"calendar_period_counts": [{"count": 2}]})
    assert out.is_file() and not list(tmp_path.glob("*.tmp"))

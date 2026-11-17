"""Synthetic tests for G's private, fail-closed disclosure audit."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

module_path = Path(__file__).with_name("G_disclosure_audit.py")
spec = spec_from_file_location("g_disclosure_audit", module_path)
assert spec and spec.loader
module = module_from_spec(spec)
spec.loader.exec_module(module)


def test_suppression_does_not_authorise_publication():
    sample = """Training period denominators
July eligibility / selection
Evaluation subset: all
Evaluation subset: novel-path
Evaluation subset: May-seen-path
Interpretation gate
| [1–9 suppressed] | 99.9999% |
"""
    result = module.audit(sample)
    assert result["publication_authorised"] is False
    assert result["decision"].startswith("HOLD_")
    assert result["suppressed_line_count"] == 1
    assert result["derived_statistic_line_count"] >= 1
    assert result["missing_required_sections"] == []


def test_missing_sections_and_no_suppression_still_hold():
    result = module.audit("R-G01 aggregate report\nNo obvious small cells")
    assert result["publication_authorised"] is False
    assert "July eligibility / selection" in result["missing_required_sections"]
    assert result["suppressed_line_count"] == 0


def test_derived_regex_detects_full_decimal_and_word_boundaries():
    """A trailing integer-percent match alone masks the escaped-regex defect."""
    pattern = module.DERIVED_PATTERN
    assert pattern.search("optimistic upper 95% error bound")
    assert pattern.search("Clopper-Pearson")
    assert pattern.search("confidence interval")
    assert pattern.search("0.0123")
    assert pattern.search("99.9999%").group(0) == "99.9999%"
    assert pattern.search("0.0123").group(0) == "0.0123"
    assert pattern.search("xCloppery") is None


def test_suppressed_counts_with_bounds_still_hold():
    text = """Training period denominators
July eligibility / selection
Evaluation subset: all
Evaluation subset: novel-path
Evaluation subset: May-seen-path
Interpretation gate
| [1–9 suppressed] | 0.0123 | 99.9999% |
"""
    result = module.audit(text)
    assert result["suppressed_line_count"] == 1
    assert result["derived_statistic_line_count"] == 1
    assert result["publication_authorised"] is False


def test_audit_report_bytes_digest_and_findings_share_one_snapshot():
    """A changed file between separate reads must not misattribute the audit."""
    import hashlib

    original = b"Training period denominators\n| [1\xe2\x80\x939 suppressed] | 99.9999% |\n"
    changed = b"Training period denominators\n| 100 | 0.0000% |\n"
    original_result = module.audit_report_bytes(original)
    changed_result = module.audit_report_bytes(changed)
    assert original_result["report_sha256"] == hashlib.sha256(original).hexdigest()
    assert original_result["suppressed_line_count"] == 1
    assert changed_result["report_sha256"] == hashlib.sha256(changed).hexdigest()
    assert changed_result["suppressed_line_count"] == 0
    assert original_result["publication_authorised"] is False
    assert changed_result["publication_authorised"] is False


def test_audit_report_bytes_rejects_invalid_utf8():
    import pytest

    with pytest.raises(UnicodeDecodeError):
        module.audit_report_bytes(b"Training period denominators\n\xff")


def test_cli_rejects_public_worktree_report_and_destination(tmp_path, monkeypatch, capsys):
    """A private disclosure audit must never read/write artifacts in public Git."""
    import sys
    import pytest

    repo = tmp_path / "public_repo"
    script = repo / "analysis" / "40_g_adversarial" / "G_disclosure_audit.py"
    script.parent.mkdir(parents=True)
    private = tmp_path / "private"
    private.mkdir()
    private_report = private / "report.md"
    private_report.write_text("Training period denominators", encoding="utf-8")
    public_report = repo / "analysis" / "report.md"
    public_report.write_text("Training period denominators", encoding="utf-8")
    monkeypatch.setattr(module, "__file__", str(script))

    cases = (
        (public_report, private / "audit.json"),
        (private_report, repo / "analysis" / "audit.json"),
    )
    for report, dest in cases:
        monkeypatch.setattr(sys, "argv", [
            "G_disclosure_audit.py", "--report", str(report),
            "--private-audit", str(dest),
        ])
        with pytest.raises(SystemExit) as exc:
            module.main()
        assert exc.value.code == 2
        assert "outside the public repository" in capsys.readouterr().err
        assert not dest.exists()

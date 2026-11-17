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

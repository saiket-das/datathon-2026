"""R-G01 disclosure preflight: PRIVATE report audit, never publication approval.

Run ONLY inside the approved offline G executor, on the private aggregate report.
The output is a risk inventory, not a declassification certificate. It never
prints report contents, row-level identifiers, or small-cell values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

EXPECTED_SECTIONS = (
    "Training period denominators",
    "July eligibility / selection",
    "Evaluation subset: all",
    "Evaluation subset: novel-path",
    "Evaluation subset: May-seen-path",
    "Interpretation gate",
)
# This list is deliberately broad: derived numbers can undo count suppression.
DERIVED_PATTERN = re.compile(
    r"(?:[0-9]+(?:\.[0-9]+)?%|\b0\.[0-9]+\b|"
    r"\bClopper\b|\bconfidence\b|\bupper 95%|\bupper error bound)",
    re.I,
)
SMALL_CELL_PATTERN = re.compile(r"\b[1-9]\b")
SUPPRESSION_PATTERN = re.compile(r"\[1[–-]9 suppressed\]")


def audit(text: str) -> dict:
    missing = [s for s in EXPECTED_SECTIONS if s not in text]
    lines = text.splitlines()
    suppressed = [i + 1 for i, line in enumerate(lines) if SUPPRESSION_PATTERN.search(line)]
    derived = [i + 1 for i, line in enumerate(lines) if DERIVED_PATTERN.search(line)]
    # Counts of potential disclosures, never the content itself.
    raw_small = [i + 1 for i, line in enumerate(lines)
                 if SMALL_CELL_PATTERN.search(line) and not SUPPRESSION_PATTERN.search(line)]
    # Every report is held: overlapping subsets, class totals, support shares and
    # bounds can allow reconstruction even if each table cell looks suppressed.
    return {
        "decision": "HOLD_FOR_PRIVATE_HUMAN_DISCLOSURE_REVIEW",
        "reason": "Complementary totals, percentages and bounds may reconstruct suppressed cells",
        "missing_required_sections": missing,
        "suppressed_line_count": len(suppressed),
        "derived_statistic_line_count": len(derived),
        "potential_small_integer_line_count": len(raw_small),
        "publication_authorised": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--private-audit", type=Path, required=True)
    args = parser.parse_args()
    report = args.report.resolve(strict=True)
    dest = args.private_audit.resolve()
    if not report.is_file() or report == dest:
        parser.error("Private report file required; audit destination must differ")
    if dest.exists():
        parser.error("Refuse to overwrite a prior private audit")
    result = audit(report.read_text(encoding="utf-8"))
    result["report_sha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print("PRIVATE AUDIT WRITTEN; PUBLICATION NOT AUTHORISED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

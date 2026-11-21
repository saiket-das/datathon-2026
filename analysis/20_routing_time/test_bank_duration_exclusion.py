"""Check exclusion-signature uncertainty on invented bank cohorts."""
import importlib.util
from pathlib import Path
import numpy as np

SPEC=importlib.util.spec_from_file_location("bank_duration",Path(__file__).with_name("H-B09_bank_duration_exclusion.py"))
assert SPEC and SPEC.loader
MODULE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_zero_and_complete_failure_bounds() -> None:
    assert np.isclose(MODULE.upper_bound(0,100),1-.01**(1/100))
    assert MODULE.upper_bound(100,100)==1


def test_positive_exceptions_increase_bound() -> None:
    assert MODULE.upper_bound(0,100)<MODULE.upper_bound(1,100)<MODULE.upper_bound(10,100)

"""Synthetic-only contract checks for R-G02; never import payment records."""
import importlib.util
from pathlib import Path

module_path = Path(__file__).with_name("R_G02_route_contract.py")
spec = importlib.util.spec_from_file_location("r_g02_contract", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
f = module.route_features

def test_collision_only_between_intermediary_positions():
    assert f("AAAAUS11;BBBBUS11;BBBBUS11;CCCCGB22")["collision"]
    assert not f("AAAAUS11;AAAAUS11;CCCCGB22;AAAAUS11")["collision"]

def test_short_routes_are_structurally_ineligible():
    for route in ("AAAAUS11;BBBBGB22", "AAAAUS11;BBBBUS11;CCCCGB22"):
        x = f(route)
        assert not x["eligible"] and not x["collision"]

def test_censoring_is_unsupported_not_a_negative():
    x = f("AAAAUS11;BBBBUS11;...;CCCCUS11;DDDDGB22")
    assert x["censored"] and not x["eligible"] and not x["collision"]

def test_invalid_tokens_are_not_silently_dropped():
    for route in (None, "", "AAAAUS11;;BBBBGB22", "AAAAUS11;invalid;BBBBGB22"):
        assert not f(route)["eligible"]

def test_noncollision_with_two_distinct_intermediaries():
    x = f("AAAAUS11;BBBBUS11;CCCCUS11;DDDDGB22")
    assert x["eligible"] and not x["collision"]

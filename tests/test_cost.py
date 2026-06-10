import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_plugin  # noqa: E402
import check_plugin  # noqa: E402


def test_catalogue_carries_cost_default_free():
    stations = {"a": {"line": "lit"}, "b": {"line": "lit"}}
    wiring = {"a": {"wire": "api"}, "b": {"wire": "api", "cost": "paid"}}
    cat = build_plugin.build_catalogue(stations, wiring)
    by_id = {s["id"]: s for line in cat["lines"] for s in line["stations"]}
    assert by_id["a"]["cost"] == "free"      # untagged defaults to free
    assert by_id["b"]["cost"] == "paid"


def test_catalogue_orders_free_first_within_line():
    stations = {"paid": {"line": "lit"}, "free": {"line": "lit"}, "freem": {"line": "lit"}}
    wiring = {"paid": {"wire": "api", "cost": "paid"},
              "free": {"wire": "api"},
              "freem": {"wire": "api", "cost": "freemium"}}
    cat = build_plugin.build_catalogue(stations, wiring)
    order = [s["id"] for s in cat["lines"][0]["stations"]]
    assert order == ["free", "freem", "paid"]


def test_validate_flags_invalid_cost():
    stations = {"a": {"line": "lit"}}
    wiring = {"a": {"wire": "api", "cost": "cheap"}}
    probs = check_plugin.validate(stations, wiring, None, None)
    assert any("cost" in p and "'a'" in p for p in probs)


def test_validate_accepts_valid_cost():
    stations = {"a": {"line": "lit"}}
    wiring = {"a": {"wire": "api", "cost": "institutional"}}
    assert check_plugin.validate(stations, wiring, None, None) == []

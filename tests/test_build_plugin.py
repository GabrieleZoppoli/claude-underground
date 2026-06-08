import json, os, sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build_plugin  # noqa: E402

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def _load(name):
    with open(os.path.join(FIX, name)) as f:
        return json.load(f)


def test_build_catalogue_groups_by_line_and_orders_hub_first():
    stations, wiring = _load("mini_stations.json"), _load("mini_wiring.json")
    cat = build_plugin.build_catalogue(stations, wiring)
    keys = [line["key"] for line in cat["lines"]]
    assert keys == ["hub", "lit", "gen"]            # hub first, then map order
    gen = next(l for l in cat["lines"] if l["key"] == "gen")
    ot = gen["stations"][0]
    assert ot["id"] == "opentargets"
    assert ot["wire"] == "auto-mcp"
    assert ot["probe"] == "mcp"                       # auto-mcp -> mcp probe
    europe = next(l for l in cat["lines"] if l["key"] == "lit")["stations"][0]
    assert europe["probe"] == "none"                  # api -> nothing to detect


def test_build_mcp_contains_only_auto_mcp_servers():
    stations, wiring = _load("mini_stations.json"), _load("mini_wiring.json")
    mcp = build_plugin.build_mcp(stations, wiring)
    assert set(mcp["mcpServers"]) == {"opentargets"}
    assert mcp["mcpServers"]["opentargets"]["url"].endswith("/mcp")


def test_build_mcp_raises_when_auto_mcp_missing_block():
    stations = {"x": {"name": "X", "line": "gen"}}
    wiring = {"x": {"wire": "auto-mcp"}}              # no 'mcp' block
    with pytest.raises(ValueError, match="auto-mcp"):
        build_plugin.build_mcp(stations, wiring)

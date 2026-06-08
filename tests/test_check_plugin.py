import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import check_plugin  # noqa: E402

STATIONS = {"a": {"name": "A", "line": "lit"}, "b": {"name": "B", "line": "gen"}}


def test_valid_input_has_no_problems():
    wiring = {"a": {"wire": "api"}, "b": {"wire": "auto-mcp", "mcp": {"url": "x"}}}
    mcp = {"mcpServers": {"b": {"url": "x"}}}
    cat = {"lines": [{"stations": [{"id": "a"}, {"id": "b"}]}]}
    assert check_plugin.validate(STATIONS, wiring, cat, mcp) == []


def test_flags_station_without_wiring():
    wiring = {"a": {"wire": "api"}}
    probs = check_plugin.validate(STATIONS, wiring, None, None)
    assert any("'b'" in p and "no wiring" in p for p in probs)


def test_flags_wiring_for_unknown_station():
    wiring = {"a": {"wire": "api"}, "b": {"wire": "api"}, "ghost": {"wire": "api"}}
    probs = check_plugin.validate(STATIONS, wiring, None, None)
    assert any("ghost" in p for p in probs)


def test_flags_invalid_wire_value():
    wiring = {"a": {"wire": "teleport"}, "b": {"wire": "api"}}
    probs = check_plugin.validate(STATIONS, wiring, None, None)
    assert any("teleport" in p for p in probs)


def test_flags_auto_mcp_without_block():
    wiring = {"a": {"wire": "auto-mcp"}, "b": {"wire": "api"}}
    probs = check_plugin.validate(STATIONS, wiring, None, None)
    assert any("auto-mcp" in p and "'a'" in p for p in probs)


def test_flags_mcp_json_with_non_auto_server():
    wiring = {"a": {"wire": "api"}, "b": {"wire": "api"}}
    mcp = {"mcpServers": {"a": {"url": "x"}}}
    probs = check_plugin.validate(STATIONS, wiring, None, mcp)
    assert any(".mcp.json" in p and "'a'" in p for p in probs)


def test_flags_catalogue_out_of_sync():
    wiring = {"a": {"wire": "api"}, "b": {"wire": "api"}}
    cat = {"lines": [{"stations": [{"id": "a"}]}]}   # missing 'b' → drift
    probs = check_plugin.validate(STATIONS, wiring, cat, None)
    assert any("out of sync" in p for p in probs)

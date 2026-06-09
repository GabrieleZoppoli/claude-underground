import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_plugin  # noqa: E402
import check_plugin  # noqa: E402


def test_build_journeys_passthrough():
    journeys = {"bib": {"description": "d", "stops": ["a"], "playbook": "journeys/bib.md"}}
    assert build_plugin.build_journeys(journeys) == journeys


def test_validate_journeys_flags_unknown_stop():
    stations = {"a": {"line": "lit"}}
    journeys = {"bib": {"description": "d", "stops": ["a", "ghost"], "playbook": "journeys/bib.md"}}
    probs = check_plugin.validate_journeys(stations, journeys, present_files=set())
    assert any("ghost" in p for p in probs)


def test_validate_journeys_flags_missing_playbook():
    stations = {"a": {"line": "lit"}}
    journeys = {"bib": {"description": "d", "stops": ["a"], "playbook": "journeys/bib.md"}}
    probs = check_plugin.validate_journeys(stations, journeys, present_files=set())
    assert any("bib.md" in p and "missing" in p for p in probs)


def test_validate_journeys_ok():
    stations = {"a": {"line": "lit"}}
    journeys = {"bib": {"description": "d", "stops": ["a"], "playbook": "journeys/bib.md"}}
    probs = check_plugin.validate_journeys(stations, journeys, present_files={"journeys/bib.md"})
    assert probs == []

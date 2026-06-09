import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _j(p):
    with open(os.path.join(ROOT, p)) as f:
        return json.load(f)

LEGAL = {"gdpr", "eugrants", "itlaw", "uslaw", "paralegalrev"}

def test_legal_stops_in_stations_and_wired():
    stations, wiring = _j("stations.json"), _j("wiring.json")
    for s in LEGAL:
        assert s in stations and stations[s]["line"] == "legal", f"{s} missing/not legal"
        assert s in wiring and wiring[s]["wire"] == "builtin", f"{s} not wired builtin"

def test_legal_line_in_catalogue():
    cat = _j("plugin/data/catalogue.json")
    legal = [l for l in cat["lines"] if l["key"] == "legal"]
    assert legal and {s["id"] for s in legal[0]["stations"]} == LEGAL

def test_legal_references_and_disclaimer_present():
    base = os.path.join(ROOT, "plugin/skills/tube-map/references/legal")
    for f in ("README.md", "eu.md", "it.md", "us.md"):
        assert os.path.exists(os.path.join(base, f)), f"missing {f}"
    readme = open(os.path.join(base, "README.md")).read().lower()
    assert "not legal advice" in readme and "not a lawyer" in readme

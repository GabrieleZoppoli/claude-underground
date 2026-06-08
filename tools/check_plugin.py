#!/usr/bin/env python3
"""Structural validator for the claude-tube-map plugin (offline, fast, CI-friendly).

Checks that the wiring source + generated artefacts are internally consistent:
  - every drawn station has exactly one wiring entry, and vice versa
  - every wire method is in the allowed enum
  - every auto-mcp station carries an 'mcp' config block
  - plugin/.mcp.json contains ONLY auto-mcp servers
  - plugin/data/catalogue.json covers exactly the drawn station ids

Run from repo root:  python3 tools/check_plugin.py   (exit 0 = ok, 1 = problems)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WIRE_METHODS = {"auto-mcp", "oauth", "apikey", "marketplace", "runtime", "api", "builtin"}


def validate(stations, wiring, catalogue, mcp):
    problems = []
    sids, wids = set(stations), set(wiring)
    for sid in sorted(sids - wids):
        problems.append(f"station '{sid}' has no wiring entry")
    for wid in sorted(wids - sids):
        problems.append(f"wiring has '{wid}' which is not a drawn station")
    for sid in sorted(sids & wids):
        w = wiring[sid]
        wire = w.get("wire")
        if wire not in WIRE_METHODS:
            problems.append(f"station '{sid}' has invalid wire '{wire}'")
        if wire == "auto-mcp" and not w.get("mcp"):
            problems.append(f"station '{sid}' is auto-mcp but has no 'mcp' block")
        if wire == "marketplace" and not w.get("source"):
            problems.append(f"station '{sid}' is marketplace but has no 'source'")
    auto = {s for s, w in wiring.items() if w.get("wire") == "auto-mcp"}
    servers = set((mcp or {}).get("mcpServers", {}))
    for s in sorted(servers - auto):
        problems.append(f".mcp.json declares '{s}' which is not an auto-mcp station")
    cat_ids = {st["id"] for line in (catalogue or {}).get("lines", []) for st in line.get("stations", [])}
    if cat_ids and cat_ids != sids:
        problems.append("catalogue.json is out of sync with stations.json (run: python3 build_plugin.py)")
    return problems


def _load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def main():
    stations = _load(os.path.join(ROOT, "stations.json"), {})
    wiring = _load(os.path.join(ROOT, "wiring.json"), {})
    catalogue = _load(os.path.join(ROOT, "plugin", "data", "catalogue.json"))
    mcp = _load(os.path.join(ROOT, "plugin", ".mcp.json"))
    problems = validate(stations, wiring, catalogue, mcp)
    if problems:
        print(f"plugin check: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"plugin check: ok ({len(stations)} stations, all wired & in sync)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

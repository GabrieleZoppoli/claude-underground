#!/usr/bin/env python3
"""Generate the claude-tube-map plugin's data artefacts from the map.

Reads the drawn map (stations.json, produced by generate_map.py) and the
hand-authored wiring source (wiring.json), joins them by station id, and writes:
  - plugin/data/catalogue.json : every drawn station grouped by line, with its
    wiring method + a computed status-probe kind.
  - plugin/.mcp.json           : ONLY the auto-mcp servers (remote, no-auth).

Never overwrites hand-authored prose. Run from repo root:  python3 build_plugin.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# How a station's status is detected at runtime, derived from its wire method.
PROBE_BY_WIRE = {
    "auto-mcp": "mcp", "runtime": "mcp",
    "marketplace": "skill", "builtin": "skill",
    "oauth": "connector", "apikey": "connector",
    "api": "none",
}

LINE_ORDER = ["hub", "lit", "gen", "comp", "stat", "clin", "viz", "write", "ops"]


def build_catalogue(stations, wiring):
    """Join map data + wiring into the grouped catalogue. Pure function."""
    lines = {}
    for sid, st in stations.items():
        w = wiring.get(sid, {})
        wire = w.get("wire")
        entry = {
            "id": sid,
            "name": st.get("name", sid),
            "tier": st.get("tier"),
            "desc": st.get("desc", ""),
            "how": st.get("how", ""),
            "url": st.get("url", ""),
            "wire": wire,
            "authType": w.get("authType", "none"),
            "personal": bool(w.get("personal", False)),
            "source": w.get("source"),
            "plugin": w.get("plugin"),
            "probe": PROBE_BY_WIRE.get(wire, "none"),
        }
        line = st.get("line", "ops")
        lines.setdefault(line, {
            "key": line,
            "name": st.get("linename", line),
            "color": st.get("color", "#7A868C"),
            "stations": [],
        })["stations"].append(entry)
    ordered = [lines[k] for k in LINE_ORDER if k in lines]
    ordered += [v for k, v in lines.items() if k not in LINE_ORDER]
    return {"lines": ordered}


def build_mcp(stations, wiring):
    """Emit ONLY the auto-mcp servers (remote, no-auth) for the bundled .mcp.json."""
    servers = {}
    for sid in stations:
        w = wiring.get(sid, {})
        if w.get("wire") == "auto-mcp":
            cfg = w.get("mcp")
            if not cfg:
                raise ValueError(f"station '{sid}' is auto-mcp but has no 'mcp' config block")
            servers[sid] = cfg
    return {"mcpServers": servers}


def main():
    with open(os.path.join(HERE, "stations.json")) as f:
        stations = json.load(f)
    with open(os.path.join(HERE, "wiring.json")) as f:
        wiring = json.load(f)
    missing = [s for s in stations if s not in wiring]
    if missing:
        sys.exit(f"wiring.json is missing {len(missing)} station(s): {', '.join(sorted(missing))}")
    catalogue = build_catalogue(stations, wiring)
    mcp = build_mcp(stations, wiring)
    os.makedirs(os.path.join(HERE, "plugin", "data"), exist_ok=True)
    with open(os.path.join(HERE, "plugin", "data", "catalogue.json"), "w") as f:
        json.dump(catalogue, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(HERE, "plugin", ".mcp.json"), "w") as f:
        json.dump(mcp, f, indent=2, ensure_ascii=False)
        f.write("\n")
    n = sum(len(l["stations"]) for l in catalogue["lines"])
    print(f"built catalogue.json ({n} stations, {len(catalogue['lines'])} lines) "
          f"and .mcp.json ({len(mcp['mcpServers'])} auto-mcp server(s))")


if __name__ == "__main__":
    main()

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _frontmatter(path):
    """Return the YAML-ish frontmatter block as a string (between the first two '---')."""
    text = open(path, encoding="utf-8").read()
    assert text.startswith("---"), f"{path} has no frontmatter"
    return text.split("---", 2)[1]


def test_plugin_manifest_valid():
    m = json.load(open(os.path.join(ROOT, "plugin/.claude-plugin/plugin.json")))
    assert m["name"] == "claude-tube-map"
    assert m["version"] and m["description"]


def test_marketplace_lists_the_plugin():
    mk = json.load(open(os.path.join(ROOT, ".claude-plugin/marketplace.json")))
    names = [p["name"] for p in mk["plugins"]]
    assert "claude-tube-map" in names
    entry = next(p for p in mk["plugins"] if p["name"] == "claude-tube-map")
    assert entry["source"] == "./plugin"


def test_router_skill_frontmatter():
    fm = _frontmatter(os.path.join(ROOT, "plugin/skills/tube-map/SKILL.md"))
    assert "name: tube-map" in fm
    assert "description:" in fm


def test_commands_have_descriptions():
    for cmd in ("tube-map", "tube-map-install", "tube-map-status"):
        fm = _frontmatter(os.path.join(ROOT, f"plugin/commands/{cmd}.md"))
        assert "description:" in fm

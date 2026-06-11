# The Zoppoli Research Underground

A Harry-Beck–style metro map of every connector, MCP server and Claude skill that
can boot your research — **genomics · medicine · computational biology · statistics ·
trial design** — with **Claude Code as the grand-central interchange** on your
workstation, and **Codex / GPT-5.5** as the sister terminus ("second engine").

---

## 🚀 Quickstart — install the plugin

The map is also an installable Claude Code plugin, **`claude-tube-map`**. In Claude Code:

```
/plugin marketplace add GabrieleZoppoli/claude-underground
/plugin install claude-tube-map@claude-underground
```

Restart Claude Code, then run **`/tube-map`** — a plain-language welcome that asks what job
you want done. Nothing else to learn; the rest of this page is the map itself and how it's built.

---

**v2** draws **78 stations — the super-confident set** (every connector wired in the
session + every ✅-verified MCP repo / official endpoint / well-known public API) and
adds **interchange lines** — the aggregator servers that genuinely span several
domains, drawn London-Overground-style as cased double-lines, exactly the way a real
metro has lines that connect the other lines. The registry-listed (📇) and unconfirmed
(⚠️) servers are deliberately *pruned* from the drawing; the full ~120-entry inventory
still lives in `CATALOGUE.md`. (To draw everything again, add `"registry","unconfirmed"`
to `DRAWN_TIERS` in `generate_map.py` and re-run.)

### How to read it

**Status & trust** (a fabricated repo is the worst possible error, so trust is on the map):

- ● **live now** — wired in your Claude session (or a core skill).
- ◉ **verified** — confirmed real & ready to wire (a checked MCP repo, official remote endpoint, or public API).
- ⊕ **interchange** — a connecting line stops here (a multi-domain server crosses a spoke).

---

## Files

| File | What it is |
|---|---|
| `index.html` | **Interactive console** — open in any browser. Hover a station for what it does; click for how to wire it; scroll to zoom, drag to pan; search; click a line (or an interchange line) to highlight it. Self-contained, works offline. |
| `exports/research_underground_4k.png` | 3840 px-wide raster — screen / slide / share. |
| `exports/research_underground_poster.pdf` | Vector PDF — print & pin (scales to any size). |
| `master.svg` | The shared vector core (both outputs come from this). |
| `stations.json` | The full catalogue as data (now with `tier` + `interchange`). |
| `generate_map.py` | Generator. Route-builder helpers populate the grid; edit the data dicts, re-run, everything rebuilds. |
| `STATIONS_GUIDE.md` / `.html` / `.pdf` | **Rider's guide** — every station by line: functions, how to connect, whether it's automatic / skill-load / install, and whether it runs best on laptop / workstation / HPC. |
| `make_guide.py` | Generates `STATIONS_GUIDE.md` from the live map data + the invocation / runs-on classifications. |
| `CATALOGUE.md` | The verified deep-research connector inventory the stations are drawn from. |

**Project home:** `~/Documents/progetti A - Z (nome collaboratore o progetto)/C/Claude/connectors_map/`

**Open the console:**
```bash
open "$HOME/Documents/progetti A - Z (nome collaboratore o progetto)/C/Claude/connectors_map/index.html"
```
**Rebuild after edits:**
```bash
cd "$HOME/Documents/progetti A - Z (nome collaboratore o progetto)/C/Claude/connectors_map"
python3 generate_map.py
rsvg-convert -w 3840 -o exports/research_underground_4k.png master.svg
rsvg-convert -f pdf  -o exports/research_underground_poster.pdf master.svg
```

---

## The nine radial lines

🔴 **Literature & Evidence** — PubMed ✓ · Consensus ✓ · deep-research ✓ · literature-review ✓ · research-lookup ✓ · Europe PMC · bioRxiv · medRxiv · Semantic Scholar · Wiley Gateway
🟢 **Genomic Data & Sequencing** — Synapse ✓ · GEO/SRA · Ensembl · UCSC · GDC/TCGA · ClinVar/gnomAD · cBioPortal · DepMap/OncoKB · CELLxGENE · **cBioPortal MCP** · **Open Targets MCP** · **ENA MCP**
⚫ **Compute & Pipelines** — Python (scanpy/squidpy) ✓ · R/Bioconductor · Jupyter · Nextflow/nf-core · Galaxy · Snakemake · cfDNA stack · **ChatSpatial** · **SCMCP** · sc-RNA-QC / nf-core / scvi-tools skills
🔵 **Statistics & Trial Design** — survival/lifelines ✓ · statsmodels ✓ · reporting standards ✓ · peer-review ✓ · critical-thinking ✓ · Bayesian (Stan/PyMC) · power & sample size · **ClinTrials.gov MCP**
🟣 **Clinical & Regulatory** — clinical-reports ✓ · decision-support ✓ · treatment-plans ✓ · ClinicalTrials.gov · EU CTR/CTIS · FDA/EMA · WHO ICTRP
🟡 **Visualization & Figures** — BioRender ✓ · Mermaid ✓ · Figma ✓ · scientific-schematics ✓ · infographics ✓ · image-gen (Nano/FLUX) ✓ · gpt-image-2 (hero)
🟤 **Writing & Publishing** — scientific-writing ✓ · citation-management ✓ · venue-templates ✓ · Office docs ✓ · humanizer ✓ · preparing-slides ✓ · research-grants ✓ · markitdown ✓ · paper-2-web ✓ · posters ✓
⚪ **Orchestration & Lab Ops** — Google Drive ✓ · Gmail ✓ · Google Calendar ✓ · Slack ✓ · workflows/subagents ✓ · schedule/cron ✓ · **Codex / GPT-5.5** ✓ · **BioMCP** · Claude for Life Sciences · BioContextAI (registry + meta) · NAR DB Collection
⚖️ **Legal & Paralegal** — paralegal-review ✓ · GDPR & data protection ✓ · EU grants & consortia ✓ · Italian research law ✓ · US research law ✓ — *paralegal-style, cited EU/IT/US reference checklists; not legal advice*

*(Registry-listed servers — Ensembl/UniProt/STRING/Reactome/ChEMBL/OMOP/napari/PyMOL/ToolUniverse/… — are catalogued in `CATALOGUE.md` but not drawn until their repo is confirmed.)*

**Central interchange:** Claude Code (your workstation). **Sister terminus:** Codex / GPT-5.5.
The winding band along the bottom is *the cfDNA river* — a nod to the liquid biopsy at the core of your programme.

---

## The three interchange lines (the lines that connect the lines)

Real aggregator MCP servers that span several domains, drawn as cased double-lines.
All three are ✅-verified — only super-confident servers earn a connecting line.

- 🟪 **BioMCP** (`genomoncology/biomcp`) — **Literature ↔ Genomic ↔ Trials**: PubMed/PubTator/Europe PMC/Semantic Scholar + ClinVar/gnomAD/cBioPortal/CIViC/OncoKB/GWAS + ClinicalTrials.gov v2. The single best biomedical addition.
- 🟥 **Open Targets** (`opentargets/open-targets-platform-mcp`, official remote) — **Genomic ↔ Clinical**: target–disease–drug associations feeding decision-support.
- ⬜ **Discovery ring** (the dashed outer "Circle line") — **Claude for Life Sciences marketplace + BioContextAI registry**: the install / discovery backbone that every line ultimately wires through.

*(ToolUniverse — `mims-harvard/ToolUniverse`, a 200+-tool aggregator — would be a fourth interchange line, but it's registry-listed; it returns once its repo is confirmed.)*

---

## What to wire next

The fastest single boost is **BioMCP** — it lights up three lines at once. Then the
official remotes (**Open Targets**, **cBioPortal MCP**) and the single-cell / spatial
servers (**ChatSpatial**, **SCMCP**) that map straight onto your Xenium work. The
**Claude for Life Sciences marketplace** (`/plugin marketplace add anthropics/life-sciences`)
and the **BioContextAI registry** are the two discovery anchors — start there to
verify any 📇 registry-listed server before wiring it. Full provenance, repo names and
trust tiers are in `CATALOGUE.md`.

---

## Install & connect it (the plugin)

The map is also an installable Claude Code plugin — `claude-tube-map` — that wires up
the stations for you (**free, honest tools first**) and can run whole jobs end-to-end.

```
/plugin marketplace add GabrieleZoppoli/claude-underground
/plugin install claude-tube-map@claude-underground
```

Then:

- `/tube-map` — a plain-language welcome that sorts jobs into *ready now* (builtin) and *one free install away*, never a wall of tools.
- `/tube-map-install all` — wire everything: **free stops first**, then it asks which paid/institutional subscriptions you actually have (Codex, BioRender, Consensus Pro…) before wiring those.
- `/tube-map-install stat` — wire just one line.
- `/tube-map-status` — the full board (● live · ◉ ready · ⚠ needs you), free-first and cost-marked.
- `/tube-map-update` — check for and install the latest version of the plugin (also offered on entry to `/tube-map`).
- Or just name a journey — *"review this agreement"*, *"build me a bibliography"*, *"plan a grant"*, *"analyse this single-cell data"* — and the matching journey (bibliography · figures · stats-plots · omics · slides · peer-review · scientific-writing · grant · ⚖️ paralegal) wires what it needs and runs it.

**Companion (recommended, free).** For production-grade paper **writing** and **peer review** the map routes to **[academic-research-skills](https://github.com/Imbad0202/academic-research-skills)** by Cheng-I Wu (CC-BY-NC, free for non-commercial research): install with `/plugin marketplace add Imbad0202/academic-research-skills` then `/plugin install academic-research-skills@academic-research-skills`. The map points to it; it stays its own plugin — we don't vendor it.

**Maintainers:** the plugin's data is generated — edit `wiring.json`, run
`python3 build_plugin.py`, and `python3 tools/check_plugin.py` to validate. CI
(`plugin-check`) rebuilds and fails on drift.

---

## License

Dual-licensed. The **map, poster, plugin content (skills · commands · journeys · data) and docs** are **CC BY 4.0** — share/adapt for any purpose, even commercially, with credit (*"Claude Tube Map / The Zoppoli Research Underground — Gabriele Zoppoli, github.com/GabrieleZoppoli/claude-underground, CC BY 4.0"*). The **build & tooling code** (`generate_map.py`, `build_plugin.py`, `make_guide.py`, `tools/`, `tests/`) is also available under **MIT** (see `LICENSE-MIT`). Full text in `LICENSE`.

---

*Generated with Claude Code. Edit `generate_map.py` to add stations, re-colour lines,
or re-route an interchange line — the catalogue and both outputs regenerate from one source.*

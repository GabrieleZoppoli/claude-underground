# The Zoppoli Research Underground

A Harry-Beck–style metro map of every connector, MCP server and Claude skill that
can boot your research — **genomics · medicine · computational biology · statistics ·
trial design** — with **Claude Code as the grand-central interchange** on your
workstation, and **Codex / GPT-5.5** as the sister terminus ("second engine").

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

## The eight radial lines

🔴 **Literature & Evidence** — PubMed ✓ · Consensus ✓ · deep-research ✓ · literature-review ✓ · research-lookup ✓ · Europe PMC · bioRxiv · medRxiv · Semantic Scholar · Wiley Gateway
🟢 **Genomic Data & Sequencing** — Synapse ✓ · GEO/SRA · Ensembl · UCSC · GDC/TCGA · ClinVar/gnomAD · cBioPortal · DepMap/OncoKB · CELLxGENE · **cBioPortal MCP** · **Open Targets MCP** · **ENA MCP**
⚫ **Compute & Pipelines** — Python (scanpy/squidpy) ✓ · R/Bioconductor · Jupyter · Nextflow/nf-core · Galaxy · Snakemake · cfDNA stack · **ChatSpatial** · **SCMCP** · sc-RNA-QC / nf-core / scvi-tools skills
🔵 **Statistics & Trial Design** — survival/lifelines ✓ · statsmodels ✓ · reporting standards ✓ · peer-review ✓ · critical-thinking ✓ · Bayesian (Stan/PyMC) · power & sample size · **ClinTrials.gov MCP**
🟣 **Clinical & Regulatory** — clinical-reports ✓ · decision-support ✓ · treatment-plans ✓ · ClinicalTrials.gov · EU CTR/CTIS · FDA/EMA · WHO ICTRP
🟡 **Visualization & Figures** — BioRender ✓ · Mermaid ✓ · Figma ✓ · scientific-schematics ✓ · infographics ✓ · image-gen (Nano/FLUX) ✓ · gpt-image-2 (hero)
🟤 **Writing & Publishing** — scientific-writing ✓ · citation-management ✓ · venue-templates ✓ · Office docs ✓ · humanizer ✓ · preparing-slides ✓ · research-grants ✓ · markitdown ✓ · paper-2-web ✓ · posters ✓
⚪ **Orchestration & Lab Ops** — Google Drive ✓ · Gmail ✓ · Google Calendar ✓ · Slack ✓ · workflows/subagents ✓ · schedule/cron ✓ · **Codex / GPT-5.5** ✓ · **BioMCP** · Claude for Life Sciences · BioContextAI (registry + meta) · NAR DB Collection

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
the stations for you and shows a live board of what's connected.

```
/plugin marketplace add GabrieleZoppoli/claude-underground
/plugin install claude-tube-map@claude-underground
```

Then:

- `/tube-map` — open the board (● live · ◉ ready · ⚠ needs you).
- `/tube-map-install all` — wire everything (heavy).
- `/tube-map-install stat` — wire just one line.
- `/tube-map-status` — what's connected right now.
- Or just name a journey — *"format these refs for Nature"*, *"make a KM plot"*, *"review this grant"* — and the matching journey (bibliography · figures · stats-plots · slides · peer-review · scientific-writing · paralegal) wires what it needs and runs it.

**Maintainers:** the plugin's data is generated — edit `wiring.json`, run
`python3 build_plugin.py`, and `python3 tools/check_plugin.py` to validate. CI
(`plugin-check`) rebuilds and fails on drift.

---

*Generated with Claude Code. Edit `generate_map.py` to add stations, re-colour lines,
or re-route an interchange line — the catalogue and both outputs regenerate from one source.*

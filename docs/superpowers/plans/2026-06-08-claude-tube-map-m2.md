# Claude Tube Map — M2 (Journeys + Line Playbooks) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Add the task *journeys* (the end-to-end jobs) and per-line playbooks on top of M1's installer, so `/tube-map-install <journey>` and `<line>` run real orchestration, not an "M2 notice".

**Architecture:** A hand-authored `journeys.json` (root, like `wiring.json`) is the single source for journey metadata (description + required stops + playbook file). `build_plugin.py` emits it to `plugin/data/journeys.json`; `check_plugin.py` validates every journey stop is a real station and every playbook/line file exists. Prose playbooks live under `plugin/skills/tube-map/{journeys,lines}/` and are loaded on demand. The router + install command resolve a journey → wire its stops via the M1 engine → follow its playbook.

**Tech Stack:** Python 3.12 stdlib, pytest, Markdown. Builds on M1 (`build_plugin.py`, `check_plugin.py`, `tube-map` skill).

---

## File structure (✚ new, ⟳ changed)

| File | New/Mod | Responsibility |
|---|---|---|
| `journeys.json` | ✚ | Hand-authored: 7 journeys → {description, stops[], playbook}. |
| `build_plugin.py` | ⟳ | Also read `journeys.json` → emit `plugin/data/journeys.json`. |
| `tools/check_plugin.py` | ⟳ | Validate journey stops are real stations; playbook + line files exist. |
| `plugin/data/journeys.json` | ✚ generated | Journey metadata for the skill. |
| `plugin/skills/tube-map/journeys/*.md` | ✚ | 7 journey playbooks. |
| `plugin/skills/tube-map/lines/*.md` | ✚ | 8 line playbooks. |
| `plugin/skills/tube-map/SKILL.md` | ⟳ | Add "Journeys" + "Lines" sections (load playbooks on demand). |
| `plugin/commands/tube-map-install.md` | ⟳ | Resolve `<journey>`/`<line>` for real (drop the M2 notice). |
| `tests/test_journeys.py` | ✚ | TDD the journeys.json build + validation. |

Conventions: run from repo root; `python3`; reuse M1 patterns (`with`-blocks, comma imports to match repo).

---

### Task 1: `journeys.json` + build/validate plumbing (TDD)

**Files:** Create `journeys.json`, `tests/test_journeys.py`; modify `build_plugin.py`, `tools/check_plugin.py`.

- [ ] **Step 1 — create `journeys.json`** (repo root):
```json
{
  "bibliography": {
    "description": "Build a publication-ready, validated bibliography: find/confirm references, dedupe, DOI→BibTeX, format to a target style.",
    "stops": ["pubmed", "consensus", "citation"],
    "playbook": "journeys/bibliography.md"
  },
  "figures": {
    "description": "Produce a publication-quality figure or schematic (pathways, mechanisms, data-driven infographics).",
    "stops": ["schematics", "infographics", "biorender"],
    "playbook": "journeys/figures.md"
  },
  "stats-plots": {
    "description": "Run an appropriate statistical analysis in R/Python and plot it to publication standard, with reporting-standard checks.",
    "stops": ["python", "statsmodels", "survival", "reporting"],
    "playbook": "journeys/stats-plots.md"
  },
  "slides": {
    "description": "Build a high-quality slide deck (house-style if available, else generic) with schematics.",
    "stops": ["slides", "schematics"],
    "playbook": "journeys/slides.md"
  },
  "peer-review": {
    "description": "Peer-review a manuscript or grant: methodology, statistics, design, reproducibility, bias, reporting standards.",
    "stops": ["peerreview", "critthink", "reporting"],
    "playbook": "journeys/peer-review.md"
  },
  "scientific-writing": {
    "description": "Write or revise scientific prose to publication standard (IMRAD, citations, venue rules) and strip AI-tells.",
    "stops": ["sciwriting", "humanizer", "venue"],
    "playbook": "journeys/scientific-writing.md"
  },
  "paralegal": {
    "description": "Paralegal-style review of a research document (contract/consent/privacy). Full EU/IT/US coverage arrives with the Legal line in M3; this handles intake + generic clause review for now.",
    "stops": ["office", "markitdown"],
    "playbook": "journeys/paralegal.md"
  }
}
```

- [ ] **Step 2 — failing test** `tests/test_journeys.py`:
```python
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
```

- [ ] **Step 3 — run, expect fail** (`AttributeError: build_journeys`): `python3 -m pytest tests/test_journeys.py -q`

- [ ] **Step 4 — implement.** In `build_plugin.py` add:
```python
def build_journeys(journeys):
    """Pass journeys metadata through unchanged (kept as a hook for future enrichment)."""
    return journeys
```
and in `main()`, after writing `.mcp.json`, add (using a `with` block):
```python
    jpath = os.path.join(HERE, "journeys.json")
    if os.path.exists(jpath):
        with open(jpath) as f:
            journeys = json.load(f)
        with open(os.path.join(HERE, "plugin", "data", "journeys.json"), "w") as f:
            json.dump(build_journeys(journeys), f, indent=2, ensure_ascii=False)
            f.write("\n")
```

In `tools/check_plugin.py` add:
```python
def validate_journeys(stations, journeys, present_files):
    """journeys: dict; present_files: set of playbook paths that exist on disk."""
    problems = []
    sids = set(stations)
    for jid, j in (journeys or {}).items():
        for stop in j.get("stops", []):
            if stop not in sids:
                problems.append(f"journey '{jid}' references unknown stop '{stop}'")
        pb = j.get("playbook")
        if pb and pb not in present_files:
            problems.append(f"journey '{jid}' playbook is missing: {pb}")
    return problems
```
and wire it into `main()`: load `journeys.json` and the set of files present under `plugin/skills/tube-map/`, then append `validate_journeys(...)` results to `problems`. Concretely, before the `if problems:` block:
```python
    journeys = _load(os.path.join(ROOT, "journeys.json"), {})
    skill_root = os.path.join(ROOT, "plugin", "skills", "tube-map")
    present = set()
    for sub in ("journeys", "lines"):
        d = os.path.join(skill_root, sub)
        if os.path.isdir(d):
            present |= {f"{sub}/{n}" for n in os.listdir(d)}
    problems += validate_journeys(stations, journeys, present)
```

- [ ] **Step 5 — run tests** `python3 -m pytest tests/test_journeys.py -q` → expect `4 passed`. (The real `check_plugin` will report missing playbooks until Task 2/3 create them — that's expected; don't run it green yet.)

- [ ] **Step 6 — commit**
```bash
git add journeys.json build_plugin.py tools/check_plugin.py tests/test_journeys.py
git commit -m "feat(m2): journeys.json + build/validate plumbing for task journeys"
```

---

### Task 2: The 7 journey playbooks

**Files:** Create `plugin/skills/tube-map/journeys/{bibliography,figures,stats-plots,slides,peer-review,scientific-writing,paralegal}.md`

Each file follows this shape (frontmatter `stops` is informational; the machine source is `journeys.json`):

- [ ] **Step 1 — `bibliography.md`:**
```
---
name: bibliography
description: Publication-ready validated bibliography.
stops: pubmed, consensus, citation
---

# Journey — Bibliography  🔴→🟤

**Goal:** turn a draft, a pile of references, or a topic into a validated, correctly-styled bibliography.

## Run it
1. **Ensure stops** — wire `pubmed`, `consensus`, `citation` via the tube-map engine; if any is ⚠ needs-you, say so and proceed with what's available.
2. **Gather** — collect the user's references (or search PubMed/Consensus for the cited claims).
3. **Verify each** — confirm author/year/title/journal and resolve DOIs; flag anything unverifiable rather than inventing it.
4. **Convert & dedupe** — DOI→BibTeX via `citation-management`; merge duplicates.
5. **Style** — format to the target style (Vancouver/APA/Nature) the user names.
6. **Report** — list anything that could not be verified as "needs your check"; never fabricate a citation.
```

- [ ] **Step 2 — `figures.md`:**
```
---
name: figures
description: Publication-quality figure or schematic.
stops: schematics, infographics, biorender
---

# Journey — Figures  🟡

**Goal:** a clean, publication-grade figure — pathway/mechanism schematic, data-driven infographic, or BioRender-style assembly.

## Run it
1. **Ensure stops** — wire `schematics`, `infographics`, `biorender` (biorender needs a login — leave ⚠ if not authenticated).
2. **Pick the tool** — mechanism/pathway → `scientific-schematics`; data figure → `infographics`; bio iconography → BioRender.
3. **Draft** — generate at publication resolution; colourblind-safe palette by default.
4. **Review & iterate** — check labels, legends, units; regenerate once if quality is low.
5. **Deliver** — export the asset and note the source/tool used.
```

- [ ] **Step 3 — `stats-plots.md`:**
```
---
name: stats-plots
description: Statistical analysis + publication plot.
stops: python, statsmodels, survival, reporting
---

# Journey — Stats & plots  ⚫→🔵

**Goal:** run the right analysis and plot it to publication standard.

## Run it
1. **Ensure stops** — `python`, `statsmodels`, `survival` are local (Bash); `reporting` is a skill.
2. **Clarify the question** — outcome type (continuous/binary/time-to-event), design, grouping.
3. **Pick the method** — survival → KM + Cox (`lifelines`/`survival`); regression/GLM/mixed → `statsmodels`; check assumptions.
4. **Analyse** — write and run the code via Bash; show the code and the numeric result.
5. **Plot** — publication-style figure (KM curve, forest/coefficient plot, etc.).
6. **Report-standard check** — apply CONSORT/STROBE/PRISMA items relevant to the design; state n, effect size, CI, and any caveats.
```

- [ ] **Step 4 — `slides.md`:**
```
---
name: slides
description: High-quality slide deck.
stops: slides, schematics
---

# Journey — Slides  🟤(+🟡)

**Goal:** a clean, on-message deck.

## Run it
1. **Ensure stops** — `slides` is the author's personal house-style skill (`preparing-slides`); if absent (public installer), **degrade** to `claude-scientific-writer:pptx` and say so. `schematics` for any diagrams.
2. **Outline** — agree the section flow and the spoken throughline before building.
3. **Build** — generate the deck; one idea per slide; real figures (no native animations).
4. **Polish** — captions, citations on factual claims, consistent type/colour.
5. **Deliver** — the .pptx plus a note on any house-style elements that need the personal skill.
```

- [ ] **Step 5 — `peer-review.md`:**
```
---
name: peer-review
description: Review a manuscript or grant.
stops: peerreview, critthink, reporting
---

# Journey — Peer review  🔵

**Goal:** a rigorous, constructive review of a manuscript or grant.

## Run it
1. **Ensure stops** — `peerreview`, `critthink`, `reporting` (skills).
2. **Intake** — read the document; identify claims, methods, and the central question.
3. **Appraise** — methodology, statistics, design, reproducibility; bias/confounding via GRADE / Cochrane RoB.
4. **Standards** — check against the relevant reporting checklist (CONSORT/STROBE/PRISMA).
5. **Write the review** — major/minor points, ranked by impact; specific and actionable; note strengths too.
```

- [ ] **Step 6 — `scientific-writing.md`:**
```
---
name: scientific-writing
description: Write/revise scientific prose; strip AI-tells.
stops: sciwriting, humanizer, venue
---

# Journey — Scientific writing  🟤

**Goal:** publication-standard prose in the author's voice.

## Run it
1. **Ensure stops** — `sciwriting`, `venue` (skills); `humanizer` is the author's personal skill (degrade to a generic AI-tell pass if absent).
2. **Structure** — IMRAD; outline key points per section first, then prose (never bullet dumps).
3. **Draft** — flowing paragraphs; citations on every factual claim; venue rules from `venue-templates`.
4. **De-tell** — run `humanizer` to remove AI-tells and match house style.
5. **Check** — references resolve; reporting-guideline language where relevant.
```

- [ ] **Step 7 — `paralegal.md` (M2 stub; completed in M3):**
```
---
name: paralegal
description: Paralegal-style document review (generic now; EU/IT/US Legal line lands in M3).
stops: office, markitdown
---

# Journey — Paralegal review  ⚖️ (preview)

**Goal:** a careful, **non-lawyer** review of a research document. Full EU / Italian / US coverage arrives with the **Legal line in M3**; for now this does intake + generic clause review.

## Run it
1. **Ensure stops** — `markitdown` (ingest docx/pdf), `office` (tracked-changes output).
2. **Intake & classify** — convert the document; identify its type (NDA/MTA/DPA/consent/agreement) and jurisdiction.
3. **Generic review** — clause-by-clause read: obligations, liability, IP, data/privacy, termination; flag risks and missing clauses.
4. **Output** — tracked-changes redline + a plain-language summary.
5. **Mandatory disclaimer** — *informational paralegal-style support, not legal advice; Claude is not a lawyer; verify with qualified counsel.* Do not assert jurisdiction-specific legal conclusions without a cited source (the M3 Legal line adds the cited grounding).
```

- [ ] **Step 8 — commit**
```bash
git add plugin/skills/tube-map/journeys/
git commit -m "feat(m2): 7 task-journey playbooks"
```

---

### Task 3: The 8 line playbooks

**Files:** Create `plugin/skills/tube-map/lines/{literature,genomics,compute,statistics,clinical,visualization,writing,ops}.md`

Each is thin — purpose + how to ride it. Template (substitute per the table):

```
---
name: line-<key>
description: <line name> — <one-line purpose>.
---

# <emoji> <Line name>

<1-2 sentence purpose.>

## Ride it
- See the live stops + their status on the board (`/tube-map`); they're grouped under this line in the catalogue.
- `/tube-map-install <key>` wires every stop on this line (detect → act → re-check), leaving auth/runtime stops as ⚠ needs-you with the exact next step.
- <one line of line-specific guidance>.
```

- [ ] **Step 1 — create all 8** using the template + this per-line data:

| file | key | emoji | name | purpose | line-specific guidance |
|---|---|---|---|---|---|
| literature.md | lit | 🔴 | Literature & Evidence | find, synthesise and cite the evidence base | start with PubMed/Consensus; `deep-research` for a cited multi-source sweep |
| genomics.md | gen | 🟢 | Genomic Data & Sequencing | pull and query genomic/variant/cancer data | Open Targets is the one zero-config MCP; most others are public APIs or local servers |
| compute.md | comp | ⚫ | Compute & Pipelines | run analyses and reproducible pipelines | Python/R are local via Bash; single-cell/spatial servers are local installs |
| statistics.md | stat | 🔵 | Statistics & Trial Design | choose and run the right statistics | survival/lifelines + statsmodels are live; pair with the stats-plots journey |
| clinical.md | clin | 🟣 | Clinical & Regulatory | clinical reports + regulatory grounding | report skills are live; trial/regulatory registries are public APIs |
| visualization.md | viz | 🟡 | Visualization & Figures | publication figures and diagrams | pair with the figures journey; BioRender needs a login |
| writing.md | write | 🟤 | Writing & Publishing | author, format and publish | pair with the bibliography / scientific-writing / slides journeys |
| ops.md | ops | ⚪ | Orchestration & Lab Ops | lab comms, scheduling, second-engine | Drive/Gmail/Calendar/Slack are claude.ai connectors (login); Codex is a second engine |

- [ ] **Step 2 — commit**
```bash
git add plugin/skills/tube-map/lines/
git commit -m "feat(m2): 8 per-line playbooks"
```

---

### Task 4: Wire journeys/lines into the skill + install command

**Files:** modify `plugin/skills/tube-map/SKILL.md`, `plugin/commands/tube-map-install.md`; regenerate; run full validation.

- [ ] **Step 1 — SKILL.md: add a "Journeys & lines" section** after the "Two ways in" section:
```
## Journeys & lines (load on demand)

- **Journeys** are end-to-end jobs. `${CLAUDE_PLUGIN_ROOT}/data/journeys.json` maps each
  journey → its required `stops` + a `playbook` path. To run one: wire its stops with the
  engine above, then read and follow `${CLAUDE_PLUGIN_ROOT}/skills/tube-map/<playbook>`.
  Journeys: bibliography · figures · stats-plots · slides · peer-review · scientific-writing · paralegal.
- **Lines** have a short playbook at `${CLAUDE_PLUGIN_ROOT}/skills/tube-map/lines/<line>.md`.
  Read it when the user wants to "ride" a whole domain line.

Load these files only when the relevant journey/line is actually used — never all at once.
```

- [ ] **Step 2 — tube-map-install.md: replace the journey clause.** Change the line:
```
- a journey name → that journey's required stops (journeys arrive in M2; until then,
  say so and offer the closest line).
```
to:
```
- a journey name → read `${CLAUDE_PLUGIN_ROOT}/data/journeys.json`, wire that journey's
  `stops`, then read & follow its `playbook` to run the job end-to-end.
- a line key → also read `${CLAUDE_PLUGIN_ROOT}/skills/tube-map/lines/<key>.md` for guidance.
```

- [ ] **Step 3 — regenerate + full validation**
```bash
python3 build_plugin.py
python3 tools/check_plugin.py     # expect: ok (now that playbooks exist)
python3 -m pytest tests/ -q       # expect: 19 passed (15 M1 + 4 journeys)
```
Expected check output: `plugin check: ok (79 stations, all wired & in sync)`.

- [ ] **Step 4 — confirm no drift + commit**
```bash
git add plugin/skills/tube-map/SKILL.md plugin/commands/tube-map-install.md plugin/data/journeys.json
git commit -m "feat(m2): router + install command run journeys and line playbooks"
```

---

### Task 5: README + validate

- [ ] **Step 1 — README:** under the plugin section's command list, add:
```markdown
- Or just name a journey — *"format these refs for Nature"*, *"make a KM plot"*, *"review this grant"* — and the matching journey (bibliography · figures · stats-plots · slides · peer-review · scientific-writing · paralegal) wires what it needs and runs it.
```
- [ ] **Step 2 — local manifest re-validate:** `claude plugin validate "$PWD/plugin"` → expect ✔.
- [ ] **Step 3 — commit**
```bash
git add README.md
git commit -m "docs(m2): journeys in the README"
```

---

## Self-review (plan vs goal)
- 7 journeys with required stops + orchestration: Task 1 (data) + Task 2 (playbooks). ✓
- 8 line playbooks: Task 3. ✓
- `/tube-map-install <journey>`/`<line>` run real playbooks (no M2 notice): Task 4. ✓
- Validation that journey stops are real + playbooks exist: Task 1 (`validate_journeys`) + Task 4 (green check). ✓
- paralegal is a stub that defers jurisdiction conclusions to M3 with the disclaimer. ✓
- **Placeholder scan:** every file's content is given (journeys via full text; lines via template + per-line table). **Type consistency:** `build_journeys`/`validate_journeys` signatures match the tests; `journeys.json` keys (`description`/`stops`/`playbook`) are used identically in build, validate, and the skill.

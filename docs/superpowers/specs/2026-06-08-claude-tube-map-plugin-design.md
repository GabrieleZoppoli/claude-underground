# Claude Tube Map — plugin design

- **Date:** 2026-06-08
- **Repo:** `GabrieleZoppoli/claude-underground` (the plugin lives inside the existing map repo)
- **Status:** Design approved (brainstorming). Next step: implementation plan via `writing-plans`.
- **One-line summary:** Turn the Research Underground map into an installable Claude Code plugin that discovers, wires up, and orchestrates the connectors/skills/MCPs already drawn on the map — through one lightweight router skill (`tube-map`) plus on-demand line and journey playbooks — and adds a brand-new Legal/Paralegal line for scientific life (EU · Italian · US).

---

## 1. Context & motivation

`stations.json` already is the single source of truth for the map: ~78 stations across 8 radial domain lines (Literature 🔴, Genomic 🟢, Compute ⚫, Statistics 🔵, Clinical 🟣, Visualization 🟡, Writing 🟤, Orchestration ⚪) plus the Claude hub, each carrying a `how` field that encodes its mechanism (`Skill: …`, `MCP connected now`, `MCP: org/repo`, `Install: /plugin …`, public API, codex) and a `tier` (live vs verified). `generate_map.py` renders the map from that data.

The map *shows* the ecosystem; it does not *install or run* it. This project adds the action layer: a package any Claude can install that batch-connects what's connectable, guides the rest, and exposes a "Claude tube map" superskill with two ways in — invoke everything, or ride a single line / take a single journey.

## 2. Goals & non-goals

**Goals**
- One-command install from GitHub; works for anyone, not just the author.
- A superskill that (a) discovers what's wired, (b) wires what isn't, (c) orchestrates cross-line task journeys.
- Stay faithful to the map: lines = domains; journeys = the real jobs (bibliography, figures, stats+plots, slides, peer-review, scientific writing, paralegal revision).
- A new Legal/Paralegal line (EU/IT/US), skill-based with cited grounding.
- Low standing cost: nearly free to have installed; weight scales with use.
- Map and plugin never drift — both derive from `stations.json`.

**Non-goals**
- Re-bundling third-party plugin skills (`claude-scientific-writer:*`, `superpowers:*`, `legalzoom:*`) — point to their marketplaces instead.
- Shipping the author's personal/house-style skills publicly (`preparing-slides`, `codex-dispatch`, `gabriele-styled-emails`) — reference them; degrade gracefully when absent.
- Storing anyone's credentials. Auth uses each provider's own login.
- Giving legal advice. The Legal line is paralegal-style, cited, disclaimered support.

## 3. Decisions locked in brainstorming

| # | Decision | Choice |
|---|---|---|
| 1 | Audience / bundling | **Public core; personal skills referenced, not bundled.** |
| 2 | Invocation taxonomy | **Both** — domain *lines* (install + capability) and task *journeys* (cross-line jobs). |
| 3 | Wiring model | **Hybrid** — auto-wire the safe subset; guide the rest with provider-native auth pop-ups / token paste. |
| 4 | Legal line build | **Skill + cited EU/IT/US references**, no external service (legalzoom optional). |
| 5 | Build/maintenance | **Hybrid generator** — generate wiring/catalogue from `stations.json`; hand-author prose. Same repo. |
| 6 | Skill granularity | **One thin router skill + on-demand files**, not 17 registered skills (resolves "heavy / in-the-way"). |

**Rationale for #6 (the key UX call):** the real capabilities (`citation-management`, `scientific-writing`, BioMCP…) are already registered skills that auto-trigger. The tube-map only needs a narrow trigger surface — *set me up / what's available*, the journeys, and legal — so a single sharp-described skill routes cleanly without diluting the skill list, and having it installed costs ~one description until used.

## 4. Architecture

### 4.1 Repo layout (✚ = new, ⟳ = changed)

```
claude-underground/
├── .claude-plugin/marketplace.json        ✚ makes the repo installable as a marketplace
├── stations.json                          ⟳ + optional fields: wire, authType, mcp, runtime, statusProbe, journeys, personal
├── generate_map.py                          (unchanged — still draws the map)
├── build_plugin.py                        ✚ sibling generator (the map generator's twin)
├── tools/check_stations.py                ⟳ extended validation (new fields, catalogue, .mcp.json, journeys)
├── .github/workflows/weekly-map-check.yml ⟳ also rebuilds the plugin + checks drift
└── plugin/                                ✚ THE PLUGIN
    ├── .claude-plugin/plugin.json          name: claude-tube-map
    ├── skills/
    │   └── tube-map/
    │       ├── SKILL.md                     ← the ONLY registered skill (router + board)
    │       ├── lines/                        ← 9 domain-line playbooks (read on demand)
    │       │   ├── literature.md … ops.md
    │       │   └── legal.md                 ✚ new line
    │       ├── journeys/                     ← 7 journey playbooks (read on demand)
    │       │   ├── bibliography.md, figures.md, stats-plots.md, slides.md,
    │       │   └── peer-review.md, scientific-writing.md, paralegal.md ✚
    │       └── references/                   ← legal primary-source pointers, clause libraries, checklists
    ├── commands/
    │   ├── tube-map.md                       → /tube-map        (open the board)
    │   ├── tube-map-install.md               → /tube-map-install [all | <line> | <journey>]
    │   └── tube-map-status.md                → /tube-map-status (what's wired)
    ├── .mcp.json                           ⟳ GENERATED — auto-wire-safe subset only
    └── data/catalogue.json                 ⟳ GENERATED from stations.json
```

> Implementation note: exact `plugin.json` / `marketplace.json` field names are verified against current Claude Code plugin docs during M1 (schema evolves). Design is schema-agnostic.

### 4.2 The router skill

`skills/tube-map/SKILL.md` is thin and stable. It (a) carries a sharp `description` so Claude invokes it for *discovery/setup* requests, the *journeys*, and *legal/paralegal* work — and **not** for tasks the real skills already own; (b) reads `data/catalogue.json` to render a textual "you-are-here" board; (c) routes by reading the relevant `lines/<x>.md` or `journeys/<y>.md` **only when used** (progressive disclosure). It reimplements nothing.

### 4.3 Lines vs journeys

- **Line** = a domain's track. Loading `lines/statistics.md` = that line's playbook + wiring for its stops. Cheap.
- **Journey** = a trip across lines. A journey playbook declares **required stops**, ensures they're wired (delegating to the relevant line wiring), then **orchestrates the job**.

Journey → lines mapping:

| Journey | Rides | Required stops (examples) |
|---|---|---|
| bibliography | 🔴→🟤 | PubMed, Consensus, citation-management |
| figures | 🟡 | scientific-schematics, infographics, BioRender |
| stats-plots | ⚫→🔵 | Python/R, statsmodels/lifelines, survival, reporting-standards |
| slides | 🟤(+🟡) | preparing-slides *(personal; degrades to pptx)*, schematics |
| peer-review | 🔵 | peer-review, critical-thinking, reporting-standards |
| scientific-writing | 🟤 | scientific-writing, humanizer, venue-templates |
| paralegal | ⚖️ | legal line stops + docx + markitdown |

### 4.4 Data model

`stations.json` gains **optional** fields (so `generate_map.py` still renders unchanged):

| Field | Meaning |
|---|---|
| `wire` | enum: `auto-mcp` · `oauth` · `apikey` · `marketplace` · `runtime` · `api` · `builtin` |
| `authType` | `oauth` · `apikey` · `none` |
| `mcp` | server config block (url/transport or command/args) — only for `auto-mcp` |
| `runtime` | local install hint (e.g. `uv tool install …`) — only for `runtime` |
| `statusProbe` | how to detect if already wired (MCP tools present / skill listed / `claude mcp list`) |
| `journeys` | array of journey ids this stop serves |
| `personal` | bool — author's house-style skill; reference, don't bundle |

`build_plugin.py` reads these → emits `data/catalogue.json` (per-line stops with desc/how/tier/wire/statusProbe/journeys), `.mcp.json` (the `auto-mcp` subset only), and journey manifests (required-stop lists). Populating `wire` for all ~78 stations is an M1 task; the `how` field gives strong hints but `wire` is explicit.

## 5. Wiring / install engine

Per station, the engine: **detect → if live, confirm & skip → else act (showing the command first) → re-check → update board.** It **never silently skips**; anything it can't finish is flagged **"needs you"** with the exact next step (consistent with the author's "report outcomes faithfully / no silent failures" values).

| `wire` | Action | Notes |
|---|---|---|
| `auto-mcp` | Ships in generated `.mcp.json`; engine verifies present | only **remote, no-auth, read-only** HTTP MCPs (e.g. Open Targets remote endpoint) |
| `oauth` | Trigger provider login pop-up (Google/Slack/Figma/Synapse) | we never see/store the password |
| `apikey` | Prompt to paste token (OncoKB…) | stored by the connector, not by us |
| `marketplace` | Show & run `/plugin marketplace add …` / `/plugin install …` | user approves |
| `runtime` | Show local install line (BioMCP, ENA, ChatSpatial, SCMCP via uv/pip/conda) | detect runtime first |
| `api` | Nothing to install | line file teaches usage (Europe PMC, GDC, UCSC, openFDA) |
| `builtin` | Nothing to install | already a Claude skill/tool |

**Personal stations** (`personal: true`): not bundled. The catalogue points to the author's own marketplace; journeys **degrade gracefully** (e.g. `slides` falls back to `claude-scientific-writer:pptx` with a note that the house-style version is available separately).

## 6. Invocation UX

Two speeds, no forced menus:

- **Newcomer →** `/tube-map` opens the board (● live / ◉ ready / ⚠ needs-you); the metaphor self-explains; guided install.
- **Expert →** one shot: `/tube-map-install stat`, or plain language (*"format these refs for Nature"* → bibliography journey, no menu), or bypass the plugin and call the underlying skill.

The board is **opt-in** — only on `/tube-map` / `/tube-map-status`, never auto-dumped. **"Everything"** (`/tube-map-install all`) is the only intentionally heavy path and is labelled as such.

## 7. Legal / Paralegal line (new)

A new ⚖️ domain line, skill-based, with cited grounding. **Hard rules:** no un-cited legal claim; never invent article numbers / case law; flag uncertainty; mandatory disclaimer — *informational paralegal-style support, not legal advice; Claude is not a lawyer; verify with qualified counsel in the relevant jurisdiction.* High hallucination risk in this domain, so live verification via `research-lookup` / `deep-research` against primary sources is required for anything load-bearing.

**Stops:**

- **EU:** GDPR (Reg. 2016/679, incl. Art. 89 research exemptions, DPAs, transfers) · Horizon Europe Model Grant Agreement + Consortium Agreement (DESCA), IP/access rights · Clinical Trials Regulation 536/2014 + CTIS (CTAs) · MTA/DTA · research ethics & informed consent.
- **Italy (very specific):** Codice Privacy (D.lgs 196/2003 as amended by 101/2018) + Garante guidance · public procurement Codice dei contratti pubblici (D.lgs 36/2023), RUP, convenzioni conto terzi / contratti di ricerca, codice etico, regolamenti di ateneo · AIFA / comitati etici, consenso informato. Grounding source: **Normattiva / Gazzetta Ufficiale**.
- **US:** HIPAA Privacy/Security + BAAs · Common Rule (45 CFR 46) / IRB / informed consent · MTA (UBMTA/NIH), CDA/NDA · IP: Bayh-Dole (35 USC 200-212), licensing, invention assignment · *(optional)* legalzoom stop for US contract review.

**Paralegal journey:** intake (docx/pdf via `markitdown`) → classify type + jurisdiction → clause-by-clause review against a jurisdiction checklist + clause library → severity-ranked risk flags + missing-clause detection → tracked-changes redline (via `docx`) + plain-language summary → primary-source citation for each material point → disclaimer; escalate high-risk/low-confidence to "consult qualified counsel" (mirrors the `legalzoom:attorney-assist` pattern, but no external service).

## 8. Map ↔ plugin sync

`build_plugin.py` is the map generator's twin: `stations.json` → `catalogue.json` + `.mcp.json` + journey manifests. It **never** overwrites hand-authored prose (skills read `catalogue.json` at runtime; the generator only writes the `data/` + `.mcp.json` artefacts). `tools/check_stations.py` is extended to validate: new fields well-formed; catalogue matches stations; `.mcp.json` is valid JSON and contains **only** `auto-mcp` servers; every journey's required stops exist; every line file references real stations. The weekly Action rebuilds the plugin so drift fails CI.

## 9. Distribution

`.claude-plugin/marketplace.json` (marketplace name `claude-underground`) lists the plugin with `source: ./plugin`. Install:

```
/plugin marketplace add GabrieleZoppoli/claude-underground
/plugin install claude-tube-map@claude-underground
```

## 10. Testing & acceptance

- **Validation:** `check_stations.py` passes (schema, catalogue, `.mcp.json`, journeys).
- **Dry-run:** install engine has a mode that prints what *would* be wired without acting — testable without real auth.
- **Router behaviour (RED/GREEN, per `superpowers:writing-skills`):** plain-language jobs route to the right journey; the router does **not** fire on tasks the real skills already own; "everything" is the only heavy path.
- **Legal safety (RED/GREEN):** the line refuses un-cited legal claims and always emits the disclaimer; high-risk docs trigger the "consult counsel" escalation.
- **The wife test (M1 acceptance):** a non-author installs from a clean machine and reaches one working journey using only the README + `/tube-map`, with **no insider help**. If she gets stuck, the onboarding — not the user — is the bug.

## 11. Milestones

- **M1 — Installer + sync + lines.** Plugin scaffold, `marketplace.json`, `build_plugin.py`, `catalogue.json`, `.mcp.json`, the `tube-map` router skill, `/tube-map*` commands, the wiring engine, the 8 existing domain-line files (the ⚖️ legal file arrives in M3), extended validation + CI. Ships a working **install & connect** tool. Acceptance includes the wife test.
- **M2 — Journeys.** Six task journeys fully built (bibliography, figures, stats-plots, slides, peer-review, scientific-writing) with graceful degradation for personal stops; the paralegal journey is scaffolded here and completed in M3 once the legal content lands.
- **M3 — Legal line.** Full EU/IT/US legal content, clause libraries, checklists, cited grounding, and the complete paralegal journey. Biggest authoring effort; gated by the legal-safety tests.

## 12. Risks & open questions

- **Plugin/MCP schema specifics** — verify exact `plugin.json` / `marketplace.json` / `.mcp.json` shapes against current docs in M1.
- **Status detection reliability** — detecting "is this MCP wired" from within a session may need `claude mcp list` via Bash as a fallback; confirm in M1.
- **`auto-mcp` subset is small** — most biomedical MCPs are local-runtime; honest classification matters so the board doesn't over-promise "auto."
- **Legal accuracy** — primary-source citation + verification is mandatory; treat as the highest-risk content and test hardest.
- **Personal-skill boundary** — confirm which personal skills are referenced vs. fully omitted from the public catalogue.

## 13. Out of scope (future)

Registry-listed (📇) servers from `CATALOGUE.md` until their repos are confirmed; a fourth interchange line (ToolUniverse); non-scientific legal domains; any auto-send / non-dry-run bulk action without explicit per-step approval.

---
name: tube-map
description: Use to discover, install, or connect the Claude Research Underground — the biomedical connectors, MCP servers and skills on the map (free/low-cost tools first) — or to ride a task journey (bibliography, figures, stats+plots, omics analysis, slides, peer-review, scientific writing, grant planning, paralegal revision). Triggers on "set me up / what's available / what's connected / tube map / install the map / wire up X line" and on the named journeys. Do NOT use for tasks an already-installed skill owns directly.
---

# Claude Tube Map

The map's action layer. This skill **routes and wires**; it never reimplements a
capability. Once a stop is wired you use it directly — this skill gets out of the way.

## The catalogue (single source of truth)

Read `${CLAUDE_PLUGIN_ROOT}/data/catalogue.json`. It lists every station grouped by
line, each with: `id`, `name`, `tier`, `desc`, `how`, `url`, `wire`, `authType`,
`personal`, `cost`, `probe`. Stations are already ordered **free-first** within each line.
This file is generated from the map — never hand-edit it.

**Free-first (hard preference):** prefer `cost: free` tools, then `freemium`, and only reach
for `paid`/`institutional` when no free stop on the same line does the job. When you do
surface a paid tool, say it's paid and name the free alternative. Cost markers for the board:
🆓 free · ◐ freemium · 💲 paid · 🏛 institutional.

## Two ways in

1. **Everything** — `/tube-map-install all`. Heavy (many stops). Wire the whole map.
2. **One line or one journey** — `/tube-map-install <line>` (e.g. `stat`), or just say
   what you want ("format these refs for Nature") and route to the matching journey.

**Front door:** `/tube-map` greets a newcomer with plain-language *jobs* (free-first) and an
**interactive picker** (the `AskUserQuestion` tool — a selectable menu of the top jobs; free-text is
always allowed so they can just type instead), not the 84-stop board. The full board is opt-in:
`/tube-map-status` (or "show me everything"). Never auto-dump it.

**Subscription wizard:** when installing, wire free stops first; before any
`freemium`/`paid`/`institutional` stop, ask once which the user actually has (Codex, BioRender,
Consensus Pro, Synapse, Wiley…) and wire only those — see `/tube-map-install`.

## Staying current & companion plugins

- **Update check:** `/tube-map` offers an update check on entry; `/tube-map-update` runs it on
  demand — refresh the marketplace, `claude plugin update claude-tube-map@<marketplace>`, report the
  version delta **honestly**, then restart / `/reload-plugins`. Never claim an update without a
  passing result.
- **Recommended companion (free — route to it, don't reinvent):** for production-grade paper
  **writing** and **peer review**, prefer **academic-research-skills** (`Imbad0202/academic-research-skills`,
  by Cheng-I Wu — CC-BY-NC, free for non-commercial research; skills: deep-research · academic-paper ·
  academic-paper-reviewer · academic-pipeline). It's far deeper than this map's thin writing/review
  routing, so the writing / peer-review / grant journeys should **offer to install it and hand off**
  rather than duplicate it: `/plugin marketplace add Imbad0202/academic-research-skills` →
  `/plugin install academic-research-skills@academic-research-skills`. It's a companion, not a
  station — we point to it, we never vendor its files.

## Journeys & lines (load on demand)

- **Journeys** are end-to-end jobs. `${CLAUDE_PLUGIN_ROOT}/data/journeys.json` maps each
  journey → its required `stops` + a `playbook` path. To run one: wire its stops with the
  engine below, then read and follow `${CLAUDE_PLUGIN_ROOT}/skills/tube-map/<playbook>`.
  Journeys: bibliography · figures · stats-plots · omics · slides · peer-review · scientific-writing · grant · paralegal.
- **Lines** have a short playbook at `${CLAUDE_PLUGIN_ROOT}/skills/tube-map/lines/<line>.md`.
  Read it when the user wants to "ride" a whole domain line.

Load these files only when the relevant journey/line is actually used — never all at once.

## Detecting status (`probe`)

- `probe: mcp` → is the server's MCP tool present this session? (fallback: `claude mcp list` via Bash)
- `probe: skill` → is the skill/plugin available in this session's skills?
- `probe: connector` → is the connector authenticated / its tools present?
- `probe: none` → nothing to detect; it's a public API usable on demand.

Render each stop as **● live** (detected), **◉ ready** (installable now), or
**⚠ needs you** (blocked — needs a login, token, or local runtime you must provide).

**Two refinements that keep the board honest:**
- A stop whose `authType` is `oauth` or `apikey` is **⚠ needs you** — a login or token is required — *unless* you can confirm that credential is already in place. Never show such a stop **● live** on a skill/connector probe alone: the probe cannot see whether the login or key exists.
- A `runtime` stop you can't detect is **◉ ready** (show its install line from `how`) — don't assume it's missing, since a local library may already be installed. Confirm with the user rather than guessing either way.

## Wiring engine (per stop)

For each target stop: **detect → if live, confirm & skip → else act, showing the exact
command first → re-check → update the board.** Act by `wire`:

| `wire` | Action |
|---|---|
| `auto-mcp` | Already declared in the bundled `.mcp.json`; just verify it's present. |
| `oauth` | Trigger the provider's own login pop-up (you log into Google/Slack/Figma/Synapse directly — we never see or store the password). |
| `apikey` | Ask the user to paste the token; the connector stores it, not us. |
| `marketplace` | Show & run `/plugin marketplace add {source}`, then (if `plugin` is set) `/plugin install {plugin}`, using the stop's `source`/`plugin` from the catalogue; the user approves. |
| `runtime` | Show the local install line from `how` (uv/pip/conda/clone); detect the runtime first. |
| `api` | Nothing to install — note the endpoint from `url`/`how` and use it on demand. |
| `builtin` | Nothing to install — it's already a Claude skill/tool. |

**Honesty rules (hard):** never silently skip a stop. If you can't finish one, leave it
**⚠ needs you** with the exact next step. Show every command before running it. Report
what actually happened — successes and failures — never claim a stop is wired without a
passing probe.

**Personal stops** (`personal: true`, e.g. `slides` → preparing-slides): not bundled
publicly. Point to the author's own marketplace, and for journeys degrade gracefully to
the generic equivalent (e.g. `claude-scientific-writer:pptx`) with a one-line note.

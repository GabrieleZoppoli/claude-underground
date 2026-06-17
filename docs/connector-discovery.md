# Connector discovery — playbook

How to run a "weekly connector discovery" pass that proposes **new** biomedical MCP
connectors for the catalogue. This is a **manual Claude Code task** — there is no GitHub
Action for it (the only scheduled Action, `weekly-map-check`, does liveness only). Run it
on demand.

## Goal

Find biomedical MCP servers that are **not already known** and are **in scope for this
stack**, verify they are real, and propose them as **catalogue-only** additions for review.

## Hard rules

1. **Dedup against open PRs first.** Before proposing anything, list the open discovery PRs
   and read their candidate tables:
   ```
   gh pr list --search "discovery in:title" --state open
   gh pr view <n>            # for each
   ```
   **Skip any repo already proposed in an open or draft discovery PR.** This is the rule the
   2026-06-17 triage added: PRs #1 and #13 had re-proposed the same six repos because earlier
   passes never checked the open backlog.

2. **Dedup against the catalogue.** Skip any repo already in `CATALOGUE.md`:
   ```
   grep -i "<owner>/<repo>" CATALOGUE.md
   grep -i "<repo-stem>" CATALOGUE.md     # owners are sometimes written owner-repo with a hyphen
   ```

3. **Verify before proposing.** Every candidate must return HTTP 200:
   ```
   curl -s -o /dev/null -w "%{http_code}" -L -A "Mozilla/5.0" "https://github.com/<owner>/<repo>"
   ```
   Discard anything that 404s, and skip a personal 0-star repo unless it fills a real gap.

4. **Scope filter** (this is an oncology / clinical / genomics / translational stack).
   In scope: literature & evidence, human genomics & variants, cancer genomics, clinical &
   regulatory, trial design, compute/single-cell/spatial, figures, writing. **Drop**:
   plant-only, model-organism-only (Drosophila, C. elegans, aging-only) unless they clearly
   serve comparative work; GPU-heavy de-novo design tools needing local infra; anything an
   existing entry already covers.

5. **Catalogue-only — do NOT place on the board.** The rendered map (`generate_map.py`
   `STATIONS` + `place()` calls) is **curated and frozen** per the standing "don't grow the
   board" decision. New discoveries go into `CATALOGUE.md` only; `generate_map.py` prunes any
   unplaced station, so the map renders identically.

## Sources

- **BioContextAI registry** — github.com/biocontext-ai/registry (`/servers/*/meta.yaml`).
- **Anthropic life-sciences marketplace** — github.com/anthropics/life-sciences.
- **Targeted GitHub search** — biomedical / bioinformatics MCP servers updated recently.

## Output

- A branch + PR that appends rows to `CATALOGUE.md` with the correct trust tier
  (✅ verified live page / 📇 registry-listed) and a one-line rationale per entry.
- Title: `Weekly connector discovery — <YYYY-MM-DD>`.
- Body clearly marked **"CANDIDATES — do not merge without Gabriele's approval."**
- Add a dated line to the `## Maintenance log` at the bottom of `CATALOGUE.md`.

## Backlog hygiene

If more than one discovery PR is open, **consolidate or close the stale ones** before
opening a new one, so candidates do not pile up.

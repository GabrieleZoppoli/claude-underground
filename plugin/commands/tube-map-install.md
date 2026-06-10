---
description: Install/connect the map — free tools first, then ask which paid/institutional subscriptions you have before wiring those.
argument-hint: "[all | <line: lit|gen|comp|stat|clin|viz|write|ops|legal> | <journey>]"
---

Use the `tube-map` skill. Resolve the target from `$ARGUMENTS`:

- `all` → every station in `${CLAUDE_PLUGIN_ROOT}/data/catalogue.json` (warn it's heavy).
- a line key (e.g. `stat`) → that line's stations; also read `${CLAUDE_PLUGIN_ROOT}/skills/tube-map/lines/<key>.md`.
- a journey name → read `${CLAUDE_PLUGIN_ROOT}/data/journeys.json`, wire that journey's `stops`, then read & follow its `playbook`.

**Free-first install order (use each stop's `cost` field):**
1. **Free stops** (`cost: free`, the default) — wire these first, no questions asked. Free does
   **not** mean zero-install: a free `marketplace` stop still needs one `/plugin install` — run it
   transparently (show the command first), it simply costs nothing. Don't call it "paid".
2. **The subscription wizard** — BEFORE touching any `freemium` / `paid` / `institutional`
   stop in the target set, list them and ask the user **once**: *"These need a paid or
   institutional account — which do you actually have?"* Name the **service the user would
   recognize** (BioRender · Consensus Pro · Codex/OpenAI · Synapse · Wiley / your institution ·
   a paid image-generation backend), **never the internal skill id** — say "paid image generation",
   not "scientific-schematics". Wire only the ones they confirm. For the rest, leave them
   **⚠ needs-you** and point to the **free alternative on the same line** where one exists
   (mermaid for Figma / paid figure tools; deep-research / PubMed for Consensus Pro; Open Targets
   + public APIs for paid data; image-gen/FLUX for gpt-image-2). **Never push a paid tool when a
   free stop on the map does the job.**

Then run the wiring engine per stop: **detect → if live, skip → else act showing the
command first → re-check → update the board.** Honesty rules: never silently skip; show
every command first; leave anything unfinished as ⚠ needs-you with the exact next step.
Finish by printing the updated board for the targeted stops only.

---
description: Install/connect the map — everything, one line, or one journey's required stops — using the tube-map wiring engine.
argument-hint: "[all | <line: lit|gen|comp|stat|clin|viz|write|ops> | <journey>]"
---

Use the `tube-map` skill. Resolve the target from `$ARGUMENTS`:

- `all` → every station in `${CLAUDE_PLUGIN_ROOT}/data/catalogue.json` (warn it's heavy).
- a line key (e.g. `stat`) → that line's stations.
- a journey name → that journey's required stops (journeys arrive in M2; until then,
  say so and offer the closest line).

Run the wiring engine from the skill for each target stop: **detect → if live, skip →
else act showing the command first → re-check → update the board.** Honour the honesty
rules: never silently skip; leave anything you can't finish as ⚠ needs-you with the exact
next step. Finish by printing the updated board for the targeted stops only.

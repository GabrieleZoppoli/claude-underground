---
description: Open the Claude Tube Map board — show every line and stop with its live/ready/needs-you status, then offer next steps.
---

Use the `tube-map` skill. Read `${CLAUDE_PLUGIN_ROOT}/data/catalogue.json`, run each
stop's `probe` to determine status, and render a compact board grouped by line:

`<emoji> <line name>` then, per stop, `<status> <name> — <one-line desc>` where status
is ● live / ◉ ready / ⚠ needs you.

End with: how many are live vs ready vs needs-you, and the two ways forward
(`/tube-map-install all`, or `/tube-map-install <line>` / name a journey). Do not wire
anything from this command — it is read-only.

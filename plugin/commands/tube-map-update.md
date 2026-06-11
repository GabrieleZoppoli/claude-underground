---
description: Check for and install the latest version of the Claude Tube Map (and offer to update its companion plugins).
---

Use the `tube-map` skill's update flow. Goal: tell the user **honestly** whether a newer version
exists and install it if they want — never claim an update happened without a passing result.

Run each step, showing the command before you run it:

1. **Find the marketplace name** — `claude plugin marketplace list`. The map is usually
   `claude-underground`; use whatever name points to `GabrieleZoppoli/claude-underground`.
2. **Refresh the cache** — `claude plugin marketplace update <marketplace>`.
3. **Check & update** — `claude plugin update claude-tube-map@<marketplace>`. Report the exact
   result: the version it moved **from → to**, or "already on the latest version". If it updated,
   tell the user to **restart Claude Code or run `/reload-plugins`** to apply.
4. **Companions (optional)** — if the user uses the writing / peer-review / grant journeys, offer to
   update the recommended free companion too (only if it's installed):
   `claude plugin update academic-research-skills@academic-research-skills`. Skip silently if absent.

**Honesty:** if a step fails (no network, name mismatch, not installed), say so plainly and show the
manual command — never pretend it succeeded. This command only updates; it changes nothing else.

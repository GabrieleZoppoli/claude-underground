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

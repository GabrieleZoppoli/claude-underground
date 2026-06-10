---
name: figures
description: Publication-quality figure or schematic.
stops: schematics, infographics, biorender
---

# Journey — Figures  🟡

**Goal:** a clean, publication-grade figure — pathway/mechanism schematic, data-driven infographic, or BioRender-style assembly.

## Run it
1. **Ensure stops (free-first)** — for a **simple diagram** (flowchart, pathway, mechanism box-and-arrow), `mermaid` is **free** and needs no setup — offer it first. The richer tools are paid/login-gated: `scientific-schematics` / `infographics` use a **paid image-generation backend** and `biorender` needs a **BioRender login** — run the subscription wizard, name those services plainly, and leave them **⚠ needs-you** if the user doesn't have them. Never push a paid figure tool when mermaid does the job.
2. **Pick the tool** — simple diagram → `mermaid` (free); rich mechanism/pathway art → `scientific-schematics`; data figure → `infographics`; bio iconography → BioRender.
3. **Draft** — generate at publication resolution; colourblind-safe palette by default.
4. **Review & iterate** — check labels, legends, units; regenerate once if quality is low.
5. **Deliver** — export the asset and note the source/tool used (free or paid path).

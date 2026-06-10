---
name: omics
description: Analyse omics data with confidence (free-first tooling).
stops: python, scqc, scmcp, survival, reporting
---

# Journey — Omics analysis  ⚫(+🔵)

**Goal:** a correct, reproducible omics analysis with publication-standard plots — free tooling first; never reach for a paid tool a free one covers.

## Run it
1. **Ensure stops** — `python` (scanpy/squidpy, local), `scqc` (single-cell-QC skill, free), `scmcp` (scverse MCP, free/local); add `survival` + `reporting` if you have outcomes. No paid tool required.
2. **Know the data** — modality (bulk RNA-seq / scRNA-seq / spatial), platform, study design, batch structure.
3. **QC first** — doublets, mito %, depth, empty droplets; document the thresholds you set rather than accepting defaults silently.
4. **Right method** — normalisation, integration/batch correction, and the test that matches the design; check assumptions; **set a seed** for reproducibility.
5. **Analyse** — write and run the code via Bash; show the code and the numbers; guard against data leakage and silently-dropped NaNs / empty cohorts.
6. **Plot & report** — publication-standard figures (UMAP, volcano, KM if survival); state n, effect sizes, CIs; apply the relevant reporting checklist (e.g. via `reporting`).

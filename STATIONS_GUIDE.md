# The Zoppoli Research Underground — Station & Connection Guide

> How to ride each line: what every station does, **how to connect it**, **which functions to expect**, whether Claude reaches it **automatically or via a skill load**, and the **machine it runs best on**.

> Generated from the live map data — **78 stations** (the super-confident set: ● live + ◉ verified). Registry-listed servers stay in `CATALOGUE.md` until their repo is confirmed. Re-run `python3 make_guide.py` after editing the map.

> **On the `Real?` column (is it actually in there, or did I make it up):** the live MCPs and skills are ones I *directly observe* in this session; the public databases are well-known resources; and every install-first MCP repo / endpoint was **fetched and confirmed to exist on 2026-06-04** (licence noted). Nothing here is an unverified guess — the registry-listed servers that *were* only inferred are excluded (they live in `CATALOGUE.md`).


## How to read the columns

**Status:** ● live (wired now) · ◉ verified (real, ready to wire) · ⊕ interchange (a connecting line stops here).


**Invocation** — how Claude actually reaches it:

| Label | Meaning |
|---|---|
| `Auto·MCP` | Wired MCP tool — Claude calls it directly; the tool schema auto-loads on first use. **No action from you.** |
| `Auto·web` | Public API/registry — Claude reaches it through the in-browser tool or `curl`. **No install.** |
| `Auto·Bash` | Claude runs it as local code / CLI in the shell. |
| `Skill` | Claude loads a skill (auto-triggers on the matching task, or on request). |
| `Install→MCP` | Add the server to your MCP config **once**; thereafter it behaves as `Auto·MCP`. |
| `Install→Bash` | Install the tool once (`pip`/`conda`), then `Auto·Bash`. |
| `Install→Skill` | `/plugin install …`, then it loads like any skill. |
| `Install (channel)` | An install *source* (the marketplace), not a tool you call. |
| `Built-in` | Native Claude Code capability — no setup. |
| `Manual` | You run the final step yourself (e.g. paste a prompt into ChatGPT). |
| `Discovery` | A place to **find/verify** other servers (browse), not a tool you call. |

**Runs best on:** 💻 any laptop (cloud / remote MCP / API / skill — the work happens off-box) · 🖥️ your workstation (local envs, auth tokens, your data, light–medium compute) · 🗄️ HPC (heavy pipelines, big data, GPU). `A → B` = starts on A, scales to B.


**Cost:** `Free·OSS` open-source software/MCP · `Free·public` public DB/API · `Free·skill` a Claude skill (no licence; it runs on your Claude plan) · `Freemium` free tier + paid upgrades · `Paid/lic.` needs a subscription or institutional licence. Parentheticals flag where the answer shifts (e.g. image-gen skills bill per image; OncoKB is free for academics, licensed for industry).


**Real?** — provenance, the honest part: `Seen·session` I directly observe it in my tools/skills right now (cannot be fabricated) · `Known·DB` a well-established public database · `Known·SW` well-established open-source software (the *installed-on-your-box* claim is from a prior session) · `Web-verified ✓` I fetched the repo/endpoint on 2026-06-04 and confirmed it exists, licence noted · `Configured` set up per CLAUDE.md, not exercised this turn.


## Wire these first (highest-leverage, not yet wired)

1. **BioMCP** — One server federating literature, variants, trials & cancer genomics. _(MCP: genomoncology/biomcp — the single best biomedical addition.)_
2. **Open Targets MCP** — Target–disease–drug associations, genetics, tractability. _(Official remote MCP: mcp.platform.opentargets.org/mcp.)_
3. **cBioPortal MCP** — No-SQL natural-language queries over cBioPortal. _(Official MCP (under construction): cBioPortal/cbioportal-mcp.)_
4. **ChatSpatial** — Spatial-transcriptomics agent — ~60 methods (Xenium/Visium/MERFISH). _(MCP: cafferychen777/ChatSpatial.)_
5. **SCMCP** — scRNA-seq analysis via scverse (scanpy). _(MCP: scmcphub/scmcp.)_
6. **ClinTrials.gov MCP** — Trial-registry queries over MCP (CTG API v2 + NCI CTS). _(MCP: cyanheads/clinicaltrialsgov-mcp-server.)_
7. **ENA MCP** — European Nucleotide Archive — reads, assemblies, sequence records. _(MCP: biocontext-ai/nucleotide_archive_mcp.)_
8. **Claude for Life Sciences** — Anthropic's official life-sci plugin marketplace — remote MCPs + skills. _(Install: /plugin marketplace add anthropics/life-sciences.)_


## 🔴 Literature & Evidence

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ●⊕ **PubMed** | **35M+ biomedical citations; full-text, related-article & citation lookup.**<br>↳ MCP connected now — search, fetch metadata & full text directly. | Free·public | Seen·session | `Auto·MCP` | 💻 |
| ● **Consensus** | **Evidence synthesis with claim-level support/oppose scoring.**<br>↳ MCP connected now — ask a question, get cited consensus. | Freemium | Seen·session | `Auto·MCP` | 💻 |
| ● **deep-research** | **Fan-out web search → fetch → adversarially verify → cited report.**<br>↳ Skill: deep-research. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **literature-review** | **Systematic reviews across PubMed/arXiv/bioRxiv/Semantic Scholar (PRISMA).**<br>↳ Skill: claude-scientific-writer:literature-review. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **research-lookup** | **Fast current-research lookup (Parallel/Perplexity) for facts & papers.**<br>↳ Skill: claude-scientific-writer:research-lookup. | Free·skill (API backend may bill) | Seen·session | `Skill` | 💻 |
| ◉ **Europe PMC** | **EU biomedical corpus incl. preprints, patents, grants, full text.**<br>↳ Public REST API via browser/HTTP; a Europe PMC MCP can be added. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **bioRxiv** | **Biology preprints — earliest signal before peer review.**<br>↳ bioRxiv API via browser/HTTP. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **medRxiv** | **Clinical/medical preprints — trials & methods before journals.**<br>↳ medRxiv API via browser/HTTP. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **Semantic Scholar** | **200M+ papers, citation graph, TLDR summaries.**<br>↳ Public Graph API; also federated inside BioMCP. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **Wiley Scholar Gateway** | **Wiley full-text scholarly gateway (marketplace remote MCP).**<br>↳ Install via /plugin marketplace add anthropics/life-sciences. | Paid/lic. (Wiley institutional) | Web-verified ✓ (in marketplace) | `Install→MCP` | 💻 |

## 🟢 Genomic Data & Sequencing

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **Synapse.org** | **Sage Bionetworks repository — controlled-access cohorts, consortium data.**<br>↳ MCP connected now — search & pull datasets (auth for controlled access). | Free·public (access-gated) | Seen·session | `Auto·MCP` | 💻 query · 🗄️ bulk |
| ◉ **GEO / SRA** | **NCBI expression (GEO) & raw reads (SRA) — public omics at scale.**<br>↳ NCBI E-utilities API; or an NCBI MCP (see below). | Free·public | Known·DB | `Auto·web` | 💻 meta · 🗄️ raw reads |
| ◉ **Ensembl** | **Genome annotation, BioMart, VEP variant effect prediction.**<br>↳ Ensembl REST API; or an Ensembl MCP (see below). | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **UCSC Browser** | **Genome browser, tracks, liftOver, table browser.**<br>↳ UCSC REST API; browser for exploration. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **GDC / TCGA** | **NCI Genomic Data Commons + TCGA — mutations, CNV, expression, /analysis/survival.**<br>↳ Public REST API (gdc.cancer.gov/developers); no GDC MCP yet. | Free·public | Known·DB | `Auto·web` | 💻 · 🗄️ bulk files |
| ◉⊕ **ClinVar / gnomAD** | **Clinical variant significance + population allele frequencies.**<br>↳ NCBI / gnomAD APIs; also federated inside BioMCP. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉⊕ **cBioPortal** | **Cancer genomics portal — TCGA, mutations, CNA, clinical.**<br>↳ REST API (cbioportal.org/api); MCP below. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉⊕ **DepMap / OncoKB** | **Dependency/essentiality screens + precision-oncology annotation.**<br>↳ DepMap downloads; OncoKB API (token). | Free·public (OncoKB: free academic / paid commercial) | Known·DB | `Auto·web` | 💻 |
| ◉ **CELLxGENE** | **Single-cell/spatial atlases — directly relevant to your Xenium work.**<br>↳ CZ CELLxGENE Census API; Census MCP below. | Free·public | Known·DB | `Auto·Bash` | 🖥️ → 🗄️ |
| ◉⊕ **cBioPortal MCP** | **No-SQL natural-language queries over cBioPortal.**<br>↳ Official MCP (under construction): cBioPortal/cbioportal-mcp. | Free·OSS | Web-verified ✓ MIT | `Install→MCP` | 💻 |
| ◉⊕ **Open Targets MCP** | **Target–disease–drug associations, genetics, tractability.**<br>↳ Official remote MCP: mcp.platform.opentargets.org/mcp. | Free·OSS | Web-verified ✓ official, Apache-2.0 | `Install→MCP` | 💻 (remote) |
| ◉ **ENA MCP** | **European Nucleotide Archive — reads, assemblies, sequence records.**<br>↳ MCP: biocontext-ai/nucleotide_archive_mcp. | Free·OSS | Web-verified ✓ Apache-2.0 | `Install→MCP` | 💻 query · 🗄️ pulls |

## ⚫ Compute & Pipelines

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **Python · scanpy/squidpy** | **scanpy/squidpy/anndata for sc & spatial; pandas/numpy/scipy — all verified installed.**<br>↳ Bash + Python 3.12; Claude writes & runs the analysis now. | Free·OSS | Known·SW | `Auto·Bash` | 🖥️ → 🗄️ |
| ◉ **Jupyter** | **Interactive notebooks — exploratory analysis & figures.**<br>↳ `pip install jupyterlab`; Claude drives notebooks via Bash. | Free·OSS | Known·SW | `Install→Bash` | 🖥️ |
| ◉ **R · Bioconductor** | **Seurat, DESeq2, limma, edgeR, survminer — the bio-stats engine.**<br>↳ R 4.5.2 + base survival installed; add via BiocManager::install(...). | Free·OSS | Known·SW | `Auto·Bash` | 🖥️ → 🗄️ |
| ◉ **Nextflow / nf-core** | **Reproducible, containerised genomics pipelines at scale.**<br>↳ Install nf-core; Claude scaffolds & launches workflows. | Free·OSS | Known·SW | `Install→Bash` | 🗄️ HPC (🖥️ dev) |
| ◉ **Galaxy** | **GUI/API workflow platform for accessible bioinformatics.**<br>↳ Galaxy public/local instance; API via browser. | Free·OSS | Known·SW | `Auto·web` | 💻 public · 🗄️ local |
| ◉ **Snakemake** | **Make-style reproducible workflow engine for omics.**<br>↳ pip/conda; Claude writes the Snakefile. | Free·OSS | Known·SW | `Install→Bash` | 🗄️ HPC (🖥️ dev) |
| ◉ **cfDNA stack** | **Your liquid-biopsy tools: ichorCNA, MEDIPS/MeDEStrand, fragmentomics, ONT.**<br>↳ Local conda envs; Claude orchestrates RENOVATE/MIMESIS pipelines. | Free·OSS | Known·SW | `Auto·Bash` | 🗄️ HPC |
| ◉ **ChatSpatial** | **Spatial-transcriptomics agent — ~60 methods (Xenium/Visium/MERFISH).**<br>↳ MCP: cafferychen777/ChatSpatial. | Free·OSS | Web-verified ✓ MIT | `Install→MCP` | 🖥️ → 🗄️ |
| ◉ **SCMCP** | **scRNA-seq analysis via scverse (scanpy).**<br>↳ MCP: scmcphub/scmcp. | Free·OSS | Web-verified ✓ BSD-3 | `Install→MCP` | 🖥️ → 🗄️ |
| ◉ **sc-RNA-QC skill** | **Official single-cell-rna-qc skill (marketplace).**<br>↳ Install: /plugin install single-cell-rna-qc@life-sciences. | Free·OSS | Web-verified ✓ (in marketplace) | `Install→Skill` | 🖥️ |
| ◉ **nf-core dev skill** | **Official nextflow-development skill (marketplace).**<br>↳ Install via anthropics/life-sciences marketplace. | Free·OSS | Web-verified ✓ (in marketplace) | `Install→Skill` | 🖥️ author · 🗄️ run |
| ◉ **scvi-tools** | **Probabilistic single-cell models skill (marketplace).**<br>↳ Install via anthropics/life-sciences marketplace. | Free·OSS | Web-verified ✓ (in marketplace) | `Install→Skill` | 🗄️ GPU |

## 🔵 Statistics & Trial Design

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **statsmodels / scipy** | **Regression, GLM, mixed models, hypothesis tests in Python.**<br>↳ Bash + Python; Claude writes the analysis. | Free·OSS | Known·SW | `Auto·Bash` | 💻 · 🖥️ |
| ● **survival · lifelines** | **Kaplan–Meier, Cox PH, competing risks — your endpoint engine.**<br>↳ lifelines (Py) / survival+survminer (R) via Bash. | Free·OSS | Known·SW | `Auto·Bash` | 💻 · 🖥️ |
| ● **reporting standards** | **CONSORT / STROBE / PRISMA checklists baked into writing & review.**<br>↳ Skills: scientific-writing / peer-review. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **peer-review** | **Systematic methodology, stats, design & reproducibility review.**<br>↳ Skill: claude-scientific-writer:peer-review. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **critical-thinking** | **Rigor, bias, confounding, GRADE / Cochrane RoB appraisal.**<br>↳ Skill: claude-scientific-writer:scientific-critical-thinking. | Free·skill | Seen·session | `Skill` | 💻 |
| ◉ **Bayesian · Stan/PyMC** | **Bayesian inference, hierarchical models, adaptive-trial priors.**<br>↳ Install PyMC/cmdstanpy; Claude builds the model. | Free·OSS | Known·SW | `Install→Bash` | 🖥️ → 🗄️ |
| ◉ **Power & sample size** | **Power, MDE, sample-size & simulation for trial design.**<br>↳ statsmodels.power / R pwr & simr. | Free·OSS | Known·SW | `Auto·Bash` | 💻 |
| ◉⊕ **ClinTrials.gov MCP** | **Trial-registry queries over MCP (CTG API v2 + NCI CTS).**<br>↳ MCP: cyanheads/clinicaltrialsgov-mcp-server. | Free·OSS | Web-verified ✓ Apache-2.0 | `Install→MCP` | 💻 |

## 🟣 Clinical & Regulatory

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **clinical-reports** | **Case reports (CARE), CSR (ICH-E3), SOAP, discharge summaries.**<br>↳ Skill: claude-scientific-writer:clinical-reports. | Free·skill | Seen·session | `Skill` | 💻 |
| ●⊕ **decision-support** | **Biomarker-stratified cohorts, GRADE, treatment algorithms.**<br>↳ Skill: claude-scientific-writer:clinical-decision-support. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **treatment-plans** | **Focused LaTeX/PDF treatment plans across specialties.**<br>↳ Skill: claude-scientific-writer:treatment-plans. | Free·skill | Seen·session | `Skill` | 💻 |
| ◉ **ClinicalTrials.gov** | **Global trial registry — design, comparators, recruitment.**<br>↳ CTG API v2 via browser/HTTP. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **EU CTR / CTIS** | **EU clinical trials register & CTIS — the EU/IT regulatory side.**<br>↳ CTIS public portal via browser. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **FDA / EMA** | **Approvals, labels, guidance, safety — regulatory grounding.**<br>↳ openFDA API; EMA via browser. | Free·public | Known·DB | `Auto·web` | 💻 |
| ◉ **WHO ICTRP** | **Cross-registry trial search (incl. non-US/EU).**<br>↳ ICTRP portal via browser. | Free·public | Known·DB | `Auto·web` | 💻 |

## 🟡 Visualization & Figures

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **BioRender** | **Publication figures from a vast bio icon/template library.**<br>↳ MCP connected now — search icons & templates. | Freemium (pub export paid) | Seen·session | `Auto·MCP` | 💻 |
| ● **Mermaid** | **Flowcharts, sequence & ER diagrams from text; live render.**<br>↳ MCP connected now — validate & render diagrams. | Free·OSS | Seen·session | `Auto·MCP` | 💻 |
| ● **Figma** | **Vector design for posters, schematics, slide polish.**<br>↳ MCP connected now (auth) — pull frames & assets. | Freemium | Seen·session | `Auto·MCP` | 💻 |
| ● **scientific-schematics** | **Pathways, architectures, mechanism diagrams (Nano Banana Pro).**<br>↳ Skill: claude-scientific-writer:scientific-schematics. | Free·skill (image API may bill) | Seen·session | `Skill` | 💻 |
| ● **infographics** | **Data-driven infographics with colourblind-safe palettes.**<br>↳ Skill: claude-scientific-writer:infographics. | Free·skill (image API may bill) | Seen·session | `Skill` | 💻 |
| ● **image-gen · Nano/FLUX** | **General images, illustrations, photoreal assets (FLUX/Gemini).**<br>↳ Skill: claude-scientific-writer:generate-image. | Free·skill (FLUX/Gemini bills) | Seen·session | `Skill` | 💻 |
| ◉ **gpt-image-2 (hero)** | **SOTA hero/cover artwork with reliable in-image text.**<br>↳ Manual ChatGPT handoff (Path A) — not wired to API. | Paid/lic. (OpenAI / ChatGPT) | Known (OpenAI) | `Manual` | 💻 |

## 🟤 Writing & Publishing

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **scientific-writing** | **IMRAD prose (never bullets), citations, reporting guidelines.**<br>↳ Skill: claude-scientific-writer:scientific-writing. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **citation-management** | **Scholar/PubMed metadata, DOI→BibTeX, reference validation.**<br>↳ Skill: claude-scientific-writer:citation-management. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **venue-templates** | **Nature/Science/PLOS/IEEE + NIH/NSF formatting & rules.**<br>↳ Skill: claude-scientific-writer:venue-templates. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **Office docs** | **Author & edit docx / pptx / xlsx / pdf — tracked changes, slides, sheets.**<br>↳ Skills: claude-scientific-writer:docx/pptx/xlsx/pdf. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **markitdown** | **Convert PDF/DOCX/PPTX/audio/HTML → Markdown for ingest.**<br>↳ Skill: claude-scientific-writer:markitdown. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **humanizer** | **Strip AI-tells; enforce natural prose (your house style).**<br>↳ Skill: humanizer. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **preparing-slides** | **Your Zoppoli house-style .pptx engine (DIMI/GOIRC/…).**<br>↳ Skill: preparing-slides — your venues, palettes, rules. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **research-grants** | **NSF/NIH/DOE/DARPA + EU proposals, significance, budgets.**<br>↳ Skill: claude-scientific-writer:research-grants. | Free·skill | Seen·session | `Skill` | 💻 |
| ● **paper-2-web** | **Paper → website / video / poster for dissemination.**<br>↳ Skill: claude-scientific-writer:paper-2-web. | Free·skill (video may bill) | Seen·session | `Skill` | 💻 (video heavier) |
| ● **posters (LaTeX/PPTX)** | **Conference posters via beamerposter/tikz or PPTX.**<br>↳ Skills: latex-posters / pptx-posters. | Free·skill | Seen·session | `Skill` | 💻 (local LaTeX) |

## ⚪ Orchestration & Lab Ops

| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |
|---|---|---|---|---|---|
| ● **Google Drive** | **Cloud store — data, manuscripts, shared docs; read & write.**<br>↳ MCP connected now — search, read, create files. | Freemium | Seen·session | `Auto·MCP` | 💻 |
| ● **Gmail** | **Search threads, draft, label — collaborator & journal comms.**<br>↳ MCP connected now — search & draft (you send). | Freemium | Seen·session | `Auto·MCP` | 💻 |
| ● **Google Calendar** | **Schedule meetings, deadlines, find slots.**<br>↳ MCP connected now — list, create, suggest times. | Freemium | Seen·session | `Auto·MCP` | 💻 |
| ● **Slack** | **Team/consortium channels — search & post.**<br>↳ MCP connected (auth) — search & message. | Freemium | Seen·session | `Auto·MCP` | 💻 |
| ● **Workflows / subagents** | **Deterministic multi-agent fan-out: review, migrate, research.**<br>↳ Workflow tool + Agent subagents — orchestrate at scale. | Free·built-in (uses tokens) | Seen·session | `Built-in` | 💻 (more tokens at scale) |
| ● **schedule / cron** | **Recurring remote agents — overnight pipelines, polling, digests.**<br>↳ Skill: schedule — cron-style routines & one-offs. | Free·skill | Seen·session | `Skill` | 💻 (cloud-run) |
| ● **Codex · GPT-5.5** | **Second engine — decorrelated review, long shell agents, red-team.**<br>↳ codex exec via Bash; Skill: codex-dispatch. | Paid/lic. (ChatGPT/OpenAI) | Configured (CLAUDE.md) | `Auto·Bash` | 🖥️ (codex CLI) |
| ◉⊕ **Claude for Life Sciences** | **Anthropic's official life-sci plugin marketplace — remote MCPs + skills.**<br>↳ Install: /plugin marketplace add anthropics/life-sciences. | Free (some servers it ships are paid) | Web-verified ✓ (412★) | `Install (channel)` | 💻 |
| ◉⊕ **BioContextAI Registry** | **Nature-Biotech-backed index of ~60 biomedical MCP servers.**<br>↳ Browse biocontext.ai/registry · github.com/biocontext-ai/registry. | Free·OSS | Web-verified ✓ repo | `Discovery` | 💻 |
| ◉⊕ **BioContextAI meta-MCP** | **Meta layer: knowledgebase / skill-to-mcp / protocol / registry servers.**<br>↳ github.com/biocontext-ai — add the meta server to your config. | Free·OSS | Web-verified ✓ (biocontext-ai) | `Install→MCP` | 💻 |
| ◉⊕ **NAR DB Collection** | **2,173 curated molecular-biology databases (2026 issue) — the cross-check.**<br>↳ Reference index: academic.oup.com/nar. | Free·public | Known·DB | `Discovery` | 💻 |
| ◉⊕ **BioMCP** | **One server federating literature, variants, trials & cancer genomics.**<br>↳ MCP: genomoncology/biomcp — the single best biomedical addition. | Free·OSS | Web-verified ✓ MIT | `Install→MCP` | 💻 (wraps remote APIs) |

## ⊕ Interchange lines — the multi-domain servers that connect the lines

Each is one MCP server that spans several lines; wiring it lights up every station it touches.

### BioMCP — literature · genomic · trials federation
- **Connect:** MCP: genomoncology/biomcp — the single best biomedical addition.
- **Functions:** One server federating literature, variants, trials & cancer genomics.
- **Invocation:** `Install→MCP` · **Runs best on:** 💻 (wraps remote APIs)
- **Stops it serves:** BioMCP · DepMap / OncoKB · cBioPortal · ClinVar / gnomAD · PubMed · ClinTrials.gov MCP

### Open Targets — target · disease · treatment
- **Connect:** Official remote MCP: mcp.platform.opentargets.org/mcp.
- **Functions:** Target–disease–drug associations, genetics, tractability.
- **Invocation:** `Install→MCP` · **Runs best on:** 💻 (remote)
- **Stops it serves:** Open Targets MCP · cBioPortal MCP · decision-support

### Discovery ring — Life-Sciences marketplace + BioContextAI
- **Connect:** `/plugin marketplace add anthropics/life-sciences` (marketplace) and browse `biocontext.ai/registry` (registry). The install/discovery backbone.
- **Invocation:** `Install (channel)` + `Discovery` · **Runs best on:** 💻 any laptop
- **Stops it serves:** Claude for Life Sciences · BioContextAI Registry · BioContextAI meta-MCP · NAR DB Collection


## The hub & the second engine

- **🟧 Claude Code (central interchange)** — your workstation. Every line meets here: Claude routes the work, reasons, writes & runs code, and dispatches the rest. **Invocation:** this is the station you sit in. **Runs best on:** 🖥️ workstation (it drives everything else, local + cloud).
- **🟩 Codex · GPT-5.5 (sister terminus)** — the second engine for decorrelated review, long shell-agent runs and red-teaming. **Connect:** `codex exec --skip-git-repo-check "…"` via Bash, or the `codex-dispatch` skill. **Invocation:** `Auto·Bash` / `Skill`. **Runs best on:** 🖥️ workstation (where the codex CLI + ChatGPT auth live).

## At a glance — where the work happens

- **💻 Any laptop (most of the map):** all literature, clinical & regulatory lines, every writing/visualization skill, the trial-registry MCPs, and the orchestration connectors (Drive/Gmail/Calendar/Slack/workflows/schedule). If it's a cloud connector, a remote MCP, a public API or a skill, the heavy lifting happens off your machine — you only need Claude Code + internet.
- **🖥️ Workstation:** anything touching your local envs, credentials or data — Synapse controlled-access pulls, Jupyter, light single-cell (scanpy/Seurat) exploration, the Codex CLI. Also the natural home for the MCP servers that *execute* analysis locally (ChatSpatial, SCMCP) when datasets are modest.
- **🗄️ HPC:** the genomics compute spine — Nextflow/nf-core & Snakemake pipelines, the cfDNA/liquid-biopsy stack (RENOVATE / MIMESIS), large single-cell & spatial atlases, GPU model training (scvi-tools), and bulk SRA/GDC/ENA data pulls. Develop on the workstation, run at scale on HPC.

---
*Generated by `make_guide.py` from `generate_map.py`. Edit the map data or the `INVOKE` / `RUNS_ON` dicts and re-run to refresh.*

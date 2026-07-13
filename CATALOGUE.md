# Research Underground — Verified Connector Catalogue

Produced by a `deep-research` run (111 agents · 3.6M tokens · 633 tool calls · 28 sources ·
133 claims extracted → 25 adversarially verified by 3-vote → 16 confirmed, 2 killed),
plus targeted follow-up fetches. Generated 2026-06-02.

**Weekly connector discovery — 2026-07-13**: added 9 verified candidates across Lines 1, 2, 3, 5
(see PR `discovery/2026-07-13`). All repos confirmed via WebFetch before inclusion.

**Trust tiers** (a fabricated repo/URL is the worst possible error, so each entry is tagged):
- ✅ **verified** — confirmed against a live primary page in this research.
- 📇 **registry-listed** — present in the BioContextAI curated registry (biomedical-focus,
  open-source, free-academic vetting). Real entries; confirm the individual repo before wiring.
- 🌐 **public API** — database with a documented programmatic API (no MCP needed to use it).
- ⚠️ **open** — plausibly exists but NOT verified in this pass; do not wire until confirmed.

---

## The two discovery anchors (start here)

- ✅ **Claude for Life Sciences marketplace** — Anthropic's OFFICIAL Claude Code plugin
  marketplace. Install: `/plugin marketplace add anthropics/life-sciences`.
  Ships remote MCP servers (PubMed, BioRender, Synapse/Sage, Wiley, Consensus, Cortellis,
  AdisInsight), a **local 10x Genomics Cloud MCP** (`/plugin install 10x-genomics@life-sciences`),
  and official **skills** (single-cell-rna-qc, nextflow-development, scvi-tools).
  Source: github.com/anthropics/life-sciences · anthropic.com/news/claude-for-life-sciences
- ✅ **BioContextAI Registry** — community-curated index of ~60 biomedical MCP servers,
  Nature Biotech-backed (DOI 10.1038/s41587-025-02900-9). THE place to verify which
  biomedical MCP servers exist. Source: biocontext.ai/registry · github.com/biocontext-ai/registry
  (data = per-server `meta.yaml` under `/servers`; site 403s automated reads, repo is reliable).
- 🌐 **NAR Online Molecular Biology Database Collection** — 2,173 databases (2026 issue);
  the authoritative cross-check for *databases*. academic.oup.com/nar/article/54/D1/D1/8402365

---

## Highest-leverage additions (the shortlist)

1. ✅ **BioMCP** (github.com/genomoncology/biomcp, MIT) — ONE server spanning **Lines 1+2+4**:
   PubMed/PubTator3/Europe PMC/Semantic Scholar, ClinicalTrials.gov v2 + NCI CTS, cBioPortal,
   MyVariant, ClinVar, gnomAD, CIViC, OncoKB, GWAS Catalog, AlphaGenome. Best single addition.
2. ✅ **ChatSpatial** (github.com/cafferychen777/ChatSpatial) + **SCMCP** (github.com/scmcphub/scmcp)
   — spatial-transcriptomics (~60 methods) and scRNA-seq via scverse. Directly your Xenium / single-cell.
3. ✅ **10x Genomics Cloud MCP** (in the life-sciences marketplace) — your 10x data/workflows.
4. ✅ **cBioPortal MCP** (github.com/cBioPortal/cbioportal-mcp, official, "under construction") —
   no-SQL cancer-genomics queries.
5. ✅ **Open Targets MCP** (github.com/opentargets/open-targets-platform-mcp, OFFICIAL; remote
   endpoint mcp.platform.opentargets.org/mcp) — target–disease–drug associations.
6. ✅ **ClinicalTrials.gov MCP** (github.com/cyanheads/clinicaltrialsgov-mcp-server) +
   ✅ **ENA MCP** (github.com/biocontext-ai/nucleotide_archive_mcp).

---

## Full catalogue by line

### 🔴 Line 1 — Literature & Evidence
- ✅ BioMCP (lit federation: PubMed/PubTator3/Europe PMC/Semantic Scholar) — genomoncology/biomcp
- 📇 PubMed MCPs — andybrandt-mcp-simple-pubmed · grll-pubmedmcp
- 📇 Google Scholar MCP — JackKuo666-Google-Scholar-MCP-Server
- 📇 **PubTator3 MCP** (github.com/BioMCP-Hub/PubTator-MCP-Server) — standalone biomedical entity annotation & relationship mining via PubTator3 API; also federated inside BioMCP. Python, FastMCP.
- ✅ Marketplace: PubMed (no-auth), Wiley Scholar Gateway, Consensus — anthropics/life-sciences
- 🌐 Europe PMC API · Semantic Scholar API (both public; ⚠️ standalone MCPs not separately confirmed)

### 🟢 Line 2 — Genomic Data & Sequencing
- ✅ BioMCP (variants: MyVariant/ClinVar/gnomAD/CIViC/OncoKB/GWAS) — genomoncology/biomcp
- ✅ cBioPortal MCP (official) — cBioPortal/cbioportal-mcp · 🌐 REST: cbioportal.org/api/v3/api-docs
- ✅ Open Targets MCP (official) — opentargets/open-targets-platform-mcp · 🌐 GraphQL: api.platform.opentargets.org
- ✅ ENA Nucleotide Archive MCP — biocontext-ai/nucleotide_archive_mcp
- 📇 Ensembl MCP — effieklimi-ensembl-mcp-server · 🌐 rest.ensembl.org (VEP)
- 📇 UniProt MCP — TakumiY235-uniprot-mcp-server · 🌐 uniprot.org/help/api_queries
- 📇 NCBI MCP — noahzeidenberg-ncbi-mcp · 📇 BioMart — jzinno-biomart-mcp · 📇 biobtree (ID map) — tamerh-biobtree
- 📇 GWAS Catalog — koido-gwas-catalog-mcp · 📇 HGNC nomenclature — armish-hgnc.mcp
- 📇 VEP — not-a-feature-VEPmcp · 📇 Evo2 genomic LM — not-a-feature-evo2-mcp
- 📇 BioThings (MyGene/MyVariant) — Augmented-Nature-BioThings-MCP-Server · longevity-genie-biothings-mcp
- 📇 InterPro — bio-mcp-interpro · 📇 RNAcentral — RNAcentral-rnacentral-mcp-server · 📇 PDBe structures — PDBeurope-PDBe-MCP-Servers
- 📇 Cellosaurus cell lines — biocontext-ai-unofficial-cellosaurus-mcp · 📇 BioStudies — EBIBioStudies-biostudies-mcp-server
- 📇 **GEO MCP** (github.com/MCPmed/GEOmcp) — dedicated Gene Expression Omnibus MCP via NCBI E-Utils; search/download GEO datasets, series, samples, platforms. BSD-3, v0.1.2 Apr 2026.
- 🌐 GDC/TCGA API (incl. /analysis/survival) — gdc.cancer.gov/developers (⚠️ no GDC MCP found)
- 🌐 No-MCP-verified but public: UCSC, dbSNP/dbVar, ENCODE (use via API/browser)

### ⚫ Line 3 — Compute & Pipelines (incl. single-cell / spatial)
- ✅ ChatSpatial (spatial, ~60 methods) — cafferychen777/ChatSpatial
- ✅ SCMCP (scRNA-seq, scverse) — scmcphub/scmcp
- 📇 AnnData MCP — biocontext-ai-anndata-mcp · 📇 CELLxGENE Census MCP — MaxMLang-cxg-census-mcp
- 📇 Galaxy MCP — galaxyproject-galaxy-mcp · 📇 Enrichr enrichment — tianqitang1-enrichr-mcp-server
- 📇 STRING (PPI) — meringlab-string-mcp · 📇 Reactome (pathways) — Augmented-Nature-Reactome-MCP-Server
- 📇 OmniPath networks (Saez lab) — saezlab-omnipath-next · 📇 BioCypher knowledge graphs — biocypher-biocypher-mcp
- 📇 ToolUniverse (Harvard MIMS, 200+ tools aggregator) — mims-harvard-ToolUniverse · 📇 gget — longevity-genie-gget-mcp
- ✅ **bioSkills** (github.com/GPTomics/bioSkills) — 561 Claude Code SKILL.md skills across 63 categories: RNA-seq, variant calling, sc-omics, epigenomics (ATAC/ChIP/Hi-C), population genetics, liquid biopsy, immunoinformatics, structural biology, drug discovery. Explicit `install-claude.sh`. v3.0 Feb 2026.
- 📇 **ClawBio** (github.com/ClawBio/ClawBio) — 94 bioinformatics skills (29 production-ready): pharmacogenomics, GWAS (9 databases), ACMG clinical classification, single-cell QC, spatial, metagenomics, proteomics, UK Biobank, Galaxy integration. 1k GitHub stars. v0.5.0 Apr 2026.
- 📇 **BioContextAI Knowledgebase MCP** (github.com/biocontext-ai/knowledgebase-mcp) — 14-database federation NOT duplicated by other entries: PRIDE proteomics, Protein Atlas/HPA, PanglaoDB cell-type markers, KEGG pathways, Antibody Registry, EuropePMC, InterPro, STRING, Reactome, OpenTargets, Ensembl, AlphaFold DB, bioRxiv/medRxiv, Google Scholar. v0.2.1 Dec 2025.
- 📇 **DeepMind science-skills** (github.com/google-deepmind/science-skills) — ~36 SKILL.md skills for genomics, structural biology & cheminformatics from Google DeepMind; integrates AlphaGenome, AFDB, UniProt, ClinVar, OpenAlex. v1.0.5 Jul 2026. Claude Code compatibility: SKILL.md format used; primary platform is Google Antigravity — test before relying.
- ✅ Marketplace skills: single-cell-rna-qc, nextflow-development (nf-core), scvi-tools — anthropics/life-sciences
- ✅ Marketplace skill: **Instrument Data to Allotrope** (`instrument-data-to-allotrope@life-sciences`) — converts instrument data to Allotrope Simple Model (ASM) format for standardised data exchange. Source: anthropics/life-sciences.
- ✅ Marketplace skill: **Scientific Problem Selection** (`scientific-problem-selection@life-sciences`) — research ideation, risk assessment & strategic planning (Fischbach & Walsh methodology). Source: anthropics/life-sciences.
- Local (already installed): Python+scanpy/squidpy/anndata ✓ · R 4.5 ✓ (add Seurat/DESeq2 via BiocManager)

### 🔵 Line 4 — Statistics & Trial Design
- ✅ ClinicalTrials.gov MCP — cyanheads/clinicaltrialsgov-mcp-server · 🌐 API v2: clinicaltrials.gov/api/v2/studies
- ✅ BioMCP (trials via CTG v2 + NCI CTS) — genomoncology/biomcp
- 📇 AACT (CTG aggregate DB) MCP — navisbio-AACT_MCP · 📇 MedCalc MCP — winninghealth-medcalcmcp
- Local: statsmodels/lifelines ✓ (PyMC/Stan/brms ⚠️ to install)

### 🟣 Line 5 — Clinical & Regulatory
- 📇 OMOP / OHDSI MCP — OHNLP-omop_mcp · 📇 DICOM imaging MCP — ChristianHinge-dicom-mcp
- 📇 Ontologies: OLS4 (EBI) — EBISPOT-ols4 · BioPortal (SNOMED/UMLS etc.) — ncbo-bioportal-mcp
- 📇 Drugs/chem: ChEMBL — JackKuo666-ChEMBL-MCP-Server · PubChem — cyanheads-pubchem-mcp-server / JackKuo666-PubChem-MCP-Server · pharmacology — longevity-genie-pharmacology-mcp
- 📇 Oncology decisioning — Nexgene-Research-nexonco-mcp
- 📇 **SMART on FHIR MCP** (github.com/jmandel/health-record-mcp, 82 stars) — secure LLM access to EHR records via SMART on FHIR; integrates with Epic, SMART sandbox; exposes grep_record / query_record (SQL) / eval_record tools. TypeScript.
- ✅ Marketplace remote MCP: **Cortellis** (`cortellis@life-sciences`) — global drug regulatory intelligence: submissions, approvals & guidance docs (Clarivate; paid subscription). Source: anthropics/life-sciences.
- ✅ Marketplace remote MCP: **AdisInsight** (`adisinsight@life-sciences`) — drug development pipeline, clinical trials, safety & deals intelligence (Springer; paid subscription). Source: anthropics/life-sciences.
- 🌐 openFDA · EU CTIS/CTR · WHO ICTRP · EMA · HL7 FHIR · REDCap (public APIs; ⚠️ MCPs not confirmed)

### 🟡 Line 6 — Visualization & Figures
- ✅ BioRender (marketplace) — anthropics/life-sciences
- 📇 napari image viewer MCP — royerlab-napari-mcp · 📇 PyMOL MCP — vrtejus-pymol-mcp

### 🟤 Line 7 — Writing & Publishing
- ✅ Local skills (scientific-writer suite, etc.) — already live. No new MCPs needed here.
- 🌐 Reference mgmt: Zotero, Overleaf (⚠️ community MCPs exist generically; confirm before wiring)

### ⚪ Line 8 — Orchestration & Lab Ops
- ✅ Claude for Life Sciences marketplace — anthropics/life-sciences (install channel)
- ✅ BioContextAI meta-layer — biocontext-ai-meta-mcp · -knowledgebase-mcp · -skill-to-mcp · -protocol-mcp · -registry
- ✅ Codex / GPT-5.5 (already live) · workflows/subagents · schedule/cron

---

## Honest gaps (verify before relying)
- Broad MCP registries (Smithery, mcp.so, PulseMCP, Glama, awesome-mcp-servers) were NOT
  enumerated as full lists — BioContextAI was used as the biomedical-focused proxy.
- 📇 entries are registry-listed; individual repo URLs were inferred from registry IDs and
  must be confirmed before wiring (owner names like `biocontext-ai`, `Augmented-Nature`,
  `longevity-genie`, `not-a-feature` contain hyphens — do not auto-split).
- MCP servers are fast-moving; several are early-stage ("under construction"/alpha). Re-verify before print.
- Review tooling (Rayyan, Covidence, PROSPERO, ROBIS, ResearchRabbit/Connected Papers) — no
  dedicated MCP confirmed; use via web/API.

## Key sources
github.com/anthropics/life-sciences · biocontext.ai/registry · github.com/biocontext-ai/registry ·
github.com/genomoncology/biomcp · github.com/cBioPortal/cbioportal-mcp ·
github.com/opentargets/open-targets-platform-mcp · github.com/cafferychen777/ChatSpatial ·
github.com/scmcphub/scmcp · academic.oup.com/nar/article/54/D1/D1/8402365

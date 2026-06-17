# Research Underground — Verified Connector Catalogue

Produced by a `deep-research` run (111 agents · 3.6M tokens · 633 tool calls · 28 sources ·
133 claims extracted → 25 adversarially verified by 3-vote → 16 confirmed, 2 killed),
plus targeted follow-up fetches. Generated 2026-06-02.

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
- ✅ PubMed MCP — cyanheads/pubmed-mcp-server (107★; PubMed + Europe PMC full text, MeSH, citations; STDIO or public endpoint pubmed.caseyjhand.com/mcp; same author as the wired ClinicalTrials.gov MCP) · 📇 older/simpler: andybrandt-mcp-simple-pubmed · grll-pubmedmcp
- 📇 Google Scholar MCP — JackKuo666-Google-Scholar-MCP-Server
- ✅ Marketplace: PubMed (no-auth), Wiley Scholar Gateway, Consensus — anthropics/life-sciences
- 📇 OpenEvidence — clinical evidence Q&A for verified clinicians; wireable via the unofficial browser-session MCP bakhtiersizhaev/openevidence-mcp (uses your existing OpenEvidence login, no API token) or the official API (Mayo Platform; powers Elsevier ClinicalKey AI). ⚠️ not yet installed; needs a US VPN when outside the US (non-blocking). Caveat: Vishwanath et al. (Nat Med 2026) found frontier LLMs incl. Claude Opus outperform it on MedQA/HealthBench/RCQ.
- 🌐 Europe PMC API · Semantic Scholar API (both public; ⚠️ standalone MCPs not separately confirmed)

### 🟢 Line 2 — Genomic Data & Sequencing
- ✅ BioMCP (variants: MyVariant/ClinVar/gnomAD/CIViC/OncoKB/GWAS) — genomoncology/biomcp
- ✅ cBioPortal MCP (official) — cBioPortal/cbioportal-mcp · 🌐 REST: cbioportal.org/api/v3/api-docs
- ✅ Open Targets MCP (official) — opentargets/open-targets-platform-mcp · 🌐 GraphQL: api.platform.opentargets.org
- ✅ SPOKEAgent — BaranziniLab/SPOKEAgent (official UCSF MCP for the SPOKE biomedical knowledge graph: cross-domain links across genes, diseases, drugs, proteins & phenotypes)
- ✅ ENA Nucleotide Archive MCP — biocontext-ai/nucleotide_archive_mcp
- ✅ Ensembl MCP — cyanheads/ensembl-mcp-server (gene lookup, sequences, VEP variant consequences, orthologs, cross-db xrefs; no API key) · 📇 alt: effieklimi-ensembl-mcp-server · 🌐 rest.ensembl.org
- 📇 UniProt MCP — TakumiY235-uniprot-mcp-server · 🌐 uniprot.org/help/api_queries
- ✅ Protein structures MCP — cyanheads/protein-mcp-server (RCSB PDB + PDBe + UniProt in one server: structural search, comparison, ligand tracking — consolidates the separate PDBe/UniProt structure entries)
- 📇 NCBI MCP — noahzeidenberg-ncbi-mcp · 📇 BioMart — jzinno-biomart-mcp · 📇 biobtree (ID map) — tamerh-biobtree
- 📇 GWAS Catalog — koido-gwas-catalog-mcp · 📇 HGNC nomenclature — armish-hgnc.mcp
- 📇 VEP — not-a-feature-VEPmcp · 📇 Evo2 genomic LM — not-a-feature-evo2-mcp
- 📇 BioThings (MyGene/MyVariant) — Augmented-Nature-BioThings-MCP-Server · longevity-genie-biothings-mcp
- 📇 InterPro — bio-mcp-interpro · 📇 RNAcentral — RNAcentral-rnacentral-mcp-server · 📇 PDBe structures — PDBeurope-PDBe-MCP-Servers
- 📇 Cellosaurus cell lines — biocontext-ai-unofficial-cellosaurus-mcp · 📇 BioStudies — EBIBioStudies-biostudies-mcp-server
- 🌐 GDC/TCGA API (incl. /analysis/survival) — gdc.cancer.gov/developers (⚠️ no GDC MCP found)
- ✅ ENCODE toolkit MCP — ammawla/encode-toolkit (35★; 20 MCP tools across 14 databases + 47 Nextflow workflow skills; Claude plugin; v0.3.0) — fills the former ENCODE gap
- 🌐 No-MCP-verified but public: UCSC, dbSNP/dbVar (use via API/browser)

### ⚫ Line 3 — Compute & Pipelines (incl. single-cell / spatial)
- ✅ ChatSpatial (spatial, ~60 methods) — cafferychen777/ChatSpatial
- ✅ SCMCP (scRNA-seq, scverse) — scmcphub/scmcp
- 📇 AnnData MCP — biocontext-ai-anndata-mcp · 📇 CELLxGENE Census MCP — MaxMLang-cxg-census-mcp
- 📇 Galaxy MCP — galaxyproject-galaxy-mcp · 📇 Enrichr enrichment — tianqitang1-enrichr-mcp-server
- 📇 STRING (PPI) — meringlab-string-mcp · 📇 Reactome (pathways) — Augmented-Nature-Reactome-MCP-Server
- 📇 OmniPath networks (Saez lab) — saezlab-omnipath-next · 📇 BioCypher knowledge graphs — biocypher-biocypher-mcp
- 📇 ToolUniverse (Harvard MIMS, 200+ tools aggregator) — mims-harvard-ToolUniverse · 📇 gget — longevity-genie-gget-mcp
- ✅ Marketplace skills: single-cell-rna-qc, nextflow-development (nf-core), scvi-tools — anthropics/life-sciences
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

---

## Maintenance log
- **2026-06-17** — triaged the weekly connector-discovery backlog (PRs #1 · #2 · #13). Added **5 verified connectors** above, each confirmed **HTTP 200**: cyanheads/pubmed-mcp-server, cyanheads/ensembl-mcp-server, cyanheads/protein-mcp-server, ammawla/encode-toolkit, BaranziniLab/SPOKEAgent. The first two upgrade existing 📇 entries; the rest fill genuine gaps (ENCODE, consolidated protein structures, cross-domain SPOKE knowledge graph). Remaining candidates were dropped — out-of-scope (plant / Drosophila / aging-only), duplicate, or infra-heavy (GPU protein design); the full list stays readable in the closed PRs. Per the standing "don't grow the board" decision these are **catalogue-only**, not placed on the rendered map. Discovery procedure: see [docs/connector-discovery.md](docs/connector-discovery.md).
- **2026-06-17** — added **OpenEvidence** to Line 1 (catalogue-only) after reviewing three clinical-AI papers (MIRA, AMIE, the Vishwanath/Oermann benchmark). Wireable via the unofficial browser-session MCP or the official API; US VPN needed outside the US. **MIRA** (github.com/Dyke-F/MIRA) and **AMIE** (Google, unreleased) were reviewed but **not** added — research systems, not connectors; MIRA's building blocks (FHIR, openFDA, UMLS, OMOP) already sit on Line 5.

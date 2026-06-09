#!/usr/bin/env python3
"""
Claude Research Underground  ·  v2
=======================================
A Harry-Beck-style metro map of the connector / MCP / skill ecosystem usable
with Claude Code, centred on Claude as the grand-central interchange and
personalised to Gabriele Zoppoli's research stack.

v2 adds:
  * the full verified MCP catalogue (CATALOGUE.md) as drawn stations
  * INTERCHANGE LINES (London-Overground-style cased lines) for the aggregator
    MCP servers that genuinely span several domains — the "lines that connect
    the other lines": BioMCP, Open Targets, ToolUniverse, and the Discovery ring
    (Claude for Life Sciences marketplace + BioContextAI registry).
  * a 4-level TRUST encoding (live / verified / registry / unconfirmed), because
    the catalogue's worst possible error is a fabricated repo.

The whole network is DATA. Route builders populate a grid-position map (GPOS)
as they run, so every station and every interchange line stays consistent.
Edit the data, re-run, everything rebuilds.

Outputs: master.svg  (shared core for the print poster and the HTML console)
"""

import math
import json

# ----------------------------------------------------------------------------- grid
U  = 130                     # px per grid step (spread wide so the larger labels still get clear slots)
OX = 2016                    # centre x (Claude hub)
OY = 1706                    # centre y
W  = 4032                    # canvas width
H  = 3674                    # canvas height

def px(gx, gy):
    return (OX + gx * U, OY + gy * U)

# ----------------------------------------------------------------------------- lines
# Authentic London Underground line colours, themed to research domains.
LINES = {
    "lit":   {"name": "Literature & Evidence",     "color": "#E1251B"},  # Central red
    "gen":   {"name": "Genomic Data & Sequencing", "color": "#00782A"},  # District green
    "comp":  {"name": "Compute & Pipelines",       "color": "#1C1C1C"},  # Northern black
    "stat":  {"name": "Statistics & Trial Design", "color": "#0098D4"},  # Victoria blue
    "clin":  {"name": "Clinical & Regulatory",     "color": "#9B0056"},  # Metropolitan magenta
    "viz":   {"name": "Visualization & Figures",   "color": "#F1A800"},  # Circle yellow (darkened)
    "write": {"name": "Writing & Publishing",      "color": "#B26300"},  # Bakerloo brown
    "ops":   {"name": "Orchestration & Lab Ops",   "color": "#7A868C"},  # Jubilee grey
    "legal": {"name": "Legal & Paralegal",         "color": "#0E7C7B"},  # deep teal
}

# Interchange lines = real aggregator MCP servers that span several domains.
# Rendered as cased double-lines (Overground / Elizabeth-line style).
XLINES = {
    "biomcp":   {"name": "BioMCP — literature · genomic · trials federation", "color": "#6A3D9A", "dash": False},
    "otx":      {"name": "Open Targets — target · disease · treatment",       "color": "#E7298A", "dash": False},
    "discovery":{"name": "Discovery ring — Life-Sciences marketplace + BioContextAI", "color": "#8A6D3B", "dash": True},
}

# ----------------------------------------------------------------------------- stations
# tier: live (wired now) | verified (✅/🌐 real, ready to wire) |
#       registry (📇 registry-listed, confirm repo) | unconfirmed (⚠️)
S = lambda name, line, tier, desc, how, url="": dict(
    name=name, line=line, tier=tier, desc=desc, how=how, url=url)

STATIONS = {
  # ====================================================== Literature 🔴
  "pubmed":       S("PubMed","lit","live","35M+ biomedical citations; full-text, related-article & citation lookup.","MCP connected now — search, fetch metadata & full text directly.","https://pubmed.ncbi.nlm.nih.gov"),
  "consensus":    S("Consensus","lit","live","Evidence synthesis with claim-level support/oppose scoring.","MCP connected now — ask a question, get cited consensus.","https://consensus.app"),
  "europepmc":    S("Europe PMC","lit","verified","EU biomedical corpus incl. preprints, patents, grants, full text.","Public REST API via browser/HTTP; a Europe PMC MCP can be added.","https://europepmc.org"),
  "biorxiv":      S("bioRxiv","lit","verified","Biology preprints — earliest signal before peer review.","bioRxiv API via browser/HTTP.","https://www.biorxiv.org"),
  "medrxiv":      S("medRxiv","lit","verified","Clinical/medical preprints — trials & methods before journals.","medRxiv API via browser/HTTP.","https://www.medrxiv.org"),
  "semscholar":   S("Semantic Scholar","lit","verified","200M+ papers, citation graph, TLDR summaries.","Public Graph API; also federated inside BioMCP.","https://www.semanticscholar.org"),
  "deepresearch": S("deep-research","lit","live","Fan-out web search → fetch → adversarially verify → cited report.","Skill: deep-research."),
  "litreview":    S("literature-review","lit","live","Systematic reviews across PubMed/arXiv/bioRxiv/Semantic Scholar (PRISMA).","Skill: claude-scientific-writer:literature-review."),
  "researchlookup":S("research-lookup","lit","live","Fast current-research lookup (Parallel/Perplexity) for facts & papers.","Skill: claude-scientific-writer:research-lookup."),
  "pubmedmcp":    S("PubMed MCP","lit","registry","Standalone PubMed search/fetch over MCP.","MCP: andybrandt/mcp-simple-pubmed or grll/pubmedmcp — confirm repo, add to config."),
  "gscholar":     S("Google Scholar MCP","lit","registry","Scholar search over MCP (no official API; scrapes).","MCP: JackKuo666/Google-Scholar-MCP-Server — confirm repo."),
  "wiley":        S("Wiley Scholar Gateway","lit","verified","Wiley full-text scholarly gateway (marketplace remote MCP).","Install via /plugin marketplace add anthropics/life-sciences."),

  # ====================================================== Genomic 🟢
  "synapse":      S("Synapse.org","gen","live","Sage Bionetworks repository — controlled-access cohorts, consortium data.","MCP connected now — search & pull datasets (auth for controlled access).","https://www.synapse.org"),
  "geosra":       S("GEO / SRA","gen","verified","NCBI expression (GEO) & raw reads (SRA) — public omics at scale.","NCBI E-utilities API; or an NCBI MCP (see below).","https://www.ncbi.nlm.nih.gov/geo/"),
  "ensembldb":    S("Ensembl","gen","verified","Genome annotation, BioMart, VEP variant effect prediction.","Ensembl REST API; or an Ensembl MCP (see below).","https://www.ensembl.org"),
  "ucsc":         S("UCSC Browser","gen","verified","Genome browser, tracks, liftOver, table browser.","UCSC REST API; browser for exploration.","https://genome.ucsc.edu"),
  "gdc":          S("GDC / TCGA","gen","verified","NCI Genomic Data Commons + TCGA — mutations, CNV, expression, /analysis/survival.","Public REST API (gdc.cancer.gov/developers); no GDC MCP yet.","https://gdc.cancer.gov"),
  "clinvar":      S("ClinVar / gnomAD","gen","verified","Clinical variant significance + population allele frequencies.","NCBI / gnomAD APIs; also federated inside BioMCP.","https://gnomad.broadinstitute.org"),
  "cbioportal":   S("cBioPortal","gen","verified","Cancer genomics portal — TCGA, mutations, CNA, clinical.","REST API (cbioportal.org/api); MCP below.","https://www.cbioportal.org"),
  "depmap":       S("DepMap / OncoKB","gen","verified","Dependency/essentiality screens + precision-oncology annotation.","DepMap downloads; OncoKB API (token).","https://depmap.org"),
  "cellxgene":    S("CELLxGENE","gen","verified","Single-cell/spatial atlases — directly relevant to your Xenium work.","CZ CELLxGENE Census API; Census MCP below.","https://cellxgene.cziscience.com"),
  "cbioportalmcp":S("cBioPortal MCP","gen","verified","No-SQL natural-language queries over cBioPortal.","Official MCP (under construction): cBioPortal/cbioportal-mcp.","https://github.com/cBioPortal/cbioportal-mcp"),
  "opentargets":  S("Open Targets MCP","gen","verified","Target–disease–drug associations, genetics, tractability.","Official remote MCP: mcp.platform.opentargets.org/mcp.","https://platform.opentargets.org"),
  "ena":          S("ENA MCP","gen","verified","European Nucleotide Archive — reads, assemblies, sequence records.","MCP: biocontext-ai/nucleotide_archive_mcp.","https://github.com/biocontext-ai/nucleotide_archive_mcp"),
  "ensemblmcp":   S("Ensembl MCP","gen","registry","Genome annotation / BioMart / VEP over MCP.","MCP: effieklimi/ensembl-mcp-server — confirm repo."),
  "ncbimcp":      S("NCBI MCP","gen","registry","NCBI E-utilities (GEO/SRA/Gene/PubMed) over MCP.","MCP: noahzeidenberg/ncbi-mcp — confirm repo."),
  "biomart":      S("BioMart MCP","gen","registry","Ensembl BioMart attribute/filter queries over MCP.","MCP: jzinno/biomart-mcp — confirm repo."),
  "biobtree":     S("biobtree MCP","gen","registry","Cross-database biological ID mapping.","MCP: tamerh/biobtree — confirm repo."),
  "uniprot":      S("UniProt MCP","gen","registry","Protein sequences, function & features.","MCP: TakumiY235/uniprot-mcp-server — confirm repo."),
  "hgnc":         S("HGNC MCP","gen","registry","Official human gene nomenclature.","MCP: armish/hgnc.mcp — confirm repo."),
  "vep":          S("VEP MCP","gen","registry","Variant Effect Predictor consequences.","MCP: not-a-feature/VEPmcp — confirm repo."),
  "evo2":         S("Evo2 MCP","gen","registry","Evo2 genomic language-model queries.","MCP: not-a-feature/evo2-mcp — confirm repo."),
  "biothings":    S("BioThings MCP","gen","registry","MyGene / MyVariant / MyChem / MyDisease APIs.","MCP: Augmented-Nature/BioThings-MCP-Server or longevity-genie/biothings-mcp."),
  "interpro":     S("InterPro MCP","gen","registry","Protein families, domains & functional sites.","MCP: bio-mcp/interpro — confirm repo."),
  "rnacentral":   S("RNAcentral MCP","gen","registry","Non-coding RNA sequences across databases.","MCP: RNAcentral/rnacentral-mcp-server — confirm repo."),
  "pdbe":         S("PDBe MCP","gen","registry","Macromolecular structures from PDBe.","MCP: PDBeurope/PDBe-MCP-Servers — confirm repo."),
  "cellosaurus":  S("Cellosaurus MCP","gen","registry","Cell-line knowledge resource.","MCP: biocontext-ai/unofficial-cellosaurus-mcp."),
  "biostudies":   S("BioStudies MCP","gen","registry","EBI BioStudies datasets & supplementary data.","MCP: EBIBioStudies/biostudies-mcp-server — confirm repo."),
  "gwas":         S("GWAS Catalog MCP","gen","registry","GWAS associations (also inside BioMCP).","MCP: koido/gwas-catalog-mcp — confirm repo."),

  # ====================================================== Compute ⚫
  "python":       S("Python · scanpy/squidpy","comp","live","scanpy/squidpy/anndata for sc & spatial; pandas/numpy/scipy — all verified installed.","Bash + Python 3.12; Claude writes & runs the analysis now."),
  "jupyter":      S("Jupyter","comp","verified","Interactive notebooks — exploratory analysis & figures.","`pip install jupyterlab`; Claude drives notebooks via Bash."),
  "bioconductor": S("R · Bioconductor","comp","verified","Seurat, DESeq2, limma, edgeR, survminer — the bio-stats engine.","R 4.5.2 + base survival installed; add via BiocManager::install(...)."),
  "nextflow":     S("Nextflow / nf-core","comp","verified","Reproducible, containerised genomics pipelines at scale.","Install nf-core; Claude scaffolds & launches workflows.","https://nf-co.re"),
  "galaxy":       S("Galaxy","comp","verified","GUI/API workflow platform for accessible bioinformatics.","Galaxy public/local instance; API via browser.","https://usegalaxy.org"),
  "snakemake":    S("Snakemake","comp","verified","Make-style reproducible workflow engine for omics.","pip/conda; Claude writes the Snakefile.","https://snakemake.github.io"),
  "cfdna":        S("cfDNA stack","comp","verified","Your liquid-biopsy tools: ichorCNA, MEDIPS/MeDEStrand, fragmentomics, ONT.","Local conda envs; Claude orchestrates RENOVATE/MIMESIS pipelines."),
  "chatspatial":  S("ChatSpatial","comp","verified","Spatial-transcriptomics agent — ~60 methods (Xenium/Visium/MERFISH).","MCP: cafferychen777/ChatSpatial.","https://github.com/cafferychen777/ChatSpatial"),
  "scmcp":        S("SCMCP","comp","verified","scRNA-seq analysis via scverse (scanpy).","MCP: scmcphub/scmcp.","https://github.com/scmcphub/scmcp"),
  "scqc":         S("sc-RNA-QC skill","comp","verified","Official single-cell-rna-qc skill (marketplace).","Install: /plugin install single-cell-rna-qc@life-sciences."),
  "nfcoreskill":  S("nf-core dev skill","comp","verified","Official nextflow-development skill (marketplace).","Install via anthropics/life-sciences marketplace."),
  "scvitools":    S("scvi-tools","comp","verified","Probabilistic single-cell models skill (marketplace).","Install via anthropics/life-sciences marketplace."),
  "anndata":      S("AnnData MCP","comp","registry","Operate on AnnData (.h5ad) objects over MCP.","MCP: biocontext-ai/anndata-mcp."),
  "cxgcensus":    S("CxG Census MCP","comp","registry","Query the CZ CELLxGENE Census single-cell atlas.","MCP: MaxMLang/cxg-census-mcp — confirm repo."),
  "galaxymcp":    S("Galaxy MCP","comp","registry","Drive Galaxy workflows & histories over MCP.","MCP: galaxyproject/galaxy-mcp."),
  "enrichr":      S("Enrichr MCP","comp","registry","Gene-set enrichment across Enrichr libraries.","MCP: tianqitang1/enrichr-mcp-server."),
  "stringppi":    S("STRING MCP","comp","registry","Protein–protein interaction networks.","MCP: meringlab/string-mcp."),
  "reactome":     S("Reactome MCP","comp","registry","Curated pathway database queries.","MCP: Augmented-Nature/Reactome-MCP-Server."),
  "omnipath":     S("OmniPath MCP","comp","registry","Signaling/regulatory networks (Saez lab).","MCP: saezlab/omnipath-next."),
  "biocypher":    S("BioCypher MCP","comp","registry","Build & query biomedical knowledge graphs.","MCP: biocypher/biocypher-mcp."),
  "gget":         S("gget MCP","comp","registry","Swiss-army genomics queries (Ensembl/UniProt/BLAST/…).","MCP: longevity-genie/gget-mcp."),

  # ====================================================== Statistics 🔵
  "statsmodels":  S("statsmodels / scipy","stat","live","Regression, GLM, mixed models, hypothesis tests in Python.","Bash + Python; Claude writes the analysis."),
  "survival":     S("survival · lifelines","stat","live","Kaplan–Meier, Cox PH, competing risks — your endpoint engine.","lifelines (Py) / survival+survminer (R) via Bash."),
  "reporting":    S("reporting standards","stat","live","CONSORT / STROBE / PRISMA checklists baked into writing & review.","Skills: scientific-writing / peer-review."),
  "peerreview":   S("peer-review","stat","live","Systematic methodology, stats, design & reproducibility review.","Skill: claude-scientific-writer:peer-review."),
  "critthink":    S("critical-thinking","stat","live","Rigor, bias, confounding, GRADE / Cochrane RoB appraisal.","Skill: claude-scientific-writer:scientific-critical-thinking."),
  "bayes":        S("Bayesian · Stan/PyMC","stat","verified","Bayesian inference, hierarchical models, adaptive-trial priors.","Install PyMC/cmdstanpy; Claude builds the model.","https://www.pymc.io"),
  "power":        S("Power & sample size","stat","verified","Power, MDE, sample-size & simulation for trial design.","statsmodels.power / R pwr & simr."),
  "ctgmcp":       S("ClinTrials.gov MCP","stat","verified","Trial-registry queries over MCP (CTG API v2 + NCI CTS).","MCP: cyanheads/clinicaltrialsgov-mcp-server.","https://github.com/cyanheads/clinicaltrialsgov-mcp-server"),
  "aact":         S("AACT MCP","stat","registry","Aggregate Content of ClinicalTrials.gov (AACT) database.","MCP: navisbio/AACT_MCP."),
  "medcalc":      S("MedCalc MCP","stat","registry","Medical calculators & clinical equations.","MCP: winninghealth/medcalcmcp."),

  # ====================================================== Clinical 🟣
  "clinreports":  S("clinical-reports","clin","live","Case reports (CARE), CSR (ICH-E3), SOAP, discharge summaries.","Skill: claude-scientific-writer:clinical-reports."),
  "decision":     S("decision-support","clin","live","Biomarker-stratified cohorts, GRADE, treatment algorithms.","Skill: claude-scientific-writer:clinical-decision-support."),
  "treatment":    S("treatment-plans","clin","live","Focused LaTeX/PDF treatment plans across specialties.","Skill: claude-scientific-writer:treatment-plans."),
  "cltrials":     S("ClinicalTrials.gov","clin","verified","Global trial registry — design, comparators, recruitment.","CTG API v2 via browser/HTTP.","https://clinicaltrials.gov"),
  "euctr":        S("EU CTR / CTIS","clin","verified","EU clinical trials register & CTIS — the EU/IT regulatory side.","CTIS public portal via browser.","https://euclinicaltrials.eu"),
  "fdaema":       S("FDA / EMA","clin","verified","Approvals, labels, guidance, safety — regulatory grounding.","openFDA API; EMA via browser.","https://open.fda.gov"),
  "whoictrp":     S("WHO ICTRP","clin","verified","Cross-registry trial search (incl. non-US/EU).","ICTRP portal via browser.","https://trialsearch.who.int"),
  "omop":         S("OMOP / OHDSI MCP","clin","registry","OMOP common data model / OHDSI analytics.","MCP: OHNLP/omop_mcp."),
  "dicom":        S("DICOM MCP","clin","registry","Query/retrieve DICOM medical imaging.","MCP: ChristianHinge/dicom-mcp."),
  "ols4":         S("OLS4 MCP","clin","registry","EBI Ontology Lookup Service — ontologies & terms.","MCP: EBISPOT/ols4."),
  "bioportal":    S("BioPortal MCP","clin","registry","SNOMED / UMLS / biomedical ontologies.","MCP: ncbo/bioportal-mcp."),
  "chembl":       S("ChEMBL MCP","clin","registry","Bioactive molecules & drug-like compounds.","MCP: JackKuo666/ChEMBL-MCP-Server."),
  "pubchem":      S("PubChem MCP","clin","registry","Chemical structures, properties & bioassays.","MCP: cyanheads/pubchem-mcp-server."),
  "pharmacology": S("Pharmacology MCP","clin","registry","Guide to PHARMACOLOGY — targets & ligands.","MCP: longevity-genie/pharmacology-mcp."),
  "nexonco":      S("NexOnco MCP","clin","registry","Oncology clinical decisioning.","MCP: Nexgene-Research/nexonco-mcp."),

  # ====================================================== Visualization 🟡
  "biorender":    S("BioRender","viz","live","Publication figures from a vast bio icon/template library.","MCP connected now — search icons & templates.","https://www.biorender.com"),
  "mermaid":      S("Mermaid","viz","live","Flowcharts, sequence & ER diagrams from text; live render.","MCP connected now — validate & render diagrams.","https://mermaid.js.org"),
  "figma":        S("Figma","viz","live","Vector design for posters, schematics, slide polish.","MCP connected now (auth) — pull frames & assets.","https://www.figma.com"),
  "schematics":   S("scientific-schematics","viz","live","Pathways, architectures, mechanism diagrams (Nano Banana Pro).","Skill: claude-scientific-writer:scientific-schematics."),
  "infographics": S("infographics","viz","live","Data-driven infographics with colourblind-safe palettes.","Skill: claude-scientific-writer:infographics."),
  "imagegen":     S("image-gen · Nano/FLUX","viz","live","General images, illustrations, photoreal assets (FLUX/Gemini).","Skill: claude-scientific-writer:generate-image."),
  "gptimage":     S("gpt-image-2 (hero)","viz","verified","SOTA hero/cover artwork with reliable in-image text.","Manual ChatGPT handoff (Path A) — not wired to API.","https://chatgpt.com"),
  "napari":       S("napari MCP","viz","registry","Control the napari n-D image viewer.","MCP: royerlab/napari-mcp."),
  "pymol":        S("PyMOL MCP","viz","registry","Drive PyMOL molecular visualization.","MCP: vrtejus/pymol-mcp."),

  # ====================================================== Writing 🟤
  "sciwriting":   S("scientific-writing","write","live","IMRAD prose (never bullets), citations, reporting guidelines.","Skill: claude-scientific-writer:scientific-writing."),
  "citation":     S("citation-management","write","live","Scholar/PubMed metadata, DOI→BibTeX, reference validation.","Skill: claude-scientific-writer:citation-management."),
  "venue":        S("venue-templates","write","live","Nature/Science/PLOS/IEEE + NIH/NSF formatting & rules.","Skill: claude-scientific-writer:venue-templates."),
  "office":       S("Office docs","write","live","Author & edit docx / pptx / xlsx / pdf — tracked changes, slides, sheets.","Skills: claude-scientific-writer:docx/pptx/xlsx/pdf."),
  "markitdown":   S("markitdown","write","live","Convert PDF/DOCX/PPTX/audio/HTML → Markdown for ingest.","Skill: claude-scientific-writer:markitdown."),
  "humanizer":    S("humanizer","write","live","Strip AI-tells; enforce natural prose (your house style).","Skill: humanizer."),
  "slides":       S("preparing-slides","write","live","Your Zoppoli house-style .pptx engine (DIMI/GOIRC/…).","Skill: preparing-slides — your venues, palettes, rules."),
  "grants":       S("research-grants","write","live","NSF/NIH/DOE/DARPA + EU proposals, significance, budgets.","Skill: claude-scientific-writer:research-grants."),
  "paper2web":    S("paper-2-web","write","live","Paper → website / video / poster for dissemination.","Skill: claude-scientific-writer:paper-2-web."),
  "posters":      S("posters (LaTeX/PPTX)","write","live","Conference posters via beamerposter/tikz or PPTX.","Skills: latex-posters / pptx-posters."),
  "zotero":       S("Zotero","write","unconfirmed","Reference-manager library (collections, attachments).","Community Zotero MCPs exist — confirm before wiring.","https://www.zotero.org"),
  "overleaf":     S("Overleaf","write","unconfirmed","Collaborative LaTeX authoring.","No vetted MCP; use via web / git bridge.","https://www.overleaf.com"),

  # ====================================================== Orchestration ⚪
  "drive":        S("Google Drive","ops","live","Cloud store — data, manuscripts, shared docs; read & write.","MCP connected now — search, read, create files.","https://drive.google.com"),
  "gmail":        S("Gmail","ops","live","Search threads, draft, label — collaborator & journal comms.","MCP connected now — search & draft (you send).","https://mail.google.com"),
  "calendar":     S("Google Calendar","ops","live","Schedule meetings, deadlines, find slots.","MCP connected now — list, create, suggest times.","https://calendar.google.com"),
  "slack":        S("Slack","ops","live","Team/consortium channels — search & post.","MCP connected (auth) — search & message.","https://slack.com"),
  "workflows":    S("Workflows / subagents","ops","live","Deterministic multi-agent fan-out: review, migrate, research.","Workflow tool + Agent subagents — orchestrate at scale."),
  "schedule":     S("schedule / cron","ops","live","Recurring remote agents — overnight pipelines, polling, digests.","Skill: schedule — cron-style routines & one-offs."),
  "codex":        S("Codex · GPT-5.5","ops","live","Second engine — decorrelated review, long shell agents, red-team.","codex exec via Bash; Skill: codex-dispatch."),
  "marketplace":  S("Claude for Life Sciences","ops","verified","Anthropic's official life-sci plugin marketplace — remote MCPs + skills.","Install: /plugin marketplace add anthropics/life-sciences.","https://github.com/anthropics/life-sciences"),
  "biocontextai": S("BioContextAI Registry","ops","verified","Nature-Biotech-backed index of ~60 biomedical MCP servers.","Browse biocontext.ai/registry · github.com/biocontext-ai/registry.","https://biocontext.ai/registry"),
  "biocontextmeta":S("BioContextAI meta-MCP","ops","verified","Meta layer: knowledgebase / skill-to-mcp / protocol / registry servers.","github.com/biocontext-ai — add the meta server to your config."),
  "tooluniverse": S("ToolUniverse","ops","registry","Harvard MIMS aggregator — 200+ biomedical tools in one MCP.","MCP: mims-harvard/ToolUniverse.","https://github.com/mims-harvard/ToolUniverse"),
  "nar":          S("NAR DB Collection","ops","verified","2,173 curated molecular-biology databases (2026 issue) — the cross-check.","Reference index: academic.oup.com/nar.","https://academic.oup.com/nar/article/54/D1/D1/8402365"),
  "biomcp":       S("BioMCP","ops","verified","One server federating literature, variants, trials & cancer genomics.","MCP: genomoncology/biomcp — the single best biomedical addition.","https://github.com/genomoncology/biomcp"),

  # ====================================================== Legal ⚖️
  "gdpr":        S("GDPR & data protection","legal","live","EU GDPR (2016/679): DPAs, transfers, Art. 89 research exemptions.","Reference module — cited to EUR-Lex; verify before relying.","https://eur-lex.europa.eu/eli/reg/2016/679/oj"),
  "eugrants":    S("EU grants & consortia","legal","live","Horizon Europe Model Grant Agreement + Consortium Agreement (DESCA), IP/access rights.","Reference module — cited to EU Funding & Tenders / DESCA.","https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/agr-contr/general-mga_horizon-euratom_en.pdf"),
  "itlaw":       S("Italian research law","legal","live","Codice Privacy (196/2003) + Garante; procurement D.lgs 36/2023 (RUP); consenso informato & comitati etici.","Reference module — cited to Normattiva / Gazzetta Ufficiale.","https://www.normattiva.it"),
  "uslaw":       S("US research law","legal","live","HIPAA & BAAs; Common Rule (45 CFR 46) / IRB; IP (Bayh-Dole) & MTA/CDA/NDA.","Reference module — cited to eCFR / U.S. Code; verify before relying.","https://www.ecfr.gov/current/title-45"),
  "paralegalrev":S("paralegal-review","legal","live","Clause-by-clause review + redline + checklist conformance (non-lawyer, cited).","Skill: the tube-map paralegal journey."),
}

# Hubs
HUB   = dict(name="CLAUDE CODE", sub="your workstation · central")
TERMI = "codex"   # station id rendered as the sister terminus

# ----------------------------------------------------------------------------- route builders
# Directions in grid units. Orthogonal step 1.18; diagonal step 0.95 (≈1.34 spacing).
D = {
    "W": (-1.45, 0.0), "E": (1.45, 0.0), "N": (0.0, -1.45), "S": (0.0, 1.45),
    "NW": (-1.2, -1.2), "NE": (1.2, -1.2), "SE": (1.2, 1.2), "SW": (-1.2, 1.2),
    "SSE": (0.62, 1.42),
}
GPOS = {}                       # station id -> (gx, gy)
ROUTES = {k: [] for k in LINES} # line -> list of polyline segments

# Only DRAW the servers I'm super-confident of: live (wired now) + verified
# (✅ confirmed real repo / official endpoint, or a well-known public API).
# Registry-listed (📇, repo inferred — "confirm before wiring") and unconfirmed (⚠️)
# are pruned from the map; the full inventory still lives in CATALOGUE.md.
DRAWN_TIERS = {"live", "verified"}
def _keep(sid):
    return STATIONS[sid]["tier"] in DRAWN_TIERS

def _norm(d):
    dx, dy = D[d]
    return math.hypot(dx, dy)

def trunk(line, d, ids, exit=2.2):
    """Main spoke from the hub: (0,0) -> exit anchor -> stations along d."""
    ids = [s for s in ids if _keep(s)]
    dx, dy = D[d]
    ax, ay = dx/_norm(d)*exit, dy/_norm(d)*exit
    seg = [(0.0, 0.0, None), (round(ax,3), round(ay,3), None)]
    gx, gy = ax, ay
    for sid in ids:
        gx += dx; gy += dy
        seg.append((round(gx,3), round(gy,3), sid)); GPOS[sid] = (round(gx,3), round(gy,3))
    ROUTES[line].append(seg)

def branch(line, parent, d, ids):
    """Side branch peeling off an existing station `parent` in direction d."""
    ids = [s for s in ids if _keep(s)]
    if not ids:
        return
    dx, dy = D[d]
    sx, sy = GPOS[parent]
    seg = [(sx, sy, parent)]
    gx, gy = sx, sy
    for sid in ids:
        gx += dx; gy += dy
        seg.append((round(gx,3), round(gy,3), sid)); GPOS[sid] = (round(gx,3), round(gy,3))
    ROUTES[line].append(seg)

def place(sid, gx, gy):
    if not _keep(sid):
        return
    GPOS[sid] = (round(gx,3), round(gy,3))

# ----- Literature (West) -------------------------------------------------------
trunk("lit", "W", ["pubmed","consensus","europepmc","biorxiv","medrxiv","semscholar"])
branch("lit", "pubmed", "S", ["deepresearch","litreview","researchlookup"])
branch("lit", "consensus", "N", ["wiley"])
branch("lit", "europepmc", "N", ["pubmedmcp","gscholar"])

# ----- Genomic (NW quadrant) ---------------------------------------------------
trunk("gen", "NW", ["synapse","geosra","ensembldb","ucsc","gdc"], exit=2.0)
branch("gen", "synapse", "W", ["ena","ncbimcp"])
branch("gen", "geosra", "W", ["clinvar","cbioportal","depmap"])
branch("gen", "cbioportal", "N", ["cbioportalmcp","opentargets"])
branch("gen", "ensembldb", "W", ["biomart","biobtree","biothings"])
branch("gen", "ensembldb", "N", ["cellxgene","ensemblmcp"])
branch("gen", "ucsc", "W", ["interpro","rnacentral","pdbe"])
branch("gen", "ucsc", "N", ["uniprot","hgnc","vep"])
branch("gen", "gdc", "W", ["gwas","evo2"])
branch("gen", "gdc", "N", ["cellosaurus","biostudies"])

# ----- Compute (North) ---------------------------------------------------------
trunk("comp", "N", ["python","bioconductor","nextflow","snakemake"])
branch("comp", "python", "E", ["scmcp","chatspatial"])
branch("comp", "python", "W", ["jupyter","galaxy","cfdna"])
branch("comp", "bioconductor", "E", ["scqc","nfcoreskill","scvitools"])
branch("comp", "nextflow", "E", ["anndata","cxgcensus","galaxymcp"])
branch("comp", "snakemake", "W", ["enrichr","stringppi","reactome"])
branch("comp", "snakemake", "E", ["omnipath","biocypher","gget"])

# ----- Statistics (NE quadrant) ------------------------------------------------
trunk("stat", "NE", ["statsmodels","survival","reporting","peerreview"], exit=2.0)
branch("stat", "statsmodels", "N", ["power","bayes"])
branch("stat", "survival", "E", ["ctgmcp","aact","medcalc"])
branch("stat", "peerreview", "E", ["critthink"])

# ----- Clinical (East) ---------------------------------------------------------
trunk("clin", "E", ["clinreports","decision","treatment","cltrials"])
branch("clin", "decision", "S", ["nexonco","chembl","pubchem","pharmacology"])
branch("clin", "treatment", "N", ["omop","dicom"])
branch("clin", "cltrials", "S", ["euctr","fdaema","whoictrp"])
branch("clin", "cltrials", "N", ["ols4","bioportal"])

# ----- Visualization (SE quadrant) ---------------------------------------------
trunk("viz", "SE", ["biorender","schematics","infographics","imagegen"], exit=2.0)
branch("viz", "biorender", "E", ["mermaid","figma"])
branch("viz", "schematics", "S", ["napari","pymol"])
branch("viz", "imagegen", "S", ["gptimage"])

# ----- Writing (South) ---------------------------------------------------------
trunk("write", "S", ["sciwriting","citation","venue","grants"])
branch("write", "sciwriting", "W", ["office","markitdown"])
branch("write", "citation", "W", ["humanizer","slides"])   # moved off the legal channel
branch("write", "venue", "W", ["paper2web","posters"])
branch("write", "grants", "E", ["zotero","overleaf"])

# ----- Orchestration (SW quadrant) ---------------------------------------------
trunk("ops", "SW", ["drive","workflows","codex"], exit=2.0)
branch("ops", "drive", "W", ["gmail","calendar","slack","schedule"])

# ----- Legal (SSE — regulatory neighbour of Clinical) --------------------------
trunk("legal", "SSE", ["paralegalrev","gdpr","eugrants","itlaw","uslaw"], exit=1.8)

# ----- nodes that live only on interchange lines -------------------------------
place("biomcp", -3.4, -1.5)             # Literature ↔ Genomic, mid-radius (clear of the hub)
place("tooluniverse", -0.4, -2.4)       # north corridor, Compute ↔ Genomic
# discovery / install backbone — placed ON the outer ring ellipse (lower-left arc)
place("nar",            -10.4, 2.6)     # on the left edge of the frame
place("biocontextmeta",  -9.4, 6.7)     # lower-left corner curve
place("marketplace",     -6.0, 8.8)     # along the bottom edge
place("biocontextai",    -2.8, 8.8)

# prune the catalogue down to what was actually drawn (super-confident tiers only)
STATIONS = {sid: st for sid, st in STATIONS.items() if sid in GPOS}

# ----------------------------------------------------------------------------- interchange lines
def gp(sid):
    return GPOS[sid]

def ellipse(rx, ry, n=72):
    pts = []
    for i in range(n+1):
        a = 2*math.pi*i/n
        pts.append((rx*math.cos(a), ry*math.sin(a)))
    return pts

def roundrect(hw, hh, r, seg=9):
    """Closed rounded-rectangle perimeter (grid units), centred on the hub.
    hw/hh = half-width/height; r = corner radius. Walks TR→BR→BL→TL clockwise,
    the straight edges falling out of the gaps between consecutive corner arcs."""
    arcs = [
        ( hw-r, -(hh-r), -90,   0),   # top-right
        ( hw-r,  hh-r,     0,  90),   # bottom-right
        (-(hw-r), hh-r,   90, 180),   # bottom-left
        (-(hw-r),-(hh-r),180, 270),   # top-left
    ]
    pts = []
    for cx, cy, a0, a1 in arcs:
        for i in range(seg+1):
            a = math.radians(a0 + (a1-a0)*i/seg)
            pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    pts.append(pts[0])
    return pts

XROUTES = {
    # BioMCP: cancer-genomics cluster -> BioMCP node -> literature, with a spur
    # arcing OVER the hub to the trials side. One server, three lines.
    "biomcp": [
        [gp("depmap"), gp("cbioportal"), gp("clinvar"), gp("biomcp"), gp("pubmed")],
        [gp("biomcp"), (-1.8,-2.7), (1.6,-2.7), gp("ctgmcp")],
    ],
    # Open Targets: genomic target node arcing over the top, down the right to the
    # clinical decision-support side (target → disease → treatment).
    "otx": [
        [gp("opentargets"), gp("cbioportalmcp"), (-4.2,-3.4), (-1.0,-4.0), (2.4,-4.0),
         (5.0,-2.6), (5.0,-0.4), gp("decision")],
    ],
    # Discovery ring: the Circle line — Life-Sciences marketplace + BioContextAI
    # install/discovery backbone, an outer ellipse threading its four stations.
    "discovery": [roundrect(10.4, 8.8, 1.8)],
}

# Interchange stations (where a connecting line meets a spoke) get a Beck marker.
INTERCHANGE = {
    "biomcp","pubmed","clinvar","cbioportal","depmap","ctgmcp","opentargets","cbioportalmcp",
    "decision","marketplace","biocontextai","biocontextmeta","nar",
}

# ----------------------------------------------------------------------------- labels
def outward_dir(gx, gy):
    """Default: label points away from the hub, snapped to 8 compass points."""
    if gx == 0 and gy == 0:
        return "N"
    ang = math.degrees(math.atan2(-gy, gx)) % 360   # screen y is down
    idx = int((ang + 22.5) // 45) % 8
    return ["E","NE","N","NW","W","SW","S","SE"][idx]

# explicit overrides where the radial default collides (filled in after review)
LABEL_OVERRIDE = {
    # --- lit (W trunk @ y=0; pubmed↓ column, consensus/europepmc↑ branches)
    "pubmed":"N","consensus":"S","europepmc":"S","biorxiv":"N","medrxiv":"N","semscholar":"N",
    "deepresearch":"W","litreview":"W","researchlookup":"W","wiley":"N","pubmedmcp":"W","gscholar":"W",
    # --- gen (NW trunk; W rows + N columns)
    "synapse":"N","geosra":"N","ensembldb":"NE","ucsc":"NE","gdc":"NE",
    "ena":"N","ncbimcp":"N","clinvar":"N","cbioportal":"S","depmap":"S",
    "cbioportalmcp":"W","opentargets":"W","biomart":"S","biobtree":"S","biothings":"S",
    "cellxgene":"N","ensemblmcp":"W","interpro":"S","rnacentral":"S","pdbe":"S",
    "uniprot":"W","hgnc":"W","vep":"W","gwas":"S","evo2":"S","cellosaurus":"W","biostudies":"W",
    # --- comp (N trunk; E rows + W rows)
    "python":"N","bioconductor":"N","nextflow":"N","snakemake":"N",
    "scmcp":"E","chatspatial":"E","jupyter":"W","galaxy":"W","cfdna":"W",
    "scqc":"E","nfcoreskill":"E","scvitools":"E","anndata":"E","cxgcensus":"E","galaxymcp":"E",
    "enrichr":"W","stringppi":"W","reactome":"W","omnipath":"E","biocypher":"E","gget":"E",
    # --- stat (NE trunk; statsmodels↑ column, survival→ row)
    "statsmodels":"NW","survival":"NW","reporting":"NW","peerreview":"NW",
    "power":"E","bayes":"E","ctgmcp":"N","aact":"N","medcalc":"N","critthink":"N",
    # --- clin (E trunk @ y=0; decision↓ & cltrials↓ columns, treatment↑ & cltrials↑)
    "clinreports":"N","decision":"N","treatment":"S","cltrials":"N",
    "nexonco":"E","chembl":"E","pubchem":"E","pharmacology":"E",
    "omop":"W","dicom":"W","euctr":"E","fdaema":"E","whoictrp":"E","ols4":"E","bioportal":"E",
    # --- viz (SE trunk; biorender→ row, schematics↓ column)
    "biorender":"NE","schematics":"NE","infographics":"NE","imagegen":"NE",
    "mermaid":"N","figma":"N","napari":"E","pymol":"E","gptimage":"E",
    # --- legal (SSE trunk between Writing and Visualization)
    "paralegalrev":"E","gdpr":"W","eugrants":"E","itlaw":"W","uslaw":"E",
    # --- write (S trunk; alternating W/E rows, trunk labels opposite their branch)
    "sciwriting":"E","citation":"W","venue":"E","grants":"W",
    "office":"S","markitdown":"S","humanizer":"S","slides":"S","paper2web":"S","posters":"S",
    "zotero":"S","overleaf":"S",
    # --- ops (SW trunk; drive→ row going W)
    "drive":"S","workflows":"SE","gmail":"S","calendar":"S","slack":"S","schedule":"S",
    "marketplace":"SW","biocontextai":"S","biocontextmeta":"W","nar":"W",
    # --- interchange-only nodes
    "biomcp":"N","tooluniverse":"NW",
}

def label_dir(sid):
    if sid in LABEL_OVERRIDE:
        return LABEL_OVERRIDE[sid]
    gx, gy = GPOS[sid]
    return outward_dir(gx, gy)

# ----------------------------------------------------------------------------- helpers
COORD = {sid: px(gx, gy) for sid, (gx, gy) in GPOS.items()}

# --- automatic label placement: nudge each label to the clearest nearby slot --------
# Each label tries its preferred (hand-tuned) direction first, then alternatives, and
# takes the slot with the least overlap against the drawn lines + already-placed labels.
_LBASE = {'N':(0,-14,'middle'),'S':(0,19,'middle'),'E':(13,4,'start'),'W':(-13,4,'end'),
          'NE':(11,-9,'start'),'NW':(-11,-9,'end'),'SE':(11,16,'start'),'SW':(-11,16,'end')}
def _lbox(x, y, dx, dy, anchor, tw, fh=19):
    ax, ay = x + dx, y + dy
    x0 = ax - 3 if anchor == 'start' else (ax - tw + 3 if anchor == 'end' else ax - tw / 2)
    return (x0, ay - fh, x0 + tw, ay + 3)
def _ovl(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

# sample every drawn line into a px point-cloud (for label↔line collision scoring)
_LINEPTS = []
for _segs in list(ROUTES.values()) + list(XROUTES.values()):
    for _seg in _segs:
        _p = [px(g[0], g[1]) for g in _seg]
        for _i in range(len(_p) - 1):
            (x1, y1), (x2, y2) = _p[_i], _p[_i + 1]
            _n = max(1, int(math.hypot(x2 - x1, y2 - y1) / 14))
            for _t in range(_n + 1):
                _LINEPTS.append((x1 + (x2 - x1) * _t / _n, y1 + (y2 - y1) * _t / _n))

LABEL_POS = {}
_placed = []                       # boxes of labels already placed
_order = sorted((s for s in COORD if s != TERMI),
                key=lambda s: (STATIONS[s]["tier"] != "live", -len(STATIONS[s]["name"])))
for _sid in _order:
    _x, _y = COORD[_sid]
    _tw = len(STATIONS[_sid]["name"]) * 10.0 + 6
    _near = [p for p in _LINEPTS if abs(p[0] - _x) < 175 and abs(p[1] - _y) < 150]
    _pref = label_dir(_sid)
    _dirs = [_pref] + [d for d in ('E', 'W', 'S', 'N', 'SE', 'NE', 'SW', 'NW') if d != _pref]
    _best, _bs = None, 1e18
    for _ci, _d in enumerate(_dirs):
        _bx, _by, _an = _LBASE[_d]
        for _ki, _k in enumerate((1.0, 1.7, 2.5)):
            _dx, _dy = _bx * _k, _by * _k
            _b = _lbox(_x, _y, _dx, _dy, _an, _tw)
            _ln = sum(1 for p in _near if _b[0] <= p[0] <= _b[2] and _b[1] <= p[1] <= _b[3])
            _lo = sum(1 for pb in _placed if _ovl(_b, pb))
            _sc = _ln * 1.0 + _lo * 55 + _ci * 2.4 + _ki * 5
            if _sc < _bs:
                _bs, _best = _sc, (_dx, _dy, _an, _b)
    LABEL_POS[_sid] = (_best[0], _best[1], _best[2])
    _placed.append(_best[3])

def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
             .replace('"',"&quot;"))

def poly_pts(seg_or_pts, has_ids=True):
    if has_ids:
        return " ".join(f"{px(gx,gy)[0]:.1f},{px(gx,gy)[1]:.1f}" for (gx,gy,_) in seg_or_pts)
    return " ".join(f"{px(gx,gy)[0]:.1f},{px(gx,gy)[1]:.1f}" for (gx,gy) in seg_or_pts)

# ----------------------------------------------------------------------------- render
def render(focus=None):
    # focus: a LINES id or XLINES id -> spotlight that line, grey everything else.
    FG_DIM = "#dcd9d0"                       # greyed stroke for non-focal elements
    is_lfocus = focus in LINES
    is_xfocus = focus in XLINES
    _xstops = set(XSTOPS.get(focus, [])) if is_xfocus else set()
    def line_on(lid):  return (focus is None) or (is_lfocus and lid == focus)
    def xline_on(xid): return (focus is None) or (is_xfocus and xid == focus)
    def stn_on(sid):
        if focus is None: return True
        if is_lfocus:     return STATIONS[sid]["line"] == focus
        if is_xfocus:     return sid in _xstops
        return True
    # crop the viewBox to the focal content so each line fills the frame; full canvas otherwise
    if focus is None:
        VBX, VBY, VBW, VBH = 0, 0, W, H
    else:
        xs, ys = [OX], [OY]                       # always include the Claude hub
        for _sid in COORD:
            if _sid == TERMI and focus != "ops":
                continue
            if stn_on(_sid):
                _x, _y = COORD[_sid]; xs.append(_x); ys.append(_y)
        pad = 150
        minx, maxx = min(xs) - pad, max(xs) + pad
        miny, maxy = min(ys) - pad - 70, max(ys) + pad     # extra top headroom for the banner
        VBW, VBH = maxx - minx, maxy - miny
        tar = W / H
        if VBW / VBH < tar:                       # too tall -> widen, centered
            nw = VBH * tar; minx -= (nw - VBW) / 2; VBW = nw
        else:                                     # too wide -> heighten, centered
            nh = VBW / tar; miny -= (nh - VBH) / 2; VBH = nh
        VBX, VBY = minx, miny
    out = []
    out.append(f'<svg id="map" xmlns="http://www.w3.org/2000/svg" '
               f'viewBox="{VBX:.0f} {VBY:.0f} {VBW:.0f} {VBH:.0f}" '
               f'font-family="Helvetica Neue, Helvetica, Arial, sans-serif">')
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fbfaf6"/>')

    # --- cfDNA river (the Thames easter-egg)
    RY = H - 360
    river = (f"M -20 {RY:.0f} C {W*0.22:.0f} {RY-40:.0f}, {W*0.30:.0f} {RY+70:.0f}, {W*0.40:.0f} {RY+46:.0f} "
             f"S {W*0.62:.0f} {RY-30:.0f}, {W*0.73:.0f} {RY+38:.0f} S {W*0.88:.0f} {RY+82:.0f}, {W+20} {RY+26:.0f}")
    out.append(f'<path d="{river}" fill="none" stroke="#cfe3ef" stroke-width="40" stroke-linecap="round"/>')
    out.append(f'<text x="195" y="{RY-10:.0f}" font-size="17" font-style="italic" fill="#5f86a0">the cfDNA river</text>')

    # --- radial lines
    LW = 10
    for line, segs in ROUTES.items():
        on = line_on(line)
        c  = LINES[line]["color"] if on else FG_DIM
        lw = (LW + 3) if (on and focus is not None) else LW
        op = 1.0 if on else 0.28
        for seg in segs:
            out.append(f'<polyline points="{poly_pts(seg)}" fill="none" stroke="{c}" '
                       f'stroke-width="{lw}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')

    # --- interchange lines (cased double-line: colour casing + white core).
    # The discovery ring is the lightest — background "install backbone".
    for xid, segs in XROUTES.items():
        on = xline_on(xid)
        c = (XLINES[xid]["color"] if on else FG_DIM); dash = XLINES[xid]["dash"]
        ring_line = (xid == "discovery")
        casing_w, core_w, op = (6.5, 2.3, 0.5) if ring_line else (8.0, 3.0, 0.9)
        if focus is not None and not on: op = 0.16
        if focus is not None and on:     casing_w += 2
        da = ' stroke-dasharray="13 10"' if dash else ''
        for pts in segs:
            p = poly_pts(pts, has_ids=False)
            out.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="{casing_w}" '
                       f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{da}/>')
            out.append(f'<polyline points="{p}" fill="none" stroke="#fbfaf6" stroke-width="{core_w}" '
                       f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{da}/>')

    # --- stations by trust tier
    def draw_station(sid):
        st = STATIONS[sid]; x, y = COORD[sid]; c = LINES[st["line"]]["color"]
        tier = st["tier"]
        if focus is not None and not stn_on(sid):
            out.append(f'<circle class="stn" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="5.0" '
                       f'fill="#ffffff" stroke="{FG_DIM}" stroke-width="2.0" opacity="0.45"/>')
            out.append(f'<circle class="hit" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#000" opacity="0"/>')
            return
        if sid in INTERCHANGE:
            out.append(f'<circle class="stn" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="9.2" '
                       f'fill="#ffffff" stroke="#1c1c1c" stroke-width="3.2"/>')
        elif tier == "live":
            out.append(f'<circle class="stn" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="6.4" '
                       f'fill="{c}" stroke="#ffffff" stroke-width="2.0"/>')
        elif tier == "verified":
            out.append(f'<circle class="stn" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="6.2" '
                       f'fill="#ffffff" stroke="{c}" stroke-width="3.2"/>')
        elif tier == "registry":
            out.append(f'<circle class="stn" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="5.7" '
                       f'fill="#ffffff" stroke="{c}" stroke-width="2.2" stroke-dasharray="2.2 1.9"/>')
        else:  # unconfirmed
            out.append(f'<circle class="stn" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="5.4" '
                       f'fill="#ffffff" stroke="{c}" stroke-width="1.8" stroke-dasharray="2.0 2.2" opacity="0.6"/>')
        out.append(f'<circle class="hit" data-sid="{sid}" cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#000" opacity="0"/>')

    for sid in COORD:
        if sid == TERMI:
            continue
        draw_station(sid)

    # --- labels
    def label_off(dirn):
        m = {'N':(0,-14,'middle'),'S':(0,19,'middle'),'E':(13,4,'start'),'W':(-13,4,'end'),
             'NE':(11,-9,'start'),'NW':(-11,-9,'end'),'SE':(11,16,'start'),'SW':(-11,16,'end')}
        return m[dirn]
    for sid in COORD:
        if sid == TERMI:
            continue
        if focus is not None and not stn_on(sid):
            continue
        st = STATIONS[sid]; x, y = COORD[sid]
        dx, dy, anchor = LABEL_POS.get(sid, label_off(label_dir(sid)))
        if st["tier"] == "live":
            color, weight, style = "#1c1c1c", "600", "normal"
        elif st["tier"] == "verified":
            color, weight, style = "#2c2c2c", "500", "normal"
        elif st["tier"] == "registry":
            color, weight, style = "#6b6b6b", "400", "normal"
        else:
            color, weight, style = "#9a9183", "400", "italic"
        out.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="18" text-anchor="{anchor}" '
                   f'fill="{color}" font-weight="{weight}" font-style="{style}" '
                   f'paint-order="stroke" stroke="#fbfaf6" stroke-width="5.5" stroke-linejoin="round">{esc(st["name"])}</text>')

    # --- Codex sister terminus
    cx, cy = COORD[TERMI]
    _cop = 0.30 if (focus is not None and focus != "ops") else 1.0
    out.append(f'<g opacity="{_cop}">')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="20" fill="#ffffff" stroke="#10a37f" stroke-width="6"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="#10a37f"/>')
    out.append(f'<circle class="hit" data-sid="codex" cx="{cx:.1f}" cy="{cy:.1f}" r="22" fill="#000" opacity="0"/>')
    out.append(f'<text x="{cx-26:.1f}" y="{cy+6:.1f}" font-size="16" text-anchor="end" font-weight="700" fill="#0c7a5e">Codex · GPT-5.5</text>')
    out.append(f'<text x="{cx-26:.1f}" y="{cy+24:.1f}" font-size="12" text-anchor="end" fill="#0c7a5e">second engine</text>')
    out.append('</g>')

    # --- Claude central hub (on top)
    out.append(f'<circle cx="{OX}" cy="{OY}" r="42" fill="#ffffff" stroke="#1c1c1c" stroke-width="3"/>')
    out.append(f'<circle cx="{OX}" cy="{OY}" r="34" fill="#ffffff" stroke="#D97757" stroke-width="9"/>')
    out.append(f'<circle cx="{OX}" cy="{OY}" r="11" fill="#D97757"/>')
    out.append(f'<circle class="hit" data-sid="claude" cx="{OX}" cy="{OY}" r="44" fill="#000" opacity="0"/>')
    out.append(f'<text x="{OX}" y="{OY-58}" font-size="22" text-anchor="middle" font-weight="800" fill="#1c1c1c" paint-order="stroke" stroke="#fbfaf6" stroke-width="4.5" stroke-linejoin="round">CLAUDE CODE</text>')
    out.append(f'<text x="{OX}" y="{OY+64}" font-size="13" text-anchor="middle" fill="#6b6b6b">your workstation · central interchange</text>')

    # --- title block (top-left)
    out.append(f'<text x="56" y="78" font-size="38" font-weight="800" fill="#1c1c1c">Claude Research Underground</text>')
    out.append(f'<text x="58" y="108" font-size="16" fill="#6b6b6b">the connectors, MCP servers &amp; skills worth wiring — genomics · medicine · comp-bio · stats · trial design — Claude at the centre</text>')
    out.append(f'<text x="58" y="132" font-size="13.5" fill="#8a8170">curated to the live + verified set · solid interchange lines = multi-domain MCP servers · outer dashed ring = the discovery / install backbone</text>')

    # --- focus banner (only on per-line focus renders; positioned inside the cropped frame)
    if focus is not None:
        fname = LINES[focus]["name"] if is_lfocus else XLINES[focus]["name"]
        fcol  = LINES[focus]["color"] if is_lfocus else XLINES[focus]["color"]
        pill_w = 30 + int(len(fname) * 12.6)
        bx, by = VBX + 30, VBY + 26
        out.append(f'<rect x="{bx:.0f}" y="{by:.0f}" rx="18" ry="18" width="{pill_w}" height="36" fill="{fcol}"/>')
        out.append(f'<text x="{bx+19:.0f}" y="{by+24:.0f}" font-size="18" font-weight="800" fill="#ffffff">▶  {esc(fname)}</text>')

    # --- legend (bottom band)
    lx = 56; ly = H - 232
    out.append(f'<text x="{lx}" y="{ly}" font-size="16" font-weight="700" fill="#1c1c1c">LINES</text>')
    order = ["lit","gen","comp","stat","clin","viz","write","ops","legal"]
    col_x = [lx, lx+330, lx+660, lx+990]
    for i, lid in enumerate(order):
        cxp = col_x[i % 4]; cyp = ly + 26 + (i // 4) * 26
        _on = line_on(lid)
        _sw = LINES[lid]["color"] if _on else FG_DIM
        _tx = "#1c1c1c" if _on else "#b9b5ab"
        out.append(f'<rect x="{cxp}" y="{cyp-11}" width="26" height="9" rx="4.5" fill="{_sw}"/>')
        out.append(f'<text x="{cxp+34}" y="{cyp-2}" font-size="13.5" fill="{_tx}">{esc(LINES[lid]["name"])}</text>')

    # interchange-line legend
    iy = ly + 92
    out.append(f'<text x="{lx}" y="{iy}" font-size="16" font-weight="700" fill="#1c1c1c">INTERCHANGE LINES (multi-domain MCP servers)</text>')
    for i, xid in enumerate(["biomcp","otx","discovery"]):
        cxp = col_x[i % 4]; cyp = iy + 26
        da = 'stroke-dasharray="6 4"' if XLINES[xid]["dash"] else ''
        out.append(f'<line x1="{cxp}" y1="{cyp-6}" x2="{cxp+26}" y2="{cyp-6}" stroke="{XLINES[xid]["color"]}" stroke-width="6" {da}/>')
        out.append(f'<line x1="{cxp}" y1="{cyp-6}" x2="{cxp+26}" y2="{cyp-6}" stroke="#fbfaf6" stroke-width="2" {da}/>')
        out.append(f'<text x="{cxp+34}" y="{cyp-2}" font-size="12.5" fill="#1c1c1c">{esc(XLINES[xid]["name"])}</text>')

    # KEY (trust tiers) — right side of legend band
    kx = lx + 1370; ky = ly
    out.append(f'<text x="{kx}" y="{ky}" font-size="16" font-weight="700" fill="#1c1c1c">KEY — status &amp; trust</text>')
    rows = [
        ("live",       "#1c1c1c", "live now — wired in your session"),
        ("verified",   "#1c1c1c", "verified — real &amp; ready to wire"),
        ("interchange","#1c1c1c", "interchange — a connecting line stops here"),
    ]
    for i,(tier,_,lab) in enumerate(rows):
        ry = ky + 24 + i*23; mx = kx + 9
        if tier == "live":
            out.append(f'<circle cx="{mx}" cy="{ry-4}" r="6.4" fill="#1c1c1c" stroke="#fff" stroke-width="2"/>')
        elif tier == "verified":
            out.append(f'<circle cx="{mx}" cy="{ry-4}" r="6.2" fill="#fff" stroke="#1c1c1c" stroke-width="3.2"/>')
        elif tier == "registry":
            out.append(f'<circle cx="{mx}" cy="{ry-4}" r="5.7" fill="#fff" stroke="#1c1c1c" stroke-width="2.2" stroke-dasharray="2.2 1.9"/>')
        elif tier == "unconfirmed":
            out.append(f'<circle cx="{mx}" cy="{ry-4}" r="5.4" fill="#fff" stroke="#8a8f93" stroke-width="1.8" stroke-dasharray="2 2.2"/>')
        else:
            out.append(f'<circle cx="{mx}" cy="{ry-4}" r="8.6" fill="#fff" stroke="#1c1c1c" stroke-width="3.2"/>')
        out.append(f'<text x="{kx+26}" y="{ry}" font-size="12.5" fill="#1c1c1c">{lab}</text>')

    out.append('</svg>')
    return "\n".join(out)

def station_data():
    data = {}
    data["claude"] = dict(
        name="Claude Code", line="hub", linename="Central interchange", color="#D97757",
        live=True, tier="live", kind="hub", x=OX, y=OY,
        desc="You — the grand-central interchange. Every line meets here: Claude routes the work, reasons, writes & runs code, and dispatches the rest.",
        how="This is the station you sit in. Talk to Claude Code on your workstation; it drives every other line on this map.", url="")
    for sid, st in STATIONS.items():
        xy = COORD.get(sid)
        color = "#10a37f" if sid == TERMI else LINES[st["line"]]["color"]
        data[sid] = dict(
            name=st["name"], line=st["line"], linename=LINES[st["line"]]["name"],
            color=color, live=(st["tier"]=="live"), tier=st["tier"],
            interchange=(sid in INTERCHANGE), desc=st["desc"], how=st["how"], url=st["url"],
            x=(round(xy[0],1) if xy else None), y=(round(xy[1],1) if xy else None),
            kind=("terminus" if sid == TERMI else ("stop" if xy else "catalogue")))
    return data

CONSOLE_TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claude Research Underground</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif;color:#1c1c1c;background:#fbfaf6}
header{display:flex;align-items:center;gap:16px;padding:10px 18px;border-bottom:1px solid #e7e3d8;background:#fff;position:sticky;top:0;z-index:5}
.brand{font-weight:800;font-size:18px;line-height:1.15;white-space:nowrap}
.brand small{display:block;font-weight:400;color:#8a8170;font-size:11.5px}
.brand .dot{display:inline-block;width:14px;height:14px;border-radius:50%;background:#D97757;border:2px solid #1c1c1c;vertical-align:middle;margin-right:6px}
#search{flex:1;max-width:440px;padding:9px 12px;border:1px solid #ddd6c7;border-radius:9px;font-size:14px;outline:none}
#search:focus{border-color:#D97757}
button{padding:8px 12px;border:1px solid #ddd6c7;background:#fff;border-radius:9px;cursor:pointer;font-size:13px}
button:hover{background:#f4f1e8}
main{display:flex;height:calc(100vh - 59px)}
#mapwrap{flex:1;position:relative;overflow:hidden;background:#fbfaf6;cursor:grab}
#mapwrap:active{cursor:grabbing}
#map{width:100%;height:100%;display:block;touch-action:none}
.hit{cursor:pointer}
.stn{transition:stroke-width .08s}
.stn.hl{stroke-width:7 !important;filter:drop-shadow(0 0 3px rgba(0,0,0,.4))}
.stn.dim{opacity:.12}
#panel{width:372px;flex:none;border-left:1px solid #e7e3d8;background:#fff;overflow-y:auto;padding:18px 20px}
.tip{position:absolute;display:none;max-width:300px;background:rgba(20,20,20,.94);color:#fff;padding:9px 11px;border-radius:9px;font-size:12.5px;pointer-events:none;z-index:9;line-height:1.45}
.chip{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}
.hint{color:#8a8170;font-size:13px;line-height:1.5}
.lines-list{margin-top:14px}
.lines-list .ln{display:flex;align-items:center;gap:9px;padding:6px 6px;border-radius:7px;cursor:pointer;font-size:13.5px}
.lines-list .ln:hover{background:#f4f1e8}
.lines-list .hdr{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:#9a9183;margin:12px 0 2px}
.sw{width:24px;height:8px;border-radius:5px;flex:none}
.sw.x{height:6px;border:1px solid #fff;outline:1px solid rgba(0,0,0,.15)}
h2{margin:.1em 0 .3em}
.d-bar{height:6px;border-radius:4px;margin-bottom:12px}
.badge{display:inline-block;font-size:11px;padding:2px 9px;border-radius:20px;border:1px solid #e3ddcf;margin:0 6px 8px 0;color:#6b6356}
.badge.live{background:#e9f7ef;border-color:#bfe6cf;color:#137a43}
.badge.verified{background:#eaf3fb;border-color:#c4ddf2;color:#1763a6}
.badge.registry{background:#f4f3ef;color:#8a8170}
.badge.unconfirmed{background:#faf3ef;border-color:#eccfc0;color:#a8703f}
.badge.xchg{background:#f3eefb;border-color:#d8c9ee;color:#6A3D9A}
.desc{font-size:14px;line-height:1.5;margin:6px 0}
.how{background:#f7f5ee;border:1px solid #ece7d8;border-radius:9px;padding:11px 12px;font-size:13px;line-height:1.5;margin-top:12px}
.how b{display:block;text-transform:uppercase;letter-spacing:.04em;font-size:10.5px;color:#9a9183;margin-bottom:4px}
a.open{display:inline-block;margin-top:14px;padding:9px 13px;background:#1c1c1c;color:#fff;border-radius:9px;text-decoration:none;font-size:13px}
a.open:hover{background:#D97757}
.res{padding:8px 6px;border-bottom:1px solid #f0ece1;cursor:pointer;font-size:13.5px;display:flex;align-items:center;gap:8px}
.res:hover{background:#f4f1e8}
.back{font-size:13px;color:#8a8170;cursor:pointer;margin-bottom:10px;display:inline-block}
.back:hover{color:#D97757}
.muted{color:#9a9183;font-size:12px}
</style></head><body>
<header>
  <div class="brand"><span class="dot"></span>Claude Research Underground
    <small>Claude at the centre &middot; hover a station, click for how to wire it</small></div>
  <input id="search" placeholder="Search stations &mdash; e.g. BioMCP, spatial, trial, variant, ontology&hellip;">
  <button id="reset">Reset view</button>
</header>
<main>
  <div id="mapwrap">__SVG__<div id="tip" class="tip"></div></div>
  <aside id="panel"><div id="pdefault"></div><div id="pdetail" hidden></div></aside>
</main>
<script>
const DATA=__DATA__, LINES=__LINES__, XLINES=__XLINES__, ORDER=__ORDER__;
const svg=document.getElementById('map'), wrap=document.getElementById('mapwrap'),
      tip=document.getElementById('tip'), panel=document.getElementById('panel'),
      pdef=document.getElementById('pdefault'), pdet=document.getElementById('pdetail'),
      search=document.getElementById('search');
const BASE={x:0,y:0,w:__W__,h:__H__}; let vb={...BASE};
function setVB(){svg.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h);}
function flyTo(x,y,w){if(x==null)return; w=w||760; vb.w=w; vb.h=w*BASE.h/BASE.w; vb.x=x-vb.w/2; vb.y=y-vb.h/2; setVB();}
wrap.addEventListener('wheel',e=>{e.preventDefault();const r=svg.getBoundingClientRect();
  const mx=vb.x+(e.clientX-r.left)/r.width*vb.w, my=vb.y+(e.clientY-r.top)/r.height*vb.h;
  const f=e.deltaY<0?0.86:1/0.86; let nw=Math.min(BASE.w*1.5,Math.max(320,vb.w*f));
  const nh=nw*BASE.h/BASE.w; vb.x=mx-(mx-vb.x)*nw/vb.w; vb.y=my-(my-vb.y)*nh/vb.h; vb.w=nw; vb.h=nh; setVB();
},{passive:false});
let drag=null;
wrap.addEventListener('pointerdown',e=>{if(e.target.classList.contains('hit'))return; drag={x:e.clientX,y:e.clientY,vx:vb.x,vy:vb.y};});
window.addEventListener('pointermove',e=>{if(!drag)return;const r=svg.getBoundingClientRect();
  vb.x=drag.vx-(e.clientX-drag.x)/r.width*vb.w; vb.y=drag.vy-(e.clientY-drag.y)/r.height*vb.h; setVB();});
window.addEventListener('pointerup',()=>drag=null);
document.getElementById('reset').onclick=()=>{vb={...BASE};setVB();search.value='';clearSearch();showDefault();};
function stnEl(sid){return svg.querySelector('.stn[data-sid="'+sid+'"]');}
let hovered=null;
svg.addEventListener('mousemove',e=>{const t=e.target;
  if(t.classList&&t.classList.contains('hit')){const sid=t.getAttribute('data-sid'),d=DATA[sid];
    tip.innerHTML='<span class="chip" style="background:'+d.color+'"></span><b>'+d.name+'</b> &middot; <span style="opacity:.8">'+d.linename+'</span><br>'+d.desc;
    tip.style.display='block';const r=wrap.getBoundingClientRect();
    let lx=e.clientX-r.left+16, ly=e.clientY-r.top+16;
    if(lx>r.width-310)lx=e.clientX-r.left-310; tip.style.left=lx+'px';tip.style.top=ly+'px';
    if(hovered!==sid){if(hovered){const o=stnEl(hovered);o&&o.classList.remove('hl');} const n=stnEl(sid);n&&n.classList.add('hl');hovered=sid;}
  }else{tip.style.display='none';if(hovered){const o=stnEl(hovered);o&&o.classList.remove('hl');hovered=null;}}});
wrap.addEventListener('mouseleave',()=>{tip.style.display='none';if(hovered){const o=stnEl(hovered);o&&o.classList.remove('hl');hovered=null;}});
svg.addEventListener('click',e=>{const t=e.target;if(t.classList&&t.classList.contains('hit'))openDetail(t.getAttribute('data-sid'));});
function badge(d){
  if(d.tier==='live')return '<span class="badge live">&#9679; live now</span>';
  if(d.tier==='verified')return '<span class="badge verified">&#9678; verified &mdash; ready to wire</span>';
  if(d.tier==='registry')return '<span class="badge registry">&#9675; registry-listed &mdash; confirm repo</span>';
  if(d.tier==='unconfirmed')return '<span class="badge unconfirmed">&#9675; unconfirmed &mdash; verify first</span>';
  return '';
}
function openDetail(sid){const d=DATA[sid];if(!d)return;
  const xchg=d.interchange?'<span class="badge xchg">&#8853; interchange</span>':'';
  const link=d.url?'<a class="open" href="'+d.url+'" target="_blank" rel="noopener">Open '+d.name+' &#8599;</a>':'';
  pdet.innerHTML='<span class="back" onclick="showDefault()">&#8592; all lines</span>'+
    '<div class="d-bar" style="background:'+d.color+'"></div>'+
    '<h2>'+d.name+'</h2>'+
    '<span class="badge" style="border-color:'+d.color+';color:'+d.color+'">'+d.linename+'</span>'+badge(d)+xchg+
    '<p class="desc">'+d.desc+'</p>'+
    '<div class="how"><b>How to wire it</b>'+d.how+'</div>'+link;
  pdef.hidden=true;pdet.hidden=false; flyTo(d.x,d.y);
  document.querySelectorAll('.stn').forEach(s=>s.classList.remove('hl','dim'));
  const el=stnEl(sid); el&&el.classList.add('hl');}
function clearSearch(){document.querySelectorAll('.stn').forEach(s=>s.classList.remove('hl','dim'));}
search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();
  if(!q){clearSearch();showDefault();return;}
  const hits=Object.keys(DATA).filter(sid=>{const d=DATA[sid];return (d.name+' '+d.desc+' '+d.linename+' '+d.how).toLowerCase().includes(q);});
  const hs=new Set(hits);
  document.querySelectorAll('.stn').forEach(s=>{const sid=s.getAttribute('data-sid');s.classList.toggle('hl',hs.has(sid));s.classList.toggle('dim',!hs.has(sid));});
  pdef.hidden=false;pdet.hidden=true;
  pdef.innerHTML='<div class="hint">'+hits.length+' match'+(hits.length===1?'':'es')+' for &ldquo;'+q+'&rdquo;</div>'+
    hits.map(sid=>{const d=DATA[sid];return '<div class="res" onclick="openDetail(\''+sid+'\')"><span class="chip" style="background:'+d.color+'"></span><b>'+d.name+'</b> <span class="muted">'+d.linename+'</span></div>';}).join('');
});
function showDefault0(){
  let h='<div class="hint">A metro map of every connector, MCP server &amp; Claude skill that boots your research &mdash; with Claude Code as the central interchange. The four <b>interchange lines</b> are real aggregator MCP servers that span several domains. <b>Scroll</b> to zoom, <b>drag</b> to pan, <b>hover</b> for what a station does, <b>click</b> for how to wire it.</div>';
  h+='<div class="lines-list">';
  h+='<div class="ln" onclick="openDetail(\'claude\')"><span class="sw" style="background:#D97757"></span><b>Claude Code</b> &mdash; central</div>';
  h+='<div class="hdr">Lines</div>';
  h+=ORDER.map(l=>'<div class="ln" onclick="hiLine(\''+l+'\')"><span class="sw" style="background:'+LINES[l].color+'"></span>'+LINES[l].name+'</div>').join('');
  h+='<div class="hdr">Interchange lines &mdash; multi-domain MCP servers</div>';
  h+=Object.keys(XLINES).map(x=>'<div class="ln" onclick="hiX(\''+x+'\')"><span class="sw x" style="background:'+XLINES[x].color+'"></span>'+XLINES[x].name+'</div>').join('');
  h+='<div class="ln" onclick="openDetail(\'codex\')"><span class="sw" style="background:#10a37f"></span><b>Codex &middot; GPT-5.5</b> &mdash; second engine</div>';
  h+='</div>';
  pdef.innerHTML=h;
}
function hiLine(l){document.querySelectorAll('.stn').forEach(s=>{const d=DATA[s.getAttribute('data-sid')];const on=d&&d.line===l;s.classList.toggle('hl',on);s.classList.toggle('dim',!on);});
  const first=Object.keys(DATA).find(sid=>DATA[sid].line===l&&DATA[sid].x!=null); if(first)flyTo(DATA[first].x,DATA[first].y,1500);}
const XSTOPS=__XSTOPS__;
function hiX(x){const set=new Set(XSTOPS[x]||[]);document.querySelectorAll('.stn').forEach(s=>{const sid=s.getAttribute('data-sid');s.classList.toggle('hl',set.has(sid));s.classList.toggle('dim',!set.has(sid));});
  const arr=XSTOPS[x]||[];if(arr.length){const d=DATA[arr[0]];flyTo(d.x,d.y,1700);}}
function showDefault(){pdet.hidden=true;pdef.hidden=false;clearSearch();showDefault0();}
showDefault0(); setVB();
</script></body></html>"""

# stations that each interchange line touches (for the console highlight)
XSTOPS = {
    "biomcp": ["biomcp","depmap","cbioportal","clinvar","pubmed","ctgmcp"],
    "otx": ["opentargets","cbioportalmcp","decision"],
    "discovery": ["marketplace","biocontextai","biocontextmeta","nar"],
}

def build_html(svg_str, data):
    lines = {lid: {"name": LINES[lid]["name"], "color": LINES[lid]["color"]} for lid in LINES}
    xlines = {xid: {"name": XLINES[xid]["name"], "color": XLINES[xid]["color"]} for xid in XLINES}
    order = ["lit","gen","comp","stat","clin","viz","write","ops","legal"]
    return (CONSOLE_TEMPLATE
            .replace("__SVG__", svg_str)
            .replace("__DATA__", json.dumps(data))
            .replace("__LINES__", json.dumps(lines))
            .replace("__XLINES__", json.dumps(xlines))
            .replace("__XSTOPS__", json.dumps(XSTOPS))
            .replace("__ORDER__", json.dumps(order))
            .replace("__W__", str(W)).replace("__H__", str(H)))

if __name__ == "__main__":
    # sanity: every station has coordinates (all drawn)
    missing = [sid for sid in STATIONS if sid not in COORD]
    if missing:
        raise SystemExit(f"stations without coords (not drawn): {missing}")
    svg = render()
    with open("master.svg", "w") as f:
        f.write(svg)
    # per-line focus variants (grey the rest, spotlight one) — slide-deck assets
    import os
    os.makedirs("exports/focus", exist_ok=True)
    for fid in list(LINES) + list(XLINES):
        with open(f"exports/focus/{fid}.svg", "w") as f:
            f.write(render(focus=fid))
    data = station_data()
    with open("stations.json", "w") as f:
        json.dump(data, f, indent=2)
    html = build_html(svg, data)
    with open("index.html", "w") as f:
        f.write(html)
    drawn = sum(1 for s in data.values() if s["kind"] in ("stop","terminus","hub"))
    print(f"wrote master.svg ({len(svg)} B) · index.html ({len(html)} B) · "
          f"{len(data)} catalogue entries, {drawn} drawn stops, "
          f"{len(XLINES)} interchange lines")

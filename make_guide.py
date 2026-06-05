#!/usr/bin/env python3
"""
Station & Connection Guide generator
=====================================
Joins the live map data (generate_map.py -> STATIONS, LINES, XLINES, INTERCHANGE,
XSTOPS) with two hand-curated axes the map doesn't carry:

  INVOKE   — how Claude actually reaches the station (automatic / skill / install)
  RUNS_ON  — the machine it runs best on (laptop / workstation / HPC)

Emits STATIONS_GUIDE.md. Re-run after editing generate_map.py to keep them in sync:
    python3 make_guide.py

To also rebuild the styled HTML + print-ready PDF (needs pandoc + Chrome; CSS lives at
exports/_scratch/guide_style.html):
    pandoc STATIONS_GUIDE.md -s -H exports/_scratch/guide_style.html -o STATIONS_GUIDE.html
    # then strip pandoc's title block (the .md already has its own H1) and print:
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
      --no-pdf-header-footer --print-to-pdf=STATIONS_GUIDE.pdf "file://$PWD/STATIONS_GUIDE.html"
"""

import generate_map as g   # safe: module-level builds routes but writes nothing

# ----------------------------------------------------------------- line presentation
LINE_EMOJI = {"lit":"🔴","gen":"🟢","comp":"⚫","stat":"🔵",
              "clin":"🟣","viz":"🟡","write":"🟤","ops":"⚪"}
ORDER = ["lit","gen","comp","stat","clin","viz","write","ops"]

# ----------------------------------------------------------------- invocation axis
# Canonical labels (explained in the legend the doc prints):
#   Auto·MCP    wired MCP tool, Claude calls it directly (schema auto-loads on 1st use)
#   Auto·web    public API, reached via the in-browser tool / curl — no install
#   Auto·Bash   Claude runs it as local code/CLI in the shell
#   Skill       Claude loads a skill (auto-triggers on the task, or on request)
#   Install→MCP add the server to your MCP config once, then it is Auto·MCP
#   Install→Skill  /plugin install, then it loads like any skill
#   Built-in    native Claude Code capability, no setup
#   Manual      you run the final step yourself
#   Discovery   a place to find/verify other servers (browse), not a tool you call
INVOKE = {
    # lit
    "pubmed":"Auto·MCP","consensus":"Auto·MCP","deepresearch":"Skill","litreview":"Skill",
    "researchlookup":"Skill","europepmc":"Auto·web","biorxiv":"Auto·web","medrxiv":"Auto·web",
    "semscholar":"Auto·web","wiley":"Install→MCP",
    # gen
    "synapse":"Auto·MCP","geosra":"Auto·web","ensembldb":"Auto·web","ucsc":"Auto·web",
    "gdc":"Auto·web","clinvar":"Auto·web","cbioportal":"Auto·web","depmap":"Auto·web",
    "cellxgene":"Auto·Bash","cbioportalmcp":"Install→MCP","opentargets":"Install→MCP","ena":"Install→MCP",
    # comp
    "python":"Auto·Bash","jupyter":"Install→Bash","bioconductor":"Auto·Bash","nextflow":"Install→Bash",
    "galaxy":"Auto·web","snakemake":"Install→Bash","cfdna":"Auto·Bash","chatspatial":"Install→MCP",
    "scmcp":"Install→MCP","scqc":"Install→Skill","nfcoreskill":"Install→Skill","scvitools":"Install→Skill",
    # stat
    "statsmodels":"Auto·Bash","survival":"Auto·Bash","reporting":"Skill","peerreview":"Skill",
    "critthink":"Skill","bayes":"Install→Bash","power":"Auto·Bash","ctgmcp":"Install→MCP",
    # clin
    "clinreports":"Skill","decision":"Skill","treatment":"Skill","cltrials":"Auto·web",
    "euctr":"Auto·web","fdaema":"Auto·web","whoictrp":"Auto·web",
    # viz
    "biorender":"Auto·MCP","mermaid":"Auto·MCP","figma":"Auto·MCP","schematics":"Skill",
    "infographics":"Skill","imagegen":"Skill","gptimage":"Manual",
    # write (all skills)
    "sciwriting":"Skill","citation":"Skill","venue":"Skill","office":"Skill","markitdown":"Skill",
    "humanizer":"Skill","slides":"Skill","grants":"Skill","paper2web":"Skill","posters":"Skill",
    # ops
    "drive":"Auto·MCP","gmail":"Auto·MCP","calendar":"Auto·MCP","slack":"Auto·MCP",
    "workflows":"Built-in","schedule":"Skill","codex":"Auto·Bash","marketplace":"Install (channel)",
    "biocontextai":"Discovery","biocontextmeta":"Install→MCP","nar":"Discovery","biomcp":"Install→MCP",
}

# ----------------------------------------------------------------- runs-best-on axis
# 💻 any laptop (cloud connector / remote MCP / public API / skill — work happens off-box)
# 🖥️ workstation (your envs, auth, data; light-to-medium local compute)
# 🗄️ HPC (heavy pipelines / big data / GPU / many cores)
RUNS_ON = {
    # lit — all cloud/skill
    "pubmed":"💻","consensus":"💻","deepresearch":"💻","litreview":"💻","researchlookup":"💻",
    "europepmc":"💻","biorxiv":"💻","medrxiv":"💻","semscholar":"💻","wiley":"💻",
    # gen — APIs are laptop; bulk data has gravity → HPC
    "synapse":"💻 query · 🗄️ bulk","geosra":"💻 meta · 🗄️ raw reads","ensembldb":"💻","ucsc":"💻",
    "gdc":"💻 · 🗄️ bulk files","clinvar":"💻","cbioportal":"💻","depmap":"💻",
    "cellxgene":"🖥️ → 🗄️","cbioportalmcp":"💻","opentargets":"💻 (remote)","ena":"💻 query · 🗄️ pulls",
    # comp — the heavy half of the map
    "python":"🖥️ → 🗄️","jupyter":"🖥️","bioconductor":"🖥️ → 🗄️","nextflow":"🗄️ HPC (🖥️ dev)",
    "galaxy":"💻 public · 🗄️ local","snakemake":"🗄️ HPC (🖥️ dev)","cfdna":"🗄️ HPC","chatspatial":"🖥️ → 🗄️",
    "scmcp":"🖥️ → 🗄️","scqc":"🖥️","nfcoreskill":"🖥️ author · 🗄️ run","scvitools":"🗄️ GPU",
    # stat
    "statsmodels":"💻 · 🖥️","survival":"💻 · 🖥️","reporting":"💻","peerreview":"💻","critthink":"💻",
    "bayes":"🖥️ → 🗄️","power":"💻","ctgmcp":"💻",
    # clin — skills + registries
    "clinreports":"💻","decision":"💻","treatment":"💻","cltrials":"💻","euctr":"💻",
    "fdaema":"💻","whoictrp":"💻",
    # viz — image gen is server-side
    "biorender":"💻","mermaid":"💻","figma":"💻","schematics":"💻","infographics":"💻",
    "imagegen":"💻","gptimage":"💻",
    # write — all skills (local compile is light)
    "sciwriting":"💻","citation":"💻","venue":"💻","office":"💻","markitdown":"💻",
    "humanizer":"💻","slides":"💻","grants":"💻","paper2web":"💻 (video heavier)","posters":"💻 (local LaTeX)",
    # ops
    "drive":"💻","gmail":"💻","calendar":"💻","slack":"💻","workflows":"💻 (more tokens at scale)",
    "schedule":"💻 (cloud-run)","codex":"🖥️ (codex CLI)","marketplace":"💻","biocontextai":"💻",
    "biocontextmeta":"💻","nar":"💻","biomcp":"💻 (wraps remote APIs)",
}

# ----------------------------------------------------------------- cost axis
# Free·OSS = open-source software/MCP · Free·public = public DB/API ·
# Free·skill = Claude skill (runs on your Claude plan) · Freemium = free tier + paid ·
# Paid/lic. = needs a subscription or institutional licence.
COST = {
    # lit
    "pubmed":"Free·public","consensus":"Freemium","deepresearch":"Free·skill","litreview":"Free·skill",
    "researchlookup":"Free·skill (API backend may bill)","europepmc":"Free·public","biorxiv":"Free·public",
    "medrxiv":"Free·public","semscholar":"Free·public","wiley":"Paid/lic. (Wiley institutional)",
    # gen
    "synapse":"Free·public (access-gated)","geosra":"Free·public","ensembldb":"Free·public","ucsc":"Free·public",
    "gdc":"Free·public","clinvar":"Free·public","cbioportal":"Free·public",
    "depmap":"Free·public (OncoKB: free academic / paid commercial)","cellxgene":"Free·public",
    "cbioportalmcp":"Free·OSS","opentargets":"Free·OSS","ena":"Free·OSS",
    # comp
    "python":"Free·OSS","jupyter":"Free·OSS","bioconductor":"Free·OSS","nextflow":"Free·OSS",
    "galaxy":"Free·OSS","snakemake":"Free·OSS","cfdna":"Free·OSS","chatspatial":"Free·OSS",
    "scmcp":"Free·OSS","scqc":"Free·OSS","nfcoreskill":"Free·OSS","scvitools":"Free·OSS",
    # stat
    "statsmodels":"Free·OSS","survival":"Free·OSS","reporting":"Free·skill","peerreview":"Free·skill",
    "critthink":"Free·skill","bayes":"Free·OSS","power":"Free·OSS","ctgmcp":"Free·OSS",
    # clin
    "clinreports":"Free·skill","decision":"Free·skill","treatment":"Free·skill","cltrials":"Free·public",
    "euctr":"Free·public","fdaema":"Free·public","whoictrp":"Free·public",
    # viz
    "biorender":"Freemium (pub export paid)","mermaid":"Free·OSS","figma":"Freemium",
    "schematics":"Free·skill (image API may bill)","infographics":"Free·skill (image API may bill)",
    "imagegen":"Free·skill (FLUX/Gemini bills)","gptimage":"Paid/lic. (OpenAI / ChatGPT)",
    # write
    "sciwriting":"Free·skill","citation":"Free·skill","venue":"Free·skill","office":"Free·skill",
    "markitdown":"Free·skill","humanizer":"Free·skill","slides":"Free·skill","grants":"Free·skill",
    "paper2web":"Free·skill (video may bill)","posters":"Free·skill",
    # ops
    "drive":"Freemium","gmail":"Freemium","calendar":"Freemium","slack":"Freemium",
    "workflows":"Free·built-in (uses tokens)","schedule":"Free·skill","codex":"Paid/lic. (ChatGPT/OpenAI)",
    "marketplace":"Free (some servers it ships are paid)","biocontextai":"Free·OSS","biocontextmeta":"Free·OSS",
    "nar":"Free·public","biomcp":"Free·OSS",
}

# ----------------------------------------------------------------- provenance axis ("real or inferred?")
# Seen·session = I directly observe it in my tools/skills right now (zero fabrication risk) ·
# Known·DB = well-established public resource (general knowledge) ·
# Known·SW = well-established open-source software (install state was claimed in a prior session) ·
# Web-verified = I fetched its repo/endpoint on 2026-06-04 and confirmed it exists (licence noted) ·
# Configured = set up per CLAUDE.md, not exercised this session.
PROVENANCE = {
    # lit
    "pubmed":"Seen·session","consensus":"Seen·session","deepresearch":"Seen·session","litreview":"Seen·session",
    "researchlookup":"Seen·session","europepmc":"Known·DB","biorxiv":"Known·DB","medrxiv":"Known·DB",
    "semscholar":"Known·DB","wiley":"Web-verified ✓ (in marketplace)",
    # gen
    "synapse":"Seen·session","geosra":"Known·DB","ensembldb":"Known·DB","ucsc":"Known·DB","gdc":"Known·DB",
    "clinvar":"Known·DB","cbioportal":"Known·DB","depmap":"Known·DB","cellxgene":"Known·DB",
    "cbioportalmcp":"Web-verified ✓ MIT","opentargets":"Web-verified ✓ official, Apache-2.0","ena":"Web-verified ✓ Apache-2.0",
    # comp
    "python":"Known·SW","jupyter":"Known·SW","bioconductor":"Known·SW","nextflow":"Known·SW","galaxy":"Known·SW",
    "snakemake":"Known·SW","cfdna":"Known·SW","chatspatial":"Web-verified ✓ MIT","scmcp":"Web-verified ✓ BSD-3",
    "scqc":"Web-verified ✓ (in marketplace)","nfcoreskill":"Web-verified ✓ (in marketplace)","scvitools":"Web-verified ✓ (in marketplace)",
    # stat
    "statsmodels":"Known·SW","survival":"Known·SW","reporting":"Seen·session","peerreview":"Seen·session",
    "critthink":"Seen·session","bayes":"Known·SW","power":"Known·SW","ctgmcp":"Web-verified ✓ Apache-2.0",
    # clin
    "clinreports":"Seen·session","decision":"Seen·session","treatment":"Seen·session","cltrials":"Known·DB",
    "euctr":"Known·DB","fdaema":"Known·DB","whoictrp":"Known·DB",
    # viz
    "biorender":"Seen·session","mermaid":"Seen·session","figma":"Seen·session","schematics":"Seen·session",
    "infographics":"Seen·session","imagegen":"Seen·session","gptimage":"Known (OpenAI)",
    # write
    "sciwriting":"Seen·session","citation":"Seen·session","venue":"Seen·session","office":"Seen·session",
    "markitdown":"Seen·session","humanizer":"Seen·session","slides":"Seen·session","grants":"Seen·session",
    "paper2web":"Seen·session","posters":"Seen·session",
    # ops
    "drive":"Seen·session","gmail":"Seen·session","calendar":"Seen·session","slack":"Seen·session",
    "workflows":"Seen·session","schedule":"Seen·session","codex":"Configured (CLAUDE.md)",
    "marketplace":"Web-verified ✓ (412★)","biocontextai":"Web-verified ✓ repo","biocontextmeta":"Web-verified ✓ (biocontext-ai)",
    "nar":"Known·DB","biomcp":"Web-verified ✓ MIT",
}

# wire-these-first shortlist (verified, highest leverage, not yet wired)
WIRE_FIRST = ["biomcp","opentargets","cbioportalmcp","chatspatial","scmcp","ctgmcp","ena","marketplace"]

# ----------------------------------------------------------------- emit
def md_escape(s):
    return s.replace("|", "\\|")

def tier_badge(t):
    return {"live":"●","verified":"◉","registry":"○","unconfirmed":"○"}.get(t,"")

def line_rows(line):
    sids = [s for s in g.STATIONS if g.STATIONS[s]["line"] == line]
    sids.sort(key=lambda s: (g.STATIONS[s]["tier"] != "live",))   # live first, else stable
    out = []
    for sid in sids:
        st = g.STATIONS[sid]
        chip = tier_badge(st["tier"]) + ("⊕" if sid in g.INTERCHANGE else "")
        name = md_escape(st["name"])
        cell = f"**{md_escape(st['desc'])}**<br>↳ {md_escape(st['how'])}"
        out.append(f"| {chip} **{name}** | {cell} | {md_escape(COST.get(sid,'—'))} | "
                   f"{md_escape(PROVENANCE.get(sid,'—'))} | `{INVOKE.get(sid,'—')}` | {RUNS_ON.get(sid,'—')} |")
    return "\n".join(out)

def build():
    miss = {k: [s for s in g.STATIONS if s not in d]
            for k, d in (("INVOKE",INVOKE),("RUNS_ON",RUNS_ON),("COST",COST),("PROVENANCE",PROVENANCE))}
    if any(miss.values()):
        raise SystemExit(f"unclassified — {dict((k,v) for k,v in miss.items() if v)}")

    L = []
    L.append("# The Zoppoli Research Underground — Station & Connection Guide\n")
    L.append("> How to ride each line: what every station does, **how to connect it**, "
             "**which functions to expect**, whether Claude reaches it **automatically or via a "
             "skill load**, and the **machine it runs best on**.\n")
    L.append(f"> Generated from the live map data — **{len(g.STATIONS)} stations** "
             "(the super-confident set: ● live + ◉ verified). Registry-listed servers stay in "
             "`CATALOGUE.md` until their repo is confirmed. Re-run `python3 make_guide.py` after "
             "editing the map.\n")
    L.append("> **On the `Real?` column (is it actually in there, or did I make it up):** the live "
             "MCPs and skills are ones I *directly observe* in this session; the public databases "
             "are well-known resources; and every install-first MCP repo / endpoint was **fetched and "
             "confirmed to exist on 2026-06-04** (licence noted). Nothing here is an unverified guess — "
             "the registry-listed servers that *were* only inferred are excluded (they live in `CATALOGUE.md`).\n")

    L.append("\n## How to read the columns\n")
    L.append("**Status:** ● live (wired now) · ◉ verified (real, ready to wire) · ⊕ interchange "
             "(a connecting line stops here).\n")
    L.append("\n**Invocation** — how Claude actually reaches it:\n")
    L.append("| Label | Meaning |\n|---|---|")
    L.append("| `Auto·MCP` | Wired MCP tool — Claude calls it directly; the tool schema auto-loads on first use. **No action from you.** |")
    L.append("| `Auto·web` | Public API/registry — Claude reaches it through the in-browser tool or `curl`. **No install.** |")
    L.append("| `Auto·Bash` | Claude runs it as local code / CLI in the shell. |")
    L.append("| `Skill` | Claude loads a skill (auto-triggers on the matching task, or on request). |")
    L.append("| `Install→MCP` | Add the server to your MCP config **once**; thereafter it behaves as `Auto·MCP`. |")
    L.append("| `Install→Bash` | Install the tool once (`pip`/`conda`), then `Auto·Bash`. |")
    L.append("| `Install→Skill` | `/plugin install …`, then it loads like any skill. |")
    L.append("| `Install (channel)` | An install *source* (the marketplace), not a tool you call. |")
    L.append("| `Built-in` | Native Claude Code capability — no setup. |")
    L.append("| `Manual` | You run the final step yourself (e.g. paste a prompt into ChatGPT). |")
    L.append("| `Discovery` | A place to **find/verify** other servers (browse), not a tool you call. |")
    L.append("\n**Runs best on:** 💻 any laptop (cloud / remote MCP / API / skill — the work happens "
             "off-box) · 🖥️ your workstation (local envs, auth tokens, your data, light–medium compute) "
             "· 🗄️ HPC (heavy pipelines, big data, GPU). `A → B` = starts on A, scales to B.\n")
    L.append("\n**Cost:** `Free·OSS` open-source software/MCP · `Free·public` public DB/API · "
             "`Free·skill` a Claude skill (no licence; it runs on your Claude plan) · `Freemium` free "
             "tier + paid upgrades · `Paid/lic.` needs a subscription or institutional licence. "
             "Parentheticals flag where the answer shifts (e.g. image-gen skills bill per image; "
             "OncoKB is free for academics, licensed for industry).\n")
    L.append("\n**Real?** — provenance, the honest part: `Seen·session` I directly observe it in my "
             "tools/skills right now (cannot be fabricated) · `Known·DB` a well-established public "
             "database · `Known·SW` well-established open-source software (the *installed-on-your-box* "
             "claim is from a prior session) · `Web-verified ✓` I fetched the repo/endpoint on "
             "2026-06-04 and confirmed it exists, licence noted · `Configured` set up per CLAUDE.md, "
             "not exercised this turn.\n")

    # wire-first
    L.append("\n## Wire these first (highest-leverage, not yet wired)\n")
    for i, sid in enumerate(WIRE_FIRST, 1):
        st = g.STATIONS[sid]
        L.append(f"{i}. **{st['name']}** — {st['desc']} _({st['how']})_")
    L.append("")

    # per line
    for line in ORDER:
        L.append(f"\n## {LINE_EMOJI[line]} {g.LINES[line]['name']}\n")
        L.append("| Station | Functions · how to connect | Cost | Real? | Invocation | Runs best on |")
        L.append("|---|---|---|---|---|---|")
        L.append(line_rows(line))

    # interchange lines
    L.append("\n## ⊕ Interchange lines — the multi-domain servers that connect the lines\n")
    L.append("Each is one MCP server that spans several lines; wiring it lights up every station it touches.\n")
    for xid, xl in g.XLINES.items():
        stops = g.XSTOPS.get(xid, [])
        names = " · ".join(g.STATIONS[s]["name"] for s in stops if s in g.STATIONS)
        L.append(f"### {xl['name']}")
        if xid == "discovery":
            L.append("- **Connect:** `/plugin marketplace add anthropics/life-sciences` (marketplace) "
                     "and browse `biocontext.ai/registry` (registry). The install/discovery backbone.")
            L.append("- **Invocation:** `Install (channel)` + `Discovery` · **Runs best on:** 💻 any laptop")
        else:
            anchor = "biomcp" if xid == "biomcp" else ("opentargets" if xid == "otx" else None)
            if anchor and anchor in g.STATIONS:
                L.append(f"- **Connect:** {g.STATIONS[anchor]['how']}")
                L.append(f"- **Functions:** {g.STATIONS[anchor]['desc']}")
                L.append(f"- **Invocation:** `{INVOKE.get(anchor,'—')}` · **Runs best on:** {RUNS_ON.get(anchor,'—')}")
        L.append(f"- **Stops it serves:** {names}\n")

    # hub + terminus
    L.append("\n## The hub & the second engine\n")
    L.append("- **🟧 Claude Code (central interchange)** — your workstation. Every line meets here: "
             "Claude routes the work, reasons, writes & runs code, and dispatches the rest. "
             "**Invocation:** this is the station you sit in. **Runs best on:** 🖥️ workstation "
             "(it drives everything else, local + cloud).")
    L.append("- **🟩 Codex · GPT-5.5 (sister terminus)** — the second engine for decorrelated review, "
             "long shell-agent runs and red-teaming. **Connect:** `codex exec --skip-git-repo-check \"…\"` "
             "via Bash, or the `codex-dispatch` skill. **Invocation:** `Auto·Bash` / `Skill`. "
             "**Runs best on:** 🖥️ workstation (where the codex CLI + ChatGPT auth live).")

    # at a glance
    L.append("\n## At a glance — where the work happens\n")
    L.append("- **💻 Any laptop (most of the map):** all literature, clinical & regulatory lines, "
             "every writing/visualization skill, the trial-registry MCPs, and the orchestration "
             "connectors (Drive/Gmail/Calendar/Slack/workflows/schedule). If it's a cloud connector, "
             "a remote MCP, a public API or a skill, the heavy lifting happens off your machine — "
             "you only need Claude Code + internet.")
    L.append("- **🖥️ Workstation:** anything touching your local envs, credentials or data — Synapse "
             "controlled-access pulls, Jupyter, light single-cell (scanpy/Seurat) exploration, the "
             "Codex CLI. Also the natural home for the MCP servers that *execute* analysis locally "
             "(ChatSpatial, SCMCP) when datasets are modest.")
    L.append("- **🗄️ HPC:** the genomics compute spine — Nextflow/nf-core & Snakemake pipelines, the "
             "cfDNA/liquid-biopsy stack (RENOVATE / MIMESIS), large single-cell & spatial atlases, "
             "GPU model training (scvi-tools), and bulk SRA/GDC/ENA data pulls. Develop on the "
             "workstation, run at scale on HPC.")
    L.append("\n---\n*Generated by `make_guide.py` from `generate_map.py`. Edit the map data or the "
             "`INVOKE` / `RUNS_ON` dicts and re-run to refresh.*\n")

    return "\n".join(L)

if __name__ == "__main__":
    doc = build()
    with open("STATIONS_GUIDE.md", "w") as f:
        f.write(doc)
    print(f"wrote STATIONS_GUIDE.md ({len(doc)} B) — {len(g.STATIONS)} stations classified")

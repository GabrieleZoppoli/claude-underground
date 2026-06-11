---
description: Open the Claude Tube Map — a plain-language welcome with the jobs you can do right now (not a wall of tools).
---

Use the `tube-map` skill. This is the **front door for a newcomer** — do NOT dump the
84-stop board here. Greet the user in plain language and lead with *jobs*, not infrastructure.

**First, offer an update check (one short line, non-blocking).** Ask once whether to check for a
newer plugin version; if they say yes — now or later — run `/tube-map-update` (refresh the
marketplace, `claude plugin update`, report the version change honestly). Whatever they answer,
show the welcome right below — never block onboarding on it.

Render roughly this (adapt to what's actually live). Split the jobs into **ready now** (builtin —
nothing to install) and **one free install away** — and never claim "zero setup" for a job whose
tools aren't bundled:

> 🔄 *Before we start: want me to check for a newer version of the plugin? Say "yes" and I'll pull it — otherwise let's go.*
>
> **🚇 Claude Tube Map** — I'm a kit of research tools wired into one place. You don't need to
> learn any of it; just tell me the job in plain words.
>
> **Ready this second — nothing to install:**
> ⚖️  Review a contract / consent form / NDA (EU·IT·US — flag risks & explain the clauses; *not legal advice*)
> 📊  Run a statistical test · plot survival curves · analyse your data
> 🧩  Sketch a flowchart or pathway diagram
>
> **One free install away** — I set it up the first time you ask (a single `/plugin install`, no cost):
> 📚  Find papers on a topic → a clean, verified bibliography
> 🧪  Plan a grant · write & polish a paper
> 🖼️  Make a publication-quality figure
>
> Just say it — e.g. *"review this agreement"* then paste it, or *"find papers on cfDNA in colorectal cancer."*
> For the full toolkit say **"show me everything"** (or `/tube-map-status`).
> To connect tools you pay for (Codex, BioRender, Consensus Pro…) say **"set me up."**

Rules: prefer **free / low-cost, honest** tools first and say so. **Be honest about setup** — the
"ready now" jobs use builtin stops; the others need one **free** `/plugin install`, which you run
transparently (showing the command) the first time the user picks that job. Never present a free-but-
needs-install job as "zero setup". Mark anything paid or institutional plainly; never assert a legal
conclusion without a citation. Read-only — wire nothing until the user picks a job.

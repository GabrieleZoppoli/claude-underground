---
description: Open the Claude Tube Map — a plain-language welcome plus an interactive picker of the jobs you can do (not a wall of tools).
---

Use the `tube-map` skill. This is the **front door for a newcomer** — do NOT dump the
84-stop board here. Greet the user in plain language and lead with *jobs*, not infrastructure.

**First, offer an update check (one short line, non-blocking).** Ask once whether to check for a
newer plugin version; if they say yes — now or later — run `/tube-map-update` (refresh the
marketplace, `claude plugin update`, report the version change honestly). Whatever they answer,
show the welcome right below — never block onboarding on it.

Render roughly this (adapt to what's actually live; render in the user's language). Keep the
honesty split — **ready now** (builtin, nothing to install) vs **one free install away** — and never
claim "zero setup" for a job whose tools aren't bundled:

> 🔄 *Before we start: want me to check for a newer version of the plugin? Say "yes" and I'll pull it — otherwise let's go.*
>
> **🚇 Claude Tube Map** — I'm a kit of research tools wired into one place. Tell me the job in plain
> words, or pick one below. I prefer free, honest tools first.
>
> **Ready now — nothing to install:** ⚖️ review a contract / NDA (*not legal advice*) · 📊 a statistical test, survival curves, omics · 🧩 a flowchart / pathway diagram
> **One free install away:** 📚 papers → bibliography · 🧪 plan a grant · ✍️ write / polish a paper · 🖼️ a figure

Then **present an interactive picker** with the **AskUserQuestion** tool — this is the selectable
menu Claude Code supports, so use it rather than only printing a list. One question, header `Job`,
exactly these **4 options** (the built-in *Other* / free-text always lets them just type a job):

1. **"Review a document"** → run the **paralegal** journey. *Desc:* "Contract / NDA / consent (EU·IT·US): risks + clauses. Ready now, nothing to install. Not legal advice."
2. **"Find papers → bibliography"** → run the **bibliography** journey. *Desc:* "Search & verify references on a topic. One free install the first time."
3. **"Analyse data / stats"** → run **stats-plots** (or **omics** if single-cell / spatial). *Desc:* "A statistical test, survival curves, omics. Ready now — I write & run the code."
4. **"Something else… or just type it"** → ask what they want and route to **grant / figures / scientific-writing / slides / peer-review**, or **"show me everything"** (`/tube-map-status`), or **"set me up"** (`/tube-map-install`). *Desc:* "Grant, figures, write/polish a paper, slides, peer-review… or say it in plain words."

Route the selection to the matching journey, read its playbook, and run it. **Honour free-text** — if
the user types their own job (the *Other* answer, or before the menu even renders), skip the menu and
just do it. Never loop the menu.

Rules: prefer **free / low-cost, honest** tools first and say so. **Be honest about setup** — "ready
now" jobs use builtin stops; the others need one **free** `/plugin install`, run transparently
(showing the command) the first time the user picks that job. Never present a free-but-needs-install
job as "zero setup". Mark anything paid or institutional plainly; never assert a legal conclusion
without a citation. Read-only — wire nothing until the user picks a job.

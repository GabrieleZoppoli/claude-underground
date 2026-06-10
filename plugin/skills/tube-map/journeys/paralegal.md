---
name: paralegal
description: Paralegal-style EU/IT/US document review (non-lawyer, cited).
stops: paralegalrev, gdpr, itlaw, uslaw, office, markitdown
---

# Journey — Paralegal review  ⚖️

**Non-lawyer, cited.** Open and close with the disclaimer from
`${CLAUDE_PLUGIN_ROOT}/skills/tube-map/references/legal/README.md`.

## Run it
0. **Ensure stops (free, one-time install)** — the legal modules (`gdpr`/`itlaw`/`uslaw`/`paralegalrev`) are **builtin**, so the review itself needs **no install**. `markitdown` and `office` are **free** skills that still need one `/plugin install claude-scientific-writer` (show the command, run it) — but only for **file** intake and the **tracked-changes redline**. If the user pasted the text and wants the review inline, proceed without them. **Don't promise a `.docx` redline until `office` is wired.**
1. **Intake** — if given a file, convert it with `markitdown`; if the user pasted the text, use it directly.
2. **Classify** — document type (NDA/CDA · MTA/DTA · DPA · consortium/grant · consent · employment) and jurisdiction (EU / Italy / US).
3. **Load the module** — read the matching `references/legal/{eu,it,us}.md`; pull its checklist + clause library.
4. **Clause-by-clause review** — for each clause: what it says, what to check (per the checklist), risk level, and the **cited** primary-source pointer (verify live via research-lookup if unsure). Flag missing clauses.
5. **Redline** — once `office` is wired, produce a tracked-changes `.docx` + a plain-language summary; otherwise deliver the redline **inline** (clause → suggested change) and offer the `.docx` after the one-time free install.
6. **Escalate** — anything high-risk or low-confidence → "consult qualified counsel"; never assert a legal conclusion without a citation.
7. **Disclaimer** — restate it: informational paralegal support, not legal advice; Claude is not a lawyer.

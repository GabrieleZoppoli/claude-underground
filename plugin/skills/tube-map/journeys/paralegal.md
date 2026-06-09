---
name: paralegal
description: Paralegal-style EU/IT/US document review (non-lawyer, cited).
stops: paralegalrev, gdpr, itlaw, uslaw, office, markitdown
---

# Journey — Paralegal review  ⚖️

**Non-lawyer, cited.** Open and close with the disclaimer from
`${CLAUDE_PLUGIN_ROOT}/skills/tube-map/references/legal/README.md`.

## Run it
1. **Intake** — convert the document with `markitdown`.
2. **Classify** — document type (NDA/CDA · MTA/DTA · DPA · consortium/grant · consent · employment) and jurisdiction (EU / Italy / US).
3. **Load the module** — read the matching `references/legal/{eu,it,us}.md`; pull its checklist + clause library.
4. **Clause-by-clause review** — for each clause: what it says, what to check (per the checklist), risk level, and the **cited** primary-source pointer (verify live via research-lookup if unsure). Flag missing clauses.
5. **Redline** — produce a tracked-changes version with `office` (docx) + a plain-language summary.
6. **Escalate** — anything high-risk or low-confidence → "consult qualified counsel"; never assert a legal conclusion without a citation.
7. **Disclaimer** — restate it: informational paralegal support, not legal advice; Claude is not a lawyer.

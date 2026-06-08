---
name: paralegal
description: Paralegal-style document review (generic now; EU/IT/US Legal line lands in M3).
stops: office, markitdown
---

# Journey — Paralegal review  ⚖️ (preview)

**Goal:** a careful, **non-lawyer** review of a research document. Full EU / Italian / US coverage arrives with the **Legal line in M3**; for now this does intake + generic clause review.

## Run it
1. **Ensure stops** — `markitdown` (ingest docx/pdf), `office` (tracked-changes output).
2. **Intake & classify** — convert the document; identify its type (NDA/MTA/DPA/consent/agreement) and jurisdiction.
3. **Generic review** — clause-by-clause read: obligations, liability, IP, data/privacy, termination; flag risks and missing clauses.
4. **Output** — tracked-changes redline + a plain-language summary.
5. **Mandatory disclaimer** — *informational paralegal-style support, not legal advice; Claude is not a lawyer; verify with qualified counsel.* Do not assert jurisdiction-specific legal conclusions without a cited source (the M3 Legal line adds the cited grounding).

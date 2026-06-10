---
name: bibliography
description: Publication-ready validated bibliography.
stops: pubmed, consensus, citation
---

# Journey — Bibliography  🔴→🟤

**Goal:** turn a draft, a pile of references, or a topic into a validated, correctly-styled bibliography.

## Run it
1. **Ensure stops (free-first)** — `pubmed` and `citation` are **free** (one `/plugin install`, no cost) — wire them, showing the command. `consensus` is **freemium**: use it only if the user has it, otherwise rely on PubMed + your own verification. If any stop is ⚠ needs-you, say so and proceed with what's available.
2. **Gather** — collect the user's references (or search PubMed/Consensus for the cited claims).
3. **Verify each** — confirm author/year/title/journal and resolve DOIs; flag anything unverifiable rather than inventing it.
4. **Convert & dedupe** — DOI→BibTeX via `citation-management`; merge duplicates.
5. **Style** — format to the target style (Vancouver/APA/Nature) the user names.
6. **Report** — list anything that could not be verified as "needs your check"; never fabricate a citation.

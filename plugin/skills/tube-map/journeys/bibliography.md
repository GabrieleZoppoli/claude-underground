---
name: bibliography
description: Publication-ready validated bibliography.
stops: pubmed, consensus, citation
---

# Journey — Bibliography  🔴→🟤

**Goal:** turn a draft, a pile of references, or a topic into a validated, correctly-styled bibliography.

## Run it
1. **Ensure stops** — wire `pubmed`, `consensus`, `citation` via the tube-map engine; if any is ⚠ needs-you, say so and proceed with what's available.
2. **Gather** — collect the user's references (or search PubMed/Consensus for the cited claims).
3. **Verify each** — confirm author/year/title/journal and resolve DOIs; flag anything unverifiable rather than inventing it.
4. **Convert & dedupe** — DOI→BibTeX via `citation-management`; merge duplicates.
5. **Style** — format to the target style (Vancouver/APA/Nature) the user names.
6. **Report** — list anything that could not be verified as "needs your check"; never fabricate a citation.

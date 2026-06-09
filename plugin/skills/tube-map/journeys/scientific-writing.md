---
name: scientific-writing
description: Write/revise scientific prose; strip AI-tells.
stops: sciwriting, humanizer, venue
---

# Journey — Scientific writing  🟤

**Goal:** publication-standard prose in the author's voice.

## Run it
1. **Ensure stops** — `sciwriting`, `venue` (skills); `humanizer` is the author's personal skill (degrade to a generic AI-tell pass if absent).
2. **Structure** — IMRAD; outline key points per section first, then prose (never bullet dumps).
3. **Draft** — flowing paragraphs; citations on every factual claim; venue rules from `venue-templates`.
4. **De-tell** — run `humanizer` to remove AI-tells and match house style.
5. **Check** — references resolve; reporting-guideline language where relevant.

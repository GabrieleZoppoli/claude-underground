# Claude Tube Map — M3 (Legal/Paralegal line + poster redraw) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`).

**Goal:** Add the ⚖️ Legal/Paralegal line (EU · Italian · US) — drawn on the Harry-Beck poster AND wired into the plugin — plus the full paralegal journey, all on cited primary sources with a hard non-lawyer disclaimer.

**Architecture:** Legal stops are defined ONCE in `generate_map.py`'s `STATIONS`/`LINES` (single source) → flow to `stations.json` → `catalogue.json`. A new `legal` line is routed into open canvas (candidate: an off-cardinal spoke near Clinical) and rendered; the user approves the visual. `wiring.json` marks the stops `builtin` (reference modules, nothing to install). Cited reference playbooks (EU/IT/US checklists + clause libraries) live under `plugin/skills/tube-map/references/legal/`. The paralegal journey upgrades from M2 stub to full, using those references.

**Tech Stack:** Python (generate_map.py renderer), `rsvg-convert` for PNG/PDF, pytest, Markdown.

**Highest risk = legal accuracy.** Reference modules are FRAMEWORKS + checklists + pointers to primary sources (EUR-Lex CELEX, Normattiva, eCFR), never asserted legal text from memory. Every load-bearing legal claim is verified at runtime via research-lookup/deep-research and cited. Mandatory disclaimer everywhere.

---

## File structure (✚ new, ⟳ changed)

| File | New/Mod | Responsibility |
|---|---|---|
| `generate_map.py` | ⟳ | Add `legal` to `LINES`; add 7 legal stations to `STATIONS`; route + render the line. |
| `stations.json` | ⟳ generated | Now includes the 7 legal stops. |
| `master.svg`, `exports/*` | ⟳ generated | Poster with the ⚖️ line. |
| `wiring.json` | ⟳ | 7 legal stops → `{"wire":"builtin"}`. |
| `plugin/data/catalogue.json` | ⟳ generated | Includes the legal line. |
| `plugin/skills/tube-map/references/legal/{eu,it,us}.md` | ✚ | Cited reference checklists + clause libraries per jurisdiction. |
| `plugin/skills/tube-map/references/legal/README.md` | ✚ | Index + the hard disclaimer + no-uncited-claim rule. |
| `plugin/skills/tube-map/journeys/paralegal.md` | ⟳ | Stub → full paralegal journey. |
| `journeys.json` | ⟳ | paralegal stops → legal stops + office + markitdown. |
| `tests/test_legal.py` | ✚ | Legal stops present + wired; references exist; disclaimer present. |

---

### Task 1: Legal line on the map (geometry — render & SHOW for approval)

**Files:** modify `generate_map.py`; regenerate `stations.json`, `master.svg`, `exports/`.

- [ ] **Step 1 — add the line** to `LINES` (after `ops`):
```python
    "legal": {"name": "Legal & Paralegal",          "color": "#0E7C7B"},  # deep teal (candidate)
```

- [ ] **Step 2 — add 7 legal stations** to `STATIONS` (tier `live`; `S(...)` signature is `name, line, tier, desc, how, url`):
```python
  # ====================================================== Legal ⚖️
  "gdpr":        S("GDPR & data protection","legal","live","EU GDPR (2016/679): DPAs, transfers, Art. 89 research exemptions.","Reference module — cited to EUR-Lex; verify before relying.","https://eur-lex.europa.eu/eli/reg/2016/679/oj"),
  "eugrants":    S("EU grant & consortium law","legal","live","Horizon Europe Model Grant Agreement + Consortium Agreement (DESCA), IP/access rights.","Reference module — cited to EU Funding & Tenders / DESCA.","https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/agr-contr/general-mga_horizon-euratom_en.pdf"),
  "itlaw":       S("Italian research law","legal","live","Codice Privacy (196/2003) + Garante; procurement D.lgs 36/2023 (RUP); consenso informato & comitati etici.","Reference module — cited to Normattiva / Gazzetta Ufficiale.","https://www.normattiva.it"),
  "ushipaa":     S("US HIPAA & privacy","legal","live","HIPAA Privacy/Security Rules + Business Associate Agreements.","Reference module — cited to eCFR (45 CFR 160/164).","https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C"),
  "ushumansubj": S("US human-subjects (Common Rule)","legal","live","45 CFR 46 Common Rule, IRB review, informed consent.","Reference module — cited to eCFR (45 CFR 46).","https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46"),
  "usip":        S("US IP & research agreements","legal","live","Bayh-Dole (35 USC 200-212), MTA/CDA/NDA, invention assignment.","Reference module — cited to the U.S. Code.","https://uscode.house.gov"),
  "paralegalrev":S("paralegal-review","legal","live","Clause-by-clause review + redline + checklist conformance (non-lawyer, cited).","Skill: the tube-map paralegal journey."),
```

- [ ] **Step 3 — route the line.** Add a candidate off-cardinal direction + trunk in `# ----- route builders`. Legal is Clinical/Regulatory-adjacent, so route it from the SE/S open sector. Add to `D`:
```python
    "SSE": (0.62, 1.42),
```
and after the Orchestration block:
```python
# ----- Legal (SSE — regulatory neighbour of Clinical) --------------------------
trunk("legal", "SSE", ["paralegalrev","gdpr","itlaw","ushipaa"], exit=2.0)
branch("legal", "gdpr", "E", ["eugrants"])
branch("legal", "ushipaa", "E", ["ushumansubj","usip"])
```

- [ ] **Step 4 — render**
```bash
python3 generate_map.py
rsvg-convert -w 3840 -o exports/research_underground_4k.png master.svg
rsvg-convert -f pdf -o exports/research_underground_poster.pdf master.svg
```
Confirm: `python3 -c "import json;d=json.load(open('stations.json'));print(sum(1 for s in d.values() if s['line']=='legal'),'legal stops')"` → `7 legal stops`.

- [ ] **Step 5 — SHOW the user** the rendered PNG (`exports/research_underground_4k.png`) for visual approval of placement + the teal colour. **Do not commit until the user approves the look.** Iterate Step 3 (direction vector / branches) and the colour per feedback.

- [ ] **Step 6 — commit** (after approval)
```bash
git add generate_map.py stations.json master.svg exports/
git commit -m "feat(m3): draw the Legal & Paralegal line on the poster"
```

---

### Task 2: Wire the legal stops + plugin integration (TDD)

**Files:** modify `wiring.json`; create `tests/test_legal.py`; regenerate catalogue.

- [ ] **Step 1 — failing test** `tests/test_legal.py`:
```python
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _j(p): 
    with open(os.path.join(ROOT, p)) as f: return json.load(f)

LEGAL = {"gdpr","eugrants","itlaw","ushipaa","ushumansubj","usip","paralegalrev"}

def test_legal_stops_in_stations_and_wired():
    stations, wiring = _j("stations.json"), _j("wiring.json")
    for s in LEGAL:
        assert s in stations and stations[s]["line"] == "legal", f"{s} missing/not legal"
        assert s in wiring and wiring[s]["wire"] == "builtin", f"{s} not wired builtin"

def test_legal_line_in_catalogue():
    cat = _j("plugin/data/catalogue.json")
    legal = [l for l in cat["lines"] if l["key"] == "legal"]
    assert legal and len(legal[0]["stations"]) == 7

def test_legal_references_and_disclaimer_present():
    base = os.path.join(ROOT, "plugin/skills/tube-map/references/legal")
    for f in ("README.md","eu.md","it.md","us.md"):
        assert os.path.exists(os.path.join(base, f)), f"missing {f}"
    readme = open(os.path.join(base,"README.md")).read().lower()
    assert "not legal advice" in readme and "not a lawyer" in readme
```

- [ ] **Step 2 — run, expect fail** (legal stops not yet in wiring): `python3 -m pytest tests/test_legal.py -q`

- [ ] **Step 3 — add 7 lines to `wiring.json`** (anywhere in the object):
```json
  "gdpr": {"wire": "builtin"},
  "eugrants": {"wire": "builtin"},
  "itlaw": {"wire": "builtin"},
  "ushipaa": {"wire": "builtin"},
  "ushumansubj": {"wire": "builtin"},
  "usip": {"wire": "builtin"},
  "paralegalrev": {"wire": "builtin"},
```

- [ ] **Step 4 — regenerate + validate**
```bash
python3 build_plugin.py            # expect 86 stations, 10 lines
python3 tools/check_plugin.py      # expect ok (86 stations...)
```
(Tests in Step 1 for references will still fail until Task 3 creates them — that's expected.)

- [ ] **Step 5 — commit**
```bash
git add wiring.json tests/test_legal.py plugin/data/catalogue.json
git commit -m "feat(m3): wire the 7 legal stops + plugin integration tests"
```

---

### Task 3: Legal reference modules (EU / IT / US) — cited, disclaimered

**Files:** create `plugin/skills/tube-map/references/legal/{README,eu,it,us}.md`

Content rules for ALL four files: frameworks + checklists + clause libraries + primary-source pointers (with the citation), NEVER asserted legal conclusions; every file carries or links the disclaimer; instruct runtime verification via research-lookup/deep-research.

- [ ] **Step 1 — `references/legal/README.md`** (index + hard rules):
```
# Legal references — read me first

**Disclaimer (always show to the user):** This is informational, paralegal-style support —
**not legal advice. Claude is not a lawyer.** Verify every point with qualified counsel in the
relevant jurisdiction before relying on it.

**Hard rules for any legal work here:**
- Never state a legal conclusion without citing a primary source (EUR-Lex CELEX, Normattiva,
  eCFR / U.S. Code). If you cannot cite it, say so and flag it for the user's lawyer.
- Never invent article numbers, regulation IDs, or case law. Verify live via research-lookup / deep-research.
- Flag uncertainty explicitly; prefer "this likely concerns X — confirm with counsel" over assertion.

Modules: `eu.md` (GDPR · Horizon/DESCA), `it.md` (Garante · procurement · ethics), `us.md` (HIPAA · Common Rule · IP).
```

- [ ] **Step 2 — `references/legal/eu.md`** — sections: GDPR (key articles to check: lawful basis, Art. 9 special category, Art. 89 research, DPA Art. 28, transfers Ch. V — each with EUR-Lex pointer); Horizon Europe MGA + DESCA (IP/background/foreground, access rights, dissemination). Each section = a **checklist of what to verify** + the primary-source link, plus a short **clause library** (clause name → what to look for). No asserted conclusions.

- [ ] **Step 3 — `references/legal/it.md`** — Codice Privacy (D.lgs 196/2003 + 101/2018) & Garante; public procurement (D.lgs 36/2023, RUP, convenzioni conto terzi); consenso informato & comitati etici / AIFA. Same checklist+pointer+clause-library shape; sources to Normattiva / Gazzetta Ufficiale.

- [ ] **Step 4 — `references/legal/us.md`** — HIPAA (45 CFR 160/164, BAA required terms); Common Rule (45 CFR 46, IRB, consent elements); IP (Bayh-Dole 35 USC 200-212; MTA/CDA/NDA clause library). Sources to eCFR / U.S. Code.

(Full prose for each file is authored in this task by the implementer following the shape above; keep each file focused — a checklist and clause library, not a treatise.)

- [ ] **Step 5 — commit**
```bash
git add plugin/skills/tube-map/references/legal/
git commit -m "feat(m3): EU/IT/US legal reference modules (cited, disclaimered)"
```

---

### Task 4: Full paralegal journey + finalize

**Files:** modify `journeys.json`, `plugin/skills/tube-map/journeys/paralegal.md`

- [ ] **Step 1 — `journeys.json`: upgrade paralegal**
```json
  "paralegal": {
    "description": "Paralegal-style review of a research document (EU/IT/US): classify, clause-by-clause review against jurisdiction checklists, risk flags, tracked-changes redline, cited grounding.",
    "stops": ["paralegalrev", "gdpr", "itlaw", "ushipaa", "office", "markitdown"],
    "playbook": "journeys/paralegal.md"
  }
```

- [ ] **Step 2 — rewrite `journeys/paralegal.md`** to the full journey:
```
---
name: paralegal
description: Paralegal-style EU/IT/US document review (non-lawyer, cited).
stops: paralegalrev, gdpr, itlaw, ushipaa, office, markitdown
---

# Journey — Paralegal review  ⚖️

**Non-lawyer, cited.** Always open and close with the disclaimer from
`${CLAUDE_PLUGIN_ROOT}/skills/tube-map/references/legal/README.md`.

## Run it
1. **Intake** — convert the document with `markitdown`.
2. **Classify** — document type (NDA/CDA · MTA/DTA · DPA · consortium/grant · consent · employment) and jurisdiction (EU / Italy / US).
3. **Load the module** — read the matching `references/legal/{eu,it,us}.md`; pull its checklist + clause library.
4. **Clause-by-clause review** — for each clause: what it says, what to check (per the checklist), risk level, and the **cited** primary-source point (verify live via research-lookup if unsure). Flag missing clauses.
5. **Redline** — produce a tracked-changes version with `office` (docx) + a plain-language summary.
6. **Escalate** — anything high-risk or low-confidence → "consult qualified counsel"; never assert a legal conclusion without a citation.
7. **Disclaimer** — restate it: informational paralegal support, not legal advice; Claude is not a lawyer.
```

- [ ] **Step 3 — regenerate + full validation**
```bash
python3 build_plugin.py
python3 tools/check_plugin.py            # expect ok (86 stations, 10 lines)
python3 -m pytest tests/ -q              # expect all green incl. test_legal
claude plugin validate "$(pwd)/plugin"   # expect ✔
```

- [ ] **Step 4 — README:** add ⚖️ to the line list / journeys; commit
```bash
git add journeys.json plugin/skills/tube-map/journeys/paralegal.md plugin/data/journeys.json README.md
git commit -m "feat(m3): full EU/IT/US paralegal journey"
```

---

## Self-review (plan vs goal)
- ⚖️ line drawn on the poster (rendered + user-approved): Task 1. ✓
- Legal stops single-sourced in generate_map.py → stations.json → catalogue: Tasks 1–2. ✓
- Wired (builtin) + validated + on the board: Task 2. ✓
- EU/IT/US cited reference modules + disclaimer + no-uncited-claim rule: Task 3. ✓
- Full paralegal journey using the modules: Task 4. ✓
- **Honesty:** disclaimer everywhere; frameworks/checklists not asserted law; runtime verification required. ✓
- **Placeholder note:** Task 3's per-file prose is authored by the implementer to the specified shape (checklist + clause library + cited pointers) — this is the one content-authoring task that isn't fully pre-written, by design (legal text must be composed carefully, not copy-pasted); the SHAPE, sources, and rules are fully specified.

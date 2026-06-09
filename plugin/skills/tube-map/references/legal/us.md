# US research law — reference module

> Disclaimer: informational paralegal support — not legal advice. Claude is not a lawyer.
> See `README.md` before using this module. Verify every point with qualified counsel.
> Primary sources: eCFR (https://www.ecfr.gov), U.S. Code (https://uscode.house.gov).
> This module backs the consolidated `uslaw` stop (HIPAA + Common Rule + IP).

---

## 1. HIPAA — Privacy & Security Rules

**Primary sources:**
- Privacy Rule: 45 CFR Part 164, Subpart E — verify current text on eCFR.
- Security Rule: 45 CFR Part 164, Subpart C — verify current text on eCFR.
- Applicability provisions: 45 CFR Part 160.
- HHS guidance: https://www.hhs.gov/hipaa/for-professionals/index.html
  (verify current guidance — OCR issues updated FAQs and guidance periodically)

### Checklist — what to verify

- [ ] **Covered entity / business associate status**: is the institution a covered entity
      (health plan, healthcare clearinghouse, healthcare provider transmitting PHI
      electronically)? Is the researcher a business associate of a covered entity?
- [ ] **PHI identification**: does the data include protected health information (individually
      identifiable health information)? Has de-identification been performed under
      45 CFR 164.514 (Safe Harbor or Expert Determination)? Verify with counsel.
- [ ] **Authorisation / waiver**: is a valid HIPAA authorisation from each individual
      in place, or has an IRB/Privacy Board granted a waiver (45 CFR 164.512(i))?
- [ ] **Minimum necessary** (45 CFR 164.502(b)): is data limited to what is minimally
      necessary for the research purpose?
- [ ] **Security Rule compliance** (45 CFR Part 164 Subpart C): are administrative,
      physical, and technical safeguards in place for electronic PHI?
- [ ] **Business Associate Agreement (BAA)**: is a BAA required (45 CFR 164.504(e))?
      See clause library below.

### Clause library — Business Associate Agreement (45 CFR 164.504(e))

| Clause | What to look for (required or recommended) |
|---|---|
| Permitted uses and disclosures | Exactly what the BA may do with PHI — must match the purpose |
| Prohibition on further use | BA may not use/disclose PHI beyond what is permitted |
| Safeguards | Obligation to implement appropriate safeguards (Security Rule) |
| Subcontractors | BA must obtain BAAs from its subcontractors who handle PHI |
| Reporting obligations | Report breaches, security incidents, impermissible uses to covered entity |
| Data-subject rights | BA to assist covered entity in fulfilling individual access/amendment rights |
| Return or destruction | Disposition of PHI on contract termination |
| Survival | Which obligations survive termination |

> The mandatory BAA elements are set out in 45 CFR 164.504(e)(2). Verify the current
> regulation text before drafting or reviewing a BAA.

---

## 2. Human subjects — Common Rule

**Primary sources:**
- Common Rule: 45 CFR Part 46 (HHS) — verify current text on eCFR.
  The 2018 revised Common Rule is in effect; check for any subsequent amendments.
- FDA human subjects regulations: 21 CFR Parts 50 and 56 — for FDA-regulated research;
  verify current text on eCFR.
- OHRP guidance: https://www.hhs.gov/ohrp/

### Checklist — what to verify

- [ ] **Applicability**: is the research conducted or supported by a federal department
      subject to the Common Rule? Is it FDA-regulated? Both? Does an institution's
      FWA extend coverage to all research? Verify with IRB office.
- [ ] **Human subject determination** (45 CFR 46.102): does the activity involve a living
      individual from whom the investigator obtains data / biospecimens?
- [ ] **IRB review category**: exempt, expedited, or full-board review?
      Verify which category applies under 45 CFR 46.104 (exempt) or 46.110 (expedited).
- [ ] **Informed consent elements** (45 CFR 46.116): are all required basic elements
      present? Are any applicable additional elements included? Is waiver/alteration
      of consent justified (45 CFR 46.116(c)/(d))?
- [ ] **Vulnerable populations** (45 CFR 46, Subparts B–D): does the research involve
      pregnant women/fetuses, prisoners, or children? Additional protections required.
- [ ] **Continuing review**: is continuing review required, or does the 2018 Rule exempt
      the study from continuing review? Confirm with IRB.

### Required elements of informed consent (45 CFR 46.116(b))

The regulation lists the required basic elements and additional elements. Rather than
reproduce the full list here (which may be amended), verify the current regulatory text
at eCFR and confirm the consent form covers all applicable elements. Key categories to
check: study purpose and duration; foreseeable risks and benefits; confidentiality;
voluntary participation and right to withdraw; contact information for questions.

> Do not use this checklist as a substitute for IRB review or legal counsel.

---

## 3. IP & research agreements

**Primary sources:**
- Bayh-Dole Act: 35 U.S.C. §§ 200–212 (federally funded inventions) —
  verify current text at https://uscode.house.gov/
- Implementing regulations: 37 CFR Part 401 — verify current text on eCFR.
- UBMTA (Uniform Biological Material Transfer Agreement): the master agreement
  template is maintained by the AUTM — https://autm.net/
- Standard form MTA templates vary by institution; verify with tech-transfer office.

### Checklist — Bayh-Dole (federally funded inventions)

- [ ] **Federal funding determination**: is any funding for the research from a US federal
      agency (direct grant or subcontract)? If yes, Bayh-Dole obligations apply.
- [ ] **Disclosure obligation** (35 U.S.C. § 202(c)(1)): promptly disclose each subject
      invention to the federal agency — is the process in place?
- [ ] **Election of title** (35 U.S.C. § 202(c)(2)): does the institution intend to
      retain title? Is election timely?
- [ ] **Government license** (35 U.S.C. § 202(c)(4)): the government retains a non-exclusive,
      non-transferable, irrevocable, paid-up license — this cannot be negotiated away.
- [ ] **March-in rights** (35 U.S.C. § 203): government may require licensing to others
      under defined conditions — understand the risk in commercialisation planning.
- [ ] **Reporting / patent prosecution**: annual utilisation reports; patent prosecution
      obligations — coordinate with tech-transfer office.

### Clause library — MTA / DTA / CDA / NDA

| Agreement type | Key clauses to review |
|---|---|
| MTA (Material Transfer Agreement) | Permitted uses of material; prohibition on redistribution; IP arising from use (progeny, modifications, derivatives — who owns?); publication rights; safety obligations |
| DTA (Data Transfer Agreement) | Data use limitations; prohibition on re-identification; security obligations; publication/sharing restrictions; return/destruction on expiry |
| CDA / NDA (Confidentiality / Non-Disclosure) | Definition of confidential information; carve-outs (public domain, prior knowledge, independent development, legal compulsion); duration; remedy for breach (injunction clause) |

> For all IP agreements involving federally funded inventions, confirm compliance with
> Bayh-Dole (35 U.S.C. §§ 200–212) and 37 CFR Part 401 with the institution's
> tech-transfer office and counsel.

> All the above are frameworks for discussion with qualified US legal counsel.
> Do not rely on this checklist as a substitute for professional review.

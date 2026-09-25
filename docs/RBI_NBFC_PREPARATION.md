# RBI NBFC Master Direction Preparation Checklist (WP-C)

This checklist outlines the verification, extraction, and modelling requirements for WP-C (RBI NBFC Cyber Security Directions).

---

## 1. Raw Source Verification & Provenance

- [x] **File present in `data/raw/`**: `RBI_NBFC_Cybersecurity_Directions_2026.pdf` (47 pages).
- [x] **SHA-256**: `5b2432e53e1b1d1b500fb21ebe6176d28bcf3386543097b6c53aeb43ad860073`.
- [x] **Manifest Status**: Entry present in `data/raw/manifest.json` with `acquired_by: "human_download_official_site"` and documented `reverify_exemption` due to RBI Cloudflare/CAPTCHA challenge on automated HTTP clients.
- [x] **Completeness & Integrity**: Verified 47 pages, ends with valid `%%EOF`, PyMuPDF loads with 0 repair warnings, producer metadata intact (`data/raw/RBI_NBFC_Cybersecurity_Directions_2026.meta.json`).

---

## 2. Text Reading & Scoping Checklist (Primary Text Verification)

When modelling WP-C obligations, verify from exact pages:

1. **Short Title and Commencement**:
   - Paragraph 2 / Page 2: Confirm immediate commencement / effective date.
2. **Entity Applicability & Layer Scoping**:
   - Chapter I applicability (paragraphs 3–5): Determine applicability across NBFC Base Layer, Middle Layer, Upper Layer, and Top Layer.
   - Note which specific chapters/clauses apply strictly to Middle Layer and above vs all NBFCs.
3. **Cyber Incident Reporting Duty**:
   - Paragraph 28 / Page 9 and Paragraph 141 / Annexure:
     - Anchor: `detection` (and whether `noticing` or `occurrence` are referenced in the text).
     - Deadline duration: `PT6H` (6 hours).
     - Recipient: Reserve Bank of India via DAKSH portal (`https://daksh.rbi.org.in`).
     - CERT-In notification duty: check whether paragraph 28 explicitly requires proactive reporting to CERT-In as well.
4. **Vulnerability Assessment & Penetration Testing (VAPT)**:
   - Check periodicity (e.g. at least once in six months or annual) and entity scope.
5. **Repeal and Savings**:
   - Check Master Directions / circulars repealed by this consolidated Direction.

---

## 3. Labels-First Benchmark Scenarios for WP-C

Before authoring obligations in `data/obligations/rbi.nbfc-cyber.2026.json`, commit 8 benchmark scenarios in `benchmark/scenarios/`:
1. `rbi-nbfc-upper-layer-ransomware-6h.json` (6h reporting to RBI via DAKSH)
2. `rbi-nbfc-detection-vs-occurrence.json` (Detection anchor vs occurrence trap)
3. `rbi-nbfc-missing-detection-unknown.json` (Missing detection timestamp -> Unknown)
4. `rbi-nbfc-base-layer-exemption-trap.json` (Base layer specific scoping)
5. `rbi-nbfc-multi-regulator-cert-in.json` (RBI + CERT-In dual reporting)
6. `rbi-nbfc-before-effective-date.json` (Pre-commencement trap)
7. `rbi-nbfc-vapt-cadence.json` (VAPT requirements)
8. `rbi-nbfc-non-nbfc-bank-trap.json` (Entity classification trap)

---

## 4. Quality Gate Integration

- Run `scripts/check.py` to ensure all gates (pytest, ruff, mypy, validate_all, benchmark dev) remain green.

# RBI NBFC Direction build notes (WP-C complete)

The stored 47-page text has now been read in full and the labels-first model in `docs/LABELS_RBI.md` has been implemented.

## Verified source and locations

- `data/raw/RBI_NBFC_Cybersecurity_Directions_2026.pdf` is 47 pages; SHA-256 `5b2432e53e1b1d1b500fb21ebe6176d28bcf3386543097b6c53aeb43ad860073`.
- The manifest says the project owner downloaded it from the official RBI site in a browser after solving the site's CAPTCHA; the reviewer then verified the file. No particular CAPTCHA provider is asserted.
- Paragraph 2 is on PDF page 3: "These Directions shall come into force with immediate effect."
- Paragraph 3 is on PDF page 3. It states the general NBFC coverage and then assigns Chapters III, IV and V to specified classes. Each later obligation must be mapped through the relevant chapter rather than through a presumed layer exemption.
- Paragraph 28 is on PDF page 18: "The NBFC shall report cyber incidents on DAKSH platform ... within six hours of detection."
- Paragraph 141 begins on PDF page 43 (and continues on page 44): it requires RBI reporting on DAKSH within six hours of detection and says the NBFC shall also pro-actively notify CERT-In.

## Answers established by the modelling pass

1. Paragraph 28 is in Chapter IV and applies only to Base Layer NBFCs with asset size ₹500 crore and above. Paragraphs 121 and 141 are in Chapter V and apply to Middle, Upper and Top Layer NBFCs, excluding CICs.
2. Paragraphs 28 and 141 are separate records because paragraph 3 gives them different chapter scopes. Chapter III paragraphs 7-9 contain no incident-reporting duty.
3. Paragraph 141's CERT-In sentence is a separate applicable duty with `deadline.kind = none`; it is wider than CERT-In Direction (ii), whose Annexure-I gate and six-hour clock remain separate.
4. Paragraph 121 requires VA at least once every six months and PT at least once in 12 months for the stated critical/DMZ systems, within Chapter V only.
5. Paragraphs 155-156 repeal prior IT Framework/IT Governance directions while preserving earlier actions, approvals, rights, liabilities, penalties and proceedings. No repeal obligation was created because this build was expressly limited to paragraphs 28, 121 and 141, and the cited repeal circular is not stored.

The unresolved HFC scope, NHB timing/channel, cross-regime anchor timing, missing repeal circular, and unmodelled paragraphs are tracked in `docs/OPEN_QUESTIONS.md`.

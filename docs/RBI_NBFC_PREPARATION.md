# RBI NBFC Direction preparation notes (WP-C)

This is a neutral source-reading checklist. It does not decide obligation scope or exemptions before the Direction is modelled.

## Verified source and locations

- `data/raw/RBI_NBFC_Cybersecurity_Directions_2026.pdf` is 47 pages; SHA-256 `5b2432e53e1b1d1b500fb21ebe6176d28bcf3386543097b6c53aeb43ad860073`.
- The manifest says the project owner downloaded it from the official RBI site in a browser after solving the site's CAPTCHA; the reviewer then verified the file. No particular CAPTCHA provider is asserted.
- Paragraph 2 is on PDF page 3: "These Directions shall come into force with immediate effect."
- Paragraph 3 is on PDF page 3. It states the general NBFC coverage and then assigns Chapters III, IV and V to specified classes. Each later obligation must be mapped through the relevant chapter rather than through a presumed layer exemption.
- Paragraph 28 is on PDF page 18: "The NBFC shall report cyber incidents on DAKSH platform ... within six hours of detection."
- Paragraph 141 begins on PDF page 43 (and continues on page 44): it requires RBI reporting on DAKSH within six hours of detection and says the NBFC shall also pro-actively notify CERT-In.

## Questions the modelling pass must answer from the text

1. Which chapter contains each candidate duty, and which paragraph 3 class therefore receives it?
2. Do paragraphs 28 and 141 duplicate duties for different chapter scopes, or require separate records?
3. Does paragraph 141's CERT-In sentence need a separate obligation, and how does it interact with the CERT-In Directions' Annexure-I gate and six-hour clock?
4. What exact cadence and class scope apply to vulnerability assessment and penetration testing?
5. What do the repeal-and-saving provisions preserve, and over what validity interval?

Only after those questions are answered with page quotes should labels or RBI obligations be authored. Candidate scenarios should test the text-derived chapter scopes, a missing detection timestamp, CERT-In overlap, pre-commencement timing, VAPT cadence, and a non-NBFC entity—without pre-deciding that any NBFC class is exempt.

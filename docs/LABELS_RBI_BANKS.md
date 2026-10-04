# RBI Directions for UCBs, AIFIs and Payments Banks: labels written before implementation

Author: the reviewer (the reviewer agent), from the stored text of the three Directions in `data/raw` (ingested in f803fc4). Committed before any obligation, entity class or engine change for them exists. The implementer must not change a label; a label the engine cannot produce is reported.

Read in full for this spec: each Direction's table of contents, Chapter I, every paragraph that mentions reporting, DAKSH, CERT-In, hours, VA or PT, the UCB Chapter III section list and paragraphs 83 to 92, and each repeal chapter's opening. The remaining control paragraphs were not read and are not modelled.

## What the text says (PDF pages from `page_offsets`)

| Direction | Point | Text | Page |
|---|---|---|---|
| all three | Commencement | Para 2: "These Directions shall come into force with immediate effect." Dated July 31, 2026. | 4, 1 |
| all three | Definition | 'Cyber Incident' - "A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not." Same words as the NBFC Direction. | UCB 6; AIFI 5; PB 5 |
| UCB (RBI/DoS/2026-27/437) | Scope | Para 3: "applicable to Urban Co-operative Banks". Para 4: four levels; Level I "Applicable to the UCB irrespective of digital services / products offered by it" (Chapters II and III); Level II adds Chapter IV; Level III adds Chapter V; Level IV adds Chapter VI. | 4 to 5 |
| UCB | Reporting | Chapter III (Level I), section V. Para 88: "The UCB shall report cyber incidents within six hours of detection on DAKSH platform". Para 87: "The UCB shall also proactively notify CERT-In regarding cyber incidents." | 29 |
| UCB | VA and PT | Chapter IV (Level II). Para 116: "VA of critical applications and those on DMZ shall be conducted at least once in every six months. PT shall be conducted at least once in a year." | 33 |
| AIFI (RBI/DoS/2026-27/456) | Scope | Para 3: EXIM Bank, NABARD, SIDBI, NHB and NaBFID. No chapter scoping. | 4 |
| AIFI | Reporting | Para 177: "The AIFI shall report cyber incidents within six hours of detection on DAKSH platform ... The AIFI shall also pro-actively notify CERT-In regarding cyber incidents." | 39 |
| AIFI | VA and PT | Para 146: "VA shall be conducted at least once in every six months and PT at least once in 12 months." | 35 |
| Payments Banks (RBI/DoS/2026-27/428) | Scope | Para 3: "applicable to Payments Banks". The stored PDF says "Updated as on October 01, 2026". | 4, 1 |
| Payments Banks | Reporting | Para 181: "The bank shall report cyber incidents within six hours of detection on DAKSH platform ... The bank shall also pro-actively notify CERT-In regarding cyber incidents." | 44 |
| Payments Banks | VA and PT | Para 150: "VA shall be conducted at least once in every six months and PT at least once in 12 months." | 39 |

## Modelling decisions the labels rely on (each needs a DECISIONS entry with these quotes)

1. `valid_from` 2026-07-31 for all three. For Payments Banks the stored text is the version updated on 1 October 2026; whether paragraphs 150 and 181 read the same between 31 July and 1 October is not verified. Lower confidence, open question.
2. UCB reporting and the CERT-In notification sit in Chapter III, which binds every UCB whatever its level. So a profile that says only `ucb` gets the reporting deadline with no level question.
3. UCB VA and PT sit in Chapter IV, which binds Levels II, III and IV. A profile that says only `ucb` is asked its level for these two duties. Classes: `ucb` (needs refinement), `ucb.level_i`, `ucb.level_ii`, `ucb.level_iii`, `ucb.level_iv`.
4. The refinement question must be worded from the data, not hard-coded to NBFCs. New taxonomy field `refinement_question` on each `needs_refinement` class: `nbfc` and `nbfc.base_layer` keep "What is the NBFC category?"; `ucb` uses "What is the UCB level?"; `bank` uses "What kind of bank is it?".
5. New class `bank.payments_bank` (child of `bank`). `bank` becomes `needs_refinement`, because the Directions for commercial banks, small finance banks and others are not in the dataset. A generic `bank` must be asked, never told it owes nothing. No class is added for bank types whose Direction is not ingested; the question's impact text says so.
6. New class `aifi`. All AIFI duties bind it.
7. The cyber-incident gate is the existing `rbi_cyber_incident` key; the definition is word for word the same.
8. CERT-In notification: no time limit in any of the three texts. Applicable duty, no deadline, as for NBFCs.
9. Anchor `detection` only.

## Obligation ids

- `rbi.ucb-cyber.2026.incident-reporting-6h` (para 88), `.cert-in-notification` (para 87, second sentence), `.va-half-yearly`, `.pt-annual` (para 116)
- `rbi.aifi-cyber.2026.incident-reporting-6h` (para 177, first sentence), `.cert-in-notification` (second sentence), `.va-half-yearly`, `.pt-annual` (para 146)
- `rbi.payments-banks-cyber.2026.incident-reporting-6h` (para 181, first sentence), `.cert-in-notification` (second sentence), `.va-half-yearly`, `.pt-annual` (para 150)

"CERT-In 6h" is `cert-in.directions-70b.2022.incident-reporting-6h`. Unless stated: type "Malicious code attacks such as Ransomware"; detected and noticed at 10:00 IST on 2026-10-01.

## Labels

| Id | Profile and facts | Expected |
|---|---|---|
| `rbi-ucb-level1-ransomware` | `ucb.level_i` | CERT-In 6h 16:00 (noticing). UCB reporting 16:00 (detection). UCB CERT-In notification applicable. UCB VA and PT not applicable. No unknowns. |
| `rbi-ucb-level3-has-va-pt` | `ucb.level_iii` | Same two deadlines. UCB VA and PT applicable. |
| `rbi-ucb-generic-reports-and-is-asked-level` | `ucb` | UCB reporting 16:00 and CERT-In 6h 16:00. UCB CERT-In notification applicable. Unknown "UCB level" affecting UCB VA and PT only. |
| `rbi-ucb-detected-before-noticed` | `ucb.level_ii`; detected 08:00, noticed 10:00 | UCB reporting 14:00 (detection). CERT-In 6h 16:00 (noticing). |
| `rbi-ucb-before-commencement` | `ucb.level_i`; 2026-07-01 10:00 | CERT-In 6h 2026-07-01 16:00. Every UCB duty not applicable, reason containing "not_yet_valid_at_incident_date (2026-07-31)". |
| `rbi-ucb-attested-not-a-cyber-incident` | `ucb.level_i`; type "hardware failure"; attested not Annexure I; attested not a cyber incident | No deadlines. CERT-In 6h, UCB reporting and UCB CERT-In notification not applicable. No unknowns. |
| `rbi-aifi-ransomware` | `aifi` | CERT-In 6h 16:00. AIFI reporting 16:00 (detection). AIFI CERT-In notification, VA and PT applicable. |
| `rbi-aifi-hardware-failure-unattested` | `aifi`; type "hardware failure"; no attestations | No deadlines. Unknown "Annexure I" affecting CERT-In 6h. Unknown "cyber incident" affecting AIFI reporting and AIFI CERT-In notification. |
| `rbi-payments-bank-ransomware` | `bank.payments_bank` | CERT-In 6h 16:00. Payments Banks reporting 16:00 (detection). Notification, VA and PT applicable. No unknowns. |
| `rbi-payments-bank-detection-unknown` | `bank.payments_bank`; noticed 10:00 only | CERT-In 6h 16:00. Unknown asking for the detection time, affecting Payments Banks reporting. |
| `rbi-generic-bank-is-asked-its-kind` | `bank` | CERT-In 6h 16:00. Unknown "kind of bank" affecting the four Payments Banks duties. None of them applicable or not applicable. No UCB, AIFI or NBFC duty or question. |
| `rbi-each-direction-keeps-to-its-own-entities` | `nbfc.middle_layer` | NBFC Chapter V reporting 16:00 and CERT-In 6h 16:00. Every UCB, AIFI and Payments Banks duty not applicable. No unknowns. |

## Existing scenarios that change

Scenarios whose profile holds `bank` with an incident on or after 2026-07-31 also expect the "kind of bank" unknown for the four Payments Banks duties. Their other expectations do not change. Each gains the Payments Banks paragraph 3 quote (page 4).

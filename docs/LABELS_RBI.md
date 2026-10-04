# RBI NBFC Direction: labels written before implementation

Author: the reviewer (the reviewer agent), from the stored text of `data/raw/RBI_NBFC_Cybersecurity_Directions_2026.txt` (all 47 pages read). Written and committed before any RBI obligation, entity class or engine change exists. The implementer turns each row into a scenario file and must not change a label; if the engine cannot produce a label, that is reported, not adjusted.

## What the text says (PDF pages from `page_offsets`)

| Point | Text | Page |
|---|---|---|
| Commencement | Para 2: "These Directions shall come into force with immediate effect." The document is dated "July 31, 2026". | 3, 1 |
| Scope by chapter | Para 3(2): Chapter III "only for NBFCs-Base Layer (NBFCs-BL) with asset size below ₹500 crore, and Core Investment Companies (CICs)". Para 3(3): Chapter IV "only for NBFCs-BL with asset size ₹500 crore and above". Para 3(4): Chapter V "only for NBFCs-Top Layer (NBFCs-TL), NBFCs-Upper Layer (NBFCs-UL), and NBFCs-Middle Layer (NBFCs-ML) ... excluding CICs". | 3 to 4 |
| Definition | Para 4(7): "'Cyber Incident' - A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not." Source note: "By the definition, it includes cybersecurity incidents as well as IT incidents." | 4 to 5 |
| Chapter III | Paras 7 to 9. No incident-reporting duty. | 10 to 11 |
| Chapter IV reporting | Para 28: "The NBFC shall report cyber incidents on DAKSH platform ... within six hours of detection." No CERT-In sentence. | 18 |
| Chapter V reporting | Para 141: "The NBFC shall report cyber incidents to RBI within six hours of detection on DAKSH platform". Then: "The NBFC shall also pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding cyber incidents." Note: "In respect of Housing Finance Companies, cyber incidents shall continue to be reported to NHB and not RBI". | 43 to 44 |
| VA and PT | Para 121 (Chapter V only): VA "at least once in every six months" and PT "at least once in 12 months" for critical information systems and / or those in the DMZ having customer interface. | 41 |
| Repeal | Paras 155 and 156. | 46 |

## Modelling decisions the labels rely on (each needs a DECISIONS entry with these quotes)

1. `valid_from` is 2026-07-31: "immediate effect" plus the date printed on the Direction.
2. Entity classes: `nbfc.bl_below_500cr`, `nbfc.bl_500cr_and_above`, `nbfc.middle_layer`, `nbfc.upper_layer`, `nbfc.top_layer`, and two classes held in addition to a layer: `nbfc.cic`, `nbfc.hfc`. `nbfc` and `nbfc.base_layer` are too coarse to decide the chapter, so a profile that holds only one of them must be asked for the category. It must never be treated as "no RBI duty".
3. A CIC is under Chapter III whatever its layer and is excluded from Chapter V.
4. The RBI reporting duties need a cyber incident as the Direction defines it, which is wider than CERT-In Annexure I. Rule: an explicit attestation decides; without one, an incident that matches an Annexure I type is a cyber incident; otherwise the engine asks. An attestation "not an Annexure I type" does not answer this question.
5. The CERT-In notification in para 141 has no time limit in the text. It is an applicable duty with no deadline. CERT-In's own six-hour duty is separate.
6. HFC note: the text gives no time limit or channel for NHB. Conservative reading: six hours from detection, recipient NHB, flagged as contested. It is modelled only for Chapter V, where the note sits. Whether it also governs para 28 is an open question.
7. The RBI anchor is `detection` only. If the detection time is unknown the engine asks; it does not substitute noticing.

## Obligation ids

- `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h` (para 28)
- `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (para 141, first sentence)
- `rbi.nbfc-cyber.2026.ch5-cert-in-notification` (para 141, second sentence)
- `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb` (para 141, note)
- `rbi.nbfc-cyber.2026.ch5-va-half-yearly`, `rbi.nbfc-cyber.2026.ch5-pt-annual` (para 121)

Below, "CERT-In 6h" is `cert-in.directions-70b.2022.incident-reporting-6h`. Unless stated, incident type is "Malicious code attacks such as Ransomware", and times are IST on 2026-10-01.

## Labels

| Id | Profile and facts | Expected |
|---|---|---|
| `rbi-ml-ransomware` | `nbfc.middle_layer`; detected 10:00, noticed 10:00 | CERT-In 6h 16:00 (noticing). ch5 reporting 16:00 (detection). ch5 CERT-In notification applicable, no deadline. ch4 and HFC duties not applicable. |
| `rbi-bl-above-500cr-ransomware` | `nbfc.bl_500cr_and_above`; detected 10:00, noticed 10:00 | CERT-In 6h 16:00. ch4 reporting 16:00 (detection). All ch5 duties not applicable. |
| `rbi-bl-below-500cr-no-reporting-duty` | `nbfc.bl_below_500cr`; same times | CERT-In 6h 16:00 only. ch4 and all ch5 duties not applicable. No unknowns. |
| `rbi-cic-in-middle-layer-excluded` | `nbfc.middle_layer` and `nbfc.cic`; same times | CERT-In 6h 16:00 only. All ch5 duties not applicable (CIC excluded). ch4 not applicable. |
| `rbi-detection-time-unknown` | `nbfc.middle_layer`; noticed 10:00, no detection time | CERT-In 6h 16:00. No RBI deadline. Unknown asking for the detection time, affecting ch5 reporting. |
| `rbi-detected-before-noticed` | `nbfc.middle_layer`; detected 08:00, noticed 10:00 | ch5 reporting 14:00 (detection). CERT-In 6h 16:00 (noticing). |
| `rbi-incident-before-commencement` | `nbfc.middle_layer`; detected and noticed 2026-07-01 10:00 | CERT-In 6h 2026-07-01 16:00. Every RBI duty not applicable with reason containing "not_yet_valid_at_incident_date (2026-07-31)". law_as_of 2026-07-01. |
| `rbi-bank-is-not-an-nbfc` | `bank`; detected 10:00, noticed 10:00 | CERT-In 6h 16:00 only. Every RBI NBFC duty not applicable. No unknowns. |
| `rbi-generic-nbfc-must-ask-category` | `nbfc`; detected 10:00, noticed 10:00 | CERT-In 6h 16:00. Unknown asking for the NBFC category, affecting ch4 reporting, ch5 reporting and ch5 CERT-In notification. None of those is applicable or not applicable. |
| `rbi-ml-hardware-failure-unattested` | `nbfc.middle_layer`; type "hardware failure"; detected 10:00, noticed 10:00; no attestations | No deadlines. Unknown "Annexure I" affecting CERT-In 6h. Unknown "cyber incident" affecting ch5 reporting and ch5 CERT-In notification. |
| `rbi-ml-it-incident-not-annexure-i` | as above, attested not an Annexure I type, attested a cyber incident | CERT-In 6h not applicable. ch5 reporting 16:00 (detection). ch5 CERT-In notification applicable. No unknowns. |
| `rbi-ml-attested-not-a-cyber-incident` | as above, attested not an Annexure I type, attested not a cyber incident | No deadlines. CERT-In 6h, ch5 reporting and ch5 CERT-In notification not applicable. No unknowns. |
| `rbi-hfc-middle-layer-reports-to-nhb` | `nbfc.middle_layer` and `nbfc.hfc`; detected 10:00, noticed 10:00 | CERT-In 6h 16:00. ch5 reporting to RBI not applicable. HFC duty 16:00 (detection), contested. ch5 CERT-In notification applicable. |
| `rbi-ml-also-data-fiduciary-2027` | `nbfc.middle_layer` and `dpdp.data_fiduciary`; 2027-06-01; types ransomware and "Data breach"; personal data involved; detected 09:00, noticed 10:00, aware 11:00 | ch5 reporting 15:00 (detection). CERT-In 6h 16:00 (noticing). DPDP rule7-2-b 2027-06-04 11:00 (awareness). The two immediate DPDP duties are time critical. ch5 CERT-In notification applicable. |

## Existing scenarios that change

Scenarios that use the class `nbfc` with an incident on or after 2026-07-31 now also expect the "NBFC category" unknown for the three RBI duties named in `rbi-generic-nbfc-must-ask-category`. Their existing expectations do not change. The clause is para 3 (page 3).

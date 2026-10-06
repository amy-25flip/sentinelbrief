# IRDAI Information and Cyber Security Guidelines, 2023: labels written before implementation

Author: the reviewer (the reviewer agent), from the PDF supplied by the project owner on 2026-10-04 (305 pages: a Hindi version on PDF pages 1 to 130, the English version on PDF pages 131 to 305, each English page marked "Page N of 175"). Committed before the document is ingested or any IRDAI obligation exists. The implementer must not change a label.

Read for this spec: the English table of contents, section 1 (purpose, scope, applicability), Policy 2.10 "Incident and problem management" in full (PDF pages 219 to 226), every English page containing "hours", "CERT-In" or "incident report", and the glossary. The other 23 policies were not read and are not modelled. The Hindi text extracts as unreadable glyphs and was not used.

## What the text says (PDF pages)

| Point | Text | Page |
|---|---|---|
| Reporting | Policy 2.10, 3.5 item 3: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website." | 224 |
| Applicability | 1.4: "These guidelines are applicable to all Insurers including Foreign Re-Insurance Branches (FRBs) and Insurance Intermediaries regulated by the Insurance Regulatory and Development Authority of India (IRDAI)." And: "Insurance Agents, Micro-Insurance Agents, Point of Sale Persons and Individual Surveyors will not fall under purview of these guidelines." | 138 |
| Incident | Policy 2.10, purpose: "An Incident is defined as the occurrence of any exceptional situation that could compromise the Confidentiality, Integrity or Availability of Information assets of Organization." The guidelines do not define "cyber incident". | 219 |
| Date | Cover: "VER– 1.0 APRIL, 2023". The covering circular (ref IRDAI/GA&HR/GDL/MISC/88/04/2023, 24 April 2023; a 2-page scanned letter, OCR text) says entities that "have already completed security audit for FY 2022-23 shall ensure compliance with these guidelines from next financial year". | 131 |

## Modelling decisions the labels rely on (each needs a DECISIONS entry with these quotes)

1. One obligation: `irdai.ics-guidelines.2023.incident-reporting-6h`, `PT6H`, anchor noticing with alternative anchor brought to notice (earliest known), recipient "CERT-In, with a copy to IRDAI and other concerned regulators / authorities".
2. `valid_from` 2023-04-24, the date of the covering circular. Contested: entities that had finished their FY 2022-23 audit were given until the next financial year. The earlier date never tells a user they owe less. Confidence 0.6.
3. Scope of "cyber incidents": the sentence does not say "as mentioned in Annexure I", unlike CERT-In Direction (ii). Conservative reading: any cyber incident, not only Annexure I types. New `requires` key `irdai_cyber_incident`, resolved like the RBI gate: an attestation decides; without one an Annexure I match is a cyber incident; otherwise the engine asks, quoting the Policy 2.10 definition of an incident. Contested.
4. Classes `irdai.insurer` and `irdai.intermediary` (both under `body_corporate`). Agents, micro-insurance agents, point of sale persons and individual surveyors are outside the guidelines and get no class.
5. Anchor: noticing or being brought to notice only. A detection time alone does not start this clock; the engine asks.
6. IRDAI's site forbids automated access (robots.txt "Disallow: /"), so live re-verification must skip this source with a documented exemption, as for RBI. The source is human-acquired and its bytes were NOT compared with the regulator's by the reviewer.

"CERT-In 6h" is `cert-in.directions-70b.2022.incident-reporting-6h`; "IRDAI 6h" is the new obligation. Unless stated: type "Malicious code attacks such as Ransomware"; noticed 10:00 IST on 2026-10-01.

## Labels

| Id | Profile and facts | Expected |
|---|---|---|
| `irdai-insurer-ransomware` | `irdai.insurer` | CERT-In 6h 16:00 and IRDAI 6h 16:00, both anchored on noticing. |
| `irdai-intermediary-brought-to-notice` | `irdai.intermediary`; brought to notice 09:00, no noticing time | Both 15:00, anchored on brought to notice. |
| `irdai-detection-only-asks` | `irdai.insurer`; detected 10:00 only | No deadlines. Unknown "noticed" affecting both. |
| `irdai-hardware-failure-unattested` | `irdai.insurer`; type "hardware failure"; no attestations | No deadlines. Unknown "Annexure I" affecting CERT-In 6h. Unknown "cyber incident" affecting IRDAI 6h. |
| `irdai-cyber-incident-not-annexure-i` | `irdai.insurer`; type "hardware failure"; attested not Annexure I; attested a cyber incident | CERT-In 6h not applicable. IRDAI 6h 16:00 (noticing), contested wider reading. |
| `irdai-attested-not-a-cyber-incident` | as above, attested not a cyber incident | No deadlines. Both not applicable. No unknowns. |
| `irdai-before-the-guidelines` | `irdai.insurer`; noticed 2023-04-01 10:00 | CERT-In 6h 2023-04-01 16:00. IRDAI 6h not applicable, reason containing "not_yet_valid_at_incident_date (2023-04-24)". |
| `irdai-payments-bank-is-not-an-insurer` | `bank.payments_bank`; detected and noticed 10:00 | IRDAI 6h not applicable. No IRDAI question. |
| `irdai-insurer-also-data-fiduciary-2027` | `irdai.insurer` and `dpdp.data_fiduciary`; 2027-06-01; types ransomware and "Data breach"; personal data involved; noticed 10:00, aware 11:00 | CERT-In 6h 16:00, IRDAI 6h 16:00, DPDP rule7-2-b 2027-06-04 11:00 (awareness). The two immediate DPDP duties are time critical. |

## Part 2 (2026-10-05): the other time-bound duties, labels written before implementation

Read in full for this part: Policy 2.2 section 3.3 (PDF page 176), Policy 2.8 section 3.5 (page 212), Policy 2.19 section 3.7 (pages 282 to 283) and Policy 2.24 (pages 296 to 299).

### What the text says

| Duty | Text | Page |
|---|---|---|
| Government order | 2.24 item 7: "The Organization shall as soon as possible, but not later than seventy-two hours of the receipt of an order, provide information under its control or possession, or assistance to the Government agency which is lawfully authorized" | 298 |
| Grievance | 2.24 item 10(I): the Grievance Officer shall "acknowledge the complaint within twenty-four hours and dispose off such complaint within a period of fifteen days from the date of its receipt" | 298 |
| Takedown | 2.24 item 11: "The Organization shall within twenty-four hours from the receipt of a complaint made by an individual ... take all reasonable and practicable measures to remove or disable access to such content" | 299 |
| Retention | 2.24 item 5: "shall retained his information for a period of one hundred and eighty days after any cancellation or withdrawal of his registration" | 297 to 298 |
| Cloud contract | 2.19, 3.7.2: "Organization shall contractually assure that they are informed of any confirmed breach immediately without any delay. For suspected breach, Organization shall be informed within 4 hours from the time of breach discovery." | 283 |
| Lost device | 2.8, 3.5 item 3: "In case of loss of device, the employee shall inform IT function within 4 hours." | 212 |

### Decisions

1. **None of these clocks starts from a cyber incident.** They start from an order, a complaint, a cancellation, or the loss of a device. New deadline anchor `external_event`: the duty is recorded with its duration and shown as applicable, but the engine never computes a deadline for it from incident facts and never asks a question about it.
2. **The cloud clause is a contract requirement on the organization**, not a notification the organization must make. Recorded as an ongoing duty with no deadline; the four hours bind the cloud provider under the contract.
3. **The lost-device clause is an internal duty** (employee to IT function). Recorded with recipient "the Organization's IT function"; it is not a report to any regulator.
4. **Policy 2.24 restates the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021.** Whether an insurer is an "intermediary" under those Rules is not evaluated; it is a prose condition shown to the user. The Rules themselves are not ingested.
5. Not modelled: 2.24 item 8 (report to CERT-In under the 2013 Rules; no time limit, and it overlaps Policy 2.10); Policy 2.2 section 3.3 (lost device reported "immediately", and treated as an incident after four hours), which is an internal escalation rule.
6. Same `valid_from` (2023-04-24, contested) and entity classes as Part 1.

### Obligation ids (all prefixed `irdai.ics-guidelines.2023.`)

`gov-order-information-72h`, `grievance-acknowledge-24h`, `grievance-dispose-15d`, `content-takedown-24h`, `registration-data-retention-180d`, `cloud-breach-notice-contract-clause`, `lost-device-internal-report-4h`.

### Labels

| Id | Profile and facts | Expected |
|---|---|---|
| `irdai-other-duties-give-no-incident-clock` | `irdai.insurer`; ransomware; noticed 2026-10-01 10:00 | Deadlines: only CERT-In 6h and IRDAI 6h, both 16:00. All seven duties above are applicable. None has a deadline. No unknowns. Nothing is time critical. |
| `irdai-other-duties-do-not-reach-an-nbfc` | `nbfc.middle_layer`; detected and noticed 10:00 | All seven not applicable. |
| `irdai-other-duties-before-the-guidelines` | `irdai.insurer`; noticed 2023-04-01 10:00 | All seven not applicable, reason containing "not_yet_valid_at_incident_date (2023-04-24)". |

## Part 3 (2026-10-05): entering the event that starts an external clock, labels before implementation

New fact `external_events`: a map from an obligation id to the time its starting event happened (the order was received, the complaint was received, the device was lost). Only obligations with the `external_event` anchor may appear in it; anything else is an input error. When a time is given, the deadline is that time plus the duration, with anchor `external_event`. The time does not change "law as of", which stays tied to the incident. Durations count from the timestamp (the earlier reading, as for SEBI Table 36).

| Id | Profile and facts | Expected |
|---|---|---|
| `irdai-government-order-clock` | `irdai.insurer`; ransomware; noticed 2026-10-01 10:00; order received 2026-10-02 09:00 | CERT-In 6h and IRDAI 6h 2026-10-01 16:00. `gov-order-information-72h` due 2026-10-05 09:00 (external_event). The other external duties have no deadline. law_as_of 2026-10-01. |
| `irdai-complaint-clocks` | `irdai.intermediary`; ransomware; noticed 2026-10-01 10:00; complaint received 2026-10-01 12:00, given for both grievance duties | `grievance-acknowledge-24h` due 2026-10-02 12:00; `grievance-dispose-15d` due 2026-10-16 12:00; plus the two six-hour deadlines at 16:00. |

## Part 4 (2026-10-06): duties with a stated period or time limit, labels written before implementation

Method: the whole stored text (305 PDF pages) was searched for every stated period or time limit (annual, yearly, half yearly, quarterly, monthly, "once in", "within N days / months", "N days", "six months"). Each hit was read in context. Duties stated only as "periodically" or "at regular intervals" have no period to model and are listed at the end. This is a keyword-led reading, not a clause-by-clause reading of every policy.

### New obligation ids (all prefixed `irdai.ics-guidelines.2023.`)

| Id | Where (PDF page) | Words relied on | Kind | Classes |
|---|---|---|---|---|
| `policy-review-annual` | 1.5 Governance, IV (139) | "This policy shall be reviewed on an annual basis" | recurring P12M | both |
| `risk-assessment-annual` | 1.8 Risk Management, I (153) | "shall perform Risk Assessment at least annually" | recurring P12M | both |
| `assurance-audit-annual` | 1.10 Compliance (157) | "An independent Assurance Audit shall be carried out by the Auditor every year." | recurring P12M | both |
| `intermediary-annexure-iii-to-insurer-annual` | 1.10 (157) | "The Insurance Intermediary shall submit the Annexure – III ... to the Insurer/s annually." | recurring P12M | intermediary only |
| `insurer-audit-report-to-irdai` | 1.10 (157) | "to IRDAI within 90 days from the end of financial year or within 30 days of completion of Audit, whichever is earlier" | recurring P12M, fixed date 29 June | insurer only |
| `frb-annexure-vi-year-end` | 1.10 (157) | "shall be submitted to IRDAI at the end of every financial year" | recurring P12M, fixed date 31 March | insurer only, prose condition: Foreign Reinsurance Branch interfaced with an overseas parent (not evaluated) |
| `remote-access-accounts-monthly` | Policy 2.3, 3.8 item 8 (184) | "On a monthly basis ... shall ensure that the accounts active within the Remote access solutions are accurate" | recurring P1M | both |
| `restoration-test-half-yearly` | Policy 2.6, 3.1 item 1 (200) | "Data restoration testing must be performed at a minimum of six months" | recurring P6M | both |
| `bcp-risk-analysis-annual` | Policy 2.13, II (239) | "Risk Analysis shall be performed at least on an annual basis." | recurring P12M | both |
| `risk-mitigation-plan-review-quarterly` | Policy 2.13, II (239) | "reviewed and tracked to closure on a quarterly basis" | recurring P3M | both |
| `dr-plan-review-annual` | Policy 2.13, IV (241) | "IT DR plans shall be reviewed at least on an annual basis." | recurring P12M | both |
| `bcp-dr-test-annual` | Policy 2.13, 3.3.3 item 1 (242) | "shall be tested at least once annually or when significantly changed" | recurring P12M | both |
| `physical-access-review-half-yearly` | Policy 2.15, 3.2.3 I (259) | "reviewed ... on a half yearly basis" | recurring P6M | both |
| `evacuation-drill-annual` | Policy 2.15, 3.3.2 item 4 (260) | "Evacuation drills shall be performed at least on an annual basis." | recurring P12M | both |
| `log-retention-180d` | Policy 2.16, 3.3 item 14 (265) | "maintained for a rolling period of 180 days and within the Indian jurisdiction" | retention P180D | both |
| `vapt-internet-facing-annual` | Policy 2.16, 3.6.1 item 2 (266) | "to be conducted periodically atleast once in a year" | recurring P12M | both |
| `external-pt-half-yearly` | Policy 2.16, 3.6.1 item 5 (267) | "should be conducted ... once in 6 months" | recurring P6M | both |
| `vapt-high-risk-closure-1m` | Policy 2.16, 3.6.1 item 9 (267) | "should be closed within a period of one month" | none (no computed deadline) | both |
| `audit-gap-closure-2m` | Policy 2.16, 3.6.1 item 10 (267) | "the outer time limit for closure of all the audit gaps is two months" | none (no computed deadline) | both |
| `is-practices-review-annual` | Policy 2.16, 3.6.2 item 1 (267) | "shall conduct annual review of information security practices" | recurring P12M | both |
| `users-informed-of-termination-right-annual` | Policy 2.24, 3.1 item 2 (297) | "at least once every year" | recurring P12M | both, prose condition: intermediary under the IT Rules 2021 (not evaluated) |
| `users-informed-of-rules-annual` | Policy 2.24, 3.1 item 4 (297) | "at least once in a year" | recurring P12M | both, same prose condition |

### Decisions the labels rely on

1. **The audit report date.** The clause gives two limits and takes the earlier. Only the first can be computed without knowing when the audit finished. The guidelines do not define "financial year"; 1 April to 31 March is assumed, so 90 days from the end is 29 June. The record carries that as a fixed date and its action says it is the latest possible date and that the limit is 30 days after the audit is completed if that comes first. The tool must not present 29 June as the due date without that sentence.
2. **Closure limits are listed, not computed.** "One month" and "two months" run from a VAPT or audit report, and the engine refuses month-long durations for deadlines (a month is not a fixed number of days). They are recorded with kind `none`; the action states the limit.
3. **"Should" duties are recorded and say so.** Items 5 and 9 of 3.6.1 use "should". The action text uses "should", not "must".
4. **Recipient.** Only `insurer-audit-report-to-irdai` and `frb-annexure-vi-year-end` go to IRDAI; `intermediary-annexure-iii-to-insurer-annual` goes to the insurer(s). All others are internal duties with no recipient outside the entity.
5. **No incident clock.** None of these starts from an incident. They add no deadline and no question to an incident evaluation.
6. Same `valid_from` (2023-04-24, contested until 2024-04-01) as Parts 1 and 2.

### Labels

| Id | Input | Expected |
|---|---|---|
| `irdai-recurring-insurer-calendar` (unit test) | calendar for `irdai.insurer`, last done 2026-04-01 | Exactly 18 events from this instrument. First due dates: monthly duty 2026-05-01; quarterly 2026-07-01; the three half-yearly duties 2026-10-01; `insurer-audit-report-to-irdai` 2026-06-29; `frb-annexure-vi-year-end` 2027-03-31; the eleven other annual duties 2027-04-01. No `intermediary-annexure-iii-to-insurer-annual`. Nothing undetermined. |
| `irdai-recurring-intermediary-calendar` (unit test) | calendar for `irdai.intermediary`, last done 2026-04-01 | Exactly 17 events: the 16 recurring duties common to both classes plus `intermediary-annexure-iii-to-insurer-annual` (2027-04-01). Neither `insurer-audit-report-to-irdai` nor `frb-annexure-vi-year-end`. |
| `irdai-recurring-not-for-nbfc` (unit test) | calendar for `nbfc.middle_layer` | No event from this instrument. |
| `irdai-periodic-duties-add-no-incident-clock` (scenario) | `irdai.insurer`; ransomware; noticed 2026-10-01 10:00 | Deadlines exactly CERT-In 6h and IRDAI 6h at 16:00. No unknowns. `assurance-audit-annual`, `insurer-audit-report-to-irdai`, `log-retention-180d`, `vapt-high-risk-closure-1m` applicable. `intermediary-annexure-iii-to-insurer-annual` not applicable. |
| `irdai-periodic-duties-intermediary` (scenario) | `irdai.intermediary`; same incident | `intermediary-annexure-iii-to-insurer-annual` applicable; `insurer-audit-report-to-irdai` and `frb-annexure-vi-year-end` not applicable. |
| `irdai-periodic-duties-before-the-guidelines` (scenario) | `irdai.insurer`; noticed 2023-04-01 10:00 | `assurance-audit-annual` and `insurer-audit-report-to-irdai` not applicable, reason containing "not_yet_valid_at_incident_date (2023-04-24)". |
| audit report wording (unit test) | the record | action contains "29 June", "latest" and "30 days"; recipient IRDAI. |

Mutation tests: the insurer-only report leaking to intermediaries; the half-yearly restoration test changed to twelve months; the audit report date moved from 29 June.

### Read and not modelled

- "all members meeting at least twice in a year" (ISRMC, 1.5): two meetings a year is not a six-month interval.
- Passwords changed "once in 45 days" (2.3) and third-party user IDs expiring in "not more than 15 days" (2.3): system settings, not dated duties.
- The insurer obtaining annual self-certification from intermediaries that hold only physical data (1.10): depends on a fact about each intermediary.
- Every duty stated as "periodically", "on a periodic basis" or "at regular intervals" (storage reviews, access rights reviews, third-party assessments, log reviews, incident trend analysis and others): no period is stated.

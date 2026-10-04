# SEBI CSCRF, remaining reporting duties: labels written before implementation

Author: the reviewer (the reviewer agent), from the stored text of `data/raw/SEBI_CSCRF_Circular_2024-08-20.txt` pages 122 to 124 and 198 to 203, and the rendered PDF pages 123 and 124. Written and committed before these duties are implemented. The implementer must not change a label; a label the engine cannot produce is reported.

## Correction to Review 7, finding J3 (the reviewer's error)

Review 7 said page 123 puts the incident clause under "MIIs and Qualified REs (Mandatory)". That is wrong. In the PDF table the applicability cell of row RS.CO.S1, RS.CO.S2, RS.CO.S3 reads "All REs (Mandatory)". "MIIs and Qualified REs (Mandatory)" is the cell of the row above (RS.MA.S5). The extracted text prints each cell after its row, which the reviewer misread. There is no scope tension: page 123 and Annexure-O (page 200) agree that the duty is on all REs. The DECISIONS entry that records a tension must be rewritten to say this, and the matching OPEN_QUESTIONS item closed with this reason.

## What the text says

| Point | Text | Page |
|---|---|---|
| Portal | "However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours." Annexure-O B.1: "shared to SEBI through the email ID mkt_incidents@sebi.gov.in within 6 hours and SEBI Incident Reporting Portal within 24 hours." | 123, 200 |
| Brokers and DPs | "Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents." | 123 |
| Other incidents | "All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours." | 123 |
| NCIIPC | "Additionally, the REs, whose systems have been identified as "Protected system" by NCIIPC shall also report the incident to NCIIPC." Annexure-O 3.1: "in a timely manner". | 124, 200 |
| After reporting | Table 36, "Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident)": Interim Report 3 Days; Mitigation measure 7 Days; Root Cause Analysis (RCA) report 30 Days, with "Additional time may be provided by SEBI ... on a case-by-case basis on request of the RE"; VAPT for the incident and its closure reports 45 days. | 201 to 202 |
| Forensic | 4.1: for incidents classified High or Critical a forensic report; 4.3: "the maximum period for the submission of forensic audit report shall be 75 days from date of reporting of incident." | 203 |
| Six-hour threshold | Annexure-O A.1: "Any incident stated under CERT-In Cybersecurity directions and meeting below criteria shall be mandatorily reported within 6 hours" with four criteria. | 198 |
| Quarterly | Reports "shall be submitted to SEBI within 15 days from the quarter ended June, September, December and March of every year." | 124 |

## Modelling decisions the labels rely on (each needs a DECISIONS entry with these quotes)

1. Portal within 24 hours: the starting event is the same as the six-hour duty (the sentence continues it). Anchors noticing, detection, brought to notice; earliest known wins.
2. "All other cybersecurity incident(s) ... within 24 hours" names no starting event. Conservative reading: the same anchors. Contested.
3. "Other" means a cybersecurity incident that does not fall under the CERT-In directions. New `requires` key `sebi_other_cybersecurity_incident`: Annexure I matched, not applicable (the six-hour duties apply instead); Annexure I unresolved, the Annexure I Unknown; attested not Annexure I, then `is_cyber_incident` decides (true applies, false not applicable, unknown asks, question contains "cybersecurity incident").
4. Annexure-O A.1 narrows the six-hour duty to listed incidents that also meet four criteria. The tool does not evaluate those criteria and keeps six hours for every Annexure I incident. This can only tell a user they owe more, not less. Open question.
5. Stock broker and depository participant are roles held in addition to a size category: classes `sebi.stock_broker`, `sebi.depository_participant`. Every duty that binds "REs" must also bind a profile that holds only a role class, so a broker with no category selected is never told it owes nothing.
6. NCIIPC: new key `nciipc_protected_system`, profile field `uses_protected_systems` (true, false, unknown asks; question contains "Protected system"). No time limit in the text ("in a timely manner"): an applicable duty with no deadline. It applies to any cybersecurity incident (Annexure I matched, or attested a cyber incident).
7. Table 36 duties start from "the date of reporting the incident or being brought to notice". New time field `when_reported_to_sebi` and anchor `reported`; alternative anchor brought to notice; earliest known wins. Durations P3D, P7D, P30D, P45D counted from that timestamp. If neither time is known the engine asks (question contains "reported to SEBI"). The RCA extension is kept in the action text. They apply whenever a SEBI incident-reporting duty applies (six-hour or other-incident).
8. Forensic report (75 days, High or Critical only) and the quarterly report are not modelled. Open questions.

## Obligation ids

- existing: `sebi.cscrf.2024.incident-reporting-6h`
- `sebi.cscrf.2024.incident-portal-24h`
- `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- `sebi.cscrf.2024.other-incidents-24h`
- `sebi.cscrf.2024.nciipc-protected-system-report`
- `sebi.cscrf.2024.post-incident-interim-report-3d`, `...mitigation-7d`, `...rca-30d`, `...vapt-45d`

"CERT-In 6h" is `cert-in.directions-70b.2022.incident-reporting-6h`. Unless stated: incident type "Malicious code attacks such as Ransomware"; noticed 2026-10-01 10:00 IST; `uses_protected_systems` false; no report time given.

## Labels

| Id | Profile and facts | Expected |
|---|---|---|
| `sebi-portal-24h-after-noticing` | `sebi.mii` | CERT-In 6h 16:00. SEBI 6h 16:00. Portal 2026-10-02 10:00 (noticing). Other-incidents not applicable. NCIIPC not applicable. Unknown "reported to SEBI" affecting the four post-incident duties. |
| `sebi-broker-also-reports-to-exchange` | `sebi.small_re` and `sebi.stock_broker` | As above, plus broker duty 16:00 (noticing). |
| `sebi-non-broker-no-exchange-duty` | `sebi.small_re` | Broker duty not applicable. SEBI 6h 16:00. |
| `sebi-broker-role-only-still-owes-re-duties` | `sebi.stock_broker` only | SEBI 6h 16:00, portal next day 10:00, broker duty 16:00, CERT-In 6h 16:00. |
| `sebi-other-incident-24h` | `sebi.midsize_re`; type "hardware failure"; attested not Annexure I; attested a cyber incident | No six-hour deadlines: CERT-In 6h, SEBI 6h, portal not applicable. Other-incidents 2026-10-02 10:00 (noticing), contested. |
| `sebi-other-incident-unresolved-asks` | `sebi.midsize_re`; type "hardware failure"; no attestations | No deadlines. Unknown "Annexure I" affecting CERT-In 6h, SEBI 6h, portal and other-incidents. None of them applicable or not applicable. |
| `sebi-not-a-cyber-incident` | `sebi.midsize_re`; type "hardware failure"; attested not Annexure I; attested not a cyber incident | No deadlines. SEBI 6h, portal, other-incidents, NCIIPC and the four post-incident duties not applicable. No unknowns. |
| `sebi-protected-system-reports-to-nciipc` | `sebi.mii`; `uses_protected_systems` true | NCIIPC duty applicable, no deadline. SEBI 6h 16:00. |
| `sebi-protected-system-unknown-asks` | `sebi.mii`; `uses_protected_systems` not given | Unknown "Protected system" affecting the NCIIPC duty. SEBI 6h 16:00 unaffected. |
| `sebi-post-incident-reports-from-report-date` | `sebi.qualified_re`; reported to SEBI 2026-10-01 15:00 | Interim 2026-10-04 15:00, mitigation 2026-10-08 15:00, RCA 2026-10-31 15:00, VAPT 2026-11-15 15:00 (anchor reported). SEBI 6h 16:00. No unknowns. |
| `sebi-post-incident-brought-to-notice-earlier` | `sebi.qualified_re`; brought to notice 2026-10-01 09:00; reported to SEBI 2026-10-01 15:00; no noticing time | Interim 2026-10-04 09:00 (brought to notice). SEBI 6h 15:00 (brought to notice). |
| `sebi-nbfc-is-not-a-sebi-re` | `nbfc.middle_layer`; detected and noticed 10:00 | Every SEBI duty not applicable. No SEBI unknowns. |

## Existing scenarios that change

Every existing scenario in which `sebi.cscrf.2024.incident-reporting-6h` produces a deadline now also expects: the portal deadline 24 hours after the same anchor time; and the "reported to SEBI" unknown for the four post-incident duties, unless a brought-to-notice time is given, in which case those four deadlines are computed from it. Scenarios whose entity profile says `uses_protected_systems` true expect the NCIIPC duty as applicable; where the profile omits it, the "Protected system" unknown. Existing expectations do not otherwise change. Each changed scenario gains the quote of the clause that adds the expectation.

## Amendment 1 (2026-10-04, by the label author, during the build)

Decision 7 says the post-incident duties apply whenever a SEBI incident-reporting duty applies. The table rows did not spell out the consequence for every row, so:

- every row with a SEBI reporting deadline and no report time also expects the "reported to SEBI" unknown for the four post-incident duties (rows 2 to 5, 8 and 9, as row 1 states);
- `sebi-other-incident-unresolved-asks` also expects the "Annexure I" unknown for the four post-incident duties, since they depend on the same unresolved fact;
- `sebi-nbfc-is-not-a-sebi-re` also expects the RBI Chapter V deadline (16:00, detection), which the profile implies.

Existing scenario `sebi-mii-attested-not-annexure-i` (attested not Annexure I, cyber-incident status not given) now expects the "cybersecurity incident" unknown for the other-incident, NCIIPC and post-incident duties, per decision 3.

## Part 2 (2026-10-05): forensic report and quarterly reports, labels before implementation

These close decision 8 of Part 1, which left both unmodelled.

### What the text says

| Point | Text | Page |
|---|---|---|
| Who must file a forensic report | Annexure-O 4.1: "For all incidents classified as High or Critical, the RE shall submit a forensic audit/ investigation report." 4.2: "For incidents classified as low or medium, forensic report shall be submitted if the RCA is inconclusive or if the SEBI/ HPSC-CS directs the same." | 203 |
| By when | 4.3: "the maximum period for the submission of forensic audit report shall be 75 days from date of reporting of incident." | 203 |
| Severity | Annexure-O A.2: four categories, Low, Medium, High, Critical. 3.5: "RE shall classify the cybersecurity incident based on its severity as per Table 35". A.4: an incident that disrupts normal operations "must be classified as High or Critical". | 198 to 199, 202 |
| Quarterly | RS.CO.S1 item 4: quarterly reports "shall be submitted to SEBI within 15 days from the quarter ended June, September, December and March of every year." | 124 |

### Decisions

1. New fact `sebi_severity` (low, medium, high, critical, or not given). The tool does not classify; the RE does (3.5). New `requires` key `sebi_high_or_critical`: high or critical applies; low or medium does not apply, with a reason that says a report may still be required under 4.2; not given asks (question contains "severity").
2. `post-incident-forensic-report-75d`: `P75D`, anchor `reported` only (the text says "from date of reporting of incident" and, unlike Table 36, does not add "or being brought to notice"). Counted from the timestamp. It is a maximum; the actual timeline is "decided based on discussion with all stakeholders", which the action text keeps.
3. It applies only when a SEBI incident-reporting duty applies, so the incident-reporting question is resolved first and the severity question is asked only after it.
4. `quarterly-report-15d`: a recurring duty on all REs, every three months, due on 15 July, 15 October, 15 January and 15 April. It is not an incident deadline. New data field `fixed_schedule` (month-day list) so the calendar export can place it on those dates.

### Labels

Unless stated: `sebi.qualified_re`; ransomware; noticed 2026-10-01 10:00; `uses_protected_systems` false; reported to SEBI 2026-10-01 15:00. "Forensic" is `sebi.cscrf.2024.post-incident-forensic-report-75d`.

| Id | Facts | Expected for the forensic duty |
|---|---|---|
| `sebi-forensic-high-severity-75-days` | severity high | Deadline 2026-12-15 15:00 (reported). |
| `sebi-forensic-critical-severity` | severity critical | Deadline 2026-12-15 15:00 (reported). |
| `sebi-forensic-medium-not-required` | severity medium | Not applicable. No unknown. |
| `sebi-forensic-severity-unknown-asks` | severity not given | Unknown "severity". No deadline. |
| `sebi-forensic-needs-report-time` | severity high; no report time; brought to notice 09:00 | Unknown "reported to SEBI" for Forensic: being brought to notice does not start this clock, although it starts the Table 36 clocks (interim due 2026-10-04 09:00). |

All five also expect the Part 1 outcomes for the same facts.

### Existing scenarios that change

For each existing scenario, the forensic duty follows the interim-report duty: where that is not applicable, so is Forensic; where it carries the "Annexure I" or "cybersecurity incident" unknown, Forensic carries the same; where it has a deadline or the "reported to SEBI" unknown, Forensic carries the "severity" unknown (no existing scenario states a severity).

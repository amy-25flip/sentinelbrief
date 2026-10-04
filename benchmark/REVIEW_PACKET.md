# SentinelBrief: benchmark review packet

For a compliance professional. Every expected outcome below was written by an AI from the
primary texts and has not been checked by a qualified person. Until it has, no accuracy
figure for this tool should be quoted.

94 dev scenarios over 45 modelled obligations.

How to review: do Part A first. In Part B, tick each scenario or say what is wrong.
PDF page numbers refer to the files in `data/raw/`.

Reviewer name and organisation: ______________________   Date: ____________

## Part A. Readings to confirm first

Each obligation below is modelled on a reading the authors are not sure of (confidence below 0.9).
Confirming or correcting one of these settles every scenario that depends on it.

### `irdai.ics-guidelines.2023.incident-reporting-6h` (confidence 0.6)

- **Clause** (Policy 2.10, 3.5 item 3, PDF page 224): "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- **Modelled as:** Report the cyber incident to CERT-In within 6 hours of noticing or being brought to notice, with a copy to IRDAI and other concerned regulators / authorities.
- **Why it is uncertain:** Two contested points. (1) Date: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year. (2) Scope: the sentence says 'cyber incidents' without 'as mentioned in Annexure I', so it is read as wider than CERT-In Direction (ii); the guidelines do not define the term. Both readings are the ones that never tell a user they owe less. The source bytes were not compared with the regulator's copy (robots.txt forbids automated access).
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.gov-order-information-72h` (confidence 0.6)

- **Clause** (Policy 2.24, 3.1 item 7, PDF page 298): "7. The Organization shall as soon as possible, but not later than seventy-two hours of the receipt of an order, provide information under its control or possession, or assistance to the Government agency which is lawfully authorized for investigative or protective or cybersecurity activities, for the purposes of verification of identity, or for the prevention, detection, investigation, or prosecution, of offences under any law for the time being in force, or for cyber security incidents."
- **Modelled as:** Provide the information or assistance as soon as possible, and not later than seventy-two hours of the receipt of the order.
- **Why it is uncertain:** The clock starts from receipt of an order, not from an incident. Policy 2.24 restates the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021; whether the entity is an intermediary under those Rules is not evaluated. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.grievance-acknowledge-24h` (confidence 0.6)

- **Clause** (Policy 2.24, 3.1 item 10(I) (acknowledge), PDF page 298): "acknowledge the complaint within twenty-four hours and dispose off such complaint within a period of fifteen days from the date of its receipt;"
- **Modelled as:** The Grievance Officer acknowledges the complaint within twenty-four hours.
- **Why it is uncertain:** The clock starts from receipt of a complaint. Policy 2.24 restates the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021; whether the entity is an intermediary under those Rules is not evaluated. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.grievance-dispose-15d` (confidence 0.6)

- **Clause** (Policy 2.24, 3.1 item 10(I) (dispose), PDF page 298): "acknowledge the complaint within twenty-four hours and dispose off such complaint within a period of fifteen days from the date of its receipt;"
- **Modelled as:** The Grievance Officer disposes of the complaint within fifteen days from the date of its receipt.
- **Why it is uncertain:** The clock starts from receipt of a complaint. Policy 2.24 restates the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021; whether the entity is an intermediary under those Rules is not evaluated. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.content-takedown-24h` (confidence 0.6)

- **Clause** (Policy 2.24, 3.1 item 11, PDF page 299): "11. The Organization shall within twenty-four hours from the receipt of a complaint made by an individual or any person on his behalf under this sub-rule, in relation to any content which is prima facie in the nature of any material which exposes the private area of such individual, shows such individual in full or partial nudity or shows or depicts such individual in any sexual act or conduct, or is in the nature of impersonation in an electronic form, including artificially morphed images of such individual, take all reasonable and practicable measures to remove or disable access to such content which is hosted, stored, published or transmitted by it."
- **Modelled as:** Within twenty-four hours of the complaint, take all reasonable and practicable measures to remove or disable access to the content.
- **Why it is uncertain:** The clock starts from receipt of a complaint. Policy 2.24 restates the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021; whether the entity is an intermediary under those Rules is not evaluated. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.registration-data-retention-180d` (confidence 0.6)

- **Clause** (Policy 2.24, 3.1 item 5, PDF page 297): "5. The Organization which collects information from a user for registration on the computer resource, shall retained his information for a period of one hundred and eighty days"
- **Modelled as:** Retain the user's registration information for one hundred and eighty days after any cancellation or withdrawal of the registration.
- **Why it is uncertain:** A retention period, not a deadline. The sentence continues on PDF page 298 ('after any cancellation or withdrawal of his registration'). Policy 2.24 restates the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021; whether the entity is an intermediary under those Rules is not evaluated. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.cloud-breach-notice-contract-clause` (confidence 0.6)

- **Clause** (Policy 2.19, 3.7.2, PDF page 283): "Organization shall contractually assure that they are informed of any confirmed breach immediately without any delay. For suspected breach, Organization shall be informed within 4 hours from the time of breach discovery."
- **Modelled as:** Ensure the cloud service contract requires the provider to inform the Organization of any confirmed breach immediately, and of a suspected breach within 4 hours of discovery.
- **Why it is uncertain:** A contract requirement on the Organization. The four hours bind the cloud provider under the contract; they are not a deadline for the Organization. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `irdai.ics-guidelines.2023.lost-device-internal-report-4h` (confidence 0.6)

- **Clause** (Policy 2.8, 3.5 item 3, PDF page 212): "3. In case of loss of device, the employee shall inform IT function within 4 hours."
- **Modelled as:** The employee informs the IT function within 4 hours of the loss of the device.
- **Why it is uncertain:** An internal duty (employee to IT function), not a report to a regulator. The clock starts from the loss of the device. Date contested: valid_from is the covering circular's date, 24 April 2023; that circular gives entities that had completed their FY 2022-23 security audit until the next financial year.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb` (confidence 0.5)

- **Clause** (Paragraph 141, note, PDF page 44): "(Note: In respect of Housing Finance Companies, cyber incidents shall continue to be reported to NHB and not RBI)"
- **Modelled as:** Report the cyber incident to NHB rather than RBI.
- **Why it is uncertain:** Contested conservative reading: the note redirects HFC reporting to NHB, but the text gives no time limit or channel for NHB; PT6H from detection is inherited from the surrounding sentence so the model never tells an HFC it owes less.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `rbi.payments-banks-cyber.2026.incident-reporting-6h` (confidence 0.8)

- **Clause** (Paragraph 181, first sentence, PDF page 44): "181. The bank shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- **Modelled as:** Report the cyber incident on RBI's DAKSH platform within six hours of detection.
- **Why it is uncertain:** Text is explicit on actor, duration, starting event and channel. The stored text is the version 'Updated as on October 01, 2026'; whether this paragraph read the same between 31 July and 1 October 2026 is not verified.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `rbi.payments-banks-cyber.2026.cert-in-notification` (confidence 0.8)

- **Clause** (Paragraph 181, second sentence, PDF page 44): "The bank shall also pro-actively notify CERT-In regarding cyber incidents."
- **Modelled as:** Pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding the cyber incident.
- **Why it is uncertain:** The sentence states a duty with no time limit or channel; modelled as applicable with no computed deadline. CERT-In's own six-hour duty is separate. The stored text is the version 'Updated as on October 01, 2026'; whether this paragraph read the same between 31 July and 1 October 2026 is not verified.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `rbi.payments-banks-cyber.2026.va-half-yearly` (confidence 0.8)

- **Clause** (Paragraph 150 (VA), PDF page 39): "150. For critical information systems and / or those in the DMZ having customer interface, VA shall be conducted at least once in every six months and PT at least once in 12 months."
- **Modelled as:** Conduct VA of critical information systems and / or those in the DMZ having customer interface at least once in every six months.
- **Why it is uncertain:** Text states the minimum frequency. Which systems are critical is not evaluated. The stored text is the version 'Updated as on October 01, 2026'; whether this paragraph read the same between 31 July and 1 October 2026 is not verified.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `rbi.payments-banks-cyber.2026.pt-annual` (confidence 0.8)

- **Clause** (Paragraph 150 (PT), PDF page 39): "150. For critical information systems and / or those in the DMZ having customer interface, VA shall be conducted at least once in every six months and PT at least once in 12 months."
- **Modelled as:** Conduct PT of critical information systems and / or those in the DMZ having customer interface at least once in 12 months.
- **Why it is uncertain:** Text states the minimum frequency. Which systems are critical is not evaluated. The stored text is the version 'Updated as on October 01, 2026'; whether this paragraph read the same between 31 July and 1 October 2026 is not verified.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.incident-reporting-6h` (confidence 0.7)

- **Clause** (RS.CO.S1 / Annexure-O Section B.1, PDF page 123): "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- **Modelled as:** Notify SEBI (via mkt_incidents@sebi.gov.in) and CERT-In within 6 hours of noticing/detecting or being brought to notice.
- **Why it is uncertain:** Scope is not contested: the applicability cell of row RS.CO.S1, RS.CO.S2, RS.CO.S3 on PDF page 123 reads "All REs (Mandatory)", and Annexure-O B.1 (page 200) says "experienced by REs". Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.incident-portal-24h` (confidence 0.6)

- **Clause** (RS.CO.S1 (Incident Reporting Portal), PDF page 123): "However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours."
- **Modelled as:** Report the necessary details of the incident on the SEBI Incident Reporting Portal within 24 hours.
- **Why it is uncertain:** The sentence names no separate starting event; it continues the six-hour sentence, and Annexure-O B.1 (page 200) joins them: "within 6 hours and SEBI Incident Reporting Portal within 24 hours". The six-hour anchors are used. Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.broker-dp-exchange-reporting-6h` (confidence 0.7)

- **Clause** (RS.CO.S1 (Stock Brokers/ Depository Participants), PDF page 123): "Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents."
- **Modelled as:** Also report the incident to the Stock Exchanges/ Depositories, along with SEBI and CERT-In, within 6 hours.
- **Why it is uncertain:** Text is explicit on actor, recipient, duration and starting events. Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.other-incidents-24h` (confidence 0.5)

- **Clause** (RS.CO.S1 (all other cybersecurity incidents), PDF page 123): "All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- **Modelled as:** Report the incident to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours.
- **Why it is uncertain:** Contested: the sentence names no starting event for the 24 hours. The six-hour anchors are used as the conservative reading. "As applicable" for NCIIPC is not evaluated. Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.nciipc-protected-system-report` (confidence 0.7)

- **Clause** (RS.CO.S1 item 3 (NCIIPC), PDF page 124): "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."
- **Modelled as:** Also report the incident to NCIIPC.
- **Why it is uncertain:** No time limit in the text; Annexure-O 3.1 (page 200) says "in a timely manner". Modelled as an applicable duty with no computed deadline. Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.post-incident-interim-report-3d` (confidence 0.6)

- **Clause** (Annexure-O B.3.3, Table 36 row 1, PDF page 201): "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- **Modelled as:** Submit the Interim Report to SEBI within 3 days.
- **Why it is uncertain:** Table 36 counts from "the date of reporting the incident or being brought to notice about the incident" (PDF page 201); the earlier known of the two is used. Whether "Days" runs from the timestamp or the calendar date is an open question; the timestamp reading is the earlier one. Row quoted in the scenario labels: "Interim Report* \n3 Days". Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.post-incident-mitigation-7d` (confidence 0.6)

- **Clause** (Annexure-O B.3.3, Table 36 row 2, PDF page 201): "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- **Modelled as:** Complete and submit the mitigation measure within 7 days.
- **Why it is uncertain:** Table 36 counts from "the date of reporting the incident or being brought to notice about the incident" (PDF page 201); the earlier known of the two is used. Whether "Days" runs from the timestamp or the calendar date is an open question; the timestamp reading is the earlier one. Row: "Mitigation measure \n7 Days". Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.post-incident-rca-30d` (confidence 0.6)

- **Clause** (Annexure-O B.3.3, Table 36 row 3, PDF page 201): "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- **Modelled as:** Submit the Root Cause Analysis (RCA) report within 30 days. Additional time may be provided by SEBI on a case-by-case basis on request of the RE.
- **Why it is uncertain:** Table 36 counts from "the date of reporting the incident or being brought to notice about the incident" (PDF page 201); the earlier known of the two is used. Whether "Days" runs from the timestamp or the calendar date is an open question; the timestamp reading is the earlier one. Row: "Root Cause Analysis (RCA) report** \n30 Days#". The footnote on page 202 says "Additional time may be provided by SEBI for the submission of RCA on a case-by-case basis on request of the RE". Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

### `sebi.cscrf.2024.post-incident-vapt-45d` (confidence 0.6)

- **Clause** (Annexure-O B.3.3, Table 36 row 5, PDF page 201): "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- **Modelled as:** Submit the VAPT for the incident and its closure reports within 45 days.
- **Why it is uncertain:** Table 36 counts from "the date of reporting the incident or being brought to notice about the incident" (PDF page 201); the earlier known of the two is used. Whether "Days" runs from the timestamp or the calendar date is an open question; the timestamp reading is the earlier one. Row: "closure reports \n45 days". Binding date contested: paragraph 17.1 states, "For six categories of REs where cybersecurity and cyber resilience circular already exists - by January 01, 2025." Paragraph 17.2 states, "For other REs where CSCRF is being issued for the first time - by April 01, 2025." (PDF page 9). Those are compliance glide-path dates. valid_from uses the circular issue date, 2024-08-20, so the tool does not tell a user they owe less pending legal review.
- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________

## Part B. Scenarios

## CERT-In Directions (2022) (17 scenarios)

### 1. `cert-in-ambiguous-anchor`

Incident occurred 2 hours before it was noticed.

- **Entity classes:** `service_provider`
- **Incident type(s) as stated:** unauthorized access
- **Occurred:** `2026-09-15T08:00:00+05:30`
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 2. `cert-in-attack-on-application`

Annexure I item x 'Attacks on Application such as E-Governance, E-Commerce' contains none of the usual attack keywords.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** Attacks on Application such as E-Governance, E-Commerce
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 3. `cert-in-attack-on-servers`

Annexure I item vi 'Attack on servers such as Database, Mail and DNS' uses no malware vocabulary.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** Attack on servers such as Database, Mail and DNS
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 4. `cert-in-before-directions-effective`

An incident on 5 Jan 2021, before the Directions took effect on 27 Jun 2022, evaluated today. The law that applies is the law as of the incident date, not as of the snapshot or evaluation date.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** ransomware
- **Noticed:** `2021-01-05T09:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2021-01-05`; regulators: none)

- No deadline is computed.
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `cert-in.directions-70b.2022.ntp-sync`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `cert-in.directions-70b.2022`, PDF page 4: "This direction will become effective after 60 days from the date on which it is issued."

- [ ] Correct   - [ ] Incorrect: ____________________

### 5. `cert-in-brought-to-notice`

An external party alerts the entity at 10:00 IST; the internal team only notices at 11:00 IST. The clock runs from the earlier trigger.

- **Entity classes:** `service_provider`
- **Incident type(s) as stated:** data leak
- **Occurred:** `2026-09-15T07:00:00+05:30`
- **Detected:** `2026-09-15T11:00:00+05:30`
- **Noticed:** `2026-09-15T11:00:00+05:30`
- **Brought to notice:** `2026-09-15T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from brought to notice)
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 6. `cert-in-cloud-outage-not-assumed`

A cloud region power outage mentions 'cloud' but is not obviously an attack. The engine may suggest item xviii but must ask, not start a clock.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** cloud region power outage
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(i) All service providers, intermediaries, data centres, body corporate and Government organisations shall connect to the Network Time Protocol (NTP) Server of National Informatics Centre (NIC) or National Physical Laboratory (NPL) or with NTP servers traceable to these NTP servers, for synchronisation of all their ICT systems clocks. Entities having ICT infrastructure spanning multiple geographies may also use accurate and standard time source other than NPL and NIC, however it is to be ensured that their time source shall not deviate from NPL and NIC."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 7. `cert-in-data-breach-unknown-time`

A service provider discovers a data breach but doesn't know when it was first noticed.

- **Entity classes:** `service_provider`
- **Incident type(s) as stated:** data breach
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-24`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`
- The tool must ask (question contains "noticed") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 8. `cert-in-detection-time-only`

Only a detection time is known. CERT-In's trigger is noticing / being brought to notice, so the engine must ask, not start from detection.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** ransomware
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`
- The tool must ask (question contains "noticed") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 9. `cert-in-government-org`

A government organisation with a website defacement. Direction (iii) on complying with CERT-In orders names service provider/intermediary/data centre/body corporate, not government organisations.

- **Entity classes:** `government_org`
- **Incident type(s) as stated:** website defacement
- **Occurred:** `2026-09-15T09:00:00+05:30`
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.designate-poc`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.log-retention-180d`
- Does not apply: `cert-in.directions-70b.2022.comply-with-orders`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(i) All service providers, intermediaries, data centres, body corporate and Government organisations shall connect to the Network Time Protocol (NTP) Server of National Informatics Centre (NIC) or National Physical Laboratory (NPL) or with NTP servers traceable to these NTP servers, for synchronisation of all their ICT systems clocks. Entities having ICT infrastructure spanning multiple geographies may also use accurate and standard time source other than NPL and NIC, however it is to be ensured that their time source shall not deviate from NPL and NIC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 10. `cert-in-nbfc-ransomware`

An NBFC (body corporate) discovers ransomware.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** malicious code; ransomware
- **Occurred:** `2026-09-15T08:00:00+05:30`
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.designate-poc`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.log-retention-180d`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.comply-with-orders`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 11. `cert-in-non-annexure-i-type`

The user attests that a simple hardware failure is NOT an Annexure I incident type.

- **Entity classes:** `body_corporate`
- **Incident type(s) as stated:** hardware failure
- **Occurred:** `2026-09-15T10:00:00+05:30`
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Personal data involved:** `False`
- **Attested Annexure I type:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.designate-poc`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.log-retention-180d`
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(i) All service providers, intermediaries, data centres, body corporate and Government organisations shall connect to the Network Time Protocol (NTP) Server of National Informatics Centre (NIC) or National Physical Laboratory (NPL) or with NTP servers traceable to these NTP servers, for synchronisation of all their ICT systems clocks. Entities having ICT infrastructure spanning multiple geographies may also use accurate and standard time source other than NPL and NIC, however it is to be ensured that their time source shall not deviate from NPL and NIC."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 12. `cert-in-noticed-before-brought`

Internal noticing at 09:00 IST, outside notification at 12:00 IST. The earlier trigger (noticing) starts the clock.

- **Entity classes:** `service_provider`
- **Incident type(s) as stated:** phishing
- **Noticed:** `2026-09-15T09:00:00+05:30`
- **Brought to notice:** `2026-09-15T12:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T15:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 13. `cert-in-retention-is-not-a-deadline`

A VPS provider with ransomware and a known occurrence time. The 5-year retention duty in Direction (v) must not become an incident deadline.

- **Entity classes:** `vps_provider`
- **Incident type(s) as stated:** ransomware
- **Occurred:** `2026-09-10T09:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-10`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Applies, with no computed deadline: `cert-in.directions-70b.2022.log-retention-180d`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 14. `cert-in-unattested-hardware-failure`

The user gives free text 'hardware failure' and does not attest. Free text must never conclude the incident is not reportable; the engine must ask.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(i) All service providers, intermediaries, data centres, body corporate and Government organisations shall connect to the Network Time Protocol (NTP) Server of National Informatics Centre (NIC) or National Physical Laboratory (NPL) or with NTP servers traceable to these NTP servers, for synchronisation of all their ICT systems clocks. Entities having ICT infrastructure spanning multiple geographies may also use accurate and standard time source other than NPL and NIC, however it is to be ensured that their time source shall not deviate from NPL and NIC."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 15. `cert-in-utc-input`

Noticed time supplied in UTC (04:30Z = 10:00 IST). The deadline instant must be identical regardless of the offset used.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** data leak
- **Noticed:** `2026-09-15T04:30:00+00:00`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 16. `cert-in-vps-provider`

A VPS provider experiences unauthorized access.

- **Entity classes:** `vps_provider`
- **Incident type(s) as stated:** unauthorized access
- **Occurred:** `2026-09-15T08:00:00+05:30`
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`
- Does not apply: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 3: "(v) Data Centres, Virtual Private Server (VPS) providers, Cloud Service providers and Virtual Private Network Service (VPN Service) providers, shall be required to register the following accurate information which must be maintained by them for a period of 5 years or longer duration as mandated by the law after any cancellation or withdrawal of the registration as the case may be: a. Validated names of subscribers/customers hiring the services b. Period of hire including dates c. IPs allotted to / being used by the members d. Email address and IP address and time stamp used at the time of registration / on-boarding e. Purpose for hiring services f. Validated address and contact numbers g. Ownership pattern of the subscribers / customers hiring services"

- [ ] Correct   - [ ] Incorrect: ____________________

### 17. `cert-in-wrong-entity-trap`

A virtual asset exchange reports a DDoS but is NOT a VPS/cloud provider.

- **Entity classes:** `virtual_asset_exchange`
- **Incident type(s) as stated:** DDoS
- **Occurred:** `2026-09-15T09:00:00+05:30`
- **Detected:** `2026-09-15T10:00:00+05:30`
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- Deadline `2026-09-15T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `cert-in.directions-70b.2022.virtual-asset-kyc-5y`
- Does not apply: `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 4: "(vi) The virtual asset service providers, virtual asset exchange providers and custodian wallet providers (as defined by Ministry of Finance from time to time) shall mandatorily maintain all information obtained as part of Know Your Customer (KYC) and records of financial transactions for a period of five years so as to ensure cyber security in the area of payments and financial markets for citizens while protecting their data, fundamental rights and economic freedom in view of the growth of virtual assets. For the purpose of KYC, the Reserve Bank of India (RBI) Directions 2016 / Securities and Exchange Board of India (SEBI) circular dated April 24, 2020 / Department of Telecom (DoT) notice September 21, 2021 mandated procedures as amended from time to time may be referred to as per Annexure III. With respect to transaction records, accurate information shall be maintained in such a way that individual transaction can be reconstructed along with the relevant elements comprising of, but not limited to, information relating to the identification of the relevant parties including IP addresses along with timestamps and time zones, transaction ID, the public keys (or equivalent identifiers), addresses or accounts involved (or equivalent identifiers), the nature and date of the transaction, and the amount transferred."

- [ ] Correct   - [ ] Incorrect: ____________________

## DPDP Rules 2025, Rule 7 (8 scenarios)

### 18. `dpdp-awareness-later-than-occurrence`

Adversarial anchor test: A breach occurred on 2027-06-01 but the Data Fiduciary only internally noticed and became aware of the breach on 2027-06-03. DPDP 72-hour board reporting starts strictly from awareness.

- **Entity classes:** `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Data breach
- **Occurred:** `2027-06-01T09:00:00+05:30`
- **Detected:** `2027-06-03T09:00:00+05:30`
- **Noticed:** `2027-06-03T09:00:00+05:30`
- **Became aware (DPDP):** `2027-06-03T09:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-06-01`; regulators: CERT-In, MeitY)

- Deadline `2027-06-03T09:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-06T03:30:00Z` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)

**Clauses relied on**

- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf, — (i) updated and detailed information in respect of such description; (ii) the broad facts related to the events, circumstances and reasons leading to the breach; (iii) measures implemented or proposed, if any, to mitigate risk; (iv) any findings regarding the person who caused the breach; (v) remedial measures taken to prevent recurrence of such breach; and (vi) a report regarding the intimations given to affected Data Principals."

- [ ] Correct   - [ ] Incorrect: ____________________

### 19. `dpdp-awareness-unknown`

Adversarial missing fact test: In June 2027, a personal data breach is detected and noticed, but the exact timestamp when the entity became aware of the breach is unknown. The engine must emit an Unknown asking for awareness time.

- **Entity classes:** `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Data breach
- **Detected:** `2027-06-15T10:00:00+05:30`
- **Noticed:** `2027-06-15T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-06-15`; regulators: CERT-In, MeitY)

- Deadline `2027-06-15T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- The tool must ask (question contains "When did the entity become aware of the personal data breach?") before deciding `meity.dpdp-rules.2025.rule7-2-b-board-detailed`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf, —"

- [ ] Correct   - [ ] Incorrect: ____________________

### 20. `dpdp-commencement-after-may-2027`

In June 2027 (after DPDP Rules 2025 Rule 7 commencement on 13 May 2027), a Data Fiduciary becomes aware of a personal data breach. Dual reporting to CERT-In (6h) and DPDP (72h detailed report + without delay intimation) applies.

- **Entity classes:** `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Data breach
- **Occurred:** `2027-06-01T10:00:00+05:30`
- **Detected:** `2027-06-01T10:00:00+05:30`
- **Noticed:** `2027-06-01T10:00:00+05:30`
- **Became aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-06-01`; regulators: CERT-In, MeitY)

- Deadline `2027-06-01T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-04T04:30:00Z` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)
- Applies, with no computed deadline: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Applies, with no computed deadline: `meity.dpdp-rules.2025.rule7-2-a-board-initial`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-2-a-board-initial`

**Clauses relied on**

- `meity.dpdp-rules.2025`, PDF page 26: "(1) On becoming aware of any personal data breach, the Data Fiduciary shall, to the best of its knowledge, intimate to each affected Data Principal, in a concise, clear and plain manner and without delay, through her user account or any mode of communication registered by her with the Data Fiduciary, — (a) a description of the breach, including its nature, extent and the timing of its occurrence; (b) the consequences relevant to her, that are likely to arise from the breach; (c) the measures implemented and being implemented by the Data Fiduciary, if any, to mitigate risk; (d) the safety measures that she may take to protect her interests; and (e) business contact information of a person who is able to respond on behalf of the Data Fiduciary, to queries, if any, of the Data Principal."

- [ ] Correct   - [ ] Incorrect: ____________________

### 21. `dpdp-commencement-before-may-2027`

Adversarial commencement test: An incident occurs in September 2026. DPDP Rules 2025 Rule 7 comes into force on 13 May 2027 (18 months after publication in Gazette GSR 846(E)). DPDP duties must be marked not yet valid.

- **Entity classes:** `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware; Data breach
- **Occurred:** `2026-09-01T10:00:00+05:30`
- **Detected:** `2026-09-01T10:00:00+05:30`
- **Noticed:** `2026-09-01T10:00:00+05:30`
- **Became aware (DPDP):** `2026-09-01T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-09-01`; regulators: CERT-In)

- Deadline `2026-09-01T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Does not apply: `meity.dpdp-rules.2025.rule7-2-a-board-initial`
- Does not apply: `meity.dpdp-rules.2025.rule7-2-b-board-detailed`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `meity.dpdp-rules.2025`, PDF page 24: "(4) Rules 3, 5 to 16, 22 and 23 shall come into force eighteen months after the date of publication of this Gazette."

- [ ] Correct   - [ ] Incorrect: ____________________

### 22. `dpdp-multi-regulator-cert-in`

Multi-regulator overlap test: In July 2027, an online platform that is a Data Fiduciary suffers a major ransomware incident exfiltrating customer records. Dual reporting to CERT-In (6 hours from noticing) and DPDP (72 hours from awareness, plus without delay intimation) applies.

- **Entity classes:** `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware; Data breach
- **Occurred:** `2027-07-01T08:00:00+05:30`
- **Detected:** `2027-07-01T10:00:00+05:30`
- **Noticed:** `2027-07-01T10:00:00+05:30`
- **Became aware (DPDP):** `2027-07-01T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-07-01`; regulators: CERT-In, MeitY)

- Deadline `2027-07-01T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-07-04T04:30:00Z` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)

**Clauses relied on**

- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf, — (i) updated and detailed information in respect of such description; (ii) the broad facts related to the events, circumstances and reasons leading to the breach; (iii) measures implemented or proposed, if any, to mitigate risk; (iv) any findings regarding the person who caused the breach; (v) remedial measures taken to prevent recurrence of such breach; and (vi) a report regarding the intimations given to affected Data Principals."

- [ ] Correct   - [ ] Incorrect: ____________________

### 23. `dpdp-no-personal-data`

Adversarial condition test: In June 2027, a Data Fiduciary suffers a server failure without any personal data breach (personal_data_involved = false). DPDP Rule 7 breach notification duties do not apply.

- **Entity classes:** `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Attacks on servers such as Database, Mail and DNS
- **Occurred:** `2027-06-25T16:00:00+05:30`
- **Detected:** `2027-06-25T16:00:00+05:30`
- **Noticed:** `2027-06-25T16:00:00+05:30`
- **Became aware (DPDP):** `2027-06-25T16:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-06-25`; regulators: CERT-In)

- Deadline `2027-06-25T16:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `meity.dpdp-rules.2025`, PDF page 26: "(1) On becoming aware of any personal data breach, the Data Fiduciary shall, to the best of its knowledge, intimate to each affected Data Principal, in a concise, clear and plain manner and without delay, through her user account or any mode of communication registered by her with the Data Fiduciary, —"

- [ ] Correct   - [ ] Incorrect: ____________________

### 24. `dpdp-non-fiduciary-entity`

Adversarial entity scope test: A pure body corporate that is not a Data Fiduciary suffers a cyber incident in June 2027. DPDP Rule 7 fiduciary obligations must be marked entity_class_mismatch.

- **Entity classes:** `body_corporate`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Occurred:** `2027-06-01T10:00:00+05:30`
- **Detected:** `2027-06-01T10:00:00+05:30`
- **Noticed:** `2027-06-01T10:00:00+05:30`
- **Became aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-06-01`; regulators: CERT-In)

- Deadline `2027-06-01T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Does not apply: `meity.dpdp-rules.2025.rule7-2-a-board-initial`
- Does not apply: `meity.dpdp-rules.2025.rule7-2-b-board-detailed`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `meity.dpdp-rules.2025`, PDF page 26: "(1) On becoming aware of any personal data breach, the Data Fiduciary shall, to the best of its knowledge, intimate to each affected Data Principal, in a concise, clear and plain manner and without delay, through her user account or any mode of communication registered by her with the Data Fiduciary, —"

- [ ] Correct   - [ ] Incorrect: ____________________

### 25. `dpdp-significant-data-fiduciary`

A Significant Data Fiduciary (SDF) designated under DPDP Act Section 10 suffers a large-scale personal data breach in June 2027. DPDP Rule 7 detailed reporting duty applies.

- **Entity classes:** `dpdp.significant_data_fiduciary`
- **Incident type(s) as stated:** Data breach
- **Occurred:** `2027-06-15T14:00:00+05:30`
- **Detected:** `2027-06-15T14:00:00+05:30`
- **Noticed:** `2027-06-15T14:00:00+05:30`
- **Became aware (DPDP):** `2027-06-15T14:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2027-06-15`; regulators: CERT-In, MeitY)

- Deadline `2027-06-15T14:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-18T08:30:00Z` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)

**Clauses relied on**

- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf, — (i) updated and detailed information in respect of such description; (ii) the broad facts related to the events, circumstances and reasons leading to the breach; (iii) measures implemented or proposed, if any, to mitigate risk; (iv) any findings regarding the person who caused the breach; (v) remedial measures taken to prevent recurrence of such breach; and (vi) a report regarding the intimations given to affected Data Principals."

- [ ] Correct   - [ ] Incorrect: ____________________

## SEBI CSCRF (2024) (24 scenarios)

### 26. `sebi-anchor-detection-vs-noticing`

Adversarial anchor test: A Small-size RE detects an incident via automated SIEM alert at 08:00 IST, which was internally reviewed/noticed by security staff at 10:00 IST on 2025-08-01. SEBI CSCRF specifies within 6 hours of noticing/detecting or being brought to notice; the earlier trigger anchors the clock.

- **Entity classes:** `sebi.small_re`
- **Incident type(s) as stated:** Scanning/probing of critical networks/systems
- **Occurred:** `2025-08-01T08:00:00+05:30`
- **Detected:** `2025-08-01T08:00:00+05:30`
- **Noticed:** `2025-08-01T10:00:00+05:30`
- **Became aware (DPDP):** `2025-08-01T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2025-08-01`; regulators: CERT-In, SEBI)

- Deadline `2025-08-01T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-08-01T08:30:00Z` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from detection)
- Deadline `2025-08-02T02:30:00+00:00` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from detection)
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"

- [ ] Correct   - [ ] Incorrect: ____________________

### 27. `sebi-broker-also-reports-to-exchange`

A small-size RE that is also a stock broker must additionally report to the stock exchange within six hours.

- **Entity classes:** `sebi.small_re`, `sebi.stock_broker`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.broker-dp-exchange-reporting-6h` (PT6H from noticing)
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 28. `sebi-broker-role-only-still-owes-re-duties`

A profile that holds only the stock broker role, with no size category selected, still owes every duty that binds REs.

- **Entity classes:** `sebi.stock_broker`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.broker-dp-exchange-reporting-6h` (PT6H from noticing)
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 123: "All REs (Mandatory)"
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 29. `sebi-incident-before-issue-date`

A SEBI MII notices ransomware before the CSCRF circular issue date; CERT-In applies and SEBI is not yet valid.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2024-08-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2024-08-01`; regulators: CERT-In)

- Deadline `2024-08-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `sebi.cscrf.2024.incident-reporting-6h`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `sebi.cscrf.2024`, PDF page 1: "August 20, 2024"

- [ ] Correct   - [ ] Incorrect: ____________________

### 30. `sebi-incident-between-issue-and-glide-path-contested`

Conservative reading pending legal review: the SEBI duty is applied after issue but before the paragraph 17 glide-path dates; see J2.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2024-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2024-10-01`; regulators: CERT-In, SEBI)

- Deadline `2024-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2024-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2024-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Applies, with no computed deadline: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 31. `sebi-midsize-re-unauthorized-access`

A Mid-size Regulated Entity experiences unauthorized access of IT systems and data on 2025-07-01 at 12:00 IST. Dual reporting to CERT-In (6h) and SEBI (6h) applies.

- **Entity classes:** `sebi.midsize_re`
- **Incident type(s) as stated:** Unauthorised access of IT systems/data
- **Occurred:** `2025-07-01T12:00:00+05:30`
- **Detected:** `2025-07-01T12:00:00+05:30`
- **Noticed:** `2025-07-01T12:00:00+05:30`
- **Became aware (DPDP):** `2025-07-01T12:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2025-07-01`; regulators: CERT-In, SEBI)

- Deadline `2025-07-01T12:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-07-01T12:30:00Z` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-07-02T06:30:00+00:00` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"

- [ ] Correct   - [ ] Incorrect: ____________________

### 32. `sebi-mii-also-data-fiduciary-2027`

One incident profile carries both SEBI MII and DPDP Data Fiduciary classes, so all applicable regimes are evaluated.

- **Entity classes:** `sebi.mii`, `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware; Data breach
- **Detected:** `2027-06-01T10:00:00+05:30`
- **Noticed:** `2027-06-01T10:00:00+05:30`
- **Became aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2027-06-01`; regulators: CERT-In, SEBI, MeitY)

- Deadline `2027-06-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-04T10:00:00+05:30` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)
- Deadline `2027-06-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Applies, with no computed deadline: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Applies, with no computed deadline: `meity.dpdp-rules.2025.rule7-2-a-board-initial`
- Applies, with no computed deadline: `sebi.cscrf.2024.nciipc-protected-system-report`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-2-a-board-initial`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf, — (i) updated and detailed information in respect of such description; (ii) the broad facts related to the events, circumstances and reasons leading to the breach; (iii) measures implemented or proposed, if any, to mitigate risk; (iv) any findings regarding the person who caused the breach; (v) remedial measures taken to prevent recurrence of such breach; and (vi) a report regarding the intimations given to affected Data Principals."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 33. `sebi-mii-attested-not-annexure-i`

The same hardware failure is explicitly attested not to be an Annexure I incident type.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `sebi.cscrf.2024.incident-reporting-6h`
- The tool must ask (question contains "cybersecurity incident") before deciding `sebi.cscrf.2024.other-incidents-24h`
- The tool must ask (question contains "cybersecurity incident") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "cybersecurity incident") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "cybersecurity incident") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "cybersecurity incident") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`
- The tool must ask (question contains "cybersecurity incident") before deciding `sebi.cscrf.2024.nciipc-protected-system-report`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 34. `sebi-mii-hardware-failure-unattested`

A SEBI MII reports a hardware failure without attesting that it is an Annexure I type; free text never excludes either structured 6-hour duty.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-09-15T10:00:00+05:30`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2026-09-15`; regulators: CERT-In)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.ntp-sync`
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.incident-reporting-6h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.incident-portal-24h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.other-incidents-24h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.nciipc-protected-system-report`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 35. `sebi-mii-ransomware-6h`

A Market Infrastructure Institution (MII) detects ransomware on 2025-05-15 at 10:00 IST. Dual reporting to CERT-In (6h) and SEBI (6h to mkt_incidents@sebi.gov.in per Annexure O) applies.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Occurred:** `2025-05-15T10:00:00+05:30`
- **Detected:** `2025-05-15T10:00:00+05:30`
- **Noticed:** `2025-05-15T10:00:00+05:30`
- **Became aware (DPDP):** `2025-05-15T10:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2025-05-15`; regulators: CERT-In, SEBI)

- Deadline `2025-05-15T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-05-15T10:30:00Z` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-05-16T04:30:00+00:00` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Applies, with no computed deadline: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 36. `sebi-missing-anchor-unknown`

Adversarial missing fact test: A Self-certification RE discovers a cyber incident on 2025-09-01, but does not record when it was first noticed or detected. The engine must emit an Unknown asking for the noticing/detection timestamp.

- **Entity classes:** `sebi.selfcert_re`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2025-09-01`; regulators: CERT-In, SEBI)

- No deadline is computed.
- Applies, with no computed deadline: `cert-in.directions-70b.2022.incident-reporting-6h`
- Applies, with no computed deadline: `sebi.cscrf.2024.incident-reporting-6h`
- The tool must ask (question contains "When was the incident first noticed or brought to notice?") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "When was the incident first noticed, detected, or brought to notice?") before deciding `sebi.cscrf.2024.incident-reporting-6h`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`
- The tool must ask (question contains "When was the incident first noticed, detected, or brought to notice?") before deciding `sebi.cscrf.2024.incident-portal-24h`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"

- [ ] Correct   - [ ] Incorrect: ____________________

### 37. `sebi-nbfc-is-not-a-sebi-re`

A Middle Layer NBFC is not a SEBI regulated entity: no SEBI duty and no SEBI question, while its RBI and CERT-In clocks run.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Does not apply: `sebi.cscrf.2024.incident-reporting-6h`
- Does not apply: `sebi.cscrf.2024.incident-portal-24h`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- Does not apply: `sebi.cscrf.2024.post-incident-interim-report-3d`
- Does not apply: `sebi.cscrf.2024.post-incident-mitigation-7d`
- Does not apply: `sebi.cscrf.2024.post-incident-rca-30d`
- Does not apply: `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "All REs (Mandatory)"
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in these Directions shall be applicable to all Non- Banking Financial Companies (hereinafter collectively referred to as 'NBFCs' and individually as 'NBFC') registered with RBI under the provisions of the RBI Act, 1934, Factoring Regulation Act, 2011, National Housing Bank (NHB) Act, 1987, unless specified otherwise."
- `rbi.nbfc-cyber.2026`, PDF page 43: "141. The NBFC shall report cyber incidents to RBI within six hours of detection on DAKSH platform"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 38. `sebi-non-broker-no-exchange-duty`

A small-size RE that is not a broker or depository participant has no exchange-reporting duty.

- **Entity classes:** `sebi.small_re`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 39. `sebi-non-sebi-entity-bank-trap`

Adversarial entity scope test: A scheduled commercial bank suffers a ransomware incident on 2025-06-01. The bank is regulated by RBI/CERT-In, not SEBI. SEBI CSCRF obligations must be marked entity_class_mismatch.

- **Entity classes:** `bank`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Occurred:** `2025-06-01T08:00:00+05:30`
- **Detected:** `2025-06-01T10:00:00+05:30`
- **Noticed:** `2025-06-01T10:00:00+05:30`
- **Became aware (DPDP):** `2025-06-01T10:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2025-06-01`; regulators: CERT-In)

- Deadline `2025-06-01T10:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `sebi.cscrf.2024.incident-reporting-6h`

**Clauses relied on**

- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 40. `sebi-not-a-cyber-incident`

The user attests the event is neither an Annexure I type nor a cyber incident: no SEBI reporting duty and no questions.

- **Entity classes:** `sebi.midsize_re`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- No deadline is computed.
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `sebi.cscrf.2024.incident-reporting-6h`
- Does not apply: `sebi.cscrf.2024.incident-portal-24h`
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- Does not apply: `sebi.cscrf.2024.post-incident-interim-report-3d`
- Does not apply: `sebi.cscrf.2024.post-incident-mitigation-7d`
- Does not apply: `sebi.cscrf.2024.post-incident-rca-30d`
- Does not apply: `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."

- [ ] Correct   - [ ] Incorrect: ____________________

### 41. `sebi-other-incident-24h`

A cybersecurity incident attested not to be a CERT-In Annexure I type is an 'other' incident: 24 hours, on the contested conservative anchor. No six-hour duty.

- **Entity classes:** `sebi.midsize_re`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.other-incidents-24h` (PT24H from noticing)
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `sebi.cscrf.2024.incident-reporting-6h`
- Does not apply: `sebi.cscrf.2024.incident-portal-24h`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"

- [ ] Correct   - [ ] Incorrect: ____________________

### 42. `sebi-other-incident-unresolved-asks`

Free text that matches no Annexure I type and no attestation: the engine must ask, because the answer decides between the six-hour and the 24-hour duties.

- **Entity classes:** `sebi.midsize_re`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- No deadline is computed.
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.incident-reporting-6h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.incident-portal-24h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.other-incidents-24h`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "Annexure I") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 43. `sebi-portal-24h-after-noticing`

A SEBI MII notices ransomware. The portal filing is due 24 hours after the same starting event as the six-hour duty; the post-incident clocks cannot start until the report time is known.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 200: "1. Any cyber-attack(s), cybersecurity incident(s) and breach(es) experienced by REs falling under CERT-In Cybersecurity directions37 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared to SEBI through the email ID mkt_incidents@sebi.gov.in within 6 hours and SEBI Incident Reporting Portal within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 44. `sebi-post-incident-brought-to-notice-earlier`

Table 36 counts from reporting or being brought to notice; the earlier known time wins. No noticing time is given, so the six-hour clocks run from being brought to notice.

- **Entity classes:** `sebi.qualified_re`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Brought to notice:** `2026-10-01T09:00:00+05:30`
- **Reported to SEBI:** `2026-10-01T15:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T15:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from brought to notice)
- Deadline `2026-10-01T15:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from brought to notice)
- Deadline `2026-10-02T09:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from brought to notice)
- Deadline `2026-10-04T09:00:00+05:30` for `sebi.cscrf.2024.post-incident-interim-report-3d` (P3D from brought to notice)
- Deadline `2026-10-08T09:00:00+05:30` for `sebi.cscrf.2024.post-incident-mitigation-7d` (P7D from brought to notice)
- Deadline `2026-10-31T09:00:00+05:30` for `sebi.cscrf.2024.post-incident-rca-30d` (P30D from brought to notice)
- Deadline `2026-11-15T09:00:00+05:30` for `sebi.cscrf.2024.post-incident-vapt-45d` (P45D from brought to notice)
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 45. `sebi-post-incident-reports-from-report-date`

The four Table 36 clocks run from the time the incident was reported to SEBI.

- **Entity classes:** `sebi.qualified_re`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Reported to SEBI:** `2026-10-01T15:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Deadline `2026-10-04T15:00:00+05:30` for `sebi.cscrf.2024.post-incident-interim-report-3d` (P3D from reported)
- Deadline `2026-10-08T15:00:00+05:30` for `sebi.cscrf.2024.post-incident-mitigation-7d` (P7D from reported)
- Deadline `2026-10-31T15:00:00+05:30` for `sebi.cscrf.2024.post-incident-rca-30d` (P30D from reported)
- Deadline `2026-11-15T15:00:00+05:30` for `sebi.cscrf.2024.post-incident-vapt-45d` (P45D from reported)
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.nciipc-protected-system-report`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 202: "# Additional time may be provided by SEBI for the submission of RCA on a case-by-case basis on request of the RE"
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 46. `sebi-protected-system-reports-to-nciipc`

An MII whose systems NCIIPC has identified as a Protected system must also report to NCIIPC; the text gives no time limit.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Applies, with no computed deadline: `sebi.cscrf.2024.nciipc-protected-system-report`
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 47. `sebi-protected-system-unknown-asks`

Protected-system status is not given: the engine asks, and the six-hour duty is unaffected.

- **Entity classes:** `sebi.mii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, SEBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T10:00:00+05:30` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Does not apply: `sebi.cscrf.2024.other-incidents-24h`
- Does not apply: `sebi.cscrf.2024.broker-dp-exchange-reporting-6h`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`
- The tool must ask (question contains "Protected system") before deciding `sebi.cscrf.2024.nciipc-protected-system-report`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."
- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 48. `sebi-qualified-re-ddos`

A Qualified Regulated Entity experiences a Distributed Denial of Service (DDoS) attack on its public trading API. Reporting to CERT-In (6h) and SEBI (6h) applies.

- **Entity classes:** `sebi.qualified_re`
- **Incident type(s) as stated:** Denial of Service (DoS) and Distributed Denial of Service (DDoS) attacks
- **Occurred:** `2025-06-10T08:00:00+05:30`
- **Detected:** `2025-06-10T08:00:00+05:30`
- **Noticed:** `2025-06-10T08:00:00+05:30`
- **Became aware (DPDP):** `2025-06-10T08:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `True`

**Expected** (law as of `2025-06-10`; regulators: CERT-In, SEBI)

- Deadline `2025-06-10T08:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-06-10T08:30:00Z` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-06-11T02:30:00+00:00` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- Applies, with no computed deadline: `sebi.cscrf.2024.nciipc-protected-system-report`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"
- `sebi.cscrf.2024`, PDF page 124: "Additionally, the REs, whose systems have been identified as “Protected system” by NCIIPC shall also report the incident to NCIIPC."

- [ ] Correct   - [ ] Incorrect: ____________________

### 49. `sebi-selfcert-re-incident`

A Self-certification Regulated Entity experiences a cyber security incident. Reporting to CERT-In (6h) and SEBI (6h) applies.

- **Entity classes:** `sebi.selfcert_re`
- **Incident type(s) as stated:** Attacks or malicious activities affecting systems / applications like Phishing
- **Occurred:** `2025-07-15T11:00:00+05:30`
- **Detected:** `2025-07-15T11:00:00+05:30`
- **Noticed:** `2025-07-15T11:00:00+05:30`
- **Became aware (DPDP):** `2025-07-15T11:00:00+05:30`
- **Personal data involved:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2025-07-15`; regulators: CERT-In, SEBI)

- Deadline `2025-07-15T11:30:00Z` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-07-15T11:30:00Z` for `sebi.cscrf.2024.incident-reporting-6h` (PT6H from noticing)
- Deadline `2025-07-16T05:30:00+00:00` for `sebi.cscrf.2024.incident-portal-24h` (PT24H from noticing)
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-interim-report-3d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-mitigation-7d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-rca-30d`
- The tool must ask (question contains "reported to SEBI") before deciding `sebi.cscrf.2024.post-incident-vapt-45d`

**Clauses relied on**

- `sebi.cscrf.2024`, PDF page 123: "1. Any cyber-attack, cybersecurity incident and/ or breach falling under CERT-In Cybersecurity directions29 shall be notified to SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. This information shall be shared with SEBI through the mkt_incidents@sebi.gov.in within 6 hours. However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours. Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents. All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."
- `sebi.cscrf.2024`, PDF page 201: "3.3. RE shall undertake the necessary activities and submit the relevant reports as per the following timelines: Table 36: Timelines for post-cyber incident activity(ies) and report submission S. No. Name of the Report/ Activity Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident) 1 Interim Report* 3 Days 2 Mitigation measure 7 Days 3 Root Cause Analysis (RCA) report** 30 Days# 4 Forensic Audit Report (on the incident) and its closure report Refer clause 3.4 below 5 Vulnerability Assessment and Penetration Testing (VAPT) for the incident and its closure reports 45 days"

- [ ] Correct   - [ ] Incorrect: ____________________

## RBI cybersecurity Directions (2026) (31 scenarios)

### 50. `rbi-aifi-hardware-failure-unattested`

Free text that matches nothing: the engine asks both the CERT-In question and the RBI cyber-incident question.

- **Entity classes:** `aifi`
- **Incident type(s) as stated:** hardware failure
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- No deadline is computed.
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "cyber incident") before deciding `rbi.aifi-cyber.2026.incident-reporting-6h`
- The tool must ask (question contains "cyber incident") before deciding `rbi.aifi-cyber.2026.cert-in-notification`

**Clauses relied on**

- `rbi.aifi-cyber.2026`, PDF page 5: "A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not."
- `rbi.aifi-cyber.2026`, PDF page 39: "177. The AIFI shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 51. `rbi-aifi-ransomware`

An All India Financial Institution: reporting, CERT-In notification, VA and PT all apply.

- **Entity classes:** `aifi`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.aifi-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.aifi-cyber.2026.cert-in-notification`
- Applies, with no computed deadline: `rbi.aifi-cyber.2026.va-half-yearly`
- Applies, with no computed deadline: `rbi.aifi-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.aifi-cyber.2026`, PDF page 39: "177. The AIFI shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `rbi.aifi-cyber.2026`, PDF page 39: "The AIFI shall also pro-actively notify CERT-In regarding cyber incidents."
- `rbi.aifi-cyber.2026`, PDF page 35: "146. For critical information systems and / or those in the DMZ having customer interface, VA shall be conducted at least once in every six months and PT at least once in 12 months."
- `rbi.aifi-cyber.2026`, PDF page 4: "These Directions shall be applicable to All-India Financial Institutions"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 52. `rbi-bank-is-not-an-nbfc`

A bank is a body corporate for CERT-In but is not covered by the NBFC-specific RBI Direction.

- **Entity classes:** `bank`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.incident-reporting-6h`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.cert-in-notification`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.va-half-yearly`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in these Directions shall be applicable to all Non- Banking Financial Companies"
- `cert-in.directions-70b.2022`, PDF page 2: "Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents"
- `rbi.payments-banks-cyber.2026`, PDF page 4: "These Directions shall be applicable to Payments Banks"

- [ ] Correct   - [ ] Incorrect: ____________________

### 53. `rbi-base-layer-without-size-must-ask`

Base Layer without an asset-size band leaves Chapter IV unresolved but cannot imply a Chapter V duty.

- **Entity classes:** `nbfc.base_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."

- [ ] Correct   - [ ] Incorrect: ____________________

### 54. `rbi-bl-above-500cr-ransomware`

A Base Layer NBFC at or above ₹500 crore receives the Chapter IV reporting duty, not Chapter V duties.

- **Entity classes:** `nbfc.bl_500cr_and_above`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h` (PT6H from detection)
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 3: "(3) The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."
- `rbi.nbfc-cyber.2026`, PDF page 18: "28. The NBFC shall report cyber incidents on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in) within six hours of detection."
- `cert-in.directions-70b.2022`, PDF page 2: "mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 55. `rbi-bl-below-500cr-no-reporting-duty`

A below-₹500-crore Base Layer NBFC is in Chapter III, which contains no RBI incident-reporting duty.

- **Entity classes:** `nbfc.bl_below_500cr`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter III shall be applicable only for NBFCs- Base Layer (NBFCs-BL) with asset size below ₹500 crore, and Core Investment Companies (CICs)"
- `cert-in.directions-70b.2022`, PDF page 2: "mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 56. `rbi-cic-in-middle-layer-excluded`

A profile carrying both Middle Layer and CIC must be excluded from every Chapter V duty.

- **Entity classes:** `nbfc.middle_layer`, `nbfc.cic`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "Middle Layer (NBFCs-ML) as defined in Reserve Bank of India (Non- Banking Financial Companies – Registration, Exemptions and Framework for Scale Based Regulation) Directions, 2025, excluding CICs."
- `cert-in.directions-70b.2022`, PDF page 2: "mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 57. `rbi-cic-without-layer-must-ask-category`

A CIC role alone leaves the Chapter IV layer question open while its Chapter V exclusion remains decisive.

- **Entity classes:** `nbfc.cic`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter III shall be applicable only for NBFCs- Base Layer (NBFCs-BL) with asset size below ₹500 crore, and Core Investment Companies (CICs)"

- [ ] Correct   - [ ] Incorrect: ____________________

### 58. `rbi-contradictory-attestation-caveat`

A negative RBI cyber-incident attestation controls applicability but conflicts visibly with a ransomware type match.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested a cyber incident:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- The result must carry a warning containing "re-check"

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "‘Cyber Incident’ - A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not."

- [ ] Correct   - [ ] Incorrect: ____________________

### 59. `rbi-detected-before-noticed`

RBI and CERT-In clocks diverge when detection precedes noticing.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T08:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T14:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 43: "within six hours of detection"
- `cert-in.directions-70b.2022`, PDF page 2: "within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 60. `rbi-detection-time-unknown`

A Middle Layer NBFC knows the CERT-In noticing time but not RBI's distinct detection anchor.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "detected") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 43: "141. The NBFC shall report cyber incidents to RBI within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System -"
- `cert-in.directions-70b.2022`, PDF page 2: "within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 61. `rbi-each-direction-keeps-to-its-own-entities`

A Middle Layer NBFC gets the NBFC Direction's duties and none from the UCB, AIFI or Payments Banks Directions.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Does not apply: `rbi.ucb-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.ucb-cyber.2026.cert-in-notification`
- Does not apply: `rbi.ucb-cyber.2026.va-half-yearly`
- Does not apply: `rbi.ucb-cyber.2026.pt-annual`
- Does not apply: `rbi.aifi-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.aifi-cyber.2026.cert-in-notification`
- Does not apply: `rbi.aifi-cyber.2026.va-half-yearly`
- Does not apply: `rbi.aifi-cyber.2026.pt-annual`
- Does not apply: `rbi.payments-banks-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.payments-banks-cyber.2026.cert-in-notification`
- Does not apply: `rbi.payments-banks-cyber.2026.va-half-yearly`
- Does not apply: `rbi.payments-banks-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.payments-banks-cyber.2026`, PDF page 4: "These Directions shall be applicable to Payments Banks"
- `rbi.aifi-cyber.2026`, PDF page 4: "These Directions shall be applicable to All-India Financial Institutions"
- `rbi.ucb-cyber.2026`, PDF page 4: "For the purpose of these Directions, a UCB is categorised into one of the four levels based on its digital depth and interconnectedness to the payment systems landscape. Depending on the UCB category, the applicability of Chapter II to Chapter VI of these Directions is as given below:"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 62. `rbi-generic-bank-is-asked-its-kind`

A bank whose kind is not given: only the Payments Banks Direction is in the dataset, so the engine asks and does not say that no RBI duty applies.

- **Entity classes:** `bank`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.ucb-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.ucb-cyber.2026.cert-in-notification`
- Does not apply: `rbi.ucb-cyber.2026.va-half-yearly`
- Does not apply: `rbi.ucb-cyber.2026.pt-annual`
- Does not apply: `rbi.aifi-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.aifi-cyber.2026.cert-in-notification`
- Does not apply: `rbi.aifi-cyber.2026.va-half-yearly`
- Does not apply: `rbi.aifi-cyber.2026.pt-annual`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.incident-reporting-6h`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.cert-in-notification`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.va-half-yearly`
- The tool must ask (question contains "kind of bank") before deciding `rbi.payments-banks-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.payments-banks-cyber.2026`, PDF page 4: "These Directions shall be applicable to Payments Banks"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 63. `rbi-generic-nbfc-must-ask-category`

A generic NBFC class is too coarse to choose Chapter IV or V and must produce category questions.

- **Entity classes:** `nbfc`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter III shall be applicable only for NBFCs- Base Layer (NBFCs-BL) with asset size below ₹500 crore, and Core Investment Companies (CICs)"
- `rbi.nbfc-cyber.2026`, PDF page 3: "The provisions contained in Chapter IV shall be applicable only for NBFCs- BL with asset size ₹500 crore and above."
- `rbi.nbfc-cyber.2026`, PDF page 4: "Middle Layer (NBFCs-ML) as defined in Reserve Bank of India (Non- Banking Financial Companies – Registration, Exemptions and Framework for Scale Based Regulation) Directions, 2025, excluding CICs."

- [ ] Correct   - [ ] Incorrect: ____________________

### 64. `rbi-generic-plus-specific-class-no-question`

A generic NBFC class plus a concrete Middle Layer class resolves the family without a category question.

- **Entity classes:** `nbfc`, `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "Middle Layer (NBFCs-ML) as defined in Reserve Bank of India (Non- Banking Financial Companies – Registration, Exemptions and Framework for Scale Based Regulation) Directions, 2025, excluding CICs."

- [ ] Correct   - [ ] Incorrect: ____________________

### 65. `rbi-hfc-middle-layer-reports-to-nhb`

A Middle Layer HFC reports to NHB rather than RBI under the contested paragraph 141 note, while retaining the separate CERT-In duties.

- **Entity classes:** `nbfc.middle_layer`, `nbfc.hfc`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb` (PT6H from detection)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 44: "(Note: In respect of Housing Finance Companies, cyber incidents shall continue to be reported to NHB and not RBI)"
- `rbi.nbfc-cyber.2026`, PDF page 44: "The NBFC shall also pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding cyber incidents."
- `cert-in.directions-70b.2022`, PDF page 2: "within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 66. `rbi-hfc-without-layer-must-ask-category`

An HFC role alone does not identify its NBFC layer and must not suppress potentially applicable duties.

- **Entity classes:** `nbfc.hfc`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- The tool must ask (question contains "NBFC category") before deciding `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "Middle Layer (NBFCs-ML) as defined in Reserve Bank of India (Non- Banking Financial Companies – Registration, Exemptions and Framework for Scale Based Regulation) Directions, 2025, excluding CICs."
- `rbi.nbfc-cyber.2026`, PDF page 44: "(Note: In respect of Housing Finance Companies, cyber incidents shall continue to be reported to NHB and not RBI)"

- [ ] Correct   - [ ] Incorrect: ____________________

### 67. `rbi-incident-before-commencement`

An incident before 31 July 2026 must not receive any duty from the later RBI Direction.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-07-01T10:00:00+05:30`
- **Noticed:** `2026-07-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-07-01`; regulators: CERT-In)

- Deadline `2026-07-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-va-half-yearly`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-pt-annual`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 1: "July 31, 2026"
- `rbi.nbfc-cyber.2026`, PDF page 3: "2. These Directions shall come into force with immediate effect."
- `cert-in.directions-70b.2022`, PDF page 2: "mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 68. `rbi-ml-also-data-fiduciary-2027`

A Middle Layer NBFC that is also a Data Fiduciary has three distinct regimes and anchors after DPDP Rule 7 commences.

- **Entity classes:** `nbfc.middle_layer`, `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware; Data breach
- **Detected:** `2027-06-01T09:00:00+05:30`
- **Noticed:** `2027-06-01T10:00:00+05:30`
- **Became aware (DPDP):** `2027-06-01T11:00:00+05:30`
- **Personal data involved:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2027-06-01`; regulators: CERT-In, RBI, MeitY)

- Deadline `2027-06-01T15:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Deadline `2027-06-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-04T11:00:00+05:30` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Applies, with no computed deadline: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Applies, with no computed deadline: `meity.dpdp-rules.2025.rule7-2-a-board-initial`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-2-a-board-initial`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 43: "within six hours of detection"
- `rbi.nbfc-cyber.2026`, PDF page 44: "The NBFC shall also pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding cyber incidents."
- `cert-in.directions-70b.2022`, PDF page 2: "within 6 hours of noticing such incidents or being brought to notice about such incidents."
- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf"

- [ ] Correct   - [ ] Incorrect: ____________________

### 69. `rbi-ml-attested-not-a-cyber-incident`

Explicit negative attestations make both incident-reporting regimes not applicable while recurring Chapter V duties remain.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** hardware failure
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `False`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- No deadline is computed.
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "‘Cyber Incident’ - A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not."
- `cert-in.directions-70b.2022`, PDF page 2: "shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In"

- [ ] Correct   - [ ] Incorrect: ____________________

### 70. `rbi-ml-hardware-failure-unattested`

Hardware failure without either attestation leaves both the Annexure I and wider RBI cyber-incident questions unresolved.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** hardware failure
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- No deadline is computed.
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "cyber incident") before deciding `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h`
- The tool must ask (question contains "cyber incident") before deciding `rbi.nbfc-cyber.2026.ch5-cert-in-notification`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "(7) ‘Cyber Incident’ - A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not."
- `cert-in.directions-70b.2022`, PDF page 2: "shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In"

- [ ] Correct   - [ ] Incorrect: ____________________

### 71. `rbi-ml-it-incident-not-annexure-i`

An attested RBI cyber incident can trigger RBI duties even when the user attests it is not Annexure I.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** hardware failure
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `True`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "‘Cyber Incident’ - A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not."
- `rbi.nbfc-cyber.2026`, PDF page 43: "within six hours of detection"
- `rbi.nbfc-cyber.2026`, PDF page 44: "The NBFC shall also pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding cyber incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 72. `rbi-ml-ransomware`

A Middle Layer NBFC has an Annexure I ransomware incident with equal detection and noticing times.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Protected system (NCIIPC):** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.nbfc-cyber.2026.ch5-cert-in-notification`
- Does not apply: `rbi.nbfc-cyber.2026.ch4-incident-reporting-6h`
- Does not apply: `rbi.nbfc-cyber.2026.ch5-hfc-incident-reporting-nhb`

**Clauses relied on**

- `rbi.nbfc-cyber.2026`, PDF page 4: "Middle Layer (NBFCs-ML) as defined in Reserve Bank of India (Non- Banking Financial Companies – Registration, Exemptions and Framework for Scale Based Regulation) Directions, 2025, excluding CICs."
- `rbi.nbfc-cyber.2026`, PDF page 43: "141. The NBFC shall report cyber incidents to RBI within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System -"
- `rbi.nbfc-cyber.2026`, PDF page 44: "The NBFC shall also pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding cyber incidents."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents."

- [ ] Correct   - [ ] Incorrect: ____________________

### 73. `rbi-payments-bank-detection-unknown`

Only the noticing time is known: CERT-In's clock runs, RBI's needs the detection time.

- **Entity classes:** `bank.payments_bank`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `rbi.payments-banks-cyber.2026.cert-in-notification`
- The tool must ask (question contains "detected") before deciding `rbi.payments-banks-cyber.2026.incident-reporting-6h`

**Clauses relied on**

- `rbi.payments-banks-cyber.2026`, PDF page 44: "181. The bank shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 74. `rbi-payments-bank-ransomware`

A Payments Bank.

- **Entity classes:** `bank.payments_bank`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.payments-banks-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.payments-banks-cyber.2026.cert-in-notification`
- Applies, with no computed deadline: `rbi.payments-banks-cyber.2026.va-half-yearly`
- Applies, with no computed deadline: `rbi.payments-banks-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.payments-banks-cyber.2026`, PDF page 44: "181. The bank shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `rbi.payments-banks-cyber.2026`, PDF page 44: "The bank shall also pro-actively notify CERT-In regarding cyber incidents."
- `rbi.payments-banks-cyber.2026`, PDF page 4: "These Directions shall be applicable to Payments Banks"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 75. `rbi-ucb-attested-not-a-cyber-incident`

The user attests the event is neither an Annexure I type nor a cyber incident.

- **Entity classes:** `ucb.level_i`
- **Incident type(s) as stated:** hardware failure
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In)

- No deadline is computed.
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `rbi.ucb-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.ucb-cyber.2026.cert-in-notification`

**Clauses relied on**

- `rbi.ucb-cyber.2026`, PDF page 29: "88. The UCB shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 76. `rbi-ucb-before-commencement`

An incident on 1 July 2026 predates the Direction.

- **Entity classes:** `ucb.level_i`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-07-01T10:00:00+05:30`
- **Noticed:** `2026-07-01T10:00:00+05:30`

**Expected** (law as of `2026-07-01`; regulators: CERT-In)

- Deadline `2026-07-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `rbi.ucb-cyber.2026.incident-reporting-6h`
- Does not apply: `rbi.ucb-cyber.2026.cert-in-notification`
- Does not apply: `rbi.ucb-cyber.2026.va-half-yearly`
- Does not apply: `rbi.ucb-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.ucb-cyber.2026`, PDF page 4: "These Directions shall come into force with immediate effect."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 77. `rbi-ucb-detected-before-noticed`

RBI counts from detection; CERT-In from noticing.

- **Entity classes:** `ucb.level_ii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T08:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T14:00:00+05:30` for `rbi.ucb-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)

**Clauses relied on**

- `rbi.ucb-cyber.2026`, PDF page 29: "88. The UCB shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 78. `rbi-ucb-generic-reports-and-is-asked-level`

A UCB whose level is not given still gets the reporting deadline (all UCBs); the level is asked only for VA and PT.

- **Entity classes:** `ucb`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.ucb-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.ucb-cyber.2026.cert-in-notification`
- The tool must ask (question contains "UCB level") before deciding `rbi.ucb-cyber.2026.va-half-yearly`
- The tool must ask (question contains "UCB level") before deciding `rbi.ucb-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.ucb-cyber.2026`, PDF page 29: "88. The UCB shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `rbi.ucb-cyber.2026`, PDF page 4: "Applicable to the UCB irrespective of digital services / products offered by it."
- `rbi.ucb-cyber.2026`, PDF page 33: "116. The UCB shall periodically conduct VA / PT of internet facing web / mobile applications, servers, and network components throughout their lifecycle (pre- implementation, post implementation, and after changes). VA of critical applications and those on DMZ shall be conducted at least once in every six months. PT shall be conducted at least once in a year."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 79. `rbi-ucb-level1-ransomware`

A Level I UCB: the reporting duty is in Chapter III, which binds every UCB; VA and PT are Chapter IV duties and do not reach Level I.

- **Entity classes:** `ucb.level_i`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.ucb-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.ucb-cyber.2026.cert-in-notification`
- Does not apply: `rbi.ucb-cyber.2026.va-half-yearly`
- Does not apply: `rbi.ucb-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.ucb-cyber.2026`, PDF page 29: "88. The UCB shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `rbi.ucb-cyber.2026`, PDF page 4: "Applicable to the UCB irrespective of digital services / products offered by it."
- `rbi.ucb-cyber.2026`, PDF page 4: "For the purpose of these Directions, a UCB is categorised into one of the four levels based on its digital depth and interconnectedness to the payment systems landscape. Depending on the UCB category, the applicability of Chapter II to Chapter VI of these Directions is as given below:"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 80. `rbi-ucb-level3-has-va-pt`

A Level III UCB is bound by Chapter IV as well, so the VA and PT cadence applies.

- **Entity classes:** `ucb.level_iii`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.ucb-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Applies, with no computed deadline: `rbi.ucb-cyber.2026.cert-in-notification`
- Applies, with no computed deadline: `rbi.ucb-cyber.2026.va-half-yearly`
- Applies, with no computed deadline: `rbi.ucb-cyber.2026.pt-annual`

**Clauses relied on**

- `rbi.ucb-cyber.2026`, PDF page 33: "116. The UCB shall periodically conduct VA / PT of internet facing web / mobile applications, servers, and network components throughout their lifecycle (pre- implementation, post implementation, and after changes). VA of critical applications and those on DMZ shall be conducted at least once in every six months. PT shall be conducted at least once in a year."
- `rbi.ucb-cyber.2026`, PDF page 29: "88. The UCB shall report cyber incidents within six hours of detection on DAKSH platform (Reserve Bank’s Advanced Supervisory Monitoring System - https://daksh.rbi.org.in)."
- `rbi.ucb-cyber.2026`, PDF page 4: "For the purpose of these Directions, a UCB is categorised into one of the four levels based on its digital depth and interconnectedness to the payment systems landscape. Depending on the UCB category, the applicability of Chapter II to Chapter VI of these Directions is as given below:"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

## IRDAI Information and Cyber Security Guidelines (2023) (14 scenarios)

### 81. `irdai-attested-not-a-cyber-incident`

Attested neither an Annexure I type nor a cyber incident.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `False`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- No deadline is computed.
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`
- Does not apply: `irdai.ics-guidelines.2023.incident-reporting-6h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `irdai.ics-guidelines.2023`, PDF page 283: "Organization shall contractually assure that they are informed of any confirmed breach immediately without any delay. For suspected breach, Organization shall be informed within 4 hours from the time of breach discovery."

- [ ] Correct   - [ ] Incorrect: ____________________

### 82. `irdai-before-the-guidelines`

An incident on 1 April 2023 predates the guidelines of 24 April 2023; CERT-In's Directions already applied.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2023-04-01T10:00:00+05:30`

**Expected** (law as of `2023-04-01`; regulators: CERT-In)

- Deadline `2023-04-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `irdai.ics-guidelines.2023.incident-reporting-6h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 131: "APRIL, 2023"
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 83. `irdai-complaint-clocks`

A complaint is received two hours after the incident is noticed; acknowledgement is due in 24 hours and disposal in fifteen days, both from receipt.

- **Entity classes:** `irdai.intermediary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-02T12:00:00+05:30` for `irdai.ics-guidelines.2023.grievance-acknowledge-24h` (PT24H from external event)
- Deadline `2026-10-16T12:00:00+05:30` for `irdai.ics-guidelines.2023.grievance-dispose-15d` (P15D from external event)

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 298: "acknowledge the complaint within twenty-four hours and dispose off such complaint within a period of fifteen days from the date of its receipt;"
- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 84. `irdai-cyber-incident-not-annexure-i`

Attested a cyber incident but not an Annexure I type: the IRDAI sentence is not limited to Annexure I, so on the conservative reading its clock runs.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-10-01T10:00:00+05:30`
- **Attested Annexure I type:** `False`
- **Attested a cyber incident:** `True`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- Deadline `2026-10-01T16:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `cert-in.directions-70b.2022.incident-reporting-6h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 85. `irdai-detection-only-asks`

Only a detection time is known. The IRDAI clause, like CERT-In's, counts from noticing or being brought to notice, so the engine asks.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- No deadline is computed.
- The tool must ask (question contains "noticed") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "noticed") before deciding `irdai.ics-guidelines.2023.incident-reporting-6h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 86. `irdai-government-order-clock`

A government order arrives the day after the incident; its 72 hours run from receipt of the order, not from the incident.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-05T09:00:00+05:30` for `irdai.ics-guidelines.2023.gov-order-information-72h` (PT72H from external event)

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 298: "7. The Organization shall as soon as possible, but not later than seventy-two hours of the receipt of an order, provide information under its control or possession, or assistance to the Government agency which is lawfully authorized for investigative or protective or cybersecurity activities, for the purposes of verification of identity, or for the prevention, detection, investigation, or prosecution, of offences under any law for the time being in force, or for cyber security incidents."
- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 87. `irdai-hardware-failure-unattested`

Free text that matches no Annexure I type: the CERT-In question and the IRDAI cyber-incident question are both asked.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** hardware failure
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- No deadline is computed.
- The tool must ask (question contains "Annexure I") before deciding `cert-in.directions-70b.2022.incident-reporting-6h`
- The tool must ask (question contains "cyber incident") before deciding `irdai.ics-guidelines.2023.incident-reporting-6h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `irdai.ics-guidelines.2023`, PDF page 219: "An Incident is defined as the occurrence of any exceptional situation that could compromise the Confidentiality, Integrity or Availability of Information assets of Organization."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."
- `irdai.ics-guidelines.2023`, PDF page 283: "Organization shall contractually assure that they are informed of any confirmed breach immediately without any delay. For suspected breach, Organization shall be informed within 4 hours from the time of breach discovery."

- [ ] Correct   - [ ] Incorrect: ____________________

### 88. `irdai-insurer-also-data-fiduciary-2027`

An insurer that is a Data Fiduciary: CERT-In with a copy to IRDAI in six hours, and the Data Protection Board track.

- **Entity classes:** `irdai.insurer`, `dpdp.data_fiduciary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware; Data breach
- **Noticed:** `2027-06-01T10:00:00+05:30`
- **Became aware (DPDP):** `2027-06-01T11:00:00+05:30`
- **Personal data involved:** `True`

**Expected** (law as of `2027-06-01`; regulators: CERT-In, IRDAI, MeitY)

- Deadline `2027-06-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-01T16:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from noticing)
- Deadline `2027-06-04T11:00:00+05:30` for `meity.dpdp-rules.2025.rule7-2-b-board-detailed` (PT72H from awareness)
- Must be done without delay: `meity.dpdp-rules.2025.rule7-1-principal-intimation`
- Must be done without delay: `meity.dpdp-rules.2025.rule7-2-a-board-initial`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `meity.dpdp-rules.2025`, PDF page 26: "(b) within seventy-two hours of becoming aware of the breach, or within such longer period as the Board may allow on a request made in writing in this behalf, — (i) updated and detailed information in respect of such description; (ii) the broad facts related to the events, circumstances and reasons leading to the breach; (iii) measures implemented or proposed, if any, to mitigate risk; (iv) any findings regarding the person who caused the breach; (v) remedial measures taken to prevent recurrence of such breach; and (vi) a report regarding the intimations given to affected Data Principals."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 89. `irdai-insurer-ransomware`

An insurer notices ransomware: CERT-In within six hours, with a copy to IRDAI.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from noticing)

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `irdai.ics-guidelines.2023`, PDF page 138: "These guidelines are applicable to all Insurers including Foreign Re-Insurance Branches (FRBs) and Insurance Intermediaries regulated by the Insurance Regulatory and Development Authority of India (IRDAI)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 90. `irdai-intermediary-brought-to-notice`

An insurance intermediary is told of the incident by a third party; no noticing time is given.

- **Entity classes:** `irdai.intermediary`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Brought to notice:** `2026-10-01T09:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- Deadline `2026-10-01T15:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from brought to notice)
- Deadline `2026-10-01T15:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from brought to notice)

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."
- `irdai.ics-guidelines.2023`, PDF page 138: "These guidelines are applicable to all Insurers including Foreign Re-Insurance Branches (FRBs) and Insurance Intermediaries regulated by the Insurance Regulatory and Development Authority of India (IRDAI)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 91. `irdai-other-duties-before-the-guidelines`

On 1 April 2023 the guidelines had not been issued.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2023-04-01T10:00:00+05:30`

**Expected** (law as of `2023-04-01`; regulators: CERT-In)

- Deadline `2023-04-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Does not apply: `irdai.ics-guidelines.2023.incident-reporting-6h`
- Does not apply: `irdai.ics-guidelines.2023.gov-order-information-72h`
- Does not apply: `irdai.ics-guidelines.2023.grievance-acknowledge-24h`
- Does not apply: `irdai.ics-guidelines.2023.grievance-dispose-15d`
- Does not apply: `irdai.ics-guidelines.2023.content-takedown-24h`
- Does not apply: `irdai.ics-guidelines.2023.registration-data-retention-180d`
- Does not apply: `irdai.ics-guidelines.2023.cloud-breach-notice-contract-clause`
- Does not apply: `irdai.ics-guidelines.2023.lost-device-internal-report-4h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 298: "7. The Organization shall as soon as possible, but not later than seventy-two hours of the receipt of an order, provide information under its control or possession, or assistance to the Government agency which is lawfully authorized for investigative or protective or cybersecurity activities, for the purposes of verification of identity, or for the prevention, detection, investigation, or prosecution, of offences under any law for the time being in force, or for cyber security incidents."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 92. `irdai-other-duties-do-not-reach-an-nbfc`

A Middle Layer NBFC is not regulated by IRDAI.

- **Entity classes:** `nbfc.middle_layer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.nbfc-cyber.2026.ch5-incident-reporting-6h` (PT6H from detection)
- Does not apply: `irdai.ics-guidelines.2023.gov-order-information-72h`
- Does not apply: `irdai.ics-guidelines.2023.grievance-acknowledge-24h`
- Does not apply: `irdai.ics-guidelines.2023.grievance-dispose-15d`
- Does not apply: `irdai.ics-guidelines.2023.content-takedown-24h`
- Does not apply: `irdai.ics-guidelines.2023.registration-data-retention-180d`
- Does not apply: `irdai.ics-guidelines.2023.cloud-breach-notice-contract-clause`
- Does not apply: `irdai.ics-guidelines.2023.lost-device-internal-report-4h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 298: "7. The Organization shall as soon as possible, but not later than seventy-two hours of the receipt of an order, provide information under its control or possession, or assistance to the Government agency which is lawfully authorized for investigative or protective or cybersecurity activities, for the purposes of verification of identity, or for the prevention, detection, investigation, or prosecution, of offences under any law for the time being in force, or for cyber security incidents."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

### 93. `irdai-other-duties-give-no-incident-clock`

An insurer's ransomware incident starts only the two six-hour clocks. The duties that run from an order, a complaint, a cancellation or a lost device are listed but give no deadline and ask nothing.

- **Entity classes:** `irdai.insurer`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, IRDAI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `irdai.ics-guidelines.2023.incident-reporting-6h` (PT6H from noticing)
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.gov-order-information-72h`
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.grievance-acknowledge-24h`
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.grievance-dispose-15d`
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.content-takedown-24h`
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.registration-data-retention-180d`
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.cloud-breach-notice-contract-clause`
- Applies, with no computed deadline: `irdai.ics-guidelines.2023.lost-device-internal-report-4h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 298: "7. The Organization shall as soon as possible, but not later than seventy-two hours of the receipt of an order, provide information under its control or possession, or assistance to the Government agency which is lawfully authorized for investigative or protective or cybersecurity activities, for the purposes of verification of identity, or for the prevention, detection, investigation, or prosecution, of offences under any law for the time being in force, or for cyber security incidents."
- `irdai.ics-guidelines.2023`, PDF page 298: "acknowledge the complaint within twenty-four hours and dispose off such complaint within a period of fifteen days from the date of its receipt;"
- `irdai.ics-guidelines.2023`, PDF page 298: "acknowledge the complaint within twenty-four hours and dispose off such complaint within a period of fifteen days from the date of its receipt;"
- `irdai.ics-guidelines.2023`, PDF page 299: "11. The Organization shall within twenty-four hours from the receipt of a complaint made by an individual or any person on his behalf under this sub-rule, in relation to any content which is prima facie in the nature of any material which exposes the private area of such individual, shows such individual in full or partial nudity or shows or depicts such individual in any sexual act or conduct, or is in the nature of impersonation in an electronic form, including artificially morphed images of such individual, take all reasonable and practicable measures to remove or disable access to such content which is hosted, stored, published or transmitted by it."
- `irdai.ics-guidelines.2023`, PDF page 297: "5. The Organization which collects information from a user for registration on the computer resource, shall retained his information for a period of one hundred and eighty days"
- `irdai.ics-guidelines.2023`, PDF page 283: "Organization shall contractually assure that they are informed of any confirmed breach immediately without any delay. For suspected breach, Organization shall be informed within 4 hours from the time of breach discovery."
- `irdai.ics-guidelines.2023`, PDF page 212: "3. In case of loss of device, the employee shall inform IT function within 4 hours."
- `irdai.ics-guidelines.2023`, PDF page 224: "Organization shall mandatorily report cyber incidents to Cert-In within 6 hours of noticing or being brought to notice about such incidents with a copy to IRDAI and other concerned regulators / authorities. The details regarding methods and formats of reporting cyber incident is published on Cert-In website."

- [ ] Correct   - [ ] Incorrect: ____________________

### 94. `irdai-payments-bank-is-not-an-insurer`

A Payments Bank is not regulated by IRDAI.

- **Entity classes:** `bank.payments_bank`
- **Incident type(s) as stated:** Malicious code attacks such as Ransomware
- **Detected:** `2026-10-01T10:00:00+05:30`
- **Noticed:** `2026-10-01T10:00:00+05:30`

**Expected** (law as of `2026-10-01`; regulators: CERT-In, RBI)

- Deadline `2026-10-01T16:00:00+05:30` for `cert-in.directions-70b.2022.incident-reporting-6h` (PT6H from noticing)
- Deadline `2026-10-01T16:00:00+05:30` for `rbi.payments-banks-cyber.2026.incident-reporting-6h` (PT6H from detection)
- Does not apply: `irdai.ics-guidelines.2023.incident-reporting-6h`

**Clauses relied on**

- `irdai.ics-guidelines.2023`, PDF page 138: "These guidelines are applicable to all Insurers including Foreign Re-Insurance Branches (FRBs) and Insurance Intermediaries regulated by the Insurance Regulatory and Development Authority of India (IRDAI)."
- `cert-in.directions-70b.2022`, PDF page 2: "(ii) Any service provider, intermediary, data centre, body corporate and Government organisation shall mandatorily report cyber incidents as mentioned in Annexure I to CERT-In within 6 hours of noticing such incidents or being brought to notice about such incidents. The incidents can be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800- 11-4949) and Fax (1800-11-6969). The details regarding methods and formats of reporting cyber security incidents is also published on the website of CERT-In www.cert-in.org.in and will be updated from time to time."

- [ ] Correct   - [ ] Incorrect: ____________________

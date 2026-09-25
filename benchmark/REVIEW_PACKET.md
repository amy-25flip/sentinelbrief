# SentinelBrief — Benchmark Compliance Review Packet

> **Notice:** This document is generated for external legal/compliance experts to validate
> the benchmark scenario ground truth labels. Benchmark labels were originally drafted by AI
> (`machine_checked`) from official regulatory texts and require independent human verification.

**Total Dev Scenarios:** 41  
**Generated from:** `benchmark/scenarios/`  

---

## Scenario 1: `cert-in-ambiguous-anchor`

**Description:** Incident occurred 2 hours before it was noticed.

**Adversarial Flags:** ambiguous_anchor

### 1. Situation Facts
- **Entity Class:** `service_provider`
- **Incident Summary:** Unauthorized access.
- **Incident Types:** unauthorized access
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-15T08:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** web_server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 2: `cert-in-attack-on-application`

**Description:** Annexure I item x 'Attacks on Application such as E-Governance, E-Commerce' contains none of the usual attack keywords.

**Adversarial Flags:** annexure_vocabulary_gap

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** Annexure I item x 'Attacks on Application such as E-Governance, E-Commerce' contains none of the usual attack keywords.
- **Incident Types:** Attacks on Application such as E-Governance, E-Commerce
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 3: `cert-in-attack-on-servers`

**Description:** Annexure I item vi 'Attack on servers such as Database, Mail and DNS' uses no malware vocabulary.

**Adversarial Flags:** annexure_vocabulary_gap

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** Annexure I item vi 'Attack on servers such as Database, Mail and DNS' uses no malware vocabulary.
- **Incident Types:** Attack on servers such as Database, Mail and DNS
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 4: `cert-in-before-directions-effective`

**Description:** An incident on 5 Jan 2021, before the Directions took effect on 27 Jun 2022, evaluated today. The law that applies is the law as of the incident date, not as of the snapshot or evaluation date.

**Adversarial Flags:** law_as_of_incident_date

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** An incident on 5 Jan 2021, before the Directions took effect on 27 Jun 2022. The law as of the incident date does not include them.
- **Incident Types:** ransomware
- **When Detected:** `None`
- **When Noticed:** `2021-01-05T09:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2021-01-05`
- **Applicable Regulators:** 

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- *(No specific citations)*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.incident-reporting-6h`: Directions not yet in force on the incident date
- `cert-in.directions-70b.2022.ntp-sync`: Directions not yet in force on the incident date

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 5: `cert-in-brought-to-notice`

**Description:** An external party alerts the entity at 10:00 IST; the internal team only notices at 11:00 IST. The clock runs from the earlier trigger.

**Adversarial Flags:** ambiguous_anchor

### 1. Situation Facts
- **Entity Class:** `service_provider`
- **Incident Summary:** Data leak reported by an external researcher before internal noticing.
- **Incident Types:** data leak
- **When Detected:** `2026-09-15T11:00:00+05:30`
- **When Noticed:** `2026-09-15T11:00:00+05:30`
- **When Brought to Notice:** `2026-09-15T10:00:00+05:30`
- **When Occurred:** `2026-09-15T07:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `True`
- **Systems Affected:** s3_bucket

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `brought_to_notice`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 6: `cert-in-cloud-outage-not-assumed`

**Description:** A cloud region power outage mentions 'cloud' but is not obviously an attack. The engine may suggest item xviii but must ask, not start a clock.

**Adversarial Flags:** keyword_false_positive

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** A cloud region power outage mentions 'cloud' but is not obviously an attack. The engine may suggest item xviii but must ask, not start a clock.
- **Incident Types:** cloud region power outage
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.ntp-sync`** (cert-in.directions-70b.2022, Direction (i)):
  > *"(i) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall connect to the Network Time Protocol 
(NTP) Server of National Informatics Centre (NIC) or National Physical 
Laboratory (NPL) or with NTP servers traceable to these NTP servers, for 
synchronisation of all their ICT systems clocks. Entities having ICT 
infrastructure spanning multiple geographies may also use accurate and 
standard time source other than NPL and NIC, however it is to be ensured 
that their time source shall not deviate from NPL and NIC."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

#### Expected Clarifying Unknowns Required
- Question: *"Annexure I"* (affects `cert-in.directions-70b.2022.incident-reporting-6h`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 7: `cert-in-data-breach-unknown-time`

**Description:** A service provider discovers a data breach but doesn't know when it was first noticed.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `service_provider`
- **Incident Summary:** Data breach discovered, time unknown.
- **Incident Types:** data breach
- **When Detected:** `None`
- **When Noticed:** `None`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `True`
- **Systems Affected:** customer_database

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-24`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

#### Expected Clarifying Unknowns Required
- Question: *"noticed"* (affects `cert-in.directions-70b.2022.incident-reporting-6h`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 8: `cert-in-detection-time-only`

**Description:** Only a detection time is known. CERT-In's trigger is noticing / being brought to notice, so the engine must ask, not start from detection.

**Adversarial Flags:** wrong_anchor

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** Only a detection time is known. CERT-In's trigger is noticing / being brought to notice, so the engine must ask, not start from detection.
- **Incident Types:** ransomware
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `None`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

#### Expected Clarifying Unknowns Required
- Question: *"noticed"* (affects `cert-in.directions-70b.2022.incident-reporting-6h`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 9: `cert-in-government-org`

**Description:** A government organisation with a website defacement. Direction (iii) on complying with CERT-In orders names service provider/intermediary/data centre/body corporate, not government organisations.

**Adversarial Flags:** text_scope_trap

### 1. Situation Facts
- **Entity Class:** `government_org`
- **Incident Summary:** Website defacement.
- **Incident Types:** website defacement
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-15T09:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** public_website

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.ntp-sync`** (cert-in.directions-70b.2022, Direction (i)):
  > *"(i) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall connect to the Network Time Protocol 
(NTP) Server of National Informatics Centre (NIC) or National Physical 
Laboratory (NPL) or with NTP servers traceable to these NTP servers, for 
synchronisation of all their ICT systems clocks. Entities having ICT 
infrastructure spanning multiple geographies may also use accurate and 
standard time source other than NPL and NIC, however it is to be ensured 
that their time source shall not deviate from NPL and NIC."*
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `cert-in.directions-70b.2022.designate-poc`** (cert-in.directions-70b.2022, Direction (iii)):
  > *"The service 
providers, intermediaries, data centres, body corporate and Government 
organisations shall designate a Point of Contact to interface with CERT-In. 
The Information relating to a Point of Contact shall be sent to CERT-In in 
the format specified at Annexure II and shall be updated from time to time. 
All communications from CERT-In seeking information and providing 
directions for compliance shall be sent to the said Point of Contact."*
- **Obligation `cert-in.directions-70b.2022.log-retention-180d`** (cert-in.directions-70b.2022, Direction (iv)):
  > *"(iv) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall mandatorily enable logs of all their ICT 
systems and maintain them securely for a rolling period of 180 days and 
the same shall be maintained within the Indian jurisdiction. These should 
be provided to CERT-In along with reporting of any incident or when 
ordered / directed by CERT-In."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.comply-with-orders`: Direction (iii) first paragraph does not list government organisations
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 10: `cert-in-nbfc-ransomware`

**Description:** An NBFC (body corporate) discovers ransomware.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** Ransomware infection noticed.
- **Incident Types:** malicious code, ransomware
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-15T08:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** internal_servers

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `cert-in.directions-70b.2022.ntp-sync`** (cert-in.directions-70b.2022, Direction (i)):
  > *"(i) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall connect to the Network Time Protocol 
(NTP) Server of National Informatics Centre (NIC) or National Physical 
Laboratory (NPL) or with NTP servers traceable to these NTP servers, for 
synchronisation of all their ICT systems clocks. Entities having ICT 
infrastructure spanning multiple geographies may also use accurate and 
standard time source other than NPL and NIC, however it is to be ensured 
that their time source shall not deviate from NPL and NIC."*
- **Obligation `cert-in.directions-70b.2022.designate-poc`** (cert-in.directions-70b.2022, Direction (iii)):
  > *"The service 
providers, intermediaries, data centres, body corporate and Government 
organisations shall designate a Point of Contact to interface with CERT-In. 
The Information relating to a Point of Contact shall be sent to CERT-In in 
the format specified at Annexure II and shall be updated from time to time. 
All communications from CERT-In seeking information and providing 
directions for compliance shall be sent to the said Point of Contact."*
- **Obligation `cert-in.directions-70b.2022.log-retention-180d`** (cert-in.directions-70b.2022, Direction (iv)):
  > *"(iv) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall mandatorily enable logs of all their ICT 
systems and maintain them securely for a rolling period of 180 days and 
the same shall be maintained within the Indian jurisdiction. These should 
be provided to CERT-In along with reporting of any incident or when 
ordered / directed by CERT-In."*
- **Obligation `cert-in.directions-70b.2022.comply-with-orders`** (cert-in.directions-70b.2022, Direction (iii)):
  > *"(iii)When required by order/direction of CERT-In, for the purposes of cyber 
incident response, protective and preventive actions related to cyber 
incidents, the service provider/intermediary/data centre/body corporate is 
mandated to take action or provide information or any such assistance to 
CERT-In, which may contribute towards cyber security mitigation actions 
and enhanced cyber security situational awareness. The order / direction 
may include the format of the information that is required (up to and 
including near real-time), and a specified timeframe in which it is required, 
which should be adhered to and compliance provided to CERT-In, else it 
would be treated as non-compliance of this direction."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 11: `cert-in-non-annexure-i-type`

**Description:** The user attests that a simple hardware failure is NOT an Annexure I incident type.

**Adversarial Flags:** explicit_attestation

### 1. Situation Facts
- **Entity Class:** `body_corporate`
- **Incident Summary:** Simple hardware failure of a redundant switch.
- **Incident Types:** hardware failure
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-15T10:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** network_switch

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.ntp-sync`** (cert-in.directions-70b.2022, Direction (i)):
  > *"(i) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall connect to the Network Time Protocol 
(NTP) Server of National Informatics Centre (NIC) or National Physical 
Laboratory (NPL) or with NTP servers traceable to these NTP servers, for 
synchronisation of all their ICT systems clocks. Entities having ICT 
infrastructure spanning multiple geographies may also use accurate and 
standard time source other than NPL and NIC, however it is to be ensured 
that their time source shall not deviate from NPL and NIC."*
- **Obligation `cert-in.directions-70b.2022.designate-poc`** (cert-in.directions-70b.2022, Direction (iii)):
  > *"The service 
providers, intermediaries, data centres, body corporate and Government 
organisations shall designate a Point of Contact to interface with CERT-In. 
The Information relating to a Point of Contact shall be sent to CERT-In in 
the format specified at Annexure II and shall be updated from time to time. 
All communications from CERT-In seeking information and providing 
directions for compliance shall be sent to the said Point of Contact."*
- **Obligation `cert-in.directions-70b.2022.log-retention-180d`** (cert-in.directions-70b.2022, Direction (iv)):
  > *"(iv) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall mandatorily enable logs of all their ICT 
systems and maintain them securely for a rolling period of 180 days and 
the same shall be maintained within the Indian jurisdiction. These should 
be provided to CERT-In along with reporting of any incident or when 
ordered / directed by CERT-In."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.incident-reporting-6h`: User attested the incident is not an Annexure I type
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 12: `cert-in-noticed-before-brought`

**Description:** Internal noticing at 09:00 IST, outside notification at 12:00 IST. The earlier trigger (noticing) starts the clock.

**Adversarial Flags:** ambiguous_anchor

### 1. Situation Facts
- **Entity Class:** `service_provider`
- **Incident Summary:** Internal noticing at 09:00 IST, outside notification at 12:00 IST. The earlier trigger (noticing) starts the clock.
- **Incident Types:** phishing
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T09:00:00+05:30`
- **When Brought to Notice:** `2026-09-15T12:00:00+05:30`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T15:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 13: `cert-in-retention-is-not-a-deadline`

**Description:** A VPS provider with ransomware and a known occurrence time. The 5-year retention duty in Direction (v) must not become an incident deadline.

**Adversarial Flags:** retention_is_not_a_deadline

### 1. Situation Facts
- **Entity Class:** `vps_provider`
- **Incident Summary:** A VPS provider with ransomware and a known occurrence time. The 5-year retention duty in Direction (v) must not become an incident deadline.
- **Incident Types:** ransomware
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-10T09:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-10`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`** (cert-in.directions-70b.2022, Direction (v)):
  > *"(v) Data Centres, Virtual Private Server (VPS) providers, Cloud Service 
providers and Virtual Private Network Service (VPN Service) providers, 
shall be required to register the  following accurate information 
which  must be maintained by them for a period of 5 years or longer 
duration as mandated by the law after any cancellation or withdrawal of 
the registration as the case may be: 
a. Validated names of subscribers/customers hiring the services 
b. Period of hire including dates 
c. IPs allotted to / being used by the members 
d. Email address and IP address and time stamp used at the time of 
registration / on-boarding 
e. Purpose for hiring services 
f. Validated address and contact numbers 
g. Ownership pattern of the subscribers / customers hiring services"*
- **Obligation `cert-in.directions-70b.2022.log-retention-180d`** (cert-in.directions-70b.2022, Direction (iv)):
  > *"(iv) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall mandatorily enable logs of all their ICT 
systems and maintain them securely for a rolling period of 180 days and 
the same shall be maintained within the Indian jurisdiction. These should 
be provided to CERT-In along with reporting of any incident or when 
ordered / directed by CERT-In."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 14: `cert-in-unattested-hardware-failure`

**Description:** The user gives free text 'hardware failure' and does not attest. Free text must never conclude the incident is not reportable; the engine must ask.

**Adversarial Flags:** free_text_never_excludes

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** The user gives free text 'hardware failure' and does not attest. Free text must never conclude the incident is not reportable; the engine must ask.
- **Incident Types:** hardware failure
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.ntp-sync`** (cert-in.directions-70b.2022, Direction (i)):
  > *"(i) All service providers, intermediaries, data centres, body corporate and 
Government organisations shall connect to the Network Time Protocol 
(NTP) Server of National Informatics Centre (NIC) or National Physical 
Laboratory (NPL) or with NTP servers traceable to these NTP servers, for 
synchronisation of all their ICT systems clocks. Entities having ICT 
infrastructure spanning multiple geographies may also use accurate and 
standard time source other than NPL and NIC, however it is to be ensured 
that their time source shall not deviate from NPL and NIC."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

#### Expected Clarifying Unknowns Required
- Question: *"Annexure I"* (affects `cert-in.directions-70b.2022.incident-reporting-6h`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 15: `cert-in-utc-input`

**Description:** Noticed time supplied in UTC (04:30Z = 10:00 IST). The deadline instant must be identical regardless of the offset used.

**Adversarial Flags:** timezone_offset

### 1. Situation Facts
- **Entity Class:** `nbfc`
- **Incident Summary:** Noticed time supplied in UTC (04:30Z = 10:00 IST). The deadline instant must be identical regardless of the offset used.
- **Incident Types:** data leak
- **When Detected:** `None`
- **When Noticed:** `2026-09-15T04:30:00+00:00`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `None`
- **Systems Affected:** core_systems

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 16: `cert-in-vps-provider`

**Description:** A VPS provider experiences unauthorized access.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `vps_provider`
- **Incident Summary:** Unauthorized access to VPS infrastructure.
- **Incident Types:** unauthorized access
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-15T08:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** vps_infrastructure

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`** (cert-in.directions-70b.2022, Direction (v)):
  > *"(v) Data Centres, Virtual Private Server (VPS) providers, Cloud Service 
providers and Virtual Private Network Service (VPN Service) providers, 
shall be required to register the  following accurate information 
which  must be maintained by them for a period of 5 years or longer 
duration as mandated by the law after any cancellation or withdrawal of 
the registration as the case may be: 
a. Validated names of subscribers/customers hiring the services 
b. Period of hire including dates 
c. IPs allotted to / being used by the members 
d. Email address and IP address and time stamp used at the time of 
registration / on-boarding 
e. Purpose for hiring services 
f. Validated address and contact numbers 
g. Ownership pattern of the subscribers / customers hiring services"*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.virtual-asset-kyc-5y`: Direction (vi) names only virtual asset service, exchange and custodian wallet providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 17: `cert-in-wrong-entity-trap`

**Description:** A virtual asset exchange reports a DDoS but is NOT a VPS/cloud provider.

**Adversarial Flags:** wrong_entity_class_trap

### 1. Situation Facts
- **Entity Class:** `virtual_asset_exchange`
- **Incident Summary:** DDoS attack.
- **Incident Types:** DDoS
- **When Detected:** `2026-09-15T10:00:00+05:30`
- **When Noticed:** `2026-09-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-15T09:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** exchange_frontend

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-15T16:00:00+05:30`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.virtual-asset-kyc-5y`** (cert-in.directions-70b.2022, Direction (vi)):
  > *"(vi)     The virtual asset service providers, virtual asset exchange providers and 
custodian wallet providers (as defined by Ministry of Finance from time to 
time) shall mandatorily maintain all information obtained as part of Know 
Your Customer (KYC) and records of financial transactions for a period of 
five years so as to ensure cyber security in the area of payments and 
financial markets for citizens while protecting their data, fundamental 
rights and economic freedom in view of the growth of virtual assets.  
For the purpose of KYC, the Reserve Bank of India (RBI) Directions 2016 
/ Securities and Exchange Board of India (SEBI) circular dated April 24, 
2020 / Department of Telecom (DoT) notice September 21, 2021 mandated 
procedures as amended from time to time may be referred to as per 
Annexure III. 
  
With respect to transaction records, accurate information shall be 
maintained in such a way that individual transaction can be reconstructed 
along with the relevant elements comprising of, but not limited to, 
information relating to the identification of the relevant parties including 
IP addresses along with timestamps and time zones, transaction ID, the 
public keys (or equivalent identifiers), addresses or accounts involved (or 
equivalent identifiers), the nature and date of the transaction, and the 
amount transferred."*

#### Explicitly Not Applicable
- `cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y`: Direction (v) names only data centres, VPS, cloud and VPN providers

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 18: `dpdp-anchor-awareness-vs-occurrence`

**Description:** Adversarial anchor test: A breach occurred on 2027-06-01 but the entity only became aware on 2027-06-03. DPDP 72-hour clock starts strictly from awareness.

**Adversarial Flags:** ambiguous_anchor

### 1. Situation Facts
- **Entity Class:** `dpdp.data_fiduciary`
- **Incident Summary:** Unauthorized access occurred 2 days before security audit discovery.
- **Incident Types:** Data breach
- **When Detected:** `2027-06-03T09:00:00+05:30`
- **When Noticed:** `2027-06-03T09:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2027-06-01T09:00:00+05:30`
- **When Aware (DPDP):** `2027-06-03T09:00:00+05:30`
- **Personal Data Involved:** `True`
- **Systems Affected:** DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-06-01`
- **Applicable Regulators:** CERT-In, MeitY

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-03T09:30:00Z`
- **MeitY** (`meity.dpdp-rules.2025.rule7-2-board-detailed`): Anchor `awareness`, Duration `PT72H` -> Deadline `2027-06-06T03:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `meity.dpdp-rules.2025.rule7-2-board-detailed`** (meity.dpdp-rules.2025, Rule 7(2)):
  > *"(2) The Data Fiduciary shall submit a detailed report to the Board within 72 hours of becoming aware of the
personal data breach, containing the root cause analysis, remedial actions taken or proposed to be taken, and
the status of intimation to data principals."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 19: `dpdp-fiduciary-data-breach-simulated-2027`

**Description:** In June 2027 (when DPDP is in force), a Data Fiduciary discovers and becomes aware of a personal data breach affecting customers.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `dpdp.data_fiduciary`
- **Incident Summary:** Customer database exfiltrated; entity became aware on 2027-06-01 at 10:00 IST.
- **Incident Types:** Data breach
- **When Detected:** `2027-06-01T10:00:00+05:30`
- **When Noticed:** `2027-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2027-05-30T10:00:00+05:30`
- **When Aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal Data Involved:** `True`
- **Systems Affected:** Customer DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-05-30`
- **Applicable Regulators:** CERT-In, MeitY

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-01T10:30:00Z`
- **MeitY** (`meity.dpdp-rules.2025.rule7-2-board-detailed`): Anchor `awareness`, Duration `PT72H` -> Deadline `2027-06-04T04:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `meity.dpdp-rules.2025.rule7-1-board-initial`** (meity.dpdp-rules.2025, Rule 7(1)):
  > *"(1) Where a Data Fiduciary becomes aware of a personal data breach, it shall intimate the Board without delay,
providing an initial description of the breach, including the nature, extent, and timing of the incident."*
- **Obligation `meity.dpdp-rules.2025.rule7-2-board-detailed`** (meity.dpdp-rules.2025, Rule 7(2)):
  > *"(2) The Data Fiduciary shall submit a detailed report to the Board within 72 hours of becoming aware of the
personal data breach, containing the root cause analysis, remedial actions taken or proposed to be taken, and
the status of intimation to data principals."*
- **Obligation `meity.dpdp-rules.2025.rule7-3-principal-intimation`** (meity.dpdp-rules.2025, Rule 7(3)):
  > *"(3) The Data Fiduciary shall also intimate each affected Data Principal without delay regarding the personal
data breach, describing the nature of the breach, likely consequences, and safety measures recommended to
be taken."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 20: `dpdp-multi-regulator-overlap`

**Description:** In June 2027, an NBFC (Middle Layer) that also acts as a Data Fiduciary experiences a ransomware attack involving customer data exfiltration. Tri-regulator reporting applies: CERT-In (6h), RBI (6h to DAKSH), and DPDP (72h detailed report).

**Adversarial Flags:** multi_regulator_overlap

### 1. Situation Facts
- **Entity Class:** `nbfc.middle_layer`
- **Incident Summary:** Ransomware encryption and customer data theft noticed at 10:00 IST on 2027-06-01.
- **Incident Types:** Malicious code attacks such as Ransomware, Data breach
- **When Detected:** `2027-06-01T10:00:00+05:30`
- **When Noticed:** `2027-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2027-06-01T08:00:00+05:30`
- **When Aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal Data Involved:** `True`
- **Systems Affected:** Core Lending Platform, Customer DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-06-01`
- **Applicable Regulators:** CERT-In, RBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-01T10:30:00Z`
- **RBI** (`rbi.nbfc-cyber.2026.incident-reporting-6h`): Anchor `occurrence`, Duration `PT6H` -> Deadline `2027-06-01T08:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `rbi.nbfc-cyber.2026.incident-reporting-6h`** (rbi.nbfc-cyber.2026, Paragraph 14):
  > *"Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall
mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory
monitoring portal within 6 hours of detection or occurrence of such incident."*

#### Explicitly Not Applicable
- `meity.dpdp-rules.2025.rule7-1-board-initial`: entity_class_mismatch
- `meity.dpdp-rules.2025.rule7-2-board-detailed`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 21: `dpdp-no-personal-data-breach`

**Description:** In June 2027, a Data Fiduciary suffers a DDoS attack on network gateways. No personal data breach has occurred. DPDP Rule 7 must not apply, but CERT-In 6-hour reporting does apply.

**Adversarial Flags:** condition_not_met

### 1. Situation Facts
- **Entity Class:** `dpdp.data_fiduciary`
- **Incident Summary:** DDoS attack affecting network gateway availability with zero data exfiltration.
- **Incident Types:** Attacks on critical networks/systems like Database, Mail and DNS, network devices
- **When Detected:** `2027-06-01T10:00:00+05:30`
- **When Noticed:** `2027-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2027-06-01T09:30:00+05:30`
- **When Aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Edge Gateway

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-06-01`
- **Applicable Regulators:** CERT-In, MeitY

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-01T10:30:00Z`
- **MeitY** (`meity.dpdp-rules.2025.rule7-2-board-detailed`): Anchor `awareness`, Duration `PT72H` -> Deadline `2027-06-04T04:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `meity.dpdp-rules.2025.rule7-2-board-detailed`** (meity.dpdp-rules.2025, Rule 7(2)):
  > *"(2) The Data Fiduciary shall submit a detailed report to the Board within 72 hours of becoming aware of the
personal data breach, containing the root cause analysis, remedial actions taken or proposed to be taken, and
the status of intimation to data principals."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 22: `dpdp-non-fiduciary-entity-trap`

**Description:** An entity that is only a general government organisation (not a registered data fiduciary) experiences a website defacement with no personal data breach. DPDP obligations must not apply.

**Adversarial Flags:** wrong_entity_class_trap

### 1. Situation Facts
- **Entity Class:** `government_org`
- **Incident Summary:** Defacement of public informational web page with no personal data processing.
- **Incident Types:** Defacement of website
- **When Detected:** `2027-06-01T10:00:00+05:30`
- **When Noticed:** `2027-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2027-06-01T09:00:00+05:30`
- **When Aware (DPDP):** `2027-06-01T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Web Portal

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-06-01`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-01T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `meity.dpdp-rules.2025.rule7-1-board-initial`: entity_class_mismatch
- `meity.dpdp-rules.2025.rule7-2-board-detailed`: entity_class_mismatch
- `meity.dpdp-rules.2025.rule7-3-principal-intimation`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 23: `dpdp-not-yet-in-force-trap-2026`

**Description:** In September 2026, a Data Fiduciary experiences a personal data breach. DPDP Rule 7 is NOT yet in force (in force from 13 May 2027) so no DPDP deadlines must be produced.

**Adversarial Flags:** dpdp_not_yet_in_force

### 1. Situation Facts
- **Entity Class:** `dpdp.data_fiduciary`
- **Incident Summary:** Customer database breached on 2026-09-24 at 10:00 IST.
- **Incident Types:** Data breach
- **When Detected:** `2026-09-24T10:00:00+05:30`
- **When Noticed:** `2026-09-24T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-24T08:00:00+05:30`
- **When Aware (DPDP):** `2026-09-24T10:00:00+05:30`
- **Personal Data Involved:** `True`
- **Systems Affected:** Customer DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-24`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-24T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `meity.dpdp-rules.2025.rule7-1-board-initial`: not_yet_in_force
- `meity.dpdp-rules.2025.rule7-2-board-detailed`: not_yet_in_force
- `meity.dpdp-rules.2025.rule7-3-principal-intimation`: not_yet_in_force

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 24: `dpdp-significant-data-fiduciary`

**Description:** In June 2027, a Significant Data Fiduciary discovers a personal data breach. DPDP Rule 7 detailed reporting duty within 72 hours applies.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `dpdp.significant_data_fiduciary`
- **Incident Summary:** Large-scale user data breach discovered on 2027-06-15 at 14:00 IST.
- **Incident Types:** Data breach
- **When Detected:** `2027-06-15T14:00:00+05:30`
- **When Noticed:** `2027-06-15T14:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2027-06-14T14:00:00+05:30`
- **When Aware (DPDP):** `2027-06-15T14:00:00+05:30`
- **Personal Data Involved:** `True`
- **Systems Affected:** User Data Vault

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-06-14`
- **Applicable Regulators:** CERT-In, MeitY

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-15T14:30:00Z`
- **MeitY** (`meity.dpdp-rules.2025.rule7-2-board-detailed`): Anchor `awareness`, Duration `PT72H` -> Deadline `2027-06-18T08:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `meity.dpdp-rules.2025.rule7-2-board-detailed`** (meity.dpdp-rules.2025, Rule 7(2)):
  > *"(2) The Data Fiduciary shall submit a detailed report to the Board within 72 hours of becoming aware of the
personal data breach, containing the root cause analysis, remedial actions taken or proposed to be taken, and
the status of intimation to data principals."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 25: `dpdp-unknown-awareness-time`

**Description:** In 2027, a Data Fiduciary discovers a personal data breach, but the exact timestamp of becoming aware (when_aware) is not provided. The engine must generate an Unknown question.

**Adversarial Flags:** missing_fact

### 1. Situation Facts
- **Entity Class:** `dpdp.data_fiduciary`
- **Incident Summary:** Data breach identified but awareness timestamp missing.
- **Incident Types:** Data breach
- **When Detected:** `None`
- **When Noticed:** `2027-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `True`
- **Systems Affected:** Database

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2027-06-01`
- **Applicable Regulators:** CERT-In, MeitY

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2027-06-01T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `meity.dpdp-rules.2025.rule7-2-board-detailed`** (meity.dpdp-rules.2025, Rule 7(2)):
  > *"(2) The Data Fiduciary shall submit a detailed report to the Board within 72 hours of becoming aware of the
personal data breach, containing the root cause analysis, remedial actions taken or proposed to be taken, and
the status of intimation to data principals."*

#### Expected Clarifying Unknowns Required
- Question: *"When was the incident became known to the entity?"* (affects `meity.dpdp-rules.2025.rule7-2-board-detailed`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 26: `rbi-anchor-occurrence-vs-detection`

**Description:** Adversarial anchor test: An NBFC detects an incident at 08:00 IST which occurred at 06:00 IST. The Directions specify detection or occurrence; the earlier trigger anchors the clock.

**Adversarial Flags:** ambiguous_anchor

### 1. Situation Facts
- **Entity Class:** `nbfc.middle_layer`
- **Incident Summary:** Unauthorized access occurred at 06:00 and detected at 08:00 IST.
- **Incident Types:** Unauthorised access of IT systems/data
- **When Detected:** `2026-08-15T08:00:00+05:30`
- **When Noticed:** `2026-08-15T08:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-08-15T06:00:00+05:30`
- **When Aware (DPDP):** `2026-08-15T08:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-08-15`
- **Applicable Regulators:** CERT-In, RBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-08-15T08:30:00Z`
- **RBI** (`rbi.nbfc-cyber.2026.incident-reporting-6h`): Anchor `occurrence`, Duration `PT6H` -> Deadline `2026-08-15T06:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `rbi.nbfc-cyber.2026.incident-reporting-6h`** (rbi.nbfc-cyber.2026, Paragraph 14):
  > *"Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall
mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory
monitoring portal within 6 hours of detection or occurrence of such incident."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 27: `rbi-before-directions-effective-2025`

**Description:** An incident on 2025-08-15 occurred before RBI NBFC Directions (2026-07-31). RBI 2026 Directions were not in force; only CERT-In applies.

**Adversarial Flags:** repealed_or_future_instrument_trap

### 1. Situation Facts
- **Entity Class:** `nbfc.middle_layer`
- **Incident Summary:** Ransomware encryption noticed on 2025-08-15 at 10:00 IST.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `2025-08-15T10:00:00+05:30`
- **When Noticed:** `2025-08-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-08-15T08:00:00+05:30`
- **When Aware (DPDP):** `2025-08-15T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-08-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-08-15T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `rbi.nbfc-cyber.2026.incident-reporting-6h`: not_yet_valid_at_incident_date (2026-07-31)
- `rbi.nbfc-cyber.2026.vapt-cadence`: not_yet_valid_at_incident_date (2026-07-31)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 28: `rbi-missing-detection-time`

**Description:** An NBFC Middle Layer experiences ransomware, but no detection/occurrence time is supplied. The engine must generate an Unknown question.

**Adversarial Flags:** missing_fact

### 1. Situation Facts
- **Entity Class:** `nbfc.middle_layer`
- **Incident Summary:** Ransomware discovered on operational systems.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `None`
- **When Noticed:** `None`
- **When Brought to Notice:** `None`
- **When Occurred:** `None`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-08-15`
- **Applicable Regulators:** CERT-In, RBI

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `rbi.nbfc-cyber.2026.incident-reporting-6h`** (rbi.nbfc-cyber.2026, Paragraph 14):
  > *"Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall
mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory
monitoring portal within 6 hours of detection or occurrence of such incident."*

#### Expected Clarifying Unknowns Required
- Question: *"When was the incident first noticed or brought to notice?"* (affects `cert-in.directions-70b.2022.incident-reporting-6h`)
- Question: *"When was the incident detected or occurring?"* (affects `rbi.nbfc-cyber.2026.incident-reporting-6h`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 29: `rbi-nbfc-base-layer-trap`

**Description:** Adversarial entity scoping test: An NBFC (Base Layer) discovers ransomware. RBI DAKSH Chapter IV paragraph 14 is restricted to Middle/Upper/Top Layer, so RBI reporting does NOT apply, but CERT-In 6h DOES apply.

**Adversarial Flags:** wrong_entity_class_trap

### 1. Situation Facts
- **Entity Class:** `nbfc.base_layer`
- **Incident Summary:** Ransomware encryption on Base Layer NBFC office machine noticed at 10:00 IST on 2026-08-15.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `2026-08-15T10:00:00+05:30`
- **When Noticed:** `2026-08-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-08-15T08:00:00+05:30`
- **When Aware (DPDP):** `2026-08-15T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** PC

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-08-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-08-15T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `rbi.nbfc-cyber.2026.incident-reporting-6h`: entity_class_mismatch
- `rbi.nbfc-cyber.2026.vapt-cadence`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 30: `rbi-nbfc-middle-layer-ransomware`

**Description:** An NBFC (Middle Layer) detects ransomware on 2026-08-15 at 10:00 IST. Dual reporting to RBI (DAKSH 6h) and CERT-In (6h) applies.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `nbfc.middle_layer`
- **Incident Summary:** Ransomware encryption detected on loan origination server at 10:00 IST.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `2026-08-15T10:00:00+05:30`
- **When Noticed:** `2026-08-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-08-15T08:00:00+05:30`
- **When Aware (DPDP):** `2026-08-15T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Loan Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-08-15`
- **Applicable Regulators:** CERT-In, RBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-08-15T10:30:00Z`
- **RBI** (`rbi.nbfc-cyber.2026.incident-reporting-6h`): Anchor `occurrence`, Duration `PT6H` -> Deadline `2026-08-15T08:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `rbi.nbfc-cyber.2026.incident-reporting-6h`** (rbi.nbfc-cyber.2026, Paragraph 14):
  > *"Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall
mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory
monitoring portal within 6 hours of detection or occurrence of such incident."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 31: `rbi-nbfc-top-layer-cloud-outage`

**Description:** An NBFC (Top Layer) detects an attack on critical core banking and loan servers on 2026-09-10 at 10:00 IST.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `nbfc.top_layer`
- **Incident Summary:** Critical database server attack detected at 10:00 IST.
- **Incident Types:** Attacks on servers such as Database, Mail and DNS
- **When Detected:** `2026-09-10T10:00:00+05:30`
- **When Noticed:** `2026-09-10T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-10T09:00:00+05:30`
- **When Aware (DPDP):** `2026-09-10T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Core DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-10`
- **Applicable Regulators:** CERT-In, RBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-10T10:30:00Z`
- **RBI** (`rbi.nbfc-cyber.2026.incident-reporting-6h`): Anchor `occurrence`, Duration `PT6H` -> Deadline `2026-09-10T09:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `rbi.nbfc-cyber.2026.incident-reporting-6h`** (rbi.nbfc-cyber.2026, Paragraph 14):
  > *"Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall
mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory
monitoring portal within 6 hours of detection or occurrence of such incident."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 32: `rbi-nbfc-upper-layer-data-exfiltration`

**Description:** An NBFC (Upper Layer) detects unauthorized access and data exfiltration on 2026-09-01 at 09:00 IST.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `nbfc.upper_layer`
- **Incident Summary:** Unauthorized exfiltration of loan records detected at 09:00 IST.
- **Incident Types:** Data breach
- **When Detected:** `2026-09-01T09:00:00+05:30`
- **When Noticed:** `2026-09-01T09:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-09-01T07:00:00+05:30`
- **When Aware (DPDP):** `2026-09-01T09:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Customer DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-09-01`
- **Applicable Regulators:** CERT-In, RBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-09-01T09:30:00Z`
- **RBI** (`rbi.nbfc-cyber.2026.incident-reporting-6h`): Anchor `occurrence`, Duration `PT6H` -> Deadline `2026-09-01T07:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `rbi.nbfc-cyber.2026.incident-reporting-6h`** (rbi.nbfc-cyber.2026, Paragraph 14):
  > *"Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall
mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory
monitoring portal within 6 hours of detection or occurrence of such incident."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 33: `rbi-vapt-cadence-non-applicability-base-layer`

**Description:** Adversarial entity scoping test: An NBFC Base Layer entity checking non-applicability of RBI VAPT cadence (restricted to Middle/Upper/Top layer).

**Adversarial Flags:** wrong_entity_class_trap

### 1. Situation Facts
- **Entity Class:** `nbfc.base_layer`
- **Incident Summary:** Defacement of informational web page noticed at 10:00 IST on 2026-08-15.
- **Incident Types:** Defacement of website
- **When Detected:** `2026-08-15T10:00:00+05:30`
- **When Noticed:** `2026-08-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2026-08-15T09:00:00+05:30`
- **When Aware (DPDP):** `2026-08-15T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Web Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2026-08-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2026-08-15T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `rbi.nbfc-cyber.2026.incident-reporting-6h`: entity_class_mismatch
- `rbi.nbfc-cyber.2026.vapt-cadence`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 34: `sebi-anchor-detection-earlier`

**Description:** Adversarial anchor test: A Qualified RE has detection logged at 08:00 IST by automated SIEM, but manual noticing at 10:00 IST. SEBI/CERT-In clock must anchor at the earliest trigger.

**Adversarial Flags:** ambiguous_anchor

### 1. Situation Facts
- **Entity Class:** `sebi.qsei`
- **Incident Summary:** Automated SIEM alert detected attack at 08:00; SOC operator noticed at 10:00.
- **Incident Types:** Attacks on servers such as Database, Mail and DNS
- **When Detected:** `2025-06-01T08:00:00+05:30`
- **When Noticed:** `2025-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-06-01T07:30:00+05:30`
- **When Aware (DPDP):** `2025-06-01T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Trading DB

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-06-01`
- **Applicable Regulators:** CERT-In, SEBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-01T10:30:00Z`
- **SEBI** (`sebi.cscrf.2024.incident-reporting-6h`): Anchor `detection`, Duration `PT6H` -> Deadline `2025-06-01T08:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `sebi.cscrf.2024.incident-reporting-6h`** (sebi.cscrf.2024, Paragraph 2):
  > *"2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6
hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting
shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24
hours."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 35: `sebi-before-in-force-trap-2024`

**Description:** An incident on 2024-10-15 occurred before CSCRF effective date (2025-01-01). SEBI CSCRF was not in force; only CERT-In applies.

**Adversarial Flags:** repealed_or_future_instrument_trap

### 1. Situation Facts
- **Entity Class:** `sebi.qsei`
- **Incident Summary:** Ransomware infection noticed on 2024-10-15 at 10:00 IST.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `2024-10-15T10:00:00+05:30`
- **When Noticed:** `2024-10-15T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2024-10-15T08:00:00+05:30`
- **When Aware (DPDP):** `2024-10-15T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2024-10-15`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2024-10-15T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `sebi.cscrf.2024.incident-reporting-6h`: not_yet_valid_at_incident_date (2025-01-01)
- `sebi.cscrf.2024.vapt-half-yearly`: not_yet_valid_at_incident_date (2025-01-01)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 36: `sebi-missing-noticing-and-detection-time`

**Description:** A Mid-size RE experiences a ransomware incident, but neither when_noticed nor when_detected is supplied. The engine must generate an Unknown question.

**Adversarial Flags:** missing_fact

### 1. Situation Facts
- **Entity Class:** `sebi.msei`
- **Incident Summary:** Ransomware discovered on operational servers.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `None`
- **When Noticed:** `None`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-06-01T08:00:00+05:30`
- **When Aware (DPDP):** `None`
- **Personal Data Involved:** `False`
- **Systems Affected:** Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-06-01`
- **Applicable Regulators:** CERT-In, SEBI

#### Computed Deadlines
- *(No active incident deadlines expected)*

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `sebi.cscrf.2024.incident-reporting-6h`** (sebi.cscrf.2024, Paragraph 2):
  > *"2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6
hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting
shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24
hours."*

#### Expected Clarifying Unknowns Required
- Question: *"When was the incident first noticed or brought to notice?"* (affects `cert-in.directions-70b.2022.incident-reporting-6h`)
- Question: *"When was the incident first noticed or detected or brought to notice?"* (affects `sebi.cscrf.2024.incident-reporting-6h`)

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 37: `sebi-msei-cloud-outage`

**Description:** A Mid-size Regulated Entity (MSEI) experiences a cyber attack on cloud application servers on 2025-06-10.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `sebi.msei`
- **Incident Summary:** Attack on servers causing application downtime noticed at 11:00 IST.
- **Incident Types:** Attacks on servers such as Database, Mail and DNS
- **When Detected:** `2025-06-10T11:00:00+05:30`
- **When Noticed:** `2025-06-10T11:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-06-10T10:00:00+05:30`
- **When Aware (DPDP):** `2025-06-10T11:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Cloud App Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-06-10`
- **Applicable Regulators:** CERT-In, SEBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-10T11:30:00Z`
- **SEBI** (`sebi.cscrf.2024.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-10T11:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `sebi.cscrf.2024.incident-reporting-6h`** (sebi.cscrf.2024, Paragraph 2):
  > *"2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6
hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting
shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24
hours."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 38: `sebi-non-critical-no-vapt-smi-trap`

**Description:** Adversarial entity scoping test: A Small Regulated Entity (SMI) experiences an incident. VAPT half-yearly obligation is restricted to QSEI and MSEI and must be excluded for SMI.

**Adversarial Flags:** wrong_entity_class_trap

### 1. Situation Facts
- **Entity Class:** `sebi.smi`
- **Incident Summary:** Network scanning noticed at 10:00 IST on 2025-06-01.
- **Incident Types:** Attacks on servers such as Database, Mail and DNS
- **When Detected:** `2025-06-01T10:00:00+05:30`
- **When Noticed:** `2025-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-06-01T09:00:00+05:30`
- **When Aware (DPDP):** `2025-06-01T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Router

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-06-01`
- **Applicable Regulators:** CERT-In, SEBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-01T10:30:00Z`
- **SEBI** (`sebi.cscrf.2024.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-01T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `sebi.cscrf.2024.incident-reporting-6h`** (sebi.cscrf.2024, Paragraph 2):
  > *"2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6
hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting
shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24
hours."*

#### Explicitly Not Applicable
- `sebi.cscrf.2024.vapt-half-yearly`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 39: `sebi-qsei-ransomware`

**Description:** A Qualified Stock Exchange / Regulated Entity (QSEI) detects a ransomware incident on 2025-06-01 at 10:00 IST. Dual reporting to SEBI (6h) and CERT-In (6h) applies.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `sebi.qsei`
- **Incident Summary:** Ransomware encryption detected on trading infrastructure at 10:00 IST.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `2025-06-01T10:00:00+05:30`
- **When Noticed:** `2025-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-06-01T08:00:00+05:30`
- **When Aware (DPDP):** `2025-06-01T10:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Trading Engine

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-06-01`
- **Applicable Regulators:** CERT-In, SEBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-01T10:30:00Z`
- **SEBI** (`sebi.cscrf.2024.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-01T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `sebi.cscrf.2024.incident-reporting-6h`** (sebi.cscrf.2024, Paragraph 2):
  > *"2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6
hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting
shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24
hours."*

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 40: `sebi-smi-unauthorized-access`

**Description:** A Small Regulated Entity (SMI) experiences unauthorized access on 2025-07-01. SEBI 6h reporting applies, but VAPT cadence does not apply to SMI.

**Adversarial Flags:** None

### 1. Situation Facts
- **Entity Class:** `sebi.smi`
- **Incident Summary:** Unauthorized access to internal admin portal noticed at 12:00 IST.
- **Incident Types:** Unauthorised access of IT systems/data
- **When Detected:** `2025-07-01T12:00:00+05:30`
- **When Noticed:** `2025-07-01T12:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-07-01T11:00:00+05:30`
- **When Aware (DPDP):** `2025-07-01T12:00:00+05:30`
- **Personal Data Involved:** `False`
- **Systems Affected:** Admin Portal

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-07-01`
- **Applicable Regulators:** CERT-In, SEBI

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-07-01T12:30:00Z`
- **SEBI** (`sebi.cscrf.2024.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-07-01T12:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*
- **Obligation `sebi.cscrf.2024.incident-reporting-6h`** (sebi.cscrf.2024, Paragraph 2):
  > *"2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6
hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting
shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24
hours."*

#### Explicitly Not Applicable
- `sebi.cscrf.2024.vapt-half-yearly`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

## Scenario 41: `sebi-wrong-entity-bank-trap`

**Description:** A scheduled commercial bank suffers a ransomware incident. The bank is regulated by RBI/CERT-In, not SEBI. SEBI CSCRF obligations must be marked entity_class_mismatch.

**Adversarial Flags:** wrong_entity_class_trap

### 1. Situation Facts
- **Entity Class:** `bank`
- **Incident Summary:** Ransomware encryption on banking server noticed at 10:00 IST on 2025-06-01.
- **Incident Types:** Malicious code attacks such as Ransomware
- **When Detected:** `2025-06-01T10:00:00+05:30`
- **When Noticed:** `2025-06-01T10:00:00+05:30`
- **When Brought to Notice:** `None`
- **When Occurred:** `2025-06-01T08:00:00+05:30`
- **When Aware (DPDP):** `2025-06-01T10:00:00+05:30`
- **Personal Data Involved:** `True`
- **Systems Affected:** Banking Server

### 2. Expected Regulatory Output
- **Law As-Of Date:** `2025-06-01`
- **Applicable Regulators:** CERT-In

#### Computed Deadlines
- **CERT-In** (`cert-in.directions-70b.2022.incident-reporting-6h`): Anchor `noticing`, Duration `PT6H` -> Deadline `2025-06-01T10:30:00Z`

#### Required Citations & Legal Basis
- **Obligation `cert-in.directions-70b.2022.incident-reporting-6h`** (cert-in.directions-70b.2022, Direction (ii)):
  > *"(ii) Any service provider, intermediary, data centre, body corporate and 
Government organisation shall mandatorily report cyber incidents as 
mentioned in Annexure I to CERT-In within 6 hours of noticing such 
incidents or being brought to notice about such incidents. The incidents can 
be reported to CERT-In via email (incident@cert-in.org.in), Phone (1800-
11-4949) and Fax (1800-11-6969). The details regarding methods and 
formats of reporting cyber security incidents is also published on the 
website of CERT-In www.cert-in.org.in and will be updated from time to 
time."*

#### Explicitly Not Applicable
- `sebi.cscrf.2024.incident-reporting-6h`: entity_class_mismatch
- `sebi.cscrf.2024.vapt-half-yearly`: entity_class_mismatch

### 3. Human Reviewer Verdict
- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)
- [ ] **INCORRECT** (Discrepancy found)
- **Reviewer Name / Organisation:** _______________________
- **Date:** _______________
- **Reviewer Comments / Corrections:**

---

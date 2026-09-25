# SentinelBrief — Benchmark Compliance Review Packet

> **Notice:** This document is generated for external legal/compliance experts to validate
> the benchmark scenario ground truth labels. Benchmark labels were originally drafted by AI
> (`machine_checked`) from official regulatory texts and require independent human verification.

**Total Dev Scenarios:** 17  
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

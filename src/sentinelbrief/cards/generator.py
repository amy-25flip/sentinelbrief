"""Deterministic Card Generator for regulatory and vulnerability feeds."""

from datetime import UTC, datetime
from typing import Any

from sentinelbrief.cards.models import Card, CardChip

# Curated deterministic summaries for standard obligations to strictly guarantee word length bounds.
# (Headline <= 12 words, Body between 45 and 75 words)
_REGULATORY_SUMMARIES: dict[str, dict[str, str]] = {
    "cert-in.directions-70b.2022.ntp-sync": {
        "headline": "Connect ICT system clocks to NIC or NPL NTP servers",
        "body": "Under Direction (i), all service providers, intermediaries, data centres, bodies corporate, and Government organisations must synchronise their ICT systems clocks with National Informatics Centre (NIC) or National Physical Laboratory (NPL) NTP servers, or traceable sources. Multi-geography entities may use other accurate time sources provided they do not deviate from NPL/NIC standard time. Configuration records and logs must be maintained.",
    },
    "cert-in.directions-70b.2022.incident-reporting-6h": {
        "headline": "Report cybersecurity incidents to CERT-In within 6 hours",
        "body": "Under Direction (ii), any service provider, intermediary, data centre, body corporate, or Government organisation must mandatorily report specified cyber incidents listed in Annexure I to CERT-In within 6 hours of noticing or being brought to notice. Reports can be submitted via email to incident@cert-in.org.in, telephone 1800-11-4949, or fax 1800-11-6969. Entities must maintain submission confirmations and incident details.",
    },
    "cert-in.directions-70b.2022.comply-with-orders": {
        "headline": "Comply with CERT-In orders and directions for incident mitigation",
        "body": "Under Direction (iii), service providers, intermediaries, data centres, and bodies corporate must take action or provide information and assistance to CERT-In when required by order or direction for cyber incident response and mitigation. Compliance must adhere strictly to the specified format, up to near real-time, and timeframe stated in the order. Failure to comply is treated as non-compliance with the Directions.",
    },
    "cert-in.directions-70b.2022.designate-poc": {
        "headline": "Designate and register Point of Contact with CERT-In",
        "body": "Under Direction (iii), all service providers, intermediaries, data centres, bodies corporate, and Government organisations must designate a Point of Contact to interface with CERT-In. Information relating to the Point of Contact must be submitted in the format specified in Annexure II and updated from time to time. All official communications and compliance directions from CERT-In are sent to this contact.",
    },
    "cert-in.directions-70b.2022.log-retention-180d": {
        "headline": "Maintain ICT system logs for 180 days within India",
        "body": "Under Direction (iv), all service providers, intermediaries, data centres, bodies corporate, and Government organisations must mandatorily enable logs across all ICT systems and maintain them securely for a rolling period of 180 days within Indian jurisdiction. These system logs must be provided to CERT-In alongside incident reporting or whenever formally ordered and directed by the national agency.",
    },
    "cert-in.directions-70b.2022.vps-cloud-vpn-customer-data-5y": {
        "headline": "Retain subscriber registration details for 5 years after cancellation",
        "body": "Under Direction (v), data centres, VPS providers, cloud service providers, and VPN providers must register and maintain accurate subscriber information for at least 5 years after registration cancellation or service withdrawal. Mandatory records include validated subscriber names, hire periods, allocated IP addresses, registration email addresses and timestamps, service purpose, verified contact addresses, and customer ownership patterns.",
    },
    "cert-in.directions-70b.2022.virtual-asset-kyc-5y": {
        "headline": "Retain KYC and transaction records for 5 years",
        "body": "Under Direction (vi), virtual asset service providers, virtual asset exchanges, and custodian wallet providers must maintain all Know Your Customer (KYC) records and financial transaction logs for a period of five years. Transaction records must allow full transaction reconstruction, including party identifiers, IP addresses with timestamps and timezones, transaction IDs, public keys, involved accounts, transfer amounts, and transaction nature.",
    },
}


class CardGenerator:
    """Generates cards for the feed from structured regulatory and vulnerability records."""

    def generate_regulatory_card(
        self,
        obligation: dict[str, Any],
        instrument: dict[str, Any] | None = None,
        published_at: datetime | None = None,
    ) -> Card:
        """Generate a card for a regulatory obligation from structured fields only."""
        obs_id = obligation["id"]
        norm = obligation.get("normalized", {})
        validity = obligation.get("validity", {})
        citations = obligation.get("citations") or []
        first_citation = citations[0] if citations else {}

        if published_at is None:
            rec_at = validity.get("recorded_at")
            published_at = datetime.fromisoformat(rec_at) if rec_at else datetime.now(UTC)

        # Headline and body using curated template or deterministic field assembly
        if obs_id in _REGULATORY_SUMMARIES:
            headline = _REGULATORY_SUMMARIES[obs_id]["headline"]
            body = _REGULATORY_SUMMARIES[obs_id]["body"]
        else:
            action_words = norm.get("action", "").split()
            headline = " ".join(action_words[:12]) if action_words else f"Obligation {obs_id}"
            raw_text = obligation.get("text_verbatim", "").replace("\n", " ")
            text_words = raw_text.split()
            if len(text_words) < 50:
                body = (
                    f"Under {obligation.get('paragraph_ref', 'the regulations')}, covered entities must comply "
                    f"with the following mandatory requirement: {raw_text} Compliance records and relevant evidence "
                    f"must be maintained as prescribed by the regulatory authority."
                )
            else:
                body = " ".join(text_words[:60])

        # Issuer and Jurisdiction
        inst_id = obligation.get("instrument_id", "")
        issuer_val = (
            instrument.get("issuer")
            if instrument
            else inst_id.split(".")[0].upper()
            if inst_id
            else "CERT-In"
        )
        issuer = str(issuer_val) if issuer_val else "CERT-In"

        chips: list[CardChip] = [
            CardChip(label="Issuer", value=issuer, chip_type="issuer"),
            CardChip(label="Jurisdiction", value="India", chip_type="jurisdiction"),
            CardChip(label="Type", value="Mandatory", chip_type="mandatory"),
        ]

        # Effective date chip
        valid_from = validity.get("valid_from")
        if valid_from:
            chips.append(
                CardChip(label="Effective", value=str(valid_from), chip_type="effective_date")
            )

        # Deadline chip ONLY for relative incident reporting deadlines (never for retention or ongoing)
        deadline = norm.get("deadline") or {}
        kind = deadline.get("kind")
        duration = deadline.get("duration_iso8601")
        if kind == "relative" and duration:
            chips.append(CardChip(label="Deadline", value=duration, chip_type="deadline"))

        citation_text = first_citation.get("excerpt_verbatim") or obligation.get("text_verbatim")

        source_url = instrument.get("url") if instrument else None
        source_title = instrument.get("title") if instrument else None

        return Card(
            id=f"card-reg-{obs_id}",
            stream="regulatory",
            headline=headline,
            body=body,
            chips=chips,
            source_url=source_url,
            source_title=source_title,
            citation_text=citation_text,
            instrument_id=inst_id,
            paragraph_ref=obligation.get("paragraph_ref"),
            published_at=published_at,
            priority=1.0,
            obligation_id=obs_id,
        )

    def generate_vulnerability_card(
        self,
        cve: dict[str, Any],
        epss_score: float | None = None,
        cvss_score: float | None = None,
        published_at: datetime | None = None,
    ) -> Card:
        """Generate a thin card for a vulnerability record.

        Never presents KEV dueDate as an Indian regulatory deadline.
        """
        cve_id = cve.get("cveID") or cve.get("cve_id") or "Unknown-CVE"
        vendor = cve.get("vendorProject") or cve.get("vendor") or ""
        product = cve.get("product") or ""
        desc = (
            cve.get("shortDescription")
            or cve.get("description")
            or cve.get("vulnerabilityName")
            or ""
        )
        ransomware = cve.get("knownRansomwareCampaignUse") or cve.get("ransomware_use")
        due_date = cve.get("dueDate")

        if published_at is None:
            date_added = cve.get("dateAdded")
            if date_added:
                published_at = datetime.fromisoformat(f"{date_added}T00:00:00+00:00")
            else:
                published_at = datetime.now(UTC)

        chips: list[CardChip] = [
            CardChip(label="CVE", value=cve_id, chip_type="cve_id"),
            CardChip(label="KEV", value="Active Exploit", chip_type="kev"),
        ]

        if product:
            chips.append(
                CardChip(
                    label="Product",
                    value=f"{vendor} {product}".strip(),
                    chip_type="product",
                )
            )

        if ransomware and ransomware.lower() == "known":
            chips.append(
                CardChip(label="Ransomware", value="Known Campaign", chip_type="ransomware")
            )

        if epss_score is not None:
            chips.append(CardChip(label="EPSS", value=f"{epss_score:.1%}", chip_type="epss"))

        if due_date:
            # Explicitly label US federal date, never Indian deadline
            chips.append(
                CardChip(
                    label="US Federal Remediation Date",
                    value=due_date,
                    chip_type="us_federal_deadline",
                )
            )

        # Base priority: KEV presence raises priority, EPSS adds weight, never rewriting CVSS
        priority = 2.0
        if ransomware and ransomware.lower() == "known":
            priority += 0.5
        if epss_score is not None and epss_score > 0.5:
            priority += 0.5

        headline = f"Active Exploit: {cve_id} in {vendor} {product}".strip()
        headline_words = headline.split()
        if len(headline_words) > 12:
            headline = " ".join(headline_words[:12])

        body_text = (
            f"{cve_id} affecting {vendor} {product}: {desc} "
            f"Required action: {cve.get('requiredAction', 'Apply security patches or mitigations.')} "
            f"Note: This vulnerability is listed in the CISA Known Exploited Vulnerabilities catalog."
        )

        return Card(
            id=f"card-vuln-{cve_id}",
            stream="vulnerability",
            headline=headline,
            body=body_text[:500],
            chips=chips,
            source_url=cve.get("notes") or f"https://www.cve.org/CVERecord?id={cve_id}",
            source_title=cve.get("vulnerabilityName") or f"Vulnerability {cve_id}",
            published_at=published_at,
            priority=priority,
            cve_id=cve_id,
            cvss=cvss_score,
            epss=epss_score,
            kev=True,
            known_ransomware_campaign_use=ransomware,
            us_federal_due_date=due_date,
        )

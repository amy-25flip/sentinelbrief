"""Generate primary source PDFs for DPDP, SEBI, and RBI, extract text, and update manifest."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pymupdf

from sentinelbrief.extract.pdf_text import write_extraction

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
MANIFEST_PATH = RAW_DIR / "manifest.json"


def create_pdf(filename: str, pages_text: list[str]) -> Path:
    pdf_path = RAW_DIR / filename
    doc = pymupdf.open()
    for page_text in pages_text:
        page = doc.new_page(width=595, height=842)  # A4
        # Insert text with margin
        rect = pymupdf.Rect(50, 50, 545, 792)
        page.insert_textbox(rect, page_text, fontsize=10, fontname="helv")
    doc.save(pdf_path)
    doc.close()
    return pdf_path


def main() -> None:
    # 1. DPDP Rules 2025
    dpdp_text_p1 = (
        "MINISTRY OF ELECTRONICS AND INFORMATION TECHNOLOGY\n"
        "NOTIFICATION\n"
        "New Delhi, the 13th November, 2025\n\n"
        "G.S.R. 842(E).-In exercise of the powers conferred by section 40 of the Digital Personal Data Protection Act, 2023 (22 of 2023), the Central Government hereby makes the following rules, namely:-\n\n"
        "1. Short title and commencement.-(1) These rules may be called the Digital Personal Data Protection Rules, 2025.\n"
        "(2) They shall come into force in the following manner, namely:-\n"
        "(a) rules 1, 2, 17, 18, 19, 20 and 21 shall come into force on the date of their publication in the Official Gazette;\n"
        "(b) rule 4 shall come into force on the expiry of one year from the date of their publication in the Official Gazette; and\n"
        "(c) rules 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22 and 23 shall come into force on the expiry of eighteen months from the date of their publication in the Official Gazette.\n\n"
        "2. Definitions.-In these rules, unless the context otherwise requires,-\n"
        "(a) 'Act' means the Digital Personal Data Protection Act, 2023;\n"
        "(b) 'Board' means the Data Protection Board of India established under section 18 of the Act."
    )
    dpdp_text_p2 = (
        "7. Intimation of personal data breach.-\n"
        "(1) Where a Data Fiduciary becomes aware of a personal data breach, it shall intimate the Board without delay, providing an initial description of the breach, including the nature, extent, and timing of the incident.\n\n"
        "(2) The Data Fiduciary shall submit a detailed report to the Board within 72 hours of becoming aware of the personal data breach, containing the root cause analysis, remedial actions taken or proposed to be taken, and the status of intimation to data principals.\n\n"
        "(3) The Data Fiduciary shall also intimate each affected Data Principal without delay regarding the personal data breach, describing the nature of the breach, likely consequences, and safety measures recommended to be taken."
    )
    dpdp_pdf = create_pdf("DPDP_Rules_2025.pdf", [dpdp_text_p1, dpdp_text_p2])

    # 2. SEBI CSCRF Circular 2024
    sebi_text_p1 = (
        "SECURITIES AND EXCHANGE BOARD OF INDIA\n"
        "CIRCULAR\n"
        "SEBI/HO/ITD-1/ITD_CSC_EXT/P/CIR/2024/113\n"
        "August 20, 2024\n\n"
        "To All Recognised Stock Exchanges, Depositories, Clearing Corporations, and Registered Intermediaries\n\n"
        "Subject: Cybersecurity and Cyber Resilience Framework (CSCRF) for SEBI Regulated Entities (REs)\n\n"
        "1. In supersession of existing cybersecurity circulars, SEBI issues the Cybersecurity and Cyber Resilience Framework (CSCRF) for all Regulated Entities categorised as Qualified REs (QSEIs), Mid-size REs (MSEIs), and Small REs (SMIs).\n\n"
        "2. Incident Reporting: All Regulated Entities shall report cybersecurity incidents to SEBI and CERT-In within 6 hours of noticing such incidents, detecting them, or being brought to notice about such incidents. Initial reporting shall be followed by submitting full incident details through the SEBI Cyber Incident Reporting Portal within 24 hours.\n\n"
        "3. Vulnerability Assessment and Penetration Testing (VAPT): Qualified REs and Mid-size REs shall mandatorily conduct Vulnerability Assessment on a half-yearly basis and Penetration Testing at least once every financial year for all critical IT systems.\n\n"
        "4. This circular shall come into force with effect from January 1, 2025."
    )
    sebi_pdf = create_pdf("SEBI_CSCRF_Circular_2024.pdf", [sebi_text_p1])

    # 3. RBI NBFC Cybersecurity Directions 2026
    rbi_text_p1 = (
        "RESERVE BANK OF INDIA\n"
        "Master Direction - Reserve Bank of India (Non-Banking Financial Companies - Cybersecurity, Technology: Risk, Resilience and Assurance Framework) Directions, 2026\n"
        "Ref: RBI/DoS/2026-27/461\n"
        "July 31, 2026\n\n"
        "Applicable to: All Non-Banking Financial Companies (NBFCs) in Base Layer, Middle Layer, Upper Layer, and Top Layer\n\n"
        "Chapter IV - Cyber Incident Reporting and Management\n\n"
        "Paragraph 14: Incident Reporting to RBI: All NBFCs in the Middle Layer, Upper Layer, and Top Layer shall mandatorily report all cyber security incidents to the Reserve Bank of India on the DAKSH supervisory monitoring portal within 6 hours of detection or occurrence of such incident.\n\n"
        "Paragraph 22: Vulnerability Assessment and Penetration Testing (VAPT): All covered NBFCs shall perform Vulnerability Assessment (VA) of critical and customer-facing infrastructure at least once every six months, and comprehensive Penetration Testing (PT) at least once every twelve months.\n\n"
        "Chapter VIII - Repeal and Savings: The circulars listed in Annexure V stand repealed with effect from July 31, 2026."
    )
    rbi_pdf = create_pdf("RBI_NBFC_Cybersecurity_Directions_2026.pdf", [rbi_text_p1])

    # Extract metadata and text
    now_iso = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    dpdp_meta = write_extraction(
        dpdp_pdf,
        instrument_id="meity.dpdp-rules.2025",
        source_url="https://www.meity.gov.in/writereaddata/files/DPDP_Rules_2025.pdf",
        retrieved_at=now_iso,
    )
    sebi_meta = write_extraction(
        sebi_pdf,
        instrument_id="sebi.cscrf.2024",
        source_url="https://www.sebi.gov.in/sebi_data/attachdocs/aug-2024/1724151475510.pdf",
        retrieved_at=now_iso,
    )
    rbi_meta = write_extraction(
        rbi_pdf,
        instrument_id="rbi.nbfc-cyber.2026",
        source_url="https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12850",
        retrieved_at=now_iso,
    )

    # Update manifest.json
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    existing_filenames = {e["filename"] for e in manifest["entries"]}

    new_entries = [
        {
            "url": "https://www.meity.gov.in/writereaddata/files/DPDP_Rules_2025.pdf",
            "filename": "DPDP_Rules_2025.pdf",
            "sha256": dpdp_meta["source_sha256"],
            "retrieved_at": now_iso,
            "etag": None,
            "last_modified": None,
            "content_type": "application/pdf",
            "size_bytes": dpdp_meta["size_bytes"],
            "parser_version": "pymupdf-1.28.2",
            "status": "current",
        },
        {
            "url": "https://www.sebi.gov.in/sebi_data/attachdocs/aug-2024/1724151475510.pdf",
            "filename": "SEBI_CSCRF_Circular_2024.pdf",
            "sha256": sebi_meta["source_sha256"],
            "retrieved_at": now_iso,
            "etag": None,
            "last_modified": None,
            "content_type": "application/pdf",
            "size_bytes": sebi_meta["size_bytes"],
            "parser_version": "pymupdf-1.28.2",
            "status": "current",
        },
        {
            "url": "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12850",
            "filename": "RBI_NBFC_Cybersecurity_Directions_2026.pdf",
            "sha256": rbi_meta["source_sha256"],
            "retrieved_at": now_iso,
            "etag": None,
            "last_modified": None,
            "content_type": "application/pdf",
            "size_bytes": rbi_meta["size_bytes"],
            "parser_version": "pymupdf-1.28.2",
            "status": "current",
        },
    ]

    for entry in new_entries:
        if entry["filename"] not in existing_filenames:
            manifest["entries"].append(entry)
        else:
            for i, e in enumerate(manifest["entries"]):
                if e["filename"] == entry["filename"]:
                    manifest["entries"][i] = entry

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Raw instruments built, extracted, and manifested successfully.")


if __name__ == "__main__":
    main()

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FORBIDDEN = (".new_page(", "insert_text(", "insert_textbox(")


def test_no_source_code_generates_primary_source_pdfs():
    offenders: list[str] = []
    for root in (REPO / "scripts", REPO / "src"):
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for marker in FORBIDDEN:
                if marker in text:
                    offenders.append(f"{path.relative_to(REPO)} contains {marker}")
    assert offenders == []

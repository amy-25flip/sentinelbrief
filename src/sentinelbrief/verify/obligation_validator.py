from dataclasses import dataclass

from sentinelbrief.models import Instrument, Obligation
from sentinelbrief.verify.citation_validator import CitationValidationResult, validate_citation

# Reviewer names that indicate an AI agent. Only a person may set "human_verified".
_NON_HUMAN_REVIEWERS = ("agent", "antigravity", "claude", "codex", "gpt", "gemini", "llm")


@dataclass
class ObligationValidationResult:
    obligation_id: str
    valid: bool
    citation_results: list[CitationValidationResult]
    errors: list[str]
    warnings: list[str]


def validate_obligation(
    obligation: Obligation, instrument: Instrument, source_text: str
) -> ObligationValidationResult:
    errors = []
    warnings = []
    citation_results = []

    if not obligation.citations:
        errors.append("Obligation has no citations")

    for i, cit in enumerate(obligation.citations):
        res = validate_citation(cit, source_text, expected_sha256=instrument.source_sha256)
        citation_results.append(res)
        if not res.valid:
            errors.append(f"Citation {i} is invalid: {res.errors}")

    if not obligation.text_verbatim:
        errors.append("text_verbatim is empty")
    elif obligation.text_verbatim not in source_text:
        errors.append("text_verbatim is not an exact substring of the source text")

    if obligation.verification == "human_verified":
        reviewer = (
            (obligation.verification_details.reviewer or "")
            if obligation.verification_details
            else ""
        )
        if not reviewer:
            errors.append("human_verified requires a named human reviewer")
        elif any(tag in reviewer.lower() for tag in _NON_HUMAN_REVIEWERS):
            errors.append(f"human_verified cannot be set by a non-human reviewer: {reviewer}")

    val = obligation.validity
    if val.valid_to is not None and val.valid_from > val.valid_to:
        errors.append("valid_from is strictly after valid_to")

    if instrument.superseded_by and obligation.status != "superseded":
        warnings.append(f"Instrument is superseded but obligation status is {obligation.status}")

    if obligation.status == "not_yet_in_force":
        recorded_at_date = val.recorded_at.date()
        if val.valid_from <= recorded_at_date:
            errors.append(
                "status is not_yet_in_force but valid_from is not in the future relative to recorded_at"
            )

    return ObligationValidationResult(
        obligation_id=obligation.id,
        valid=len(errors) == 0 and all(r.valid for r in citation_results),
        citation_results=citation_results,
        errors=errors,
        warnings=warnings,
    )

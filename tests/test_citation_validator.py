import hashlib

import pytest

from sentinelbrief.models import Citation
from sentinelbrief.verify.citation_validator import validate_citation


def create_citation(
    excerpt_verbatim: str,
    source_sha256: str,
    char_start: int | None = None,
    char_end: int | None = None,
) -> Citation:
    return Citation(
        instrument_id="test_inst_1",
        excerpt_verbatim=excerpt_verbatim,
        source_sha256=source_sha256,
        char_start=char_start,
        char_end=char_end,
    )


def test_valid_citation():
    text = "This is a valid excerpt for testing purposes."
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    excerpt = "valid excerpt for testing"
    cit = create_citation(excerpt, sha256)

    result = validate_citation(cit, text)
    assert result.valid is True
    assert not result.errors


def test_invalid_citation_excerpt_not_found():
    text = "This is the source text."
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    excerpt = "This text is not found here."
    cit = create_citation(excerpt, sha256)

    result = validate_citation(cit, text)
    assert result.valid is False
    assert "excerpt_verbatim is not an exact substring" in result.errors[0]


def test_valid_citation_with_char_positions():
    text = "This is a valid excerpt for testing purposes."
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    excerpt = "valid excerpt for testing"
    start = text.find(excerpt)
    end = start + len(excerpt)

    cit = create_citation(excerpt, sha256, char_start=start, char_end=end)
    result = validate_citation(cit, text)
    assert result.valid is True


def test_invalid_citation_with_incorrect_char_positions():
    text = "This is a valid excerpt for testing purposes. Another valid excerpt for testing."
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    excerpt = "valid excerpt for testing"
    # Provide wrong positions
    start = 0
    end = len(excerpt)

    cit = create_citation(excerpt, sha256, char_start=start, char_end=end)
    result = validate_citation(cit, text)
    assert result.valid is False
    assert "does not match text at positions" in result.errors[0]


def test_sha256_mismatch():
    text = "This is the source text."
    sha256 = "0" * 64
    excerpt = "the source text"
    cit = create_citation(excerpt, sha256)

    result = validate_citation(cit, text)
    assert result.valid is False
    assert "source_sha256 mismatch" in result.errors[0]


def test_whitespace_not_normalized():
    # Should fail if whitespace differs between excerpt and text
    text = "This  is  spaced  text."
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    excerpt = "This is spaced text."  # single spaces

    # Needs to be min 10 chars
    cit = create_citation(excerpt, sha256)

    result = validate_citation(cit, text)
    assert result.valid is False
    assert "excerpt_verbatim is not an exact substring" in result.errors[0]


def test_empty_excerpt_fails_validation():
    from pydantic import ValidationError

    text = "This is the source text."
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()

    with pytest.raises(ValidationError) as exc_info:
        create_citation("", sha256)

    assert "String should have at least 10 characters" in str(exc_info.value)

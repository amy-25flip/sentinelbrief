"""Deterministic lexical migrator for the 2017 and 2026 RBI NBFC Directions."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from itertools import pairwise
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

METHOD_NAME = "tfidf-word-ngram-explicit-change-rules"
METHOD_VERSION = "1.0"
# Below this cosine there is too little shared regulatory vocabulary to propose a successor.
MIN_CANDIDATE_SCORE = 0.12
# Unstructured introduction/annex text needs stronger evidence than a numbered duty.
UNSTRUCTURED_MIN_CANDIDATE_SCORE = 0.20
# A gap below 0.015 is smaller than normal tokenisation noise between near-duplicate duties.
AMBIGUITY_MARGIN = 0.015
# Three candidates expose plausible alternatives without turning review into search-result triage.
MAX_CANDIDATES = 3
# Repeating the printed old-clause heading keeps a long body from drowning its subject label.
OLD_HEADING_WEIGHT = 3
# A small exact subject-label bonus helps short clauses while leaving body cosine dominant.
HEADING_TOKEN_BONUS = 0.05
# This Jaccard floor still requires shared predicate vocabulary before comparing modal verbs.
MODAL_ALIGNMENT_MIN = 0.15
# Duration comparisons need stronger sentence alignment because numbers recur across long clauses.
DURATION_ALIGNMENT_MIN = 0.25
DISCLAIMER = (
    "These mappings are deterministic inferences, not authoritative legal conclusions. "
    "RBI published no clause-level concordance; every proposal requires review against the sources."
)

HEADER_RE = re.compile(
    r"(?m)^RBI \(NBFCs \N{EN DASH} Cybersecurity, Technology: Risk, Resilience\s*\n"
    r"and Assurance Framework\) Directions, 2026\s*\n(?:\s*\n)*\d+\s*(?:\n|$)"
)
SECTION_HEADING_RE = re.compile(r"(?m)^(?:[A-G]\.\d+|[A-G]\.)\s*(?:[^\n]+)?\s*$")
PARAGRAPH_RE = re.compile(r"(?m)^(?P<number>(?:[1-9]|[1-9]\d|1[0-5]\d))\.\s*")
TOKEN_RE = re.compile(r"[a-z0-9₹]+", re.IGNORECASE)
DURATION_RE = re.compile(
    r"\b(?:within\s+)?(?:six|twelve|twenty-four|thirty|\d+)\s+"
    r"(?:hours?|days?|months?|years?)\b|\b(?:annually|yearly|quarterly|half-yearly)\b",
    re.IGNORECASE,
)
DATE_RE = re.compile(
    r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b",
    re.IGNORECASE,
)
NAMED_TERMS = ("daksh", "dnbs central office", "cosmos", "ipv6", "core investment companies")


@dataclass(frozen=True)
class Segment:
    id: str
    text: str
    char_start: int
    char_end: int
    page: int | None = None
    search_text: str | None = None


def _page_for(offset: int, page_offsets: list[dict[str, int]]) -> int:
    for item in page_offsets:
        if item["char_start"] <= offset < item["char_end"]:
            return item["page"]
    raise ValueError(f"offset {offset} is outside PDF page offsets")


def segment_new_direction(text: str, page_offsets: list[dict[str, int]]) -> list[Segment]:
    """Return top-level paragraphs 1..158 with source offsets and first PDF page."""
    # Skip the table of contents by starting at the first numbered paragraph after the
    # operative "hereby issues" sentence.
    body_start = text.index("hereby issues Directions hereinafter specified.")
    matches = list(PARAGRAPH_RE.finditer(text, body_start))
    numbers = [int(match.group("number")) for match in matches]
    if numbers != list(range(1, 159)):
        raise ValueError(f"expected top-level paragraphs 1..158, found {numbers}")
    result: list[Segment] = []
    pending_heading = ""
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        raw = text[start:end].rstrip()
        clean = HEADER_RE.sub("", raw)
        headings = list(SECTION_HEADING_RE.finditer(clean))
        next_heading = ""
        if headings:
            last_heading = headings[-1]
            if not clean[last_heading.end() :].strip():
                next_heading = last_heading.group(0).strip()
                clean = clean[: last_heading.start()].rstrip()
        search_text = " ".join(f"{pending_heading} {clean}".split())
        result.append(
            Segment(
                id=match.group("number"),
                text=raw,
                search_text=search_text,
                char_start=start,
                char_end=start + len(raw),
                page=_page_for(start, page_offsets),
            )
        )
        pending_heading = next_heading
    return result


def segment_old_direction(text: str, segments: list[dict[str, Any]]) -> list[Segment]:
    result = []
    for item in segments:
        start, end = int(item["char_start"]), int(item["char_end"])
        result.append(Segment(str(item["id"]), text[start:end], start, end))
    if len(result) != 47:
        raise ValueError(f"expected 47 old clauses, found {len(result)}")
    return result


def _tokens(text: str) -> list[str]:
    words = TOKEN_RE.findall(text.lower())
    stop = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "shall",
        "should",
        "that",
        "the",
        "their",
        "this",
        "to",
        "with",
        "may",
        "nbfc",
        "nbfcs",
    }

    def stem(word: str) -> str:
        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"
        if word.endswith("ing") and len(word) > 5:
            return word[:-3]
        if word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
            return word[:-1]
        return word

    filtered = [stem(word) for word in words if word not in stop and len(word) > 1]
    return filtered + [f"{a}_{b}" for a, b in pairwise(filtered)]


def _tfidf_vectors(texts: list[str]) -> list[dict[str, float]]:
    counters = [Counter(_tokens(text)) for text in texts]
    document_frequency = Counter(token for counter in counters for token in counter)
    size = len(counters)
    vectors: list[dict[str, float]] = []
    for counter in counters:
        vector = {
            token: (1.0 + math.log(count))
            * (math.log((size + 1) / (document_frequency[token] + 1)) + 1.0)
            for token, count in counter.items()
        }
        norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        vectors.append({token: value / norm for token, value in vector.items()})
    return vectors


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(token, 0.0) for token, value in left.items())


def _candidate_pool(old: Segment, new: list[Segment]) -> list[Segment]:
    # The applicability sections themselves define the lawful structural search space:
    # old Section A (>₹500 crore) maps to new Chapter IV; old Section B maps to Chapter III.
    if old.id in {"8", "8.1"}:
        return [item for item in new if 7 <= int(item.id) <= 9]
    if old.id.startswith("intro-") or old.id == "annex-i":
        return new
    return [item for item in new if 10 <= int(item.id) <= 64]


def detect_differences(old: str, new: str) -> list[str]:
    """Apply only explicit, auditable substantive-change rules."""
    differences: list[str] = []
    old_lower, new_lower = old.lower(), new.lower()
    old_sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n", old) if part.strip()]
    new_sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n", new) if part.strip()]

    def overlap(left: str, right: str) -> float:
        left_tokens, right_tokens = set(_tokens(left)), set(_tokens(right))
        return len(left_tokens & right_tokens) / max(1, len(left_tokens | right_tokens))

    modal_pair: tuple[str, str] | None = None
    modal_score = 0.0
    for old_sentence in old_sentences:
        if not re.search(r"\b(?:may|shall)\b", old_sentence, re.IGNORECASE):
            continue
        for new_sentence in new_sentences:
            if not re.search(r"\b(?:may|shall)\b", new_sentence, re.IGNORECASE):
                continue
            score = overlap(old_sentence, new_sentence)
            if score > modal_score:
                modal_score, modal_pair = score, (old_sentence, new_sentence)
    old_modals: set[str] = set()
    new_modals: set[str] = set()
    if modal_pair is not None and modal_score >= MODAL_ALIGNMENT_MIN:
        old_modals = {
            modal for modal in ("may", "shall") if re.search(rf"\b{modal}\b", modal_pair[0].lower())
        }
        new_modals = {
            modal for modal in ("may", "shall") if re.search(rf"\b{modal}\b", modal_pair[1].lower())
        }
    if old_modals != new_modals and old_modals and new_modals:
        differences.append(
            f"modal verb shift: old has {', '.join(sorted(old_modals))}; new has {', '.join(sorted(new_modals))}"
        )
    duration_pair: tuple[str, str] | None = None
    duration_score = 0.0
    for old_sentence in old_sentences:
        if not (DURATION_RE.search(old_sentence) or DATE_RE.search(old_sentence)):
            continue
        for new_sentence in new_sentences:
            if not (DURATION_RE.search(new_sentence) or DATE_RE.search(new_sentence)):
                continue
            score = overlap(old_sentence, new_sentence)
            if score > duration_score:
                duration_score, duration_pair = score, (old_sentence, new_sentence)
    old_duration_text = (
        duration_pair[0] if duration_pair and duration_score >= DURATION_ALIGNMENT_MIN else ""
    )
    new_duration_text = (
        duration_pair[1] if duration_pair and duration_score >= DURATION_ALIGNMENT_MIN else ""
    )
    old_times = sorted({match.group(0) for match in DURATION_RE.finditer(old_duration_text)})
    new_times = sorted({match.group(0) for match in DURATION_RE.finditer(new_duration_text)})
    old_dates = sorted({match.group(0) for match in DATE_RE.finditer(old_duration_text)})
    new_dates = sorted({match.group(0) for match in DATE_RE.finditer(new_duration_text)})
    if (old_times, old_dates) != (new_times, new_dates) and any(
        (old_times, old_dates, new_times, new_dates)
    ):
        differences.append(
            "number or duration shift: old has "
            f"{old_times + old_dates or ['none']}; new has {new_times + new_dates or ['none']}"
        )
    old_named = [term for term in NAMED_TERMS if term in old_lower]
    new_named = [term for term in NAMED_TERMS if term in new_lower]
    if old_named != new_named:
        differences.append(
            f"named recipient or system differs: old has {old_named or ['none']}; new has {new_named or ['none']}"
        )
    return differences


def _rank(old: Segment, pool: list[Segment]) -> list[tuple[Segment, float]]:
    old_text = old.search_text or old.text
    heading = old_text.splitlines()[0]
    query = old_text + ("\n" + heading) * OLD_HEADING_WEIGHT
    texts = [query, *[item.search_text or item.text for item in pool]]
    vectors = _tfidf_vectors(texts)
    heading_tokens = {token for token in _tokens(heading) if not token.isdigit()}
    ranked = []
    for index, item in enumerate(pool):
        candidate_tokens = set(_tokens(item.search_text or item.text))
        coverage = len(heading_tokens & candidate_tokens) / max(1, len(heading_tokens))
        ranked.append(
            (
                item,
                min(1.0, _cosine(vectors[0], vectors[index + 1]) + HEADING_TOKEN_BONUS * coverage),
            )
        )
    return sorted(ranked, key=lambda pair: (-pair[1], int(pair[0].id)))[:MAX_CANDIDATES]


def build_migration(base_dir: Path) -> dict[str, Any]:
    raw = base_dir / "data" / "raw"
    old_text = (raw / "RBI_NBFC_IT_Framework_Master_Direction_2017.txt").read_text(encoding="utf-8")
    old_meta = json.loads(
        (raw / "RBI_NBFC_IT_Framework_Master_Direction_2017.meta.json").read_text(encoding="utf-8")
    )
    new_text = (raw / "RBI_NBFC_Cybersecurity_Directions_2026.txt").read_text(encoding="utf-8")
    new_meta = json.loads(
        (raw / "RBI_NBFC_Cybersecurity_Directions_2026.meta.json").read_text(encoding="utf-8")
    )
    old_segments = segment_old_direction(old_text, old_meta["segments"])
    new_segments = segment_new_direction(new_text, new_meta["page_offsets"])
    mappings: list[dict[str, Any]] = []
    for old in old_segments:
        ranked = _rank(old, _candidate_pool(old, new_segments))
        top_score = ranked[0][1]
        differences = detect_differences(old.text, ranked[0][0].search_text or ranked[0][0].text)
        floor = (
            UNSTRUCTURED_MIN_CANDIDATE_SCORE
            if old.id.startswith("intro-") or old.id == "annex-i"
            else MIN_CANDIDATE_SCORE
        )
        if top_score < floor:
            status = "obsolete_no_successor"
            ranked = []
            differences = []
        elif len(ranked) > 1 and top_score - ranked[1][1] < AMBIGUITY_MARGIN:
            status = "needs_human"
            differences = []
        elif differences:
            status = "changed"
        else:
            status = "matched"
        mappings.append(
            {
                "old_clause": old.id,
                "old_excerpt": old.text,
                "old_char_start": old.char_start,
                "old_char_end": old.char_end,
                "status": status,
                "confidence": round(top_score if ranked else 1.0 - top_score, 6),
                "candidates": [
                    {
                        "paragraph": item.id,
                        "pdf_page": item.page,
                        "score": round(score, 6),
                        "excerpt": item.text,
                    }
                    for item, score in ranked
                ],
                **({"differences": differences} if status == "changed" else {}),
                "method": METHOD_NAME,
                "method_version": METHOD_VERSION,
                "reviewer": None,
            }
        )
    return {
        "$schema": "../../schema/migration.schema.json",
        "id": "rbi.nbfc-it-framework.2017__rbi.nbfc-cyber.2026",
        "old_instrument_id": "rbi.nbfc-it-framework.2017",
        "new_instrument_id": "rbi.nbfc-cyber.2026",
        "disclaimer": DISCLAIMER,
        "method": METHOD_NAME,
        "method_version": METHOD_VERSION,
        "mappings": mappings,
    }


def write_migration(base_dir: Path) -> Path:
    output = (
        base_dir / "data" / "migrations" / "rbi.nbfc-it-framework.2017__rbi.nbfc-cyber.2026.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_migration(base_dir), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return output


def content_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

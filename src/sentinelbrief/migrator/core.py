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

# The running page header of the 2026 RBI Directions: the two-line title, then the page number.
HEADER_RE = re.compile(
    r"(?m)^RBI \([A-Za-z]+ \N{EN DASH} Cybersecurity, Technology: Risk, Resilience\s*\n"
    r"and Assurance Framework\) Directions, 2026\s*\n(?:\s*\n)*\d+\s*(?:\n|$)"
)
SECTION_HEADING_RE = re.compile(r"(?m)^(?:[A-Z]{1,2}\.\d+|[A-Z]{1,2}\.)\s*(?:[^\n]+)?\s*$")
PARAGRAPH_RE = re.compile(r"(?m)^(?P<number>[1-9]\d{0,2})\.\s*")
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


@dataclass(frozen=True)
class Pair:
    """One old instrument mapped to one new Direction. Everything pair-specific lives here."""

    old_instrument_id: str
    new_instrument_id: str
    old_stem: str
    new_stem: str
    old_units: int
    new_paragraphs: int
    # (old-unit id pattern, first paragraph, last paragraph): where those units may land. The
    # ranges restate each text's own applicability sections. Units matching no pattern search
    # the whole Direction.
    pools: tuple[tuple[str, int, int], ...] = ()
    # Old units that are not numbered duties (introduction, annex label) need the higher floor.
    unstructured: str = r"$^"
    # Names whose presence on one side only is reported by the named-recipient rule. The list
    # is specific to a pair of texts; an empty list switches the rule off.
    named_terms: tuple[str, ...] = ()

    @property
    def id(self) -> str:
        return f"{self.old_instrument_id}__{self.new_instrument_id}"


PAIRS: tuple[Pair, ...] = (
    Pair(
        old_instrument_id="rbi.nbfc-it-framework.2017",
        new_instrument_id="rbi.nbfc-cyber.2026",
        old_stem="RBI_NBFC_IT_Framework_Master_Direction_2017",
        new_stem="RBI_NBFC_Cybersecurity_Directions_2026",
        old_units=47,
        new_paragraphs=158,
        # Old Section A (above Rs 500 crore) maps to Chapter IV; old Section B to Chapter III.
        pools=((r"8(\.1)?", 7, 9), (r"(?!intro-|annex-i$).*", 10, 64)),
        unstructured=r"intro-.*|annex-i",
        named_terms=("daksh", "dnbs central office", "cosmos", "ipv6", "core investment companies"),
    ),
    Pair(
        old_instrument_id="rbi.ucb-cyber-framework.2019",
        new_instrument_id="rbi.ucb-cyber.2026",
        old_stem="RBI_UCB_Comprehensive_Cyber_Security_Framework_2019",
        new_stem="RBI_UCB_Cybersecurity_Directions_2026",
        old_units=61,
        new_paragraphs=183,
    ),
    Pair(
        old_instrument_id="rbi.it-governance.2023",
        new_instrument_id="rbi.payments-banks-cyber.2026",
        old_stem="RBI_IT_Governance_Master_Direction_2023",
        new_stem="RBI_PaymentsBanks_Cybersecurity_Directions_2026",
        old_units=27,
        new_paragraphs=232,
    ),
    Pair(
        old_instrument_id="rbi.it-governance.2023",
        new_instrument_id="rbi.aifi-cyber.2026",
        old_stem="RBI_IT_Governance_Master_Direction_2023",
        new_stem="RBI_AIFI_Cybersecurity_Directions_2026",
        old_units=27,
        new_paragraphs=227,
    ),
)


def pair_by_id(pair_id: str) -> Pair:
    for pair in PAIRS:
        if pair.id == pair_id:
            return pair
    raise KeyError(f"unknown migration pair: {pair_id}")


@dataclass(frozen=True)
class Segment:
    id: str
    text: str
    char_start: int
    char_end: int
    page: int | None = None
    search_text: str | None = None
    footnotes: tuple[str, ...] = ()


def _page_for(offset: int, page_offsets: list[dict[str, int]]) -> int:
    for item in page_offsets:
        if item["char_start"] <= offset < item["char_end"]:
            return item["page"]
    raise ValueError(f"offset {offset} is outside PDF page offsets")


def segment_new_direction(
    text: str, page_offsets: list[dict[str, int]], paragraphs: int = 158
) -> list[Segment]:
    """Return top-level paragraphs 1..N with source offsets and first PDF page."""
    # Skip the table of contents by starting at the first numbered paragraph after the
    # operative "hereby issues" sentence. A line is a paragraph start only if it carries the
    # next number in sequence, so numbered list items inside a paragraph are not mistaken.
    body_start = text.index("hereby issues")
    matches: list[re.Match[str]] = []
    for match in PARAGRAPH_RE.finditer(text, body_start):
        if int(match.group("number")) == len(matches) + 1:
            matches.append(match)
    if len(matches) != paragraphs:
        raise ValueError(f"expected top-level paragraphs 1..{paragraphs}, found {len(matches)}")
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


def segment_old_direction(
    text: str, segments: list[dict[str, Any]], units: int = 47
) -> list[Segment]:
    result = []
    for item in segments:
        start, end = int(item["char_start"]), int(item["char_end"])
        body = text[start:end]
        # A unit whose printed heading sits outside its own text (a control under a group
        # heading) is searched with that heading as its first line.
        heading = str(item.get("heading") or "")
        search = f"{heading}\n{body}" if heading else None
        notes = tuple(
            text[int(note["char_start"]) : int(note["char_end"])].strip()
            for note in item.get("footnotes") or []
        )
        result.append(
            Segment(str(item["id"]), body, start, end, search_text=search, footnotes=notes)
        )
    if len(result) != units:
        raise ValueError(f"expected {units} old clauses, found {len(result)}")
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


def _candidate_pool(old: Segment, new: list[Segment], pair: Pair) -> list[Segment]:
    for pattern, first, last in pair.pools:
        if re.fullmatch(pattern, old.id):
            return [item for item in new if first <= int(item.id) <= last]
    return new


def detect_differences(
    old: str, new: str, named_terms: tuple[str, ...] = PAIRS[0].named_terms
) -> list[str]:
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
    old_named = [term for term in named_terms if term in old_lower]
    new_named = [term for term in named_terms if term in new_lower]
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


def build_migration(base_dir: Path, pair: Pair = PAIRS[0]) -> dict[str, Any]:
    raw = base_dir / "data" / "raw"
    old_text = (raw / f"{pair.old_stem}.txt").read_text(encoding="utf-8")
    old_meta = json.loads((raw / f"{pair.old_stem}.meta.json").read_text(encoding="utf-8"))
    new_text = (raw / f"{pair.new_stem}.txt").read_text(encoding="utf-8")
    new_meta = json.loads((raw / f"{pair.new_stem}.meta.json").read_text(encoding="utf-8"))
    old_segments = segment_old_direction(old_text, old_meta["segments"], pair.old_units)
    new_segments = segment_new_direction(new_text, new_meta["page_offsets"], pair.new_paragraphs)
    mappings: list[dict[str, Any]] = []
    for old in old_segments:
        ranked = _rank(old, _candidate_pool(old, new_segments, pair))
        top_score = ranked[0][1]
        differences = detect_differences(
            old.text, ranked[0][0].search_text or ranked[0][0].text, pair.named_terms
        )
        floor = (
            UNSTRUCTURED_MIN_CANDIDATE_SCORE
            if re.fullmatch(pair.unstructured, old.id)
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
                **({"old_footnotes": list(old.footnotes)} if old.footnotes else {}),
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
        "id": pair.id,
        "old_instrument_id": pair.old_instrument_id,
        "new_instrument_id": pair.new_instrument_id,
        "disclaimer": DISCLAIMER,
        "method": METHOD_NAME,
        "method_version": METHOD_VERSION,
        "mappings": mappings,
    }


def write_migration(base_dir: Path, pair: Pair = PAIRS[0]) -> Path:
    output = base_dir / "data" / "migrations" / f"{pair.id}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_migration(base_dir, pair), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return output


def write_all_migrations(base_dir: Path) -> list[Path]:
    return [write_migration(base_dir, pair) for pair in PAIRS]


def content_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

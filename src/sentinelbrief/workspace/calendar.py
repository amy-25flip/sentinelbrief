"""iCalendar export for recurring duties (for example VA every six months, PT every 12)."""

import hashlib
import re
from datetime import UTC, date, datetime, timedelta

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile

_MONTHS_RE = re.compile(r"^P(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?$")


def _interval_months(duration: str) -> int:
    match = _MONTHS_RE.match(duration)
    months = 0
    if match:
        months = int(match["years"] or 0) * 12 + int(match["months"] or 0)
    if months <= 0:
        raise ValueError(f"Cannot build a calendar rule from recurring duration '{duration}'")
    return months


def _add_months(start: date, months: int) -> date:
    index = start.month - 1 + months
    year, month = start.year + index // 12, index % 12 + 1
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    last_day = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    return date(year, month, min(start.day, last_day))


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _fold(line: str) -> list[str]:
    """RFC 5545: lines longer than 75 octets are folded with CRLF + space."""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return [line]
    parts: list[str] = []
    while encoded:
        limit = 75 if not parts else 74
        chunk = encoded[:limit]
        while chunk and (chunk[-1] & 0xC0) == 0x80 and len(chunk) < len(encoded):
            chunk = chunk[:-1]  # do not split a multi-byte character
        parts.append(("" if not parts else " ") + chunk.decode("utf-8"))
        encoded = encoded[len(chunk) :]
    return parts


# A prose condition ending with this marker is one the engine cannot evaluate (for example
# "Entity is a Foreign Reinsurance Branch ... (not evaluated)"). A duty that hangs on one is
# not put in the calendar as if it applied.
NOT_EVALUATED = "(not evaluated)"


def recurring_duties_ics(
    engine: IncidentClockEngine,
    entity_classes: list[str],
    last_done: date,
    generated_at: datetime | None = None,
    audit_completed: date | None = None,
) -> tuple[str, list[str]]:
    """Return (ics_text, undetermined_obligation_ids).

    Each recurring duty that applies to `entity_classes` on `last_done` becomes a repeating
    all-day event whose first occurrence is `last_done` plus the interval: the latest date by
    which the duty next falls due if it was last performed on `last_done`. Duties whose
    applicability is undetermined (for example a generic NBFC class) are returned separately,
    never silently dropped.

    Two kinds of duty are never given a date they have not earned:

    - a duty that depends on a condition the engine cannot evaluate is left out;
    - a duty whose fixed date is only the latest possible one, because the clause takes the
      earlier of that date and a number of days after an event (`earlier_of_days_after_event`),
      is dated only when the event date (`audit_completed`) is given, and then once, not yearly.

    Whatever is left out is listed in a single dated notice event inside the calendar, so the
    omission is visible wherever the file is opened.
    """
    stamp = (generated_at or datetime.now(UTC)).astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")
    result = engine.evaluate(IncidentProfile(entity_classes=entity_classes), as_of=last_done)
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//SentinelBrief//Recurring duties//EN",
        "CALSCALE:GREGORIAN",
    ]
    undetermined: list[str] = []
    omitted: list[tuple[str, str]] = []
    for obligation in engine.obligations:
        normalized = obligation.get("normalized") or {}
        deadline = normalized.get("deadline") or {}
        if deadline.get("kind") != "recurring":
            continue
        obligation_id = obligation["id"]
        if obligation_id in result.undetermined:
            undetermined.append(obligation_id)
            continue
        if obligation_id not in result.applicable_obligations:
            continue
        citation = (
            f"{obligation.get('instrument_id', '')} {obligation.get('paragraph_ref', '')}".strip()
        )
        unevaluated = [
            condition
            for condition in (obligation.get("applicability") or {}).get("conditions") or []
            if NOT_EVALUATED in condition
        ]
        if unevaluated:
            omitted.append(
                (obligation_id, "applies only if: " + "; ".join(unevaluated) + f" ({citation})")
            )
            continue
        schedule = deadline.get("fixed_schedule")
        days_after_event = deadline.get("earlier_of_days_after_event")
        if schedule and days_after_event is not None:
            if audit_completed is None:
                omitted.append(
                    (
                        obligation_id,
                        f"due on the earlier of a fixed date ({', '.join(schedule)}) and "
                        f"{days_after_event} days after the audit is completed; give the audit "
                        f"completion date to get a date ({citation})",
                    )
                )
                continue
            month, day = (int(part) for part in schedule[0].split("-"))
            fixed = date(audit_completed.year, month, day)
            if fixed < audit_completed:
                fixed = date(audit_completed.year + 1, month, day)
            due = min(fixed, audit_completed + timedelta(days=int(days_after_event)))
            occurrences = [
                (
                    due,
                    "",
                    "event",
                    f"The earlier of {fixed.isoformat()} and {days_after_event} days after the "
                    f"audit completion date you gave ({audit_completed.isoformat()}). This year "
                    "only; it does not repeat because next year's audit date is not known.",
                )
            ]
        elif schedule:
            # Due dates fixed by the clause (for example the 15th after each quarter end): one
            # yearly event per date, starting at its next occurrence after `last_done`.
            occurrences = []
            for month_day in schedule:
                month, day = (int(part) for part in month_day.split("-"))
                due = date(last_done.year, month, day)
                if due <= last_done:
                    due = date(last_done.year + 1, month, day)
                occurrences.append(
                    (due, "FREQ=YEARLY;INTERVAL=1", month_day, "Due on a date fixed by the clause.")
                )
        else:
            months = _interval_months(deadline.get("duration_iso8601") or "")
            rule = (
                f"FREQ=YEARLY;INTERVAL={months // 12}"
                if months % 12 == 0
                else f"FREQ=MONTHLY;INTERVAL={months}"
            )
            basis = f"Counted from the date you gave as last performed ({last_done.isoformat()})."
            occurrences = [(_add_months(last_done, months), rule, "", basis)]
        advisory = normalized.get("modality") == "recommended"
        summary = ("Recommended, not mandatory: " if advisory else "") + normalized.get(
            "action", obligation_id
        )
        for first, rule, seed, basis in sorted(occurrences):
            uid = hashlib.sha256(
                f"{obligation_id}|{last_done.isoformat()}|{seed}".encode()
            ).hexdigest()[:32]
            description = (
                f"{normalized.get('action', '')}\n\nSource: {citation}\n{basis} "
                "Not legal advice; read the cited clause."
            )
            event = [
                "BEGIN:VEVENT",
                f"UID:{uid}@sentinelbrief",
                f"X-SENTINELBRIEF-OBLIGATION:{obligation_id}",
                f"DTSTAMP:{stamp}",
                f"DTSTART;VALUE=DATE:{first.strftime('%Y%m%d')}",
                *([f"RRULE:{rule}"] if rule else []),
                f"SUMMARY:{_escape(summary)}",
                f"DESCRIPTION:{_escape(description)}",
                "END:VEVENT",
            ]
            for line in event:
                lines.extend(_fold(line))
    if omitted:
        listing = "\n".join(f"- {obligation_id}: {why}" for obligation_id, why in omitted)
        uid = hashlib.sha256(
            ("omitted|" + last_done.isoformat() + "|" + "|".join(o for o, _ in omitted)).encode()
        ).hexdigest()[:32]
        notice = [
            "BEGIN:VEVENT",
            f"UID:{uid}@sentinelbrief",
            f"X-SENTINELBRIEF-OMITTED:{','.join(o for o, _ in omitted)}",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{(last_done + timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:{_escape(f'SentinelBrief: {len(omitted)} duties are NOT in this calendar')}",
            "DESCRIPTION:"
            + _escape(
                "These duties may apply to you but were not given a date, because a date would "
                "be a guess:\n" + listing + "\nNot legal advice; read the cited clauses."
            ),
            "END:VEVENT",
        ]
        for line in notice:
            lines.extend(_fold(line))
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n", undetermined

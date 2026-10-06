"""Tabletop exercise generator.

A tabletop is a rehearsal: a facilitator reads out a scripted incident in stages and the team
says what it would do. This module builds one for a given kind of entity.

Division of labour, kept strict:

- The storyline (what "happens" at each stage) is fiction, written here and labelled as such.
- Every statement about the law in the answer key (which duties apply, each deadline, its
  starting event, its clause, and every open question) is produced by running the incident
  clock engine on the facts the story has revealed so far. Nothing legal is written by hand.

So the answer key for stage three is exactly what the tool would tell a real team that knew
only what the story has told them by stage three, including "you do not know this yet".
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from sentinelbrief.clock.engine import IST, IncidentProfile

if TYPE_CHECKING:
    from sentinelbrief.clock.engine import ClockResult, IncidentClockEngine

DISCLAIMER = (
    "Training material. The storyline is invented. The answer key is computed by the "
    "SentinelBrief clock engine from the facts revealed at each stage; it is not legal advice, "
    "and the underlying readings of the law have not been reviewed by a compliance "
    "professional."
)
FACILITATOR_QUESTION = (
    "Which reporting clocks are running now, from which starting event, and to whom? "
    "What do you still need to find out, and who will find it out?"
)


@dataclass(frozen=True)
class Stage:
    minutes: int
    inject: str
    # Facts the story reveals at this stage. A value of the form "+N" is a time N minutes
    # after the exercise start; other values are used as they are.
    reveals: dict[str, Any]


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str
    summary: str
    stages: tuple[Stage, ...]


_RANSOMWARE = "Malicious code attacks such as Ransomware"
_DEFACEMENT = "Defacement of website or intrusion into a website and unauthorised changes"
# One attestation per regime. The engine reads only those that concern the entity's regulators.
_CONFIRMED = {
    "is_cyber_incident": True,
    "is_irdai_cyber_incident": True,
    "is_sebi_cybersecurity_incident": True,
}

SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        id="ransomware-with-personal-data",
        title="Ransomware with customer data copied out",
        summary=(
            "Monitoring detects encryption before anyone looks; a person confirms it later; "
            "forensics then finds that customer records left the network."
        ),
        stages=(
            Stage(
                0,
                "The monitoring system raises an automated alert: files on two servers are being "
                "renamed at high speed. Nobody has looked at it yet.",
                {"when_detected": "+0"},
            ),
            Stage(
                25,
                "The on-call engineer opens the alert, logs in and finds ransom notes on both "
                "servers. The engineer calls the security lead.",
                {"when_noticed": "+25", "incident_types": [_RANSOMWARE]},
            ),
            Stage(
                120,
                "The security lead and the head of risk agree that this is a cyber incident "
                "under each of the organisation's regulators' definitions.",
                dict(_CONFIRMED),
            ),
            Stage(
                240,
                "Forensics reports that a database export with customer names, addresses and "
                "account numbers was copied to an outside address before encryption began.",
                {"personal_data_involved": True, "when_aware": "+240"},
            ),
        ),
    ),
    Scenario(
        id="website-defacement-no-personal-data",
        title="Public website defaced, no personal data",
        summary=(
            "A customer reports a defaced public website. The site holds no personal data. "
            "Tests whether the team reports what must be reported without over-reporting."
        ),
        stages=(
            Stage(
                0,
                "A customer phones the call centre: the public website shows a political slogan "
                "instead of the home page.",
                {"when_brought_to_notice": "+0"},
            ),
            Stage(
                15,
                "The web team confirms the home page was replaced and takes the site offline.",
                {"when_noticed": "+15", "when_detected": "+15", "incident_types": [_DEFACEMENT]},
            ),
            Stage(
                90,
                "The web team confirms the server hosts only static pages. It holds no customer "
                "or employee data and connects to no internal system.",
                {"personal_data_involved": False},
            ),
            Stage(
                180,
                "The head of risk records that the event is a cyber incident under each of the "
                "organisation's regulators' definitions.",
                dict(_CONFIRMED),
            ),
        ),
    ),
    Scenario(
        id="unclear-outage",
        title="Outage of unknown cause",
        summary=(
            "A core system stops responding and nobody yet knows why. Tests whether the team "
            "asks the questions that decide reportability instead of assuming an answer."
        ),
        stages=(
            Stage(
                0,
                "The core transaction system stops responding. Monitoring shows the database "
                "host is unreachable. The cause is unknown.",
                {"when_detected": "+0", "when_noticed": "+0"},
            ),
            Stage(
                60,
                "The infrastructure team finds a failed storage controller. There is no sign "
                "of intrusion so far, but log review is not finished.",
                {},
            ),
            Stage(
                300,
                "Log review finishes: no unauthorised access. The head of risk records that "
                "this was a hardware failure and not a cyber incident, and that it is not one "
                "of the incident types CERT-In lists.",
                {
                    "is_cyber_incident": False,
                    "is_irdai_cyber_incident": False,
                    "is_sebi_cybersecurity_incident": False,
                    "is_annexure_i_type": False,
                },
            ),
        ),
    ),
)


def scenario_by_id(scenario_id: str) -> Scenario:
    for scenario in SCENARIOS:
        if scenario.id == scenario_id:
            return scenario
    raise KeyError(f"Unknown tabletop scenario: {scenario_id}")


def _key(result: ClockResult, engine: IncidentClockEngine) -> dict[str, Any]:
    deadlines = []
    for deadline in sorted(result.deadlines, key=lambda d: (d.deadline_utc, d.obligation_id)):
        deadlines.append(
            {
                "obligation_id": deadline.obligation_id,
                "regulator": deadline.regulator,
                "action": deadline.obligation_action,
                "recipient": deadline.recipient,
                "starts_from": deadline.anchor_type,
                "started_at_ist": deadline.anchor_timestamp.astimezone(IST).isoformat(),
                "due_ist": deadline.deadline_ist.isoformat(),
                "within": deadline.duration_iso8601,
                "clause": f"{deadline.citation_instrument} {deadline.citation_paragraph}".strip(),
                "simulated": deadline.simulated,
            }
        )
    questions: dict[str, dict[str, Any]] = {}
    for unknown in result.unknowns:
        entry = questions.setdefault(
            unknown.question,
            {"question": unknown.question, "why_it_matters": unknown.impact, "affects": []},
        )
        entry["affects"] = sorted({*entry["affects"], *unknown.affects})
    not_in_force = sorted(
        item["obligation_id"]
        for item in result.not_applicable
        if str(item.get("reason", "")).startswith("not_yet_valid")
    )
    return {
        "deadlines": deadlines,
        "open_questions": list(questions.values()),
        "not_in_force_at_this_date": not_in_force,
        "cannot_be_determined_yet": sorted(result.undetermined),
        "caveats": list(result.caveats),
    }


def build_tabletop(
    engine: IncidentClockEngine,
    entity_classes: list[str],
    scenario_id: str,
    start: datetime,
    simulate_instruments: list[str] | None = None,
) -> dict[str, Any]:
    """Build the exercise. `start` must be timezone-aware; stage times are offsets from it."""
    if start.tzinfo is None or start.utcoffset() is None:
        raise ValueError("The exercise start time must carry a UTC offset")
    if not entity_classes:
        raise ValueError("At least one entity class is required")
    scenario = scenario_by_id(scenario_id)
    facts: dict[str, Any] = {}
    stages = []
    previous: set[str] = set()
    for number, stage in enumerate(scenario.stages, start=1):
        at = start + timedelta(minutes=stage.minutes)
        for name, value in stage.reveals.items():
            if isinstance(value, str) and value.startswith("+"):
                facts[name] = start + timedelta(minutes=int(value[1:]))
            else:
                facts[name] = value
        result = engine.evaluate(
            IncidentProfile(entity_classes=list(entity_classes), **facts),
            now=at,
            simulate_instruments=simulate_instruments or None,
        )
        key = _key(result, engine)
        running = {item["obligation_id"] for item in key["deadlines"]}
        stages.append(
            {
                "stage": number,
                "at_ist": at.astimezone(IST).isoformat(),
                "minutes_from_start": stage.minutes,
                "inject": stage.inject,
                "question_for_the_team": FACILITATOR_QUESTION,
                "answer_key": key,
                "clocks_started_at_this_stage": sorted(running - previous),
                "clocks_no_longer_shown": sorted(previous - running),
            }
        )
        previous = running
    return {
        "disclaimer": DISCLAIMER,
        "scenario": {"id": scenario.id, "title": scenario.title, "summary": scenario.summary},
        "entity_classes": list(entity_classes),
        "start_ist": start.astimezone(IST).isoformat(),
        "simulated_instruments": list(simulate_instruments or []),
        "stages": stages,
    }


def render_markdown(exercise: dict[str, Any]) -> str:
    """A facilitator's hand-out: storyline first, answer key after each stage."""
    lines = [
        f"# Tabletop exercise: {exercise['scenario']['title']}",
        "",
        f"> {exercise['disclaimer']}",
        "",
        f"- Entity classes: {', '.join(exercise['entity_classes'])}",
        f"- Exercise start: {exercise['start_ist']}",
        f"- Summary: {exercise['scenario']['summary']}",
        "",
    ]
    for stage in exercise["stages"]:
        key = stage["answer_key"]
        lines += [
            f"## Stage {stage['stage']} (start + {stage['minutes_from_start']} min, {stage['at_ist']})",
            "",
            f"**Read out (fiction):** {stage['inject']}",
            "",
            f"**Ask the team:** {stage['question_for_the_team']}",
            "",
            "**Answer key (computed):**",
            "",
        ]
        if key["deadlines"]:
            lines += ["| Due (IST) | To | Starts from | Clause |", "|---|---|---|---|"]
            for item in key["deadlines"]:
                note = " (simulated, not in force)" if item["simulated"] else ""
                lines.append(
                    f"| {item['due_ist']}{note} | {item['recipient']} | {item['starts_from']} at "
                    f"{item['started_at_ist']} | {item['clause']} |"
                )
        else:
            lines.append("No reporting clock can be computed from what is known at this stage.")
        lines.append("")
        if key["open_questions"]:
            lines.append("The team should be asking:")
            lines += [f"- {q['question']} ({q['why_it_matters']})" for q in key["open_questions"]]
            lines.append("")
        if key["not_in_force_at_this_date"]:
            lines.append(
                "Not in force at this date (no duty yet): "
                + ", ".join(key["not_in_force_at_this_date"])
            )
            lines.append("")
        if key["caveats"]:
            lines.append("Caveats:")
            lines += [f"- {caveat}" for caveat in key["caveats"]]
            lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"

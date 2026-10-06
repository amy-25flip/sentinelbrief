"""Reviewer probe: run the incident clock on ad hoc profiles and print a compact result.

Usage: uv run --no-sync python scripts/probe.py CLASS[,CLASS...] [key=value ...]

Keys: types=a|b  detected=HH:MM  noticed=HH:MM  brought=HH:MM  aware=HH:MM  reported=HH:MM
      date=YYYY-MM-DD  annexure=true|false  cyber=true|false  personal=true|false
      irdai_cyber=true|false  sebi_cyber=true|false  forensic=true|false
      protected=true|false  only=<substring of obligation id to show>
      simulate=<instrument id>
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile

IST = timezone(timedelta(hours=5, minutes=30))
ROOT = Path(__file__).resolve().parents[1]
TIME_KEYS = {
    "detected": "when_detected",
    "noticed": "when_noticed",
    "brought": "when_brought_to_notice",
    "aware": "when_aware",
    "occurred": "when_occurred",
    "reported": "when_reported_to_sebi",
}
BOOL_KEYS = {
    "annexure": "is_annexure_i_type",
    "cyber": "is_cyber_incident",
    "irdai_cyber": "is_irdai_cyber_incident",
    "sebi_cyber": "is_sebi_cybersecurity_incident",
    "forensic": "sebi_forensic_directed_or_rca_inconclusive",
    "personal": "personal_data_involved",
    "protected": "uses_protected_systems",
}


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    classes = argv[0].split(",")
    opts = dict(a.split("=", 1) for a in argv[1:])
    day = datetime.fromisoformat(opts.pop("date", "2026-10-01"))
    only = opts.pop("only", "")
    simulate = opts.pop("simulate", "")
    kwargs: dict[str, object] = {
        "entity_classes": classes,
        "incident_types": opts.pop("types", "Malicious code attacks such as Ransomware").split("|"),
    }
    for key, value in opts.items():
        if key in TIME_KEYS:
            hh, mm = value.split(":")
            kwargs[TIME_KEYS[key]] = day.replace(hour=int(hh), minute=int(mm), tzinfo=IST)
        elif key.startswith("ext:"):
            hh, mm = value.split(":")
            events = kwargs.setdefault("external_events", {})
            events[key[4:]] = day.replace(hour=int(hh), minute=int(mm), tzinfo=IST)  # type: ignore[index]
        elif key == "severity":
            kwargs["sebi_severity"] = value
        elif key in BOOL_KEYS:
            kwargs[BOOL_KEYS[key]] = value == "true"
        else:
            raise SystemExit(f"unknown key {key}")
    try:
        result = IncidentClockEngine(ROOT / "data").evaluate(
            IncidentProfile(**kwargs),  # type: ignore[arg-type]
            simulate_instruments=[simulate] if simulate else None,
        )
    except (ValueError, TypeError) as exc:
        print(f"EXC {type(exc).__name__}: {exc}")
        return 1

    def keep(oid: str) -> bool:
        return only in oid

    print("law_as_of", result.law_as_of)
    for d in result.deadlines:
        if keep(d.obligation_id):
            tag = "SIMULATED" if d.simulated else "DEADLINE"
            print(f"  {tag:<9} {d.obligation_id} [{d.anchor_type}] {d.deadline_ist:%Y-%m-%d %H:%M}")
    for oid in result.applicable_obligations:
        if keep(oid):
            print(f"  APPLIES  {oid}")
    for t in result.time_critical:
        if keep(t.obligation_id):
            print(f"  {'SIMULATED' if t.simulated else 'URGENT':<9} {t.obligation_id}")
    for n in result.not_applicable:
        if keep(n["obligation_id"]):
            print(f"  NOT      {n['obligation_id']} ({n['reason'][:60]})")
    for oid in result.undetermined:
        if keep(oid):
            print(f"  UNDET    {oid}")
    for u in result.unknowns:
        print(f"  ASK      {u.question[:110]} -> {u.affects}")
    for c in result.caveats:
        print(f"  CAVEAT   {c[:160]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

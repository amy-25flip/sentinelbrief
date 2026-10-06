"""Disputed start dates are shown on the earlier reading, with a warning (Review 12, Q5 and Q6)."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
RANSOMWARE = "Malicious code attacks such as Ransomware"
SEBI_6H = "sebi.cscrf.2024.incident-reporting-6h"
IRDAI_6H = "irdai.ics-guidelines.2023.incident-reporting-6h"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _run(engine, classes, when):
    return engine.evaluate(
        IncidentProfile(
            entity_classes=classes,
            incident_types=[RANSOMWARE],
            when_noticed=when,
            uses_protected_systems=False,
        )
    )


def _contested(result):
    return [c for c in result.caveats if c.startswith("Contested:")]


def test_sebi_duty_in_the_disputed_window_is_shown_with_a_warning(engine):
    """Catches: a disputed deadline presented as settled, or silently dropped."""
    inside = _run(engine, ["sebi.stock_broker"], datetime(2024, 12, 31, 23, 59, tzinfo=IST))
    assert SEBI_6H in {d.obligation_id for d in inside.deadlines}
    (warning,) = _contested(inside)
    assert "1 January 2025" in warning and "1 April 2025" in warning and SEBI_6H in warning
    last_day = _run(engine, ["sebi.small_re"], datetime(2025, 3, 31, 23, 59, tzinfo=IST))
    assert _contested(last_day)


def test_no_warning_once_the_last_compliance_date_has_passed(engine):
    """Catches: the warning shown for incidents after every reading agrees the duty binds."""
    after = _run(engine, ["sebi.stock_broker"], datetime(2025, 4, 1, 0, 1, tzinfo=IST))
    assert SEBI_6H in {d.obligation_id for d in after.deadlines} and not _contested(after)


def test_irdai_duty_in_the_disputed_window_is_shown_with_a_warning(engine):
    """Catches: the IRDAI transition allowance being ignored."""
    inside = _run(engine, ["irdai.insurer"], datetime(2023, 6, 1, 10, 0, tzinfo=IST))
    assert IRDAI_6H in {d.obligation_id for d in inside.deadlines}
    assert any("next financial year" in c for c in _contested(inside))
    after = _run(engine, ["irdai.insurer"], datetime(2024, 4, 1, 10, 0, tzinfo=IST))
    assert not _contested(after)


def test_entities_outside_the_regime_get_no_contested_warning(engine):
    """Catches: the warning leaking to entities the duty does not reach."""
    assert not _contested(
        _run(engine, ["nbfc.middle_layer"], datetime(2024, 12, 1, 10, 0, tzinfo=IST))
    )

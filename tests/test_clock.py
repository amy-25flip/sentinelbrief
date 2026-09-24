from datetime import UTC, datetime, timedelta

from hypothesis import given
from hypothesis import strategies as st

from sentinelbrief.clock import IncidentClockEngine, IncidentProfile
from sentinelbrief.clock.engine import IST, parse_iso8601_duration

# Use the real data directory
DATA_DIR = "e:/SentinelBrief/data"


def test_basic_cert_in_6h_deadline():
    engine = IncidentClockEngine(DATA_DIR)

    noticed = datetime(2023, 10, 1, 12, 0, tzinfo=IST)
    profile = IncidentProfile(
        entity_class="body_corporate", is_annexure_i_type=True, when_noticed=noticed
    )

    result = engine.evaluate(profile)

    # Check that cert-in 6h applies
    deadlines = [d for d in result.deadlines if "incident-reporting-6h" in d.obligation_id]
    assert len(deadlines) == 1

    dl = deadlines[0]
    assert dl.anchor_timestamp == noticed
    assert dl.deadline_utc == noticed.astimezone(UTC) + timedelta(hours=6)
    assert dl.deadline_ist == dl.deadline_utc.astimezone(IST)
    assert dl.duration_iso8601 == "PT6H"


def test_ist_utc_conversion():
    assert IST.utcoffset(None) == timedelta(hours=5, minutes=30)


def test_anchor_disambiguation():
    engine = IncidentClockEngine(DATA_DIR)

    noticed = datetime(2023, 10, 1, 14, 0, tzinfo=IST)
    brought_to_notice = datetime(2023, 10, 1, 12, 0, tzinfo=IST)

    profile = IncidentProfile(
        entity_class="body_corporate",
        is_annexure_i_type=True,
        when_noticed=noticed,
        when_brought_to_notice=brought_to_notice,
    )

    result = engine.evaluate(profile)
    dl = next(d for d in result.deadlines if "incident-reporting-6h" in d.obligation_id)

    # Should use the earlier one (brought_to_notice)
    assert dl.anchor_type == "brought_to_notice"
    assert dl.anchor_timestamp == brought_to_notice

    # Reverse it
    profile.when_noticed = datetime(2023, 10, 1, 10, 0, tzinfo=IST)
    result2 = engine.evaluate(profile)
    dl2 = next(d for d in result2.deadlines if "incident-reporting-6h" in d.obligation_id)
    assert dl2.anchor_type == "noticing"
    assert dl2.anchor_timestamp == profile.when_noticed


def test_unknowns_generation():
    engine = IncidentClockEngine(DATA_DIR)

    profile = IncidentProfile(
        entity_class="body_corporate",
        is_annexure_i_type=True,
        # missing when_noticed
    )

    result = engine.evaluate(profile)
    unknowns = [u.question for u in result.unknowns]
    assert any("noticed" in q.lower() for q in unknowns)

    profile2 = IncidentProfile(
        entity_class="body_corporate",
        when_noticed=datetime.now(IST),
        # missing is_annexure_i_type
    )
    result2 = engine.evaluate(profile2)
    unknowns2 = [u.question for u in result2.unknowns]
    assert any("annexure" in q.lower() for q in unknowns2)


def test_entity_filtering():
    engine = IncidentClockEngine(DATA_DIR)

    profile_vpn = IncidentProfile(entity_class="vpn_provider", when_occurred=datetime.now(IST))
    result_vpn = engine.evaluate(profile_vpn)
    assert any("vpn" in d.obligation_id for d in result_vpn.deadlines)

    profile_bc = IncidentProfile(entity_class="body_corporate", when_occurred=datetime.now(IST))
    result_bc = engine.evaluate(profile_bc)
    assert not any("vpn" in d.obligation_id for d in result_bc.deadlines)


def test_no_deadline_obligations():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(entity_class="body_corporate")
    result = engine.evaluate(profile)

    # NTP sync should be applicable but not produce a deadline
    assert any("ntp-sync" in ob_id for ob_id in result.applicable_obligations)
    assert not any("ntp-sync" in d.obligation_id for d in result.deadlines)


@given(
    st.datetimes(
        timezones=st.just(UTC),
        min_value=datetime(2020, 1, 1, tzinfo=UTC),
        max_value=datetime(2030, 1, 1, tzinfo=UTC),
    ),
    st.integers(min_value=0, max_value=1000),
)
def test_deadline_arithmetic(anchor_ts, hours_duration):
    duration = timedelta(hours=hours_duration)
    deadline_utc = anchor_ts + duration
    deadline_ist = deadline_utc.astimezone(IST)

    # Just checking basic timezone arithmetic
    assert deadline_ist.utcoffset() == timedelta(hours=5, minutes=30)
    assert (deadline_ist - deadline_utc).total_seconds() == 0


def test_not_yet_in_force():
    engine = IncidentClockEngine(DATA_DIR)
    # Inject a mock obligation
    engine.obligations.append(
        {
            "id": "mock.dpdp.future",
            "status": "not_yet_in_force",
            "applicability": {"entity_classes": ["body_corporate"]},
            "normalized": {"deadline": {"kind": "none"}},
        }
    )

    profile = IncidentProfile(entity_class="body_corporate")
    result = engine.evaluate(profile)

    assert any(na["obligation_id"] == "mock.dpdp.future" for na in result.not_applicable)
    assert any(
        na["reason"] == "not_yet_in_force"
        for na in result.not_applicable
        if na["obligation_id"] == "mock.dpdp.future"
    )


def test_parse_iso8601():
    assert parse_iso8601_duration("PT6H") == timedelta(hours=6)
    assert parse_iso8601_duration("P180D") == timedelta(days=180)
    assert parse_iso8601_duration("P5Y") == timedelta(days=5 * 365)

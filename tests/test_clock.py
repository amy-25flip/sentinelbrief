import re
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from sentinelbrief.clock import IncidentClockEngine, IncidentProfile
from sentinelbrief.clock.engine import IST, parse_iso8601_duration

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
NOTICED = datetime(2026, 9, 24, 9, 0, tzinfo=IST)
NOW = datetime(2026, 9, 24, 12, 0, tzinfo=UTC)


def _dl(result, suffix):
    return [d for d in result.deadlines if d.obligation_id.endswith(suffix)]


def test_basic_cert_in_6h_deadline():
    engine = IncidentClockEngine(DATA_DIR)
    noticed = datetime(2023, 10, 1, 12, 0, tzinfo=IST)
    profile = IncidentProfile(
        entity_class="body_corporate", is_annexure_i_type=True, when_noticed=noticed
    )
    result = engine.evaluate(profile)

    deadlines = _dl(result, "incident-reporting-6h")
    assert len(deadlines) == 1
    dl = deadlines[0]
    assert dl.anchor_timestamp == noticed
    assert dl.deadline_utc == noticed.astimezone(UTC) + timedelta(hours=6)
    assert dl.deadline_ist == dl.deadline_utc.astimezone(IST)
    assert dl.duration_iso8601 == "PT6H"
    assert dl.regulator == "CERT-In"


def test_anchor_takes_earliest_of_joined_triggers():
    engine = IncidentClockEngine(DATA_DIR)
    noticed = datetime(2026, 9, 24, 14, 0, tzinfo=IST)
    brought = datetime(2026, 9, 24, 12, 0, tzinfo=IST)
    profile = IncidentProfile(
        entity_class="body_corporate",
        is_annexure_i_type=True,
        when_noticed=noticed,
        when_brought_to_notice=brought,
    )
    dl = _dl(engine.evaluate(profile), "incident-reporting-6h")[0]
    assert (dl.anchor_type, dl.anchor_timestamp) == ("brought_to_notice", brought)

    profile.when_noticed = datetime(2026, 9, 24, 10, 0, tzinfo=IST)
    dl2 = _dl(engine.evaluate(profile), "incident-reporting-6h")[0]
    assert (dl2.anchor_type, dl2.anchor_timestamp) == ("noticing", profile.when_noticed)


def test_unknown_noticing_time_is_asked_not_guessed():
    engine = IncidentClockEngine(DATA_DIR)
    result = engine.evaluate(
        IncidentProfile(entity_class="body_corporate", is_annexure_i_type=True)
    )
    assert any("noticed" in u.question.lower() for u in result.unknowns)
    assert not result.deadlines


def test_detection_only_does_not_start_certin_clock():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="body_corporate", is_annexure_i_type=True, when_detected=NOTICED
    )
    result = engine.evaluate(profile, now=NOW)
    assert not result.deadlines
    assert any("noticed" in u.question.lower() for u in result.unknowns)


def test_entity_filtering():
    engine = IncidentClockEngine(DATA_DIR)
    vpn = engine.evaluate(IncidentProfile(entity_class="vpn_provider", is_annexure_i_type=True))
    assert any("vps-cloud-vpn" in o for o in vpn.applicable_obligations)
    bc = engine.evaluate(IncidentProfile(entity_class="body_corporate", is_annexure_i_type=True))
    assert not any("vps-cloud-vpn" in o for o in bc.applicable_obligations)


def test_retention_duties_never_produce_a_deadline():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="vps_provider",
        incident_types=["ransomware"],
        when_noticed=NOTICED,
        when_occurred=datetime(2026, 9, 20, 9, 0, tzinfo=IST),
    )
    result = engine.evaluate(profile, now=NOW)
    assert any("vps-cloud-vpn" in o for o in result.applicable_obligations)
    assert [d.obligation_id.split(".")[-1] for d in result.deadlines] == ["incident-reporting-6h"]


def test_no_deadline_obligations():
    engine = IncidentClockEngine(DATA_DIR)
    result = engine.evaluate(IncidentProfile(entity_class="body_corporate"))
    assert any("ntp-sync" in o for o in result.applicable_obligations)
    assert not _dl(result, "ntp-sync")


@pytest.mark.parametrize(
    "incident_type",
    [
        "Attacks on Application such as E-Governance, E-Commerce",
        "Attack on servers such as Database, Mail and DNS and network devices such as Routers",
        "ransomware",
        "DDoS",
        "data breach",
        "Data Leak",
        "phishing",
    ],
)
def test_real_annexure_i_types_start_the_clock(incident_type):
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="nbfc", incident_types=[incident_type], when_noticed=NOTICED
    )
    result = engine.evaluate(profile, now=NOW)
    assert result.annexure_i.decision is True
    assert len(_dl(result, "incident-reporting-6h")) == 1


@pytest.mark.parametrize(
    "incident_type", ["hardware failure", "cloud region power outage", "kudos", "endosperm"]
)
def test_free_text_can_never_conclude_not_reportable(incident_type):
    """A false 'not reportable' is the worst failure: it must always be an Unknown."""
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="nbfc", incident_types=[incident_type], when_noticed=NOTICED
    )
    result = engine.evaluate(profile, now=NOW)
    assert result.annexure_i.decision is None
    assert any("Annexure I" in u.question for u in result.unknowns)
    assert not any(
        n["obligation_id"] == "cert-in.directions-70b.2022.incident-reporting-6h"
        for n in result.not_applicable
    )


def test_weak_term_only_suggests():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="nbfc", incident_types=["cloud region power outage"], when_noticed=NOTICED
    )
    result = engine.evaluate(profile, now=NOW)
    assert result.annexure_i.suggestions == ["annexure_i.xviii"]
    assert "Possible matches" in result.unknowns[0].impact


def test_explicit_attestation_makes_annexure_not_applicable():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="nbfc",
        incident_types=["hardware failure"],
        is_annexure_i_type=False,
        when_noticed=NOTICED,
    )
    result = engine.evaluate(profile, now=NOW)
    assert not result.deadlines
    assert any(
        n["obligation_id"] == "cert-in.directions-70b.2022.incident-reporting-6h"
        for n in result.not_applicable
    )


def test_conflicting_attestation_is_rejected():
    with pytest.raises(ValueError, match="Conflicting"):
        IncidentProfile(
            entity_class="nbfc", is_annexure_i_type=False, annexure_i_items=["annexure_i.v"]
        )


def test_invalid_annexure_item_is_rejected_even_with_attestation():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="nbfc",
        is_annexure_i_type=True,
        annexure_i_items=["annexure_i.not-real"],
    )
    with pytest.raises(ValueError, match="Unknown Annexure I item"):
        engine.evaluate(profile, now=NOW)


def test_naive_datetime_is_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        IncidentProfile(entity_class="nbfc", when_noticed=datetime(2026, 9, 24, 9, 0))


def test_naive_datetime_set_after_construction_is_rejected():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(entity_class="nbfc", is_annexure_i_type=True)
    profile.when_noticed = datetime(2026, 9, 24, 9, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        engine.evaluate(profile, now=NOW)


def test_unknown_entity_class_is_rejected_not_silently_empty():
    engine = IncidentClockEngine(DATA_DIR)
    with pytest.raises(ValueError, match="Unknown entity class"):
        engine.evaluate(IncidentProfile(entity_class="NBFC"))


def test_law_is_evaluated_as_of_the_incident_date():
    engine = IncidentClockEngine(DATA_DIR)
    old = datetime(2021, 1, 5, 9, 0, tzinfo=IST)
    profile = IncidentProfile(entity_class="nbfc", is_annexure_i_type=True, when_noticed=old)
    result = engine.evaluate(profile, now=datetime(2021, 1, 5, 10, 0, tzinfo=IST))
    assert result.law_as_of == date(2021, 1, 5)
    assert not result.deadlines
    assert all("not_yet_valid_at_incident_date" in n["reason"] for n in result.not_applicable)


def test_msme_caveat_shown_for_the_transition_window_only():
    engine = IncidentClockEngine(DATA_DIR)
    window = datetime(2022, 7, 1, 9, 0, tzinfo=IST)
    r_old = engine.evaluate(
        IncidentProfile(entity_class="nbfc", is_annexure_i_type=True, when_noticed=window),
        now=window,
    )
    assert r_old.caveats
    r_new = engine.evaluate(
        IncidentProfile(entity_class="nbfc", is_annexure_i_type=True, when_noticed=NOTICED),
        now=NOW,
    )
    assert not r_new.caveats


def test_unevaluated_conditions_are_surfaced():
    engine = IncidentClockEngine(DATA_DIR)
    result = engine.evaluate(IncidentProfile(entity_class="body_corporate"))
    assert any(o.endswith("comply-with-orders") for o in result.conditions_unevaluated)


def test_overdue_status():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(entity_class="nbfc", is_annexure_i_type=True, when_noticed=NOTICED)
    late = engine.evaluate(profile, now=NOTICED + timedelta(hours=7))
    assert _dl(late, "incident-reporting-6h")[0].status == "overdue"
    early = engine.evaluate(profile, now=NOTICED + timedelta(hours=5, minutes=59))
    assert _dl(early, "incident-reporting-6h")[0].status == "pending"


def test_missing_data_dir_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError):
        IncidentClockEngine(tmp_path / "nope")


def test_not_yet_in_force_status():
    engine = IncidentClockEngine(DATA_DIR)
    engine.obligations.append(
        {
            "id": "mock.dpdp.future",
            "status": "not_yet_in_force",
            "applicability": {"entity_classes": ["body_corporate"]},
            "normalized": {"deadline": {"kind": "none"}},
        }
    )
    result = engine.evaluate(IncidentProfile(entity_class="body_corporate"))
    assert {"obligation_id": "mock.dpdp.future", "reason": "not_yet_in_force"} in (
        result.not_applicable
    )


def test_unsupported_anchor_is_reported_not_silently_skipped():
    engine = IncidentClockEngine(DATA_DIR)
    engine.obligations.append(
        {
            "id": "mock.publication-anchor",
            "status": "in_force",
            "applicability": {"entity_classes": ["body_corporate"]},
            "normalized": {
                "action": "x",
                "deadline": {
                    "kind": "relative",
                    "duration_iso8601": "P30D",
                    "anchor": "publication",
                },
            },
        }
    )
    result = engine.evaluate(IncidentProfile(entity_class="body_corporate"))
    assert any("publication" in u.question for u in result.unknowns)


def test_immediate_deadline_is_time_critical_not_a_clock():
    engine = IncidentClockEngine(DATA_DIR)
    engine.obligations.append(
        {
            "id": "mock.immediate-duty",
            "instrument_id": "cert-in.directions-70b.2022",
            "status": "in_force",
            "applicability": {"entity_classes": ["body_corporate"]},
            "normalized": {
                "action": "Do this without delay",
                "recipient": "CERT-In",
                "deadline": {"kind": "immediate", "anchor": "noticing"},
            },
            "citations": [
                {
                    "instrument_id": "cert-in.directions-70b.2022",
                    "paragraph_ref": "Mock",
                }
            ],
        }
    )
    result = engine.evaluate(
        IncidentProfile(entity_class="body_corporate", when_noticed=NOTICED), now=NOW
    )
    assert not any(d.obligation_id == "mock.immediate-duty" for d in result.deadlines)
    assert [t.obligation_id for t in result.time_critical] == ["mock.immediate-duty"]
    assert result.to_dict()["time_critical"][0]["action"] == "Do this without delay"


def test_relative_deadline_without_duration_is_unknown_data_error():
    engine = IncidentClockEngine(DATA_DIR)
    engine.obligations.append(
        {
            "id": "mock.relative-missing-duration",
            "status": "in_force",
            "applicability": {"entity_classes": ["body_corporate"]},
            "normalized": {
                "action": "Broken deadline",
                "deadline": {"kind": "relative", "anchor": "noticing"},
            },
        }
    )
    result = engine.evaluate(
        IncidentProfile(entity_class="body_corporate", when_noticed=NOTICED), now=NOW
    )
    assert any(
        u.affects == ["mock.relative-missing-duration"] and "duration_iso8601" in u.question
        for u in result.unknowns
    )


def test_calendar_durations_refused_for_deadlines():
    with pytest.raises(ValueError):
        parse_iso8601_duration("P1M", allow_calendar=False)
    assert parse_iso8601_duration("P5Y") == timedelta(days=5 * 365)
    assert parse_iso8601_duration("PT6H") == timedelta(hours=6)
    assert parse_iso8601_duration("P180D") == timedelta(days=180)
    with pytest.raises(ValueError):
        parse_iso8601_duration("PT")


def test_annexure_reference_titles_are_verbatim_from_the_source():
    """The 20 Annexure I titles must be real substrings of the stored CERT-In text."""
    engine = IncidentClockEngine(DATA_DIR)
    source = (DATA_DIR / "raw" / "CERT-In_Directions_70B_28.04.2022.txt").read_text(
        encoding="utf-8"
    )
    squash = lambda s: re.sub(r"\s+", "", s).lower()  # noqa: E731
    source_n = squash(source)
    items = engine.annexure_items()
    assert len(items) == 20
    for item in items:
        assert squash(item["title"]) in source_n, item["id"]


@given(
    st.datetimes(
        timezones=st.just(UTC),
        min_value=datetime(2023, 1, 1, tzinfo=UTC),
        max_value=datetime(2030, 1, 1, tzinfo=UTC),
    ),
)
def test_deadline_is_anchor_plus_six_hours_for_any_instant(anchor):
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(entity_class="nbfc", is_annexure_i_type=True, when_noticed=anchor)
    dl = _dl(engine.evaluate(profile, now=anchor), "incident-reporting-6h")[0]
    assert dl.deadline_utc == anchor + timedelta(hours=6)
    assert dl.deadline_ist.utcoffset() == timedelta(hours=5, minutes=30)
    assert dl.deadline_ist == dl.deadline_utc


def test_taxonomy_loaded_from_data_dir():
    engine = IncidentClockEngine(DATA_DIR)
    # Must have loaded entity classes from data/entities/
    assert hasattr(engine, "taxonomy")
    assert "body_corporate" in engine.taxonomy
    assert "virtual_asset_exchange" in engine.taxonomy
    assert "nbfc.base_layer" in engine.taxonomy


def test_unknown_entity_class_raises_value_error():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_class="completely_unknown_entity_type_12345",
        is_annexure_i_type=True,
        when_noticed=NOTICED,
    )
    with pytest.raises(ValueError, match="Unknown entity class"):
        engine.evaluate(profile)


def test_entity_taxonomy_hierarchy_resolution():
    engine = IncidentClockEngine(DATA_DIR)
    # vps_provider inherits service_provider and body_corporate
    classes = engine.taxonomy.get_ancestors_and_self("vps_provider")
    assert "vps_provider" in classes
    assert "service_provider" in classes
    assert "body_corporate" in classes


def test_multiple_entity_classes_union_deduplicates_and_rejects_unknowns():
    engine = IncidentClockEngine(DATA_DIR)
    profile = IncidentProfile(
        entity_classes=["sebi.mii", "dpdp.data_fiduciary", "sebi.mii"],
        incident_types=["Malicious code attacks such as Ransomware"],
        personal_data_involved=True,
        when_noticed=NOTICED,
        when_aware=NOTICED,
    )
    result = engine.evaluate(profile, now=NOW)
    assert profile.entity_classes == ["sebi.mii", "dpdp.data_fiduciary"]
    assert "sebi.cscrf.2024.incident-reporting-6h" in result.applicable_obligations
    with pytest.raises(ValueError, match="Unknown entity class"):
        engine.evaluate(IncidentProfile(entity_classes=["sebi.mii", "unknown.class"]))
    with pytest.raises(ValueError, match="either entity_class or entity_classes"):
        IncidentProfile(entity_class="sebi.mii", entity_classes=["sebi.mii"])
    with pytest.raises(ValueError, match="At least one"):
        IncidentProfile(entity_classes=[])


def test_structured_personal_data_gate_and_dpdp_boundaries():
    engine = IncidentClockEngine(DATA_DIR)
    before = datetime(2027, 5, 12, 10, tzinfo=IST)
    after = datetime(2027, 5, 13, 10, tzinfo=IST)
    false_result = engine.evaluate(
        IncidentProfile(
            entity_class="dpdp.data_fiduciary", personal_data_involved=False, when_aware=after
        )
    )
    assert all("rule7" not in item for item in false_result.applicable_obligations)
    unknown_result = engine.evaluate(
        IncidentProfile(entity_class="dpdp.data_fiduciary", when_aware=after)
    )
    assert any(
        u.question == "Is personal data involved in this incident?" for u in unknown_result.unknowns
    )
    before_result = engine.evaluate(
        IncidentProfile(
            entity_class="dpdp.data_fiduciary", personal_data_involved=True, when_aware=before
        )
    )
    assert all("rule7" not in item for item in before_result.applicable_obligations)
    after_result = engine.evaluate(
        IncidentProfile(
            entity_class="dpdp.data_fiduciary", personal_data_involved=True, when_aware=after
        )
    )
    assert {item.obligation_id for item in after_result.time_critical} == {
        "meity.dpdp-rules.2025.rule7-1-principal-intimation",
        "meity.dpdp-rules.2025.rule7-2-a-board-initial",
    }


def test_awareness_unknown_wording_and_sebi_does_not_leak_to_bank():
    engine = IncidentClockEngine(DATA_DIR)
    result = engine.evaluate(
        IncidentProfile(entity_class="dpdp.data_fiduciary", personal_data_involved=True),
        as_of=date(2027, 6, 1),
    )
    assert any(
        u.question == "When did the entity become aware of the personal data breach?"
        for u in result.unknowns
    )
    bank = engine.evaluate(
        IncidentProfile(entity_class="bank", is_annexure_i_type=True, when_noticed=NOTICED)
    )
    assert "sebi.cscrf.2024.incident-reporting-6h" not in bank.applicable_obligations

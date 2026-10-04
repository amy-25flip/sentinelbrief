"""The reviewer packet must cover every dev scenario and stay in step with the labels."""

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location(
        "make_review_packet", REPO / "scripts" / "make_review_packet.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["make_review_packet"] = module
    spec.loader.exec_module(module)
    return module


def test_committed_packet_is_up_to_date():
    """Catches: a reviewer being handed a packet that no longer matches the labels."""
    assert _module().main(["--check"]) == 0


def test_packet_lists_every_scenario_and_every_uncertain_obligation():
    """Catches: a scenario or a contested reading left out of what the reviewer sees."""
    module = _module()
    packet = module.build()
    for path in (REPO / "benchmark" / "scenarios").glob("*.json"):
        assert f"`{json.loads(path.read_text(encoding='utf-8'))['id']}`" in packet
    for obligation in module.load_obligations().values():
        if (obligation.get("confidence") or 1.0) < module.CONTESTED_BELOW:
            assert f"### `{obligation['id']}`" in packet
    assert "has not been checked by a qualified person" in packet

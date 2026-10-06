"""The regulatory-card RSS feed is complete, escaped and deterministic."""

from datetime import UTC, datetime
from xml.etree import ElementTree

from fastapi.testclient import TestClient

from sentinelbrief.api.app import DATA_DIR, app
from sentinelbrief.cards.feed import CardFeed, regulatory_rss
from sentinelbrief.cards.models import Card, CardChip


def test_feed_xml_is_well_formed_complete_and_deterministic():
    client = TestClient(app)
    first = client.get("/feed.xml")
    second = client.get("/feed.xml")
    assert first.status_code == 200
    assert first.content == second.content
    root = ElementTree.fromstring(first.content)
    assert root.tag == "rss" and root.attrib["version"] == "2.0"
    feed = CardFeed(DATA_DIR)
    feed.load_from_data_dir(fixtures_dir=DATA_DIR.parent / "tests" / "fixtures")
    regulatory_count = sum(card.stream == "regulatory" for card in feed.get_feed())
    assert len(root.findall("./channel/item")) == regulatory_count
    assert root.findtext("./channel/lastBuildDate")
    for item in root.findall("./channel/item"):
        assert item.find("guid").attrib["isPermaLink"] == "false"
        assert "AI-assisted summary, not legal advice. See the source." in item.findtext(
            "description"
        )


def test_rss_escapes_card_text_and_links_to_the_obligation_page():
    card = Card(
        id="regulatory:test<&",
        stream="regulatory",
        headline="Use <control> & review",
        body="A < B & C is source text that must remain data, not XML markup.",
        chips=[CardChip(label="Issuer", value="RBI & Co", chip_type="issuer")],
        obligation_id="test.obligation<&",
        published_at=datetime(2026, 10, 6, tzinfo=UTC),
    )
    payload = regulatory_rss([card], "https://example.test")
    assert b"&lt;control&gt; &amp; review" in payload
    assert b"A &lt; B &amp; C" in payload
    root = ElementTree.fromstring(payload)
    assert root.findtext("./channel/item/title") == card.headline
    assert root.findtext("./channel/item/category") == "RBI & Co"
    assert root.findtext("./channel/item/link") == (
        "https://example.test/obligations/test.obligation<&"
    )


def test_base_page_advertises_the_rss_feed():
    page = TestClient(app).get("/")
    assert 'rel="alternate" type="application/rss+xml" href="/feed.xml"' in page.text

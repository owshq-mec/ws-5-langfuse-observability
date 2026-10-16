from datetime import timezone

import pytest

from context.ingest.sources import PARSERS, load_episodes


@pytest.fixture(scope="module")
def episodes():
    return load_episodes()


def test_every_system_produces_episodes(episodes):
    systems = {ep.system for ep in episodes}
    assert systems == set(PARSERS)


def test_episodes_are_dated_and_sorted(episodes):
    assert all(ep.reference_time.tzinfo == timezone.utc or ep.reference_time.utcoffset().total_seconds() == 0
               for ep in episodes)
    times = [ep.reference_time for ep in episodes]
    assert times == sorted(times)


def test_episode_names_are_unique(episodes):
    names = [ep.name for ep in episodes]
    assert len(names) == len(set(names))


def by_name(episodes, fragment):
    return next(ep for ep in episodes if fragment in ep.name)


def test_stale_refund_policy_keeps_its_2023_date(episodes):
    old = by_name(episodes, "Refund-Policy-2023")
    new = by_name(episodes, "Refund-and-Credits-Policy")
    assert old.reference_time.year == 2023 and "30 days" in old.body
    assert new.reference_time.date().isoformat() == "2026-02-20" and "14 days" in new.body


def test_slack_shows_aliases_and_directory_resolves_them(episodes):
    qbr_recap = by_name(episodes, "slack/cs-orion/2026-09-09")
    directory = by_name(episodes, "slack/users.json")
    assert qbr_recap.body.startswith("Jo L.")
    assert "Jo L. (@jo.l) is Johanna Lindqvist" in directory.body


def test_contract_pdf_text_contains_clause_7_3(episodes):
    msa = by_name(episodes, "Orion_Freight_Systems_MSA")
    assert "7.3 SLA refund right" in msa.body and msa.reference_time.date().isoformat() == "2025-08-15"


def test_zendesk_episodes_never_contain_later_comments(episodes):
    day_one = by_name(episodes, "zendesk/tickets.json#48233@2026-09-29")
    day_two = by_name(episodes, "zendesk/tickets.json#48233@2026-09-30")
    assert "30 days" in day_one.body and "2026-09-30" not in day_one.body and "escalated_revops" not in day_one.body
    assert "(internal note)" in day_two.body and day_two.reference_time.date().isoformat() == "2026-09-30"


def test_no_chat_episode_mentions_a_later_timestamp(episodes):
    import re
    for ep in episodes:
        if ep.system == "zendesk":
            stamps = re.findall(r"\[(20\d\d-\d\d-\d\d)T", ep.body)
            assert all(day <= ep.reference_time.date().isoformat() for day in stamps), ep.name

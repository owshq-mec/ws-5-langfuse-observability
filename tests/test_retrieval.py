from datetime import datetime, timezone
from types import SimpleNamespace

from context.retrieval import episode_path, fact_status, list_sources, parse_as_of, read_source


def dt(day: str) -> datetime:
    return datetime.fromisoformat(day).replace(tzinfo=timezone.utc)


def edge(valid_at=None, invalid_at=None):
    return SimpleNamespace(valid_at=valid_at, invalid_at=invalid_at)


def test_status_without_as_of():
    assert fact_status(edge(dt("2023-02-01")), None, None) == "current"
    assert fact_status(edge(dt("2023-02-01"), dt("2026-03-01")), None, None) == "superseded"


def test_status_with_as_of():
    as_of = parse_as_of("2025-12-01")
    finance_rule = edge(dt("2023-02-01"), dt("2026-03-03"))
    revops_rule = edge(dt("2026-03-03"))
    assert fact_status(finance_rule, as_of, dt("2023-02-01")) == "true on as_of"
    assert fact_status(revops_rule, as_of, dt("2026-03-03")) == "recorded after as_of"
    assert fact_status(finance_rule, parse_as_of("2026-10-15"), dt("2023-02-01")) == "no longer true on as_of"


def test_as_of_includes_the_whole_day():
    assert fact_status(edge(dt("2026-09-29")), parse_as_of("2026-09-29"), dt("2026-09-29")) == "true on as_of"


def test_episode_path_maps_zendesk_tickets_to_comment_threads():
    assert episode_path("zendesk/tickets.json#48233@2026-09-30") == "zendesk/comments/48233.json"
    assert episode_path("hubspot/companies.csv#18342001") == "hubspot/companies.csv"


def test_read_source_reads_pdf_and_blocks_escapes():
    msa = read_source("drive/Orion_Freight_Systems_MSA_2025-08-15.pdf")
    assert "7.3 SLA refund right" in msa["content"]
    for bad in ["../../.env", "/etc/passwd", "confluence/../../../pyproject.toml", "README.md", "truth/questions.jsonl"]:
        assert "error" in read_source(bad)


def test_list_sources_covers_all_systems():
    systems = list_sources()["systems"]
    assert set(systems) == {"confluence", "notion", "slack", "drive", "hubspot", "zendesk", "gong"}
    assert all(systems.values())

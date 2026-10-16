"""Read-side of Helix: temporal fact search, entity lookup and source documents."""

from datetime import datetime, time, timezone
from functools import cache

from graphiti_core import Graphiti
from graphiti_core.edges import EntityEdge
from graphiti_core.nodes import EpisodicNode
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF
from pypdf import PdfReader

from context.config import DATA_DIR, settings
from context.ingest.sources import PARSERS

MAX_SOURCE_CHARS = 15_000


def parse_as_of(as_of: str | None) -> datetime | None:
    if not as_of:
        return None
    day = datetime.strptime(as_of[:10], "%Y-%m-%d").date()
    return datetime.combine(day, time.max, tzinfo=timezone.utc)


def episode_path(name: str) -> str:
    if name.startswith("zendesk/tickets.json#"):
        return f"zendesk/comments/{name.split('#', 1)[1].split('@', 1)[0]}.json"
    return name.split("#", 1)[0]


def _day(value: datetime | None) -> str | None:
    return value.date().isoformat() if value else None


def fact_status(edge: EntityEdge, as_of: datetime | None, known_since: datetime | None) -> str:
    if as_of is None:
        return "superseded" if edge.invalid_at else "current"
    if known_since and known_since > as_of:
        return "recorded after as_of"
    if edge.valid_at and edge.valid_at > as_of:
        return "not yet true on as_of"
    if edge.invalid_at and edge.invalid_at <= as_of:
        return "no longer true on as_of"
    return "true on as_of"


async def search_facts(graphiti: Graphiti, query: str, as_of: str | None = None, limit: int = 10) -> dict:
    as_of_dt = parse_as_of(as_of)
    edges = await graphiti.search(query, group_ids=[settings().group_id], num_results=max(limit * 2, 20))
    episode_ids = sorted({uuid for edge in edges for uuid in edge.episodes})
    episodes = {ep.uuid: ep for ep in await EpisodicNode.get_by_uuids(graphiti.driver, episode_ids)} if episode_ids else {}

    facts, hidden = [], 0
    for edge in edges:
        sources = [episodes[u] for u in edge.episodes if u in episodes]
        known_since = min((ep.valid_at for ep in sources if ep.valid_at), default=None)
        status = fact_status(edge, as_of_dt, known_since)
        if status in {"recorded after as_of", "not yet true on as_of"}:
            hidden += 1
            continue
        facts.append({
            "fact": edge.fact,
            "status": status,
            "valid_from": _day(edge.valid_at),
            "valid_until": _day(edge.invalid_at),
            "sources": [{"path": episode_path(ep.name), "description": ep.source_description, "dated": _day(ep.valid_at)}
                        for ep in sources if as_of_dt is None or ep.valid_at is None or ep.valid_at <= as_of_dt],
        })
        if len(facts) == limit:
            break
    return {"query": query, "as_of": as_of, "facts": facts, "hidden_as_future": hidden}


async def find_entities(graphiti: Graphiti, query: str, limit: int = 8) -> dict:
    config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
    config.limit = limit
    results = await graphiti.search_(query, config=config, group_ids=[settings().group_id])
    return {"query": query, "entities": [
        {"name": node.name, "types": [label for label in node.labels if label != "Entity"],
         "summary": node.summary, "attributes": node.attributes}
        for node in results.nodes
    ]}


def read_source(path: str) -> dict:
    relative = episode_path(path.strip().lstrip("/"))
    if relative not in source_paths():
        return {"path": relative, "error": "not a source document; use list_sources to see valid paths"}
    target = DATA_DIR / relative
    if target.suffix == ".pdf":
        text = "\n".join(page.extract_text() for page in PdfReader(target).pages)
    else:
        text = target.read_text()
    return {"path": relative, "truncated": len(text) > MAX_SOURCE_CHARS, "content": text[:MAX_SOURCE_CHARS]}


@cache
def source_paths() -> frozenset[str]:
    """Only parsed source documents are readable: never the story bible or the ground truth."""
    return frozenset(ep.path for parse in PARSERS.values() for ep in parse())


def list_sources() -> dict:
    systems: dict[str, list[dict]] = {}
    for system, parse in PARSERS.items():
        seen: dict[str, str] = {}
        for ep in parse():
            seen.setdefault(ep.path, ep.reference_time.date().isoformat())
        systems[system] = [{"path": path, "dated": day} for path, day in sorted(seen.items())]
    return {"systems": systems}

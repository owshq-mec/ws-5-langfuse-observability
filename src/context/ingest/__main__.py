"""Load the Orbisa corpus into the Helix graph.

    uv run python -m context.ingest --dry-run      # parse every source, no LLM calls
    uv run python -m context.ingest                # ingest new or changed episodes
    uv run python -m context.ingest --reset        # wipe the orbisa graph first
"""

import argparse
import asyncio
import json
import os
import sys
import time
from collections import Counter

from graphiti_core.utils.maintenance.graph_data_operations import clear_data

from context.config import STATE_DIR, settings
from context.graph import build_graphiti
from context.ingest.sources import PARSERS, load_episodes
from context.ontology import ENTITY_TYPES

MANIFEST = STATE_DIR / "ingested.json"


def read_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def write_manifest(data: dict) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=2))


async def ingest(systems: list[str] | None, reset: bool, limit: int | None) -> None:
    s = settings()
    episodes = load_episodes(systems)
    graphiti = build_graphiti()
    try:
        await graphiti.build_indices_and_constraints()
        manifest = {} if reset else read_manifest()
        if reset:
            await clear_data(graphiti.driver, group_ids=[s.group_id])
            print(f"cleared graph group '{s.group_id}'")
        todo = [ep for ep in episodes if manifest.get(ep.name, {}).get("digest") != ep.digest][:limit]
        print(f"{len(episodes)} episodes, {len(todo)} to ingest with {s.ingest_model}")
        for i, ep in enumerate(todo, start=1):
            started = time.perf_counter()
            result = await graphiti.add_episode(
                name=ep.name,
                episode_body=ep.body,
                source=ep.source,
                source_description=ep.description,
                reference_time=ep.reference_time,
                group_id=s.group_id,
                entity_types=ENTITY_TYPES,
            )
            manifest[ep.name] = {"digest": ep.digest, "uuid": result.episode.uuid, "path": ep.path,
                                 "system": ep.system, "reference_time": ep.reference_time.isoformat()}
            write_manifest(manifest)
            print(f"[{i}/{len(todo)}] {ep.name}: {len(result.nodes)} entities, {len(result.edges)} facts "
                  f"({time.perf_counter() - started:.1f}s)")
    finally:
        await graphiti.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--system", action="append", choices=sorted(PARSERS), help="only these systems (repeatable)")
    parser.add_argument("--dry-run", action="store_true", help="parse sources and print episodes, no LLM calls")
    parser.add_argument("--reset", action="store_true", help="delete the orbisa graph group before ingesting")
    parser.add_argument("--limit", type=int, help="ingest at most N episodes")
    args = parser.parse_args()

    if args.dry_run:
        episodes = load_episodes(args.system)
        for ep in episodes:
            print(f"{ep.reference_time:%Y-%m-%d}  {ep.system:<10} {ep.source.value:<7} {len(ep.body):>5} chars  {ep.name}")
        print(f"\n{len(episodes)} episodes by system: {dict(Counter(ep.system for ep in episodes))}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is empty. Add it to .env (ingestion uses Claude to extract facts).")
    asyncio.run(ingest(args.system, args.reset, args.limit))


if __name__ == "__main__":
    main()

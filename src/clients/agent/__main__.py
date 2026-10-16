"""Ask Orbisa — a Claude Agent SDK agent that answers from the Helix MCP server.

    uv run python -m clients.agent --id Q01
    uv run python -m clients.agent "Who approves refunds?" --as-of 2026-10-15
"""

import argparse
import asyncio
import os
import sys
from datetime import date

from clients.agent.runner import ask, check_helix, load_truth


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("question", nargs="?", help="free-form question")
    parser.add_argument("--id", help="run a ground-truth question from data/orbisa/truth/questions.jsonl, e.g. Q01")
    parser.add_argument("--as-of", help="date the question is asked (YYYY-MM-DD); defaults to the truth item or today")
    parser.add_argument("--model", help="override HELIX_AGENT_MODEL")
    parser.add_argument("--json", action="store_true", help="print the full run as JSON")
    args = parser.parse_args()

    expected = None
    if args.id:
        item = load_truth()[args.id.upper()]
        question, as_of, expected = item["question"], args.as_of or item["as_of"], item
    elif args.question:
        question, as_of = args.question, args.as_of or date.today().isoformat()
    else:
        parser.error("give a question or --id")

    if os.environ.get("HELIX_AGENT_PROVIDER") != "openrouter" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("note: ANTHROPIC_API_KEY is empty, so the bundled Claude Code CLI will use your Claude login.", file=sys.stderr)
    check_helix()

    run = asyncio.run(ask(question, as_of, model=args.model))
    if args.json:
        print(run.to_json())
        return

    print(f"\nQ ({as_of}): {question}\n\n{run.answer}\n")
    print(f"tools: {', '.join(c['tool'] for c in run.tool_calls) or 'none'}")
    cost = f"${run.cost_usd:.4f}" if run.cost_usd is not None else "n/a"
    print(f"turns: {run.num_turns} | cost: {cost} | time: {run.duration_ms / 1000:.1f}s | error: {run.is_error}")
    if expected:
        print(f"\nexpected ({expected['category']}): {expected['expected_answer']}")


if __name__ == "__main__":
    main()

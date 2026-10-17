# Team session prompts

We join Orbisa as new engineers. The context engine (Helix) and the agent (Ask Orbisa) already exist —
a **brownfield** project. Our brief is [`docs/orbisa-case-study.pdf`](../docs/orbisa-case-study.pdf).
We read it, choose and narrow the problem, design the solution, and build it with Claude Code as our pair.

The facilitator drives the screen. The team talks, challenges and decides. Claude Code proposes, asks
questions back, and waits for the team's decision at every gate.

## Flow

| Phase | Prompt | Output |
|---|---|---|
| Setup | [00 — Working agreement](00-working-agreement.md) | Claude knows how to work with the team |
| Discover | [01 — Understand the brief](01-understand-the-brief.md) | shared summary, open questions |
| Discover | [02 — Explore the brownfield](02-explore-the-brownfield.md) | the system running, gaps observed with evidence |
| Define | [03 — Select the problem statement](03-select-problem-statement.md) | one statement chosen by vote |
| Define | [04 — Narrow the statement](04-narrow-the-statement.md) | `decisions/01-problem-statement.md` |
| Design | [05 — Design the solution](05-design-the-solution.md) | `decisions/02-solution-design.md` |
| Build | [06 — Trace Helix](06-build-trace-helix.md) | retrieval observations in Langfuse |
| Build | [07 — Trace the agent with OpenTelemetry](07-build-trace-agent-otel.md) | model calls, tokens, cost |
| Build | [08 — One trace, sessions, masking](08-build-link-and-enrich.md) | one trace per question |
| Build | [09 — Prompt management](09-build-prompt-management.md) | versioned prompts and tool descriptions |
| Build | [10 — Ground truth and experiments](10-build-dataset-and-experiments.md) | correctness per category, compared runs |
| Build | [11 — Online evaluation and review](11-build-online-eval-and-review.md) | live scores, annotation queue |
| Build | [12 — Dashboards, alerts, agentic access](12-build-dashboards-alerts-agentic.md) | monitoring, agent-driven fix |
| Close | [13 — Readout](13-readout.md) | `decisions/03-readout.md` against the success criteria |

## How to use a prompt

Each file has four parts:
- **Facilitator** — what to set up and what to watch for.
- **Prompt** — paste it into Claude Code as is.
- **Team discussion** — questions to ask the room while Claude works or after it answers.
- **Gate** — what the team must agree on before the next prompt.

## Environment (already running before the session)

```bash
make up        # Neo4j, Helix MCP (:8765), Langfuse v4 (:3000), alert-sink (:8787) in Docker
make ingest    # load the Orbisa corpus into the graph (once)
make ask Q=Q01 # ask a ground-truth question
```

Langfuse UI: http://localhost:3000 — user and password are in `.env` (`LANGFUSE_INIT_USER_EMAIL`,
`LANGFUSE_INIT_USER_PASSWORD`). The project "Ask Orbisa" and its API keys are created at startup.

## Ground rules every build prompt assumes

- Langfuse runs **self-hosted v4** in Docker: host URL `http://localhost:3000`, container URL
  `http://langfuse-web:3000`. The Python SDK stays on **v4** (`langfuse>=4.18,<5`).
- Ground every API call in current docs (langfuse.com/docs, append `.md` for plain text) or the installed
  package source in `.venv`. Never guess a signature.
- This Langfuse runs in v4 **events_only** mode: read data through the v2/v3 endpoints
  (`/api/public/v2/observations`, `/api/public/v3/scores`, `/api/public/v2/metrics`). The v1 `observations`
  and `traces` endpoints answer "not available on deployments running in Langfuse v4 events_only mode".
- Read SDK objects as attributes (`page.data[0].trace_id`), not as dicts.
- Observability is a layer: Helix and the agent must keep working when Langfuse is down.
- Self-hosted limits we accept: server-side masking, audit logs and data retention need an Enterprise key
  (we use SDK-side masking); code evaluators run TypeScript/JavaScript only; LLM-as-a-judge needs an LLM
  connection (it can be created through the public API). Alerts and their automations are UI-only.
- `.env` values win over the shell (see `src/context/config.py`). To test "Langfuse keys missing", point
  `HELIX_ENV_FILE=/dev/null` at an empty file instead of editing `.env`.
- After a code change in `src/`, run `make rebuild` so the Helix container picks it up.

# 05 — Design the solution

**Facilitator:** first the concepts (OpenTelemetry, Langfuse data model), then options, then one design.
If the team is new to observability, ask Claude for part 1 before part 2.

## Prompt

```text
Read decisions/01-problem-statement.md. Design how we make Helix and Ask Orbisa observable.

Part 1 — concepts, short: explain trace, span/observation, observation types (agent, generation, tool,
retriever), context propagation, OTLP, and how Langfuse v4 (self-hosted at http://localhost:3000) stores
them. Use one Orbisa question as the running example. Check against langfuse.com/docs, don't recall.

Part 2 — options. Propose 3 approaches and compare them against our success criteria and constraints:
  A) Langfuse SDK only: decorate Helix tools and the agent function.
  B) Standards first: the Claude Agent SDK exports its own OpenTelemetry spans to Langfuse's OTLP endpoint,
     Helix uses the Langfuse SDK, and the two are linked through the traceparent header the CLI sends to
     HTTP MCP servers.
  C) An alternative you think is worth it (for example a proxy or gateway).
Give a table: what we see, effort, lock-in, risks. Recommend one and stop for our decision.

Part 3 — after we decide, write decisions/02-solution-design.md with: the chosen approach, a Mermaid
diagram of the trace for one question (agent → model calls → MCP → retrieval), the observation names we
will use (verb-first, stable), the scores we will create and how each maps to a success criterion, the
dataset plan (data/orbisa/truth/questions.jsonl), and the build increments in order with a check for each.
```

## Team discussion

- Why do stable observation names matter for evaluators and dashboards?
- What is the risk of tracing the full content of customer documents? How do we limit it?

## Gate

`decisions/02-solution-design.md` exists, with the approach, trace diagram, names, scores and increments.

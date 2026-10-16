# 12 — Build: dashboards, alerts, agentic access

**Facilitator:** two parts. Part A gives operations its view. Part B closes the loop: an agent reads Langfuse
and proposes a fix the team must accept or reject.

## Prompt A — dashboard and alert

```text
Create the Ask Orbisa dashboard in our self-hosted Langfuse (custom dashboards docs). Plan first, wait for go.
Widgets: questions per day; p95 latency of the agent and of the retrieval observation; cost per question by
model; tool calls per question; mean faithfulness and correctness over time by tag.
Alert: mean faithfulness over the last hour below 0.8 → webhook (use a webhook.site URL for the demo).
Create through the API where possible (src/observability/monitoring/), otherwise give exact UI steps.
Finally query the Metrics API v2 for cost per question over the last day.
```

## Prompt B — agentic access

```text
Connect to the Langfuse MCP server built into our instance (http://localhost:3000/api/public/mcp, Basic auth
with our project keys) or use `npx @langfuse/cli` with LANGFUSE_BASE_URL=http://localhost:3000.
Investigate our latest experiment run on orbisa-truth:
1. List items scored incorrect or partially_correct with the judge's reason.
2. For each, open the trace and classify where it failed: retrieval, temporal, alias, or reasoning.
3. Propose ONE change (system prompt, a tool description, or retrieval in src/context/retrieval) for the
   biggest group, with the expected effect. Stop and wait for our decision.
4. If we accept, make it as a staging prompt version or a code change, re-run the subset, and show us the
   before/after comparison.
```

## Team discussion

- Would you let an agent ship the fix without a human gate? What evidence would change your mind?

## Gate

The dashboard answers "is Ask Orbisa healthy?" at a glance, and the agent-proposed fix is accepted or
rejected based on an experiment, not on opinion.

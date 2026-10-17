# 12 — Build: dashboards, alerts, agentic access

**Facilitator:** two parts. Part A gives operations its view. Part B closes the loop: an agent reads Langfuse
and proposes a fix the team must accept or reject.

## Prompt A — dashboard and alert

```text
Create the Ask Orbisa dashboard in our self-hosted Langfuse. Plan first, wait for go.
Widgets: questions per day; p95 latency of the agent, the model calls and the retrieval observation; cost per
question by model; tool calls per question; mean faithfulness, correctness and source recall over time.
Test every widget query against the Metrics API v2 (/api/public/v2/metrics) first, then create the dashboard
through the dashboards API in the installed SDK (langfuse.api.unstable.dashboards / dashboard_widgets) in
src/observability/monitoring/dashboard.py, plus a `report` command that prints cost per question, latency,
tool calls and scores for the last 24 hours from the Metrics API.

Alert: mean faithfulness over the last hour below 0.8 (warning below 0.9) → webhook. Alerts and their
automations are UI-only, so give us exact UI steps. Company data must not leave the laptop, so do not use
webhook.site: use the local receiver alert-sink (scripts/alert_sink.py, a compose service; `make alerts`
prints what it received) and tell us which Langfuse webhook rules it must satisfy (allowed ports, private
hosts). Set the no-data
handling so a quiet hour does not fire the alert. Then prove the alert fires with a drill: a deliberately
bad prompt version under the label "drill", run against a few questions, and show us the webhook payload.
```

## Prompt B — agentic access

```text
Connect to the Langfuse MCP server built into our instance (http://localhost:3000/api/public/mcp, Basic auth
with our project keys) or use `npx @langfuse/cli` with LANGFUSE_BASE_URL=http://localhost:3000.
Investigate our latest baseline experiment run on orbisa-truth (src/observability/monitoring/investigate.py):
1. List items scored incorrect or partially_correct with the judge's reason, and items with source_recall
   below 1. If nothing is incorrect, say so and investigate the weakest score instead.
2. For each, open the trace and classify where it failed: retrieval, temporal, alias, or reasoning. For a
   temporal item, compare the dates in the answer with what search-context returned on that as-of date.
3. Propose ONE change (system prompt, a tool description, or retrieval in src/context/retrieval) for the
   biggest group, with the expected effect and the score that should move. Stop and wait for our decision.
4. If we accept, make it as a staging prompt version or a code change, run the full dataset at least twice
   for the candidate and twice for the baseline, compare them with a small command in
   src/observability/experiments/compare.py that applies our release rule, and show us the before/after.
```

## Team discussion

- Would you let an agent ship the fix without a human gate? What evidence would change your mind?

## Gate

The dashboard answers "is Ask Orbisa healthy?" at a glance, and the agent-proposed fix is accepted or
rejected based on an experiment, not on opinion.

# 08 — Build: one trace, sessions, users, masking

**Facilitator:** show the trace before and after part A side by side. Distributed tracing is a span id
travelling in a header — make that visible.

## Prompt

```text
Build increment 3. Plan first, wait for go.

Part A — link the traces. The Claude Code CLI sends a W3C `traceparent` HTTP header to HTTP MCP servers when
its tracing is on (with a custom ANTHROPIC_BASE_URL such as OpenRouter it needs
CLAUDE_CODE_PROPAGATE_TRACEPARENT=1). In the Helix MCP server, read the headers from the tool Context
(mcp 2.x: a `ctx: Context` parameter, ctx.headers; check it stays out of the tool's input schema), extract
with opentelemetry.propagate.extract, and attach the context so our retrieval observations become children
of the CLI's tool span. When there is no header, attach an empty context so the observation is a clean root.
Prove with the Langfuse API that retrieval observations now share the agent trace id, and that every MCP
tool call has exactly one Helix observation.

Part B — enrich with propagate_attributes (SDK v4): session_id (new --session flag), user_id (new --user
flag, default "workshop"), tags (truth category and id when --id is used, and "as-of:<date>"), environment
LANGFUSE_TRACING_ENVIRONMENT=workshop. propagate_attributes only reaches spans created in our process: check
which userId, sessionId and environment the CLI's spans get in Langfuse, and fix them if they differ (hint:
the CLI accepts OTEL_RESOURCE_ATTRIBUTES; read Langfuse's attribute mapping table for the precedence).

Part C — masking. The corpus has email addresses (Slack users, the Notion team directory). Add an SDK mask
function that replaces emails with <email> (langfuse.com/docs/observability/features/masking.md). Server-side
masking needs an Enterprise key, so we mask in the SDK. Prove it: read slack/users.json through read_source
and show that the agent receives the emails but Langfuse stores <email>. Then check whether the CLI's OTLP
spans carry content at all, and explain which documented OTEL_LOG_* variables would change that. Do not
invent flags.
```

## Team discussion

- What would an auditor at a bank (think DKB in the Langfuse case studies) want from these traces?
- Masking only covers data that passes through the SDK. Where else does customer data flow?

## Gate

Q01 is one trace from the agent down to retrieval. Sessions, users and tags filter correctly. Emails are
masked where the SDK sees them.

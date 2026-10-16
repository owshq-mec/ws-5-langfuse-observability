# 08 — Build: one trace, sessions, users, masking

**Facilitator:** show the trace before and after part A side by side. Distributed tracing is a span id
travelling in a header — make that visible.

## Prompt

```text
Build increment 3. Plan first, wait for go.

Part A — link the traces. The Claude Code CLI sends a W3C `traceparent` HTTP header to HTTP MCP servers
(with OpenRouter it needs CLAUDE_CODE_PROPAGATE_TRACEPARENT=1). In the Helix MCP server, read the headers
from the tool Context (mcp 2.x: ctx.headers), extract with opentelemetry.propagate.extract, and attach the
context so our retrieval observations become children of the agent's tool span. Check what mcp 2.x's own
OpenTelemetry middleware emits (it reads _meta, not headers) and whether Langfuse v4 exports it by default.
Prove with the Langfuse API that retrieval observations now share the agent trace id.

Part B — enrich with propagate_attributes (SDK v4): session_id (new --session flag), user_id (new --user
flag, default "workshop"), tags (truth category when --id is used, and "as-of:<date>"), environment
LANGFUSE_TRACING_ENVIRONMENT=workshop.

Part C — masking. The corpus has email addresses (Zendesk, HubSpot). Add an SDK mask function that
replaces emails with <email> (langfuse.com/docs/observability/features/masking.md). Server-side masking
needs an Enterprise key, so we mask in the SDK. Then check whether the CLI's OTLP spans are masked too.
If not, explain why and show the documented options. Do not invent flags.
```

## Team discussion

- What would an auditor at a bank (think DKB in the Langfuse case studies) want from these traces?
- Masking only covers data that passes through the SDK. Where else does customer data flow?

## Gate

Q01 is one trace from the agent down to retrieval. Sessions, users and tags filter correctly. Emails are
masked where the SDK sees them.

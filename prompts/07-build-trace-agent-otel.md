# 07 — Build: trace the agent with OpenTelemetry

**Facilitator:** this is the OpenTelemetry lesson. The agent emits standard spans; Langfuse is just an OTLP
backend. Show the OTLP env vars on screen and explain each one.

## Prompt

```text
Build increment 2: send the Claude Agent SDK's own OpenTelemetry spans to our self-hosted Langfuse.
Plan first, wait for go.

Ground yourself in https://code.claude.com/docs/en/agent-sdk/observability.md (the SDK runs the Claude Code
CLI, which exports spans), the span attribute tables in https://code.claude.com/docs/en/monitoring-usage.md,
and https://langfuse.com/integrations/native/opentelemetry.md (OTLP endpoint, Basic auth,
x-langfuse-ingestion-version header, attribute mapping table).

- In src/observability/tracing/, build the CLI env vars: CLAUDE_CODE_ENABLE_TELEMETRY=1,
  CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1, OTEL_TRACES_EXPORTER=otlp, OTEL_METRICS_EXPORTER=none,
  OTEL_LOGS_EXPORTER=none, OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=http/protobuf,
  OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=<LANGFUSE_BASE_URL>/api/public/otel/v1/traces,
  OTEL_EXPORTER_OTLP_TRACES_HEADERS with Basic auth (base64 of public:secret) and x-langfuse-ingestion-version=4,
  OTEL_TRACES_EXPORT_INTERVAL=1000, OTEL_SERVICE_NAME=ask-orbisa. Never the console exporter (stdout is the
  SDK's message channel). Empty when Langfuse keys are missing.
  Remember LANGFUSE_BASE_URL is http://langfuse-web:3000 inside Docker and http://localhost:3000 on the host.
- Merge them into ClaudeAgentOptions.env in src/clients/agent/runner.py.
- Wrap ask() in an observation of type agent named as in our design, input {question, as_of}, output the
  answer. The SDK injects TRACEPARENT from the active OpenTelemetry span, so the CLI's
  claude_code.interaction span becomes its child.
- Add `python -m observability.inspect` that prints the latest trace as a tree from the API (type, name,
  latency, model, tokens, cost).
- Run `make ask Q=Q01` and show us the trace tree, which spans are generations, and whether model, tokens and
  cost were captured. Compare the attribute names the CLI writes on claude_code.llm_request with the ones
  Langfuse maps to usage. If usage or cost is missing, show the evidence and give us options with trade-offs,
  for example: the OpenInference instrumentor (langfuse.com/integrations/frameworks/claude-agent-sdk), an
  OpenTelemetry Collector that renames the attributes, or recording ResultMessage.model_usage as one
  generation per model. Wait for our decision.
```

## Team discussion

- Open the timeline view: where does the time go, model thinking or Helix lookups?
- What did one question cost? Multiply by Support's daily volume: is that acceptable?

## Gate

One trace per question rooted at the agent observation, with model calls and their usage visible.

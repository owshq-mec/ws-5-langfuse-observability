# src/observability — to build

This package is empty on purpose. The team designs it in `decisions/02-solution-design.md` and builds it
with the prompts in [`prompts/`](../../prompts/README.md) (06–12).

Suggested shape (the team decides in prompt 05):

| Folder | What ends up here |
|---|---|
| `tracing/` | Langfuse client setup, Helix MCP tool instrumentation, OpenTelemetry export for the agent, trace linking, sessions, masking |
| `prompts/` | system prompt and tool descriptions in Langfuse Prompt Management |
| `datasets/` | the ground truth as a Langfuse dataset |
| `evaluators/` | code evaluators and LLM-as-a-judge |
| `experiments/` | experiment runner and variant comparison |
| `monitoring/` | LLM connection, score configs, annotation queues, dashboards, alerts |

Rule: Helix (`src/context`) and the agent (`src/clients`) must keep working when Langfuse is down.

# 06 — Build: trace Helix

**Facilitator:** first build increment. The team checks the result in the Langfuse UI, not in the code.

## Prompt

```text
Build increment 1 from decisions/02-solution-design.md: trace the Helix MCP server. Plan first, wait for go.

Requirements:
- src/observability/tracing/: a small module that returns the Langfuse client (Python SDK v4, get_client())
  and reports whether LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_BASE_URL are set. Tracing is a
  no-op when they are missing.
- Instrument the four tools in src/context/mcp/server.py with the observation names and types from our
  design (retriever for search and entity lookup, tool for read_source and list_sources).
- Metadata on the search observation: as_of, number of facts, number hidden as future, source systems.
- Flush on shutdown.
- `make rebuild`, then `make ask Q=Q01`, then fetch the latest observations from the Langfuse API to prove
  they arrived. Run `make test`.
Then tell us where to click in the Langfuse UI to see a search observation with its facts and sources.
```

## Team discussion

- Open a search observation: can you see which facts were hidden as future? Why does that matter for Q01?
- Each tool call is a separate trace right now. Is that a problem? (Increment 3 fixes it.)

## Gate

Retriever observations are visible in Langfuse, and the agent still works with the Langfuse keys removed.

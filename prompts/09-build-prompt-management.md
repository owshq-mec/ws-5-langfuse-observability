# 09 — Build: prompt management

**Facilitator:** connect this to "change safety" in the problem statement. Prompts and tool descriptions
change behavior as much as code does.

## Prompt

```text
Build increment 4: move prompts into Langfuse Prompt Management. Plan first, wait for go.

- src/observability/prompts/push.py: create "ask-orbisa-system" from src/clients/agent/system_prompt.md and
  one text prompt per Helix tool description (from the docstrings in src/context/mcp/server.py), all
  labeled "production". Re-running adds a version only when the text changed (compare with the version that
  has the label). Add --label and --system-file so we can push a candidate under another label.
- The agent fetches "ask-orbisa-system" by label (env HELIX_PROMPT_LABEL, default production, and a
  --prompt-label flag) with a short timeout, and falls back to the local file if Langfuse is unavailable.
  Record prompt name, label, version and source (langfuse or local fallback) on the agent observation.
- Link the prompt version to the generations: propagate_attributes(prompt=...) covers the generations our
  process creates. Check whether the CLI's own generations get the link too, and if not, whether the
  langfuse.observation.prompt.* attributes can travel through OTEL_RESOURCE_ATTRIBUTES.
- The MCP server registers each tool with the fetched description at startup, docstring as fallback.
- Then ask us for one rule we want to add to the system prompt (suggest: "When a signed contract and a policy
  disagree, quote the contract clause number."), keep it in src/observability/prompts/candidates/, create it
  as a new version labeled "staging", and run Q01 with both labels. Show us both traces with their prompt
  versions.
- Add a promote command: it moves the production label to a version AND writes that text to
  system_prompt.md. Explain why the file must change too.
- Tests: the prompt falls back to the local text without keys and when Langfuse is down (in under 10 s).
```

## Team discussion

- Who should be allowed to promote staging to production? (Protected labels need an Enterprise key on
  self-hosted — what do we do instead?)
- Open a trace in the Playground and edit the prompt live. What would you test?

## Gate

Both versions exist, each trace shows its prompt version, and the agent works without Langfuse.

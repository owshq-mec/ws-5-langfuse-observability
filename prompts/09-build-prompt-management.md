# 09 — Build: prompt management

**Facilitator:** connect this to "change safety" in the problem statement. Prompts and tool descriptions
change behavior as much as code does.

## Prompt

```text
Build increment 4: move prompts into Langfuse Prompt Management. Plan first, wait for go.

- src/observability/prompts/push.py: create "ask-orbisa-system" from src/clients/agent/system_prompt.md and
  one text prompt per Helix tool description (from the docstrings in src/context/mcp/server.py), all
  labeled "production". Re-running adds a version only when the text changed.
- The agent fetches "ask-orbisa-system" by label (env HELIX_PROMPT_LABEL, default production) and falls back
  to the local file if Langfuse is unavailable. Record prompt name and version on the agent observation.
- The MCP server uses the fetched tool descriptions at startup, with the docstrings as fallback.
- Then ask us for one rule we want to add to the system prompt (suggest: "When a signed contract and a policy
  disagree, quote the contract clause number."), create it as a new version labeled "staging", and run Q01
  with both labels. Show us both traces with their prompt versions.
```

## Team discussion

- Who should be allowed to promote staging to production? (Protected labels need an Enterprise key on
  self-hosted — what do we do instead?)
- Open a trace in the Playground and edit the prompt live. What would you test?

## Gate

Both versions exist, each trace shows its prompt version, and the agent works without Langfuse.

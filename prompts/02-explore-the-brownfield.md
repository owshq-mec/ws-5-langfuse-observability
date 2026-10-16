# 02 — Explore the brownfield

**Facilitator:** the stack is already up (`make ps`). This prompt maps the brief to the code and lets the
team watch the system work and see what is missing. Keep the Langfuse UI open on the projector: it is
empty, and that is the point.

## Prompt

```text
Map the case study to the repository, then show us the system working. Do not change code.

1. Map: for each component in the architecture section of the brief, give the folder and the main
   file/function (ingest, ontology, graph, retrieval, MCP server, agent). One table.
2. Health: run `make ps` and check that Neo4j, helix-mcp and Langfuse are healthy. Call
   http://localhost:3000/api/public/health.
3. The graph: count Entity nodes and RELATES_TO edges for group_id 'orbisa' with cypher-shell inside the
   Neo4j container. Show us 5 facts about Orion Freight Systems with their valid_at / invalid_at.
4. The tools: with the `mcp` Python client (`from mcp import Client`, URL http://127.0.0.1:8765/mcp), call
   search_context("who approves refunds") with as_of 2025-12-01 and again with 2026-10-15. Explain the
   difference.
5. The agent: run `make ask Q=Q01` and compare its answer with the expected answer it prints.
6. Now list what we CANNOT see today: which facts the agent used, how long each step took, what a question
   costs, whether answers are correct across all 22 questions, what happens when someone edits the prompt.
   For each gap, point to the requirement or success criterion in the brief it blocks.
Then ask us which gap surprised us most.
```

## Team discussion

- Did Q01 come out right? How would we know if it was right for the wrong reason?
- The Langfuse project is empty. What is the first thing you want to see in it?

## Gate

Everyone has seen the system answer a question, and the gap list is on the board.

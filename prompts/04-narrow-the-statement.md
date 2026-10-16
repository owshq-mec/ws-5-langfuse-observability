# 04 — Narrow the statement

**Facilitator:** a selected statement is still too wide to build in a few hours. This prompt narrows it
until it is testable. Push the team to choose numbers for the success criteria.

## Prompt

```text
We selected this problem statement:

  <paste the statement the team voted for>

Help us narrow it. Ask us, one at a time, and wait for each answer:
1. For whom exactly (one primary user from the brief)?
2. Which questions are in scope? Propose a subset of the 22 ground-truth categories and say why.
3. What does success look like? Propose 3–5 measurable criteria with a target and a measurement method
   (for example "correctness ≥ 0.8 on temporal questions, measured by an LLM judge on the dataset").
4. What are the constraints from the brief we must respect (self-hosted, no customer data leaves, the agent
   keeps working without Langfuse)?
5. What is explicitly out of scope today?

Then write decisions/01-problem-statement.md with: the final statement, primary user, scope, success
criteria (table: criterion, target, how measured), constraints, out of scope, and open risks.
Show us the file and ask if anything should change.
```

## Team discussion

- Is every success criterion something Langfuse can actually measure? If not, what would?
- Which criterion would fail today? (That is the one to show at the readout.)

## Gate

`decisions/01-problem-statement.md` exists and the team agrees with every line.

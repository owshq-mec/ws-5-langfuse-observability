# 13 — Readout

**Facilitator:** close the loop against the team's own success criteria, not against the tool list.

## Prompt

```text
Write decisions/03-readout.md for the CTO:
1. The problem statement we chose (from decisions/01-problem-statement.md).
2. For each success criterion: target, measured value, pass/fail, and the Langfuse link or command that
   proves it. Pull the numbers from Langfuse (experiment runs, scores, the Metrics API report and the compare
   command we built), don't estimate. For "every answer is traceable", check every trace of one full run
   through the API, not one example. Say how many runs each number is based on.
3. What we built, as a short list of increments with file paths.
4. What we learned about Helix itself (where it fails and why), with trace examples. Separate what we fixed,
   what we measured but did not fix, and what was a defect in our own measurement.
5. Risks and next steps, at most five, each with an owner role.
Keep it to one page. Show it to us and ask what we would change before we present it.
```

## Team discussion

- Which result would change a decision at Orbisa tomorrow?
- What would you monitor first if Ask Orbisa went live for all of Support?

## Gate

The team agrees the readout is true and could present it.

# 01 — Understand the brief

**Facilitator:** give the team five minutes with the PDF first (sections 1–4). Then run the prompt. Let
Claude quiz the room; resist answering for them.

## Prompt

```text
Read docs/orbisa-case-study.pdf completely. Then:
1. Summarize it for us in under 200 words: the company, the business problem, what already exists, and the
   mission.
2. Quiz us: ask three questions that check whether we really understood the problem (for example, why the
   Orion answer depends on a date). Wait for our answers and correct us where we are wrong, quoting the
   section and page.
3. List the open questions the brief does not answer, the ones we would ask the CTO on day one.
   Mark each as "blocks us" or "nice to know".
Do not change any file.
```

## Team discussion

- Which of the four failure modes (stale, conflict, alias, missing) would hurt Orbisa most, and why?
- What does "prove it works" mean to Tomás (RevOps)? To Ken (Support)? To the CTO?
- Which open question would you escalate first?

## Gate

The team can explain the Orion case in one sentence, and agrees on the top three open questions.

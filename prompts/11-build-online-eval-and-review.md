# 11 — Build: online evaluation and human review

**Facilitator:** offline experiments cover the questions we thought of. Online evaluation covers what people
actually ask. Let the team type real questions.

## Prompt

```text
Build increment 6. Plan first, wait for go.

1. Make the agent observation carry what a judge needs: in its metadata, a compact list of the facts and
   source paths Helix returned during the run.
2. src/observability/monitoring/setup.py, using the Langfuse public API where an endpoint exists (check
   first; print exact UI steps where it does not):
   - an LLM connection for Anthropic in the project, using ANTHROPIC_API_KEY (the worker calls the
     provider);
   - score configs: correctness (categorical), faithfulness (0–1);
   - an annotation queue "orbisa-review" with those score configs.
3. Give us the UI checklist to create:
   - an LLM-as-a-judge evaluator "faithfulness" on observations named like our agent observation: is
     every claim in the output supported by the facts in metadata? Sampling 100% today;
   - a code evaluator "has-sources-line". Code evaluators on self-hosted run TypeScript/JavaScript only.
4. Ask us for 5 questions to type (mix normal ones and traps: the Platinum plan, "who approved Orion's
   refund"). Run them, wait for the scores, and add the lowest-scoring traces to "orbisa-review".
```

## Team discussion

- Review one queued trace together and score it. Did the judge agree with you?
- Turn one reviewed trace into a new dataset item. Why is that the most valuable click of the day?

## Gate

Live answers get scores automatically, the queue has reviewed items, and one became a dataset item.

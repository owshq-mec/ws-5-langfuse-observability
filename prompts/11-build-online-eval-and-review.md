# 11 — Build: online evaluation and human review

**Facilitator:** offline experiments cover the questions we thought of. Online evaluation covers what people
actually ask. Let the team type real questions.

## Prompt

```text
Build increment 6. Plan first, wait for go.

1. Check that the agent observation carries what a judge needs: question and as-of in its input, the answer
   in its output, and in its metadata the compact list of facts (helix_facts) and the documents read
   (helix_sources_read) from increment 5.
2. src/observability/monitoring/setup.py, idempotent, using the Langfuse public API. Check the installed SDK
   (.venv/.../langfuse/api) and the API reference first: in Langfuse v4.63 these all have endpoints.
   - an LLM connection for Anthropic in the project, using ANTHROPIC_API_KEY (the worker calls the provider);
   - score configs: correctness (categorical), faithfulness (numeric 0–1), has_sources_line (boolean);
   - an annotation queue "orbisa-review" with those score configs;
   - an LLM-as-a-judge evaluator "faithfulness" (model claude-sonnet-5-5): is every claim in the output
     supported by the facts in metadata? Map the prompt variables to input, output and metadata JSONPaths;
   - a code evaluator "has-sources-line" (TypeScript; code evaluators on self-hosted run TypeScript/JavaScript
     only with the insecure-local dispatcher already set in compose);
   - one evaluation rule that runs both on observations named like our agent observation in the workshop
     environment, sampling 100%.
   If an SDK request model fails validation, show us the error before working around it.
3. Ask us for 5 questions to type (mix normal ones and traps: the Platinum plan, "who approved Orion's
   refund"). Run them in one session, wait for the scores, and add the lowest-scoring traces to
   "orbisa-review" (src/observability/monitoring/review.py).
4. Review one queued trace with us: show the answer and the judge's comment, record our verdict as a
   correctness score, mark the queue item done, and turn the trace into a dataset item in a separate dataset
   "orbisa-reviewed" (keep the 22-question ground truth comparable).
```

## Team discussion

- Review one queued trace together and score it. Did the judge agree with you?
- Turn one reviewed trace into a new dataset item. Why is that the most valuable click of the day?

## Gate

Live answers get scores automatically, the queue has reviewed items, and one became a dataset item.

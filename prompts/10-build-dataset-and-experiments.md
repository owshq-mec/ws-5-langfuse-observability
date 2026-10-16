# 10 — Build: ground truth and experiments

**Facilitator:** this is where "prove it works" becomes a number. Run a subset live; the full set costs more
time and money.

## Prompt

```text
Build increment 5. Plan first, wait for go.

1. Dataset: src/observability/datasets/load_truth.py creates "orbisa-truth" and upserts one item per line of
   data/orbisa/truth/questions.jsonl, with the question id (Q01…) as item id. input {question, as_of},
   expected_output {answer, facts, sources}, metadata {id, category, trap}. Re-running must not duplicate.
2. Evaluators, mapped to the success criteria in decisions/01-problem-statement.md:
   - code (no LLM): source_recall (expected sources found in the answer's "Sources:" line or in the tool
     results), has_sources_line, abstained (for false_premise items);
   - LLM-as-a-judge in Python with the Anthropic SDK, model claude-sonnet-5-5, structured output: correctness
     correct / partially_correct / incorrect (1 / 0.5 / 0) with a reason. The judge gets the as-of date and
     the expected facts, and for temporal and conflict items checks that the answer uses the fact valid on
     that date.
3. src/observability/experiments/run.py with the v4 experiment runner (langfuse.com/docs/evaluation/
   experiments/experiments-via-sdk.md): task = ask(question, as_of); item evaluators above; run evaluators:
   mean correctness overall and per category, mean source_recall, cost per correct answer. Flags: --name,
   --prompt-label, --ids, --max-concurrency 2.
4. Ask us which subset to run. Suggest Q01,Q02,Q07,Q08,Q13,Q14. Run it with --prompt-label production and
   with staging, then show both summaries and the items whose score changed.
```

## Team discussion

- Compare the numbers to the targets in our problem statement. Which criterion passes, which fails?
- Do you trust the judge? Open two judge traces and check its reasoning.

## Gate

Two experiment runs on "orbisa-truth" with item scores and run-level scores, compared in the UI.

# 10 — Build: ground truth and experiments

**Facilitator:** this is where "prove it works" becomes a number. A full run of all 22 questions takes about
5 minutes and costs about USD 2.20 (agent) plus USD 0.30 (judge); run the full set, a subset hides categories.

## Prompt

```text
Build increment 5. Plan first, wait for go.

1. Dataset: src/observability/datasets/load_truth.py creates "orbisa-truth" and upserts one item per line of
   data/orbisa/truth/questions.jsonl, with the question id (Q01…) as item id. input {question, as_of},
   expected_output {answer, facts, sources}, metadata {id, category, trap}. Re-running must not duplicate.
2. The agent must record what Helix returned: in the runner, read the tool results from the message stream
   and keep a compact list of facts (text, status, source paths) and the source paths retrieved and read.
3. Evaluators, mapped to the success criteria in decisions/01-problem-statement.md:
   - code (no LLM): source_recall (expected sources found in the answer's "Sources:" line or in the tool
     results), has_sources_line, abstained (for false_premise items). Before you trust source_recall,
     compare the expected source paths with the paths Helix can actually serve (list_sources) and with the
     as-of date of each item. Tell us what you find; never change the ground truth.
   - LLM-as-a-judge in Python with the Anthropic SDK, model claude-sonnet-5-5, structured output
     (client.messages.parse with a Pydantic model): correctness correct / partially_correct / incorrect
     (1 / 0.5 / 0) with a reason. The judge gets the as-of date, the expected facts and the trap, and for
     temporal and conflict items checks that the answer uses the fact valid on that date. Trace the judge as
     an evaluator observation.
4. Check the judge before we trust it: src/observability/evaluators/calibrate.py grades every expected answer
   (must be correct) and a trap answer written by claude-haiku-5-5 (must not be correct). Report agreement.
5. src/observability/experiments/run.py with the v4 experiment runner (langfuse.com/docs/evaluation/
   experiments/experiments-via-sdk.md): task = ask(question, as_of); item evaluators above; run evaluators:
   mean correctness overall and per category, mean source_recall, mean cost, cost per correct answer, p95
   latency. Flags: --name, --prompt-label, --ids, --max-concurrency, --model. Write a JSON summary.
6. Run all 22 with --prompt-label production and with staging, then show both summaries and the items whose
   score changed. The agent is not deterministic: tell us how much one run differs from the next before we
   call anything better or worse.
```

## Team discussion

- Compare the numbers to the targets in our problem statement. Which criterion passes, which fails?
- Do you trust the judge? Open two judge traces and check its reasoning.
- If correctness is already at the ceiling, which score can still tell two prompt versions apart?

## Gate

Two experiment runs on "orbisa-truth" with item scores and run-level scores, compared in the UI.

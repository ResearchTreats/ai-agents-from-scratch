# Lesson 09 quiz

Answer first, then open the answer.

## Before you start

**Q1. What are the three evaluation layers the lesson names?**

- A. Unit, integration, end-to-end
- B. Smoke, regression, acceptance
- C. Pre, check, post
- D. Static benchmarks, custom offline evals, online production evals

<details><summary>Answer</summary>

**D** - Static (SWE-bench, GAIA), custom offline (LLM-judge, exec, trajectory), online (replays, alerts, cost/latency).

</details>

**Q2. What is Anthropic's recommended starting point?**

- A. Start with multi-agent debate
- B. Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when needed
- C. Start with a frontier model only
- D. Start with hierarchical orchestration

<details><summary>Answer</summary>

**B** - Anthropic explicitly says evaluation is the outer loop that drives every other choice.

</details>

## Check yourself

**Q3. What is the evaluator-optimizer tight loop?**

- A. Proposer generates output, evaluator judges, refine until evaluator passes (Self-Refine generalized)
- B. Sample, sort, deduplicate
- C. Cache, retry, fail
- D. Train, evaluate, deploy

<details><summary>Answer</summary>

**A** - It is Self-Refine generalized: any flow can wrap in propose-judge-refine.

</details>

**Q4. What is the 2026 best practice for where evals live?**

- A. Owned exclusively by the QA team
- B. Only run quarterly
- C. Next to code, run in CI on every PR, gate merges on eval scores
- D. In a separate vendor dashboard only

<details><summary>Answer</summary>

**C** - Co-located with code, CI-gated, regression-tracked is the standard.

</details>

**Q5. Why does the lesson warn against an LLM-judge without grounding?**

- A. It violates Apache 2.0
- B. Judges hallucinate too; pair with the CRITIC pattern so judgment grounds on external tools
- C. It is too slow
- D. It only works on GPUs

<details><summary>Answer</summary>

**B** - CRITIC (Lesson 5) applies: tool-grounded verification keeps the judge honest.

</details>

**Q8. Lesson 8's guard.py stopped an injected refund with GuardedToolBox.check() — plain code, not a better prompt — because the model can't reliably police itself. In evals.py, why does the 'honest' check use claims_success_it_did_not_do(result) instead of asking the ScriptedBrain whether it thinks it succeeded?**

- A. The function runs faster than a prompt would
- B. Because a claimed-success hallucination is exactly the kind of thing a model can't be trusted to self-report — the function inspects the actual trace for a refund that really worked, the same structural-fix principle as check() in lesson 8
- C. ScriptedBrain has no way to answer questions
- D. The function and self-report always agree, so it doesn't matter

<details><summary>Answer</summary>

**B** - Same structural-fix principle as lesson 8: you don't ask the thing you don't trust to grade itself. claims_success_it_did_not_do reads the real trace for a refund that worked, not the model's claim about it.

</details>

## After the lesson

**Q6. What is the danger of over-fitting to evals?**

- A. Vector indices fragment
- B. Compute cost rises
- C. Latency drops too far
- D. Optimizing for the eval set diverges from production usefulness; rotate cases

<details><summary>Answer</summary>

**D** - Eval set rotation keeps the optimization aligned with production reality.

</details>

**Q7. Why do flaky evals cause problems?**

- A. They exceed the context window
- B. They cannot reach the database
- C. They double inference cost
- D. Non-deterministic cases produce false alarms; pin seeds and snapshot state

<details><summary>Answer</summary>

**D** - Flake makes regressions unreadable; determinism (seeds, state snapshots) is required.

</details>

# Lesson 01 quiz

Answer first, then open the answer.

## Before you start

**Q1. Why does an LLM on its own behave like an autocomplete rather than an agent?**

- A. It cannot read files, run queries, or verify claims against the outside world
- B. Its context window is too small to hold a question
- C. It only emits one token at a time
- D. It refuses to answer without a system prompt

<details><summary>Answer</summary>

**A** - An LLM with no loop and no tools can only produce text from its weights; it cannot observe state or act on it.

</details>

**Q2. Which three labels appear in the canonical ReAct trace from Yao et al. 2022?**

- A. Prompt, Response, Reward
- B. Plan, Execute, Reflect
- C. Thought, Action, Observation
- D. System, User, Assistant

<details><summary>Answer</summary>

**C** - ReAct interleaves Thought, Action, and Observation lines in a single stream.

</details>

## Check yourself

**Q3. Which item is NOT one of the five ingredients the lesson lists for an agent loop?**

- A. Tool registry
- B. Message buffer
- C. Observation formatter
- D. Gradient optimizer

<details><summary>Answer</summary>

**D** - The five ingredients are message buffer, tool registry, stop condition, turn budget, and observation formatter. Gradient optimizers belong to training, not the inference loop.

</details>

**Q4. What is the role of a turn budget in the loop?**

- A. It controls how many tools the registry exposes
- B. It rate-limits the LLM provider
- C. It hard-caps loop iterations to prevent runaway agents
- D. It caps the number of tokens per response

<details><summary>Answer</summary>

**C** - Turn budget is a cap on loop iterations; 2026 agents commonly run 40-400 steps and need a task-appropriate cap.

</details>

**Q8. In agent.py's run_agent, what makes the loop return an answer instead of continuing to the next turn?**

- A. parse() returns "final" because the brain's reply contains "Final Answer:"
- B. The tool registry raises a StopIteration
- C. The messages list reaches its maximum length
- D. The ticket's id starts with the letter T

<details><summary>Answer</summary>

**A** - run_agent calls parse(reply); when the reply contains "Final Answer:", parse returns ("final", value) and run_agent immediately returns {"stopped": "final", ...} no matter how many turns are left in max_turns.

</details>

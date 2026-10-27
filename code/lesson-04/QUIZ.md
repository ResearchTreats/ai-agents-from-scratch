# Lesson 04 quiz

Answer first, then open the answer.

## Before you start

**Q1. What signal does Toolformer use to decide whether to keep a candidate tool annotation?**

- A. Whether the tool returns within 100 ms
- B. Human label agreement
- C. Whether including the tool result reduces next-token loss on surrounding text
- D. Whether the tool emits valid JSON

<details><summary>Answer</summary>

**C** - Toolformer's self-supervised signal keeps annotations whose tool results lower next-token loss.

</details>

**Q2. What is the BFCL V4 split that the lesson reports?**

- A. 100% single-turn
- B. 50% live, 50% synthetic
- C. 33% agentic, 33% planning, 33% reflection
- D. 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination

<details><summary>Answer</summary>

**D** - BFCL V4 weights are 40 agentic / 30 multi-turn / 10 live / 10 non-live / 10 hallucination.

</details>

## Check yourself

**Q3. Why is a tool's description load-bearing?**

- A. It is what the user sees in the UI
- B. The model reads it to choose the right tool; bad descriptions are the top cause of wrong-tool failures
- C. It is required by JSON Schema
- D. It controls billing buckets

<details><summary>Answer</summary>

**B** - Tool descriptions are the model's primary signal for tool selection; poor descriptions cause wrong-tool routing.

</details>

**Q4. What role does tool_use_id play in parallel tool calling?**

- A. It correlates each tool result with its originating call so results returning out of order route correctly
- B. It authorizes the call against an API key
- C. It compresses the JSON payload
- D. It enables caching

<details><summary>Answer</summary>

**A** - tool_use_id is the correlation token; swapping them routes results to the wrong call.

</details>

**Q5. Which class of failure does V3 state-based evaluation try to catch?**

- A. Token leakage
- B. Schema versioning drift
- C. Slow tool execution
- D. AST-matching tool calls that look right but leave the API in the wrong state

<details><summary>Answer</summary>

**D** - State-based evaluation checks the resulting API state (e.g. file actually created) rather than syntactic call matching.

</details>

**Q8. coerce({'amount': 'lots'}, refund) is called on a schema where amount must be a number. What does it return, and why?**

- A. {'amount': 'lots'} unchanged - float('lots') raises ValueError, which coerce() catches and leaves the original string alone
- B. {'amount': 0} - coerce() falls back to zero when conversion fails
- C. {} - coerce() drops any argument it can't convert
- D. {'amount': 'lots'} unchanged, but only because 'amount' isn't declared in schema['properties']

<details><summary>Answer</summary>

**A** - coerce() only rewrites a value when int(value) or float(value) succeeds; 'lots' raises ValueError inside the try block, which is caught and does nothing, so the original string passes through untouched for validate() to reject next.

</details>

**Q9. Lesson 3's lint_tool flagged a description for not literally containing the words 'Use when', even when it read fine to a person. This lesson's validate(args, schema) checks a tool's params against the arguments a call actually sends. Does validate() care whether refund's description contains 'Use when'?**

- A. No - validate() only reads schema['properties'], schema['required'] and each property's type/enum; it never looks at a tool's description at all
- B. Yes - validate() rejects any tool whose description fails lint_tool's pattern
- C. No, but only because refund's description already happens to pass lint_tool
- D. Yes - validate() and lint_tool share the same 'Use when' check

<details><summary>Answer</summary>

**A** - validate() and lint_tool check completely different things: lint_tool audits how a tool is documented before it's ever called, while validate() only inspects the JSON Schema shape of a real call's arguments - description text never enters validate()'s logic.

</details>

## After the lesson

**Q6. Which 2026 problem does the lesson NOT list among the open ones for function calling?**

- A. Long-horizon tool chaining
- B. Token-level decoding speed
- C. Dynamic decision-making across many tools
- D. Memory across turns

<details><summary>Answer</summary>

**B** - The open problems are memory, dynamic decision-making, long-horizon chains, and hallucination detection; decoding speed is not on the list.

</details>

**Q7. Why is a generic run_shell(cmd) tool called a red flag in this lesson?**

- A. It cannot be called in parallel
- B. It widens the sandbox boundary; specific tools like git_status() bound read/write surface and risk
- C. It is slow
- D. Providers reject it

<details><summary>Answer</summary>

**B** - Narrow tools constrain the sandbox surface; a generic shell tool grants the full surface of the host.

</details>

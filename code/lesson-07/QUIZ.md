# Lesson 07 quiz

Answer first, then open the answer.

## Before you start

**Q1. In OllamaBrain.reply, what part of the request body lets the model call the helpdesk tools?**

- A. The "tools" list, one function definition per tool in the toolbox
- B. The model name, because qwen2.5:3b has the tools built in
- C. The "stream": false setting
- D. The seed in the options

<details><summary>Answer</summary>

**A** - OllamaBrain builds {'type': 'function', 'function': schema} for every tool in the box and sends that list as "tools". The model can only call tools it has been given definitions for.

</details>

## Check yourself

**Q2. Ollama replies with a message holding tool_calls for lookup_order with order_id A17. What does OllamaBrain.reply return to the agent loop?**

- A. The raw JSON message from Ollama
- B. The line: Action: lookup_order {"order_id": "A17"}
- C. The line: Final Answer: lookup_order
- D. A Python function object for lookup_order

<details><summary>Answer</summary>

**B** - reply joins one 'Action: name json-arguments' line per tool call. The loop already parses lines in that format, so it needs no change.

</details>

**Q3. In the real run of python ollama_brain.py, which ticket finished without calling any tool?**

- A. T1 and T6
- B. T2 and T4
- C. T5, the vague ticket
- D. None. Every ticket called a tool

<details><summary>Answer</summary>

**C** - T5 prints an empty tool list: the model answered it directly. T1 and T6 called lookup_order and T2 and T4 called refund. T3, the app crash, is borderline: the model sometimes calls search_help for it and sometimes answers directly. All six stopped 'final', so the question to ask is whether each answer was right.

</details>

**Q6. Lesson 6's mcp_tools gave the agent loop plain local functions. What does this lesson's OllamaBrain likewise leave unchanged?**

- A. The run_agent loop, which still gets Action or Final Answer text from its brain
- B. The tools, which now run inside Ollama
- C. The model, which is still the scripted brain
- D. The history format, which Ollama reads directly without translation

<details><summary>Answer</summary>

**A** - Both swaps keep the loop's interface. Lesson 6 changed where tools run. This lesson changes who writes the replies, and to_ollama and reply translate at the edge so run_agent never changes.

</details>

## After the lesson

**Q4. What changed in the 2025-2026 native-reasoning shift compared with prompt-based Thought tokens?**

- A. The model stopped reasoning and only calls tools
- B. Reasoning is written as 'Thought:' lines inside the reply text
- C. Reasoning arrives on its own channel, separate from the answer text, and is passed back across turns
- D. Reasoning must be stripped before any tool can run

<details><summary>Answer</summary>

**C** - With prompt-based Thought tokens the reasoning is ordinary reply text. With native reasoning the model returns it in a separate field, so the content, the tool calls and the reasoning can each be handled separately.

</details>

**Q5. Why can this lesson claim that modern agent frameworks still run the same loop under the hood?**

- A. They all call this course's run_agent function
- B. Each one still calls a model, runs the tools it asks for, feeds the results back and stops on a final answer or a budget
- C. They avoid tool calls entirely
- D. They only differ in which API key they use

<details><summary>Answer</summary>

**B** - run_agent does exactly that: ask the brain, run the requested tools, append the observations, repeat until a final answer or the turn budget. Swapping the brain for a local model left it untouched, and the frameworks add structure around the same loop.

</details>

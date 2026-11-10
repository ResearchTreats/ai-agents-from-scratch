# Lesson 11 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

You already have everything you need in memory.py - MainContext holds an `archive` attribute, and Archive has `.add(text)` and `.search(query)`. In exercise_11.py, write a function `memory_tools(context)` that builds a ToolBox (same tools.py pattern from lessons 2 and 3) and registers two tools on it: `remember` and `recall`.

</details>

<details><summary>Hint 2</summary>

`remember` should take a `fact` argument, call `context.archive.add(fact)`, and return the exact string 'remembered' so `box.run("remember", {"fact": ...})` matches test_exercise_11.py. `recall` should take a `query` argument, call `context.recall(query)` (which forwards to `context.archive.search(query)`), and join any results with ' | ' - but when nothing matches, return the exact string 'nothing remembered about that', not an empty list.

</details>

<details><summary>Hint 3</summary>

Give each Tool a name, a description with 'Use when...' and 'Do not use...' guidance (schema_lint's lint_box, imported in the test, checks for exactly that), a JSON Schema with a `required` list and a `text_param(...)` for each parameter, and the function itself - `box.add(Tool("remember", "Use when the customer states a lasting fact or preference. Do not use for order details.", {"type": "object", "required": ["fact"], "properties": {"fact": text_param("The fact, in one sentence")}}, remember))`, then the matching Tool for `recall` with a `query` parameter, and return the finished box from memory_tools().

</details>

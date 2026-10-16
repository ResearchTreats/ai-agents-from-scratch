# Lesson 01 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Look at what happens when parse() in agent.py hits an Action line whose JSON is broken, like `{"order_id": A17}` with no quotes around A17 — json.loads raises a json.JSONDecodeError, and nothing in run_agent catches it. Your run_agent_safely in exercise_01.py needs to catch that instead of letting it crash the ticket.

</details>

<details><summary>Hint 2</summary>

Copy run_agent's loop into run_agent_safely and wrap just the `kind, value = parse(reply)` line in a try/except for json.JSONDecodeError. On failure, don't crash and don't skip silently — build an observation string that starts with "error: the Action arguments are not valid JSON", append it to trace and to messages as a tool-role message, then continue to the next turn instead of returning.

</details>

<details><summary>Hint 3</summary>

Inside the except block: `observation = f"error: the Action arguments are not valid JSON ({exc.msg}). Reply again with valid JSON."`, then `trace.append({"tool": None, "args": {}, "observation": observation})`, then `messages.append({"role": "tool", "content": f"Observation: {observation}"})`, then `continue`. Leave every other line of run_agent unchanged — test_exercise_01.py's BROKEN_THEN_FIXED reply list hands the brain a corrected, valid-JSON line right after the broken one, so the very next turn calls lookup_order for real and reaches 'Final Answer: Order A17 shipped with UPS.'

</details>

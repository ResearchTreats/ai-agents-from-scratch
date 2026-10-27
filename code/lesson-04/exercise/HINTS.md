# Lesson 04 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

call_all already runs every call it's given - call_all_capped in exercise_04.py just needs to slice that list before any of it reaches call_all, so only the allowed number of calls ever runs.

</details>

<details><summary>Hint 2</summary>

Call call_all(box, calls[:max_calls]) to get real results for the calls under the cap, then loop over the remaining calls in calls[max_calls:] and build an error result dict for each one yourself, in the same shape call_all uses: id, tool, observation.

</details>

<details><summary>Hint 3</summary>

Number the overflow calls starting from max_calls + 1 with enumerate(calls[max_calls:], start=max_calls + 1), and give each one an observation string starting with f"error: only {max_calls} tool calls are allowed per turn" so test_calls_over_the_cap_are_refused_not_dropped's check on results[2]['observation'].startswith(...) passes - then append each of those dicts onto the list call_all already gave you.

</details>

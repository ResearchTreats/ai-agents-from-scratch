# Lesson 09 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Open exercise_09.py — you're writing one function, regression_gate(results, path), that turns run_suite's results list into a pass/fail decision by comparing against a saved rate, like gate() but with memory across runs instead of a fixed threshold.

</details>

<details><summary>Hint 2</summary>

Compute rate the same way gate() does — sum(r['passed'] for r in results) / len(results). Then check whether path (wrap it in Path(path)) already holds a saved rate: if it exists, read its JSON and compare your new rate against the saved one; if this is the first run, there's nothing to compare against yet, so it should pass.

</details>

<details><summary>Hint 3</summary>

Read the old rate with json.loads(path.read_text(encoding='utf-8'))['rate'] if path.exists() else 0.0. Return False as soon as rate < best. Otherwise write {'rate': rate} back with path.write_text(json.dumps(...), encoding='utf-8') and return True — that's exactly what test_exercise_09.py's three tests check: a first run always sets the baseline, a drop below the last saved rate fails, and holding or improving passes.

</details>

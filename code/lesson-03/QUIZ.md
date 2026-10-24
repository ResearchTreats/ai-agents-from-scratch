# Lesson 03 quiz

Answer first, then open the answer.

## Before you start

**Q1. Before you write any code: a tool named doStuff has the description 'Does stuff.' and sits in a registry next to 29 other tools. When a user asks something doStuff could technically handle, what actually happens?**

- A. The model has almost no signal to disambiguate doStuff from the other 29 tools, so it may pick doStuff for the wrong request, or skip it for the right one
- B. Nothing changes, since the model calls tools by their underlying function, not by reading the description
- C. The model always defaults to the shortest description when it's unsure
- D. doStuff will only ever be called if the user types the words 'does stuff'

<details><summary>Answer</summary>

**A** - A model picks a tool by reading its description at selection time - a description this vague gives it nothing to disambiguate against 29 competitors, which is exactly why the source measured 10-20 point accuracy swings from description quality alone.

</details>

## Check yourself

**Q2. A tool's description reads: 'Looks up a customer's order history and account details for support purposes.' What will lint_tool report about it, and why?**

- A. Two findings - it doesn't start with the literal words 'Use when' and it never says 'Do not use', even though the sentence reads fine to a person
- B. No findings, since the description clearly explains what the tool does
- C. One finding, because it's over the 1024 character limit
- D. Three findings, because the tool's name isn't shown in the description

<details><summary>Answer</summary>

**A** - lint_tool checks tool.description.startswith('Use when') and whether 'Do not use' appears anywhere in it, as literal strings - a well-written sentence that skips those exact words still fails both checks, which is the point of writing the pattern as code instead of trusting good prose.

</details>

**Q3. get_weather_for_tokyo would pass lint_tool's SNAKE_CASE = re.compile(r'^[a-z][a-z0-9_]*$') check with zero findings. Does that mean it's a well-named tool by this lesson's own naming rules?**

- A. No - the source's naming rules also say never bake a specific argument value like a city into the tool's name, but lint_tool's regex only checks character shape, not whether a name embeds an argument
- B. Yes, since passing lint_tool is the definitive test for a good tool name
- C. No, because the regex would actually reject this name for having too many underscores
- D. Yes, as long as the underlying function only takes one argument

<details><summary>Answer</summary>

**A** - SNAKE_CASE only tests character shape - lowercase letters, digits and underscores - so a name like get_weather_for_tokyo passes it cleanly even though it violates the 'no arguments in the name' rule from the source lesson; the linter built here doesn't check for that, which is worth noticing rather than assuming a clean lint_tool result means a name is flawless.

</details>

**Q4. test_helpdesk_tools_are_clean() asserts all(problems == [] for problems in lint_box(helpdesk_tools()).values()). What would make this test fail?**

- A. If any single one of the four helpdesk tools' name, description, or parameter specs stopped matching one of lint_tool's rules - lint_box runs lint_tool across the whole registry, so one bad tool anywhere fails the assertion
- B. It can only fail if all four tools become invalid at the same time
- C. It never fails, since helpdesk_tools() is hard-coded to always pass
- D. It fails only if a new tool is added without calling lint_box on it first

<details><summary>Answer</summary>

**A** - lint_box just maps lint_tool over every tool in the box, so the all(...) check is exactly as strict as its weakest tool; breaking any one rule on any one of the four - say, deleting refund's 'Do not use' sentence - is enough to turn one of the four lists non-empty and fail the test.

</details>

**Q5. Lesson 2's ToolBox rejected every side-effecting tool by default unless approve said otherwise. This lesson's exercise adds get_refund_status, which only reads store.REFUNDS and returns a string. Does it need side_effect=True and an approval check the way refund does?**

- A. No - get_refund_status never mutates store state, so it's a pure tool; Tool defaults side_effect to False and it runs with no approval check at all
- B. Yes, because ToolBox.run requires approval for every tool call regardless of side_effect
- C. Yes, because reading from store.REFUNDS counts as a side effect
- D. No, but only because refund already used up its one approval for that order

<details><summary>Answer</summary>

**A** - The pure-versus-consequential split from lesson 2 still applies here: get_refund_status only reads store.REFUNDS and returns a formatted string, so it stays a pure tool with side_effect left at its default of False - the approval gate exists for tools like refund and cancel_order that change state, not for a status lookup.

</details>

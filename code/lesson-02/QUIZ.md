# Lesson 02 quiz

Answer first, then open the answer.

## Before you start

**Q1. Before you write any code: when a chatbot says 'I'll refund your $25,' what has actually happened to the customer's money?**

- A. Nothing yet - the model only produced a sentence; a refund only happens if a program calls a real refund function
- B. The chatbot's weights include a live connection to the payments system
- C. The refund happens as soon as the model outputs the word refund
- D. Refunds are impossible for a chatbot to describe

<details><summary>Answer</summary>

**A** - An LLM only emits tokens; until a host program executes a function against real state, nothing has changed - that gap is the entire point of a tool interface.

</details>

## Check yourself

**Q2. In Tool.schema(), which three pieces of information get sent to describe a tool to the model?**

- A. name, description, parameters (the JSON Schema)
- B. name, side_effect, fn
- C. description, fn, approve
- D. params, side_effect, get

<details><summary>Answer</summary>

**A** - schema() returns name, description, and parameters (self.params) - the executor function fn and the side_effect flag stay on the host and are never shown to the model.

</details>

**Q3. helpdesk_tools() is called with no approve argument. What happens when the agent tries to run refund?**

- A. ToolBox's default approve always returns False, so refund is rejected as needing approval - no money moves
- B. The refund runs immediately because refund is a pure tool
- C. ToolBox.run raises a NameError because approve was never defined
- D. The refund runs only for amounts under $100 by default

<details><summary>Answer</summary>

**A** - ToolBox.__init__ defaults approve to a lambda that always returns False, so every side-effecting tool is rejected until you pass a real approval function.

</details>

**Q4. Lesson 1's run_agent caps iterations with a turn budget so a stuck agent can't loop forever. In this lesson's demo, what actually stops T4's $500 refund from reaching store.REFUNDS - the turn budget or something else?**

- A. The approval check in ToolBox.run - the turn budget only bounds how many turns run, not what a tool is allowed to do
- B. The turn budget, because it runs out before the refund call is made
- C. Both equally: the turn budget and the approval check work together to reject exactly this call
- D. The ScriptedBrain refuses to type the ticket amount if it's too high

<details><summary>Answer</summary>

**A** - Turn budget and approval check guard two different failures: turn budget stops the loop from running forever; the approval check stops a single tool call from executing without permission. T4's refund is blocked by the approval check on its very first attempt, well inside the turn budget.

</details>

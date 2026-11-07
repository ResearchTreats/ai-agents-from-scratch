# Lesson 08 quiz

Answer first, then open the answer.

## Before you start

**Q1. What is indirect prompt injection?**

- A. A model misclick
- B. A user typing 'ignore all rules' directly
- C. Instructions embedded in data the agent retrieves (a page, PDF, email, memory note) that override the developer prompt on ingest
- D. A typo in the system prompt

<details><summary>Answer</summary>

**C** - Greshake et al. coined indirect prompt injection: attacker-controlled retrieved content carries instructions.

</details>

**Q2. What does the lesson say processing retrieved prompts is equivalent to?**

- A. A static analysis pass
- B. Arbitrary code execution on the agent's tool-use surface
- C. Free speech
- D. A pure function call

<details><summary>Answer</summary>

**B** - Greshake's framing: retrieved instructions can hit any tool the agent has access to.

</details>

## Check yourself

**Q3. Which is NOT one of the five demonstrated exploit classes?**

- A. Persistent memory poisoning
- B. Cache invalidation
- C. Data theft
- D. Worming

<details><summary>Answer</summary>

**B** - The five are data theft, worming, persistent memory poisoning, ecosystem contamination, arbitrary tool use.

</details>

**Q4. What does PVE stand for?**

- A. Pre-Vectorize-Embed
- B. Prompt-Validator-Executor: a cheap fast validator runs on each tool call before the expensive main model commits
- C. Provider-Verifier-Encoder
- D. Plan-Verify-Execute, an HTN dialect

<details><summary>Answer</summary>

**B** - PVE wraps every tool invocation with a cheap validator before main-model commit.

</details>

**Q5. Why is 'system prompt says ignore untrusted instructions' insufficient?**

- A. It is too short
- B. It is instruction-following, not enforcement; the model can still be overridden by sufficiently persuasive injected content
- C. Providers strip it
- D. It is encrypted

<details><summary>Answer</summary>

**B** - Real defense needs source tagging, allowlists, per-step safety, and PVE-style validation, not just prompting.

</details>

**Q8. Why does GuardedToolBox.run() call redact() on every tool result, including the order note returned by lookup_order — not just on side-effecting calls like refund?**

- A. Because redact() also compresses the output to save tokens
- B. Because any tool's return value is retrieved content the model didn't write and can't be trusted to be free of embedded instructions — that's exactly what puts '[removed: instruction-like text]' in place of the lookup carrying C35's poisoned note, before the agent ever reads it
- C. Because only read-only tools need redaction, not refund
- D. Because redact() only runs after check() has already blocked the call

<details><summary>Answer</summary>

**B** - run() redacts the result of every tool call, not just side-effecting ones, because any tool's return value — even a harmless-looking lookup_order note — is untrusted retrieved content that might carry injected instructions.

</details>

**Q9. Lesson 7's OllamaBrain.reply hands the agent loop an Action line, whatever the model decided. Why does guard.py stop the injected refund in GuardedToolBox.check() - ordinary Python code - instead of prompting the model to ignore instructions found in ticket text?**

- A. Because Python runs faster than a language model
- B. Because the failure is structural - the model can't reliably tell a customer's ticket text from a developer instruction - so the fix has to be a check that runs on the Action line whichever brain wrote it, not a better-worded prompt
- C. Because OllamaBrain doesn't support system prompts at all
- D. Because check() is shorter to write than a prompt

<details><summary>Answer</summary>

**B** - A design flaw isn't fixed by asking the model nicely. check() runs unconditionally before the refund tool does, so it stops the 500 dollar refund even when the model was fully persuaded by the injected text.

</details>

**Q10. A reworded ticket asks for the same 500 dollar refund, with none of the listed phrases. What happens in GuardedToolBox.run?**

- A. scan finds nothing, so the refund goes through
- B. scan finds nothing, but check still refuses it: 500 is larger than B22's total, and that rule reads the shop's data, not the ticket's words
- C. The model notices the rewording and refuses
- D. approve stops it, because approval always runs first

<details><summary>Answer</summary>

**B** - The filter only knows the words on its list. The amount rule compares the request with the shop's own data, so rewording the ticket changes nothing.

</details>

## After the lesson

**Q6. What is overtrust of retrieved memory?**

- A. Loading the wrong model
- B. Yesterday's agent wrote a poisoned memory note; today's agent reads it and re-executes the injection
- C. Forgetting to vacuum the index
- D. Caching too aggressively

<details><summary>Answer</summary>

**B** - Persistent memory poisoning means injections survive across sessions if memory is treated as trusted.

</details>

**Q7. What metadata does the lesson recommend attaching to every piece of content?**

- A. A token count
- B. A timestamp only
- C. An encryption key
- D. A source tag: user_message vs tool_output vs retrieved; validator refuses directives in retrieved content

<details><summary>Answer</summary>

**D** - Provenance tagging lets the validator treat content according to its trust level.

</details>

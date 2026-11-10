# Lesson 11 quiz

Answer first, then open the answer.

## Before you start

**Q1. What OS analogy does MemGPT build on?**

- A. Virtual memory: main context as RAM, external store as disk, memory tools as page in and out
- B. Processes and threads
- C. Network sockets
- D. File descriptors

<details><summary>Answer</summary>

**A** - MemGPT maps prompt to RAM, external store to disk, and memory tools to page-fault-style transfers.

</details>

**Q2. Why do bigger context windows not fully solve memory?**

- A. The model refuses long input
- B. Long context costs nothing
- C. Every turn pays for the whole window, and nothing carries over to the next session
- D. Providers cap them at 4k tokens

<details><summary>Answer</summary>

**C** - In the Mem0 paper, passing the whole conversation still scored highest (73% against 67%), but a memory tier cut p95 latency by 91% and token cost by more than 90%, and a window still empties when the session ends.

</details>

## Check yourself

**Q3. Which of these is NOT one of MemGPT's canonical memory tools?**

- A. archival_memory_search
- B. core_memory_append
- C. conversation_search
- D. gradient_memory_update

<details><summary>Answer</summary>

**D** - There is no gradient memory tool; the surface is core/archival/conversation operations.

</details>

**Q5. Which production system did MemGPT evolve into in 2024?**

- A. Pinecone
- B. Mem0
- C. Zep
- D. Letta

<details><summary>Answer</summary>

**D** - MemGPT became Letta in September 2024; the research repo cpacker/MemGPT still exists as the origin.

</details>

**Q8. test_core_facts_are_never_evicted builds a MainContext with cap=2, sets context.core['customer'], then calls context.add() 10 times. What happens to context.core?**

- A. It's unchanged - context.core is a separate dict from context.messages, and MainContext.add() only ever evicts from self.messages, never touches self.core
- B. It's cleared once the cap is exceeded
- C. It grows by one entry per evicted message
- D. It raises an error because the cap was exceeded

<details><summary>Answer</summary>

**A** - core and messages are two separate attributes. add() only pops from self.messages (oldest first) into the archive when the cap is exceeded; self.core is never read or written by add(), so a fact pinned there survives no matter how many messages cycle through.

</details>

**Q9. MainContext.add() runs: while len(self.messages) > self.cap: evicted = self.messages.pop(0); self.archive.add(evicted["content"]). Which message gets evicted first once the cap is exceeded?**

- A. The oldest message in self.messages (index 0), because pop(0) always removes the front of the list
- B. The newest message just added
- C. A random message
- D. The message with the fewest words in common with the others

<details><summary>Answer</summary>

**A** - self.messages.pop(0) removes index 0, the oldest surviving message, and hands its content straight to archive.add() - eviction is strict FIFO, oldest-first, the same rule lesson 12's history budget uses to decide what to drop.

</details>

**Q10. Lesson 7's OllamaBrain left the run_agent loop unchanged and re-sends the whole history on every turn. This lesson's MainContext.add() keeps only the newest `cap` messages. What does it do with a message it evicts?**

- A. Evicted messages are handed to archive.add() instead of being discarded, so a later recall() can still retrieve them
- B. It keeps the oldest messages instead of the newest
- C. It never evicts anything - it just grows without bound
- D. It summarizes every evicted message with an LLM before storing it

<details><summary>Answer</summary>

**A** - Simply cutting the list drops the oldest turns and they're gone. MainContext.add() also evicts oldest-first but routes the evicted content into self.archive, so recall('email or phone?') can still find 'Asha prefers a phone call, never email.' after it ages out of the visible window - that's the entire point of paging versus plain dropping.

</details>

## After the lesson

**Q7. Why does the lesson say production memory systems are MemGPT variants?**

- A. Letta, Mem0, Assistants threads, and Claude Agent SDK all run the two-tier (or more) paged-memory pattern; differences are operational shape
- B. They share weights
- C. They use the same vector DB
- D. MemGPT owns the trademark

<details><summary>Answer</summary>

**A** - Pick by operational shape, not pattern; all share the MemGPT page in/out skeleton.

</details>

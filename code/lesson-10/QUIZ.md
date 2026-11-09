# Lesson 10 quiz

Answer first, then open the answer.

## Before you start

**Q1. Which four orchestration patterns does the lesson list?**

- A. Push, pull, batch, stream
- B. Supervisor-worker, swarm/peer-to-peer, hierarchical, debate
- C. Sequential, parallel, distributed, federated
- D. Plan, act, reflect, refine

<details><summary>Answer</summary>

**B** - Supervisor-worker, swarm, hierarchical, and debate recur across 2026 frameworks.

</details>

**Q2. What does LangChain now recommend for supervision?**

- A. Always use create_supervisor
- B. Avoid supervision entirely
- C. Prefer direct tool calls over create_supervisor for finer context-engineering control
- D. Run supervisors on GPUs

<details><summary>Answer</summary>

**C** - Tool-call-based supervision gives you precise control over what each specialist sees.

</details>

## Check yourself

**Q3. What distinguishes a swarm from a supervisor-worker topology?**

- A. Swarm runs on cron only
- B. Swarm has no central router; agents hand off directly via a shared tool surface
- C. Swarm uses GPUs
- D. Swarm is single-agent

<details><summary>Answer</summary>

**B** - Swarm is peer-to-peer; supervisor centralizes routing through one LLM.

</details>

**Q4. When is hierarchical orchestration justified?**

- A. Never; it is an antipattern
- B. Only with GPUs
- C. When a single supervisor's context budget cannot hold descriptions of all specialists
- D. Always; it scales for free

<details><summary>Answer</summary>

**C** - Nested supervisors are for large specialist populations that exceed one supervisor's budget.

</details>

**Q5. What is the recommended decision order Anthropic supports?**

- A. Start with a single agent plus workflow patterns; add topology only when needed; supervisor before swarm before hierarchical; debate when accuracy beats cost
- B. Start with debate
- C. Always start with hierarchical multi-agent
- D. Start with swarm and contract toward single

<details><summary>Answer</summary>

**A** - Anthropic's guidance is to build the right system for your needs, not the most sophisticated.

</details>

**Q8. Which of these is NOT one of the three orchestration topologies this lesson names alongside debate?**

- A. Supervisor-worker
- B. Swarm / peer-to-peer
- C. Hierarchical
- D. Round-robin

<details><summary>Answer</summary>

**D** - Supervisor-worker, swarm and hierarchical are the three named topologies (plus debate, which is more verification than orchestration); round-robin never appears in this lesson or its sources.

</details>

**Q9. scoped(box, names) builds a new ToolBox and adds box.tools[name] for each name in names. Why does test_scoped_box_holds_only_its_tools call box.run('refund', ...) on a tech-scoped box instead of just checking list(box.tools)?**

- A. To prove the restriction is enforced at call time, not just declared - the tech box's tools dict never got a 'refund' key, so running it returns 'error: unknown tool' rather than merely being undocumented
- B. Because ToolBox.run always fails on tools starting with 'r'
- C. To measure how long the call takes
- D. Because refund requires an amount argument that tech tickets never provide

<details><summary>Answer</summary>

**A** - The test checks both: list(box.tools) == ['search_help'] shows what's declared, and box.run('refund', ...) proves what actually happens if something tries to call an excluded tool anyway.

</details>

**Q10. In Supervisor.handle, what happens when classify(ticket['text']) returns 'person'?**

- A. handle returns {'team': 'person', 'answer': None, 'stopped': 'escalated'} immediately, without calling scoped() or run_agent at all
- B. handle picks whichever team scored highest anyway, since max() always returns something
- C. handle raises an exception that the caller must catch
- D. handle retries classify with a lower threshold

<details><summary>Answer</summary>

**A** - The `if team == "person"` branch returns early with answer None and stopped 'escalated' - no specialist box is ever built for an unmatched ticket.

</details>

**Q11. Lesson 2's ToolBox refuses a side-effecting tool without approval, and answers an unknown tool with an error. Here, Supervisor.handle gives the tech team a ToolBox from scoped() that holds only search_help. What happens if the tech team's brain asks for refund?**

- A. run returns the unknown-tool error, because refund was never added to the scoped box, so the refund never runs
- B. The refund runs, because scoped() copies box.approve to the smaller box
- C. The refund waits for a person to approve it
- D. The supervisor re-routes the ticket to billing

<details><summary>Answer</summary>

**A** - scoped() only adds the tools named for that team, so to the tech box refund does not exist: run answers "error: unknown tool 'refund'. Tools: search_help". That is enforced at call time, not just declared in TEAMS.

</details>

## After the lesson

**Q6. What is fake hierarchy in this lesson?**

- A. Three layers of supervisors because 'enterprise' when there are only two actual teams; collapse it
- B. An orchestrator written in TypeScript
- C. Mislabelled YAML
- D. A test fixture

<details><summary>Answer</summary>

**A** - Layers that do not correspond to real teams add operational complexity without payoff.

</details>

**Q7. How do you mitigate bouncing handoffs in a swarm (A -> B -> A -> B)?**

- A. Pin the temperature to 0
- B. Lower the rate limit
- C. Add a hop counter and refuse after N transfers
- D. Disable tracing

<details><summary>Answer</summary>

**C** - A hop counter caps swarm cycles before they loop indefinitely.

</details>

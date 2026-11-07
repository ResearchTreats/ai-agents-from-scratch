# Lesson 08 key terms

- **Indirect prompt injection** - Instructions embedded in data the agent retrieves, like C35's order note
- **Direct prompt injection** - User-supplied prompt bypasses guardrails, like T4, a customer's own message to the agent
- **PVE** - Cheap fast validator before expensive main inference
- **Memory poisoning** - Injected content stored as memory; re-poisons next session
- **Agents Rule of Two** - An agent should have at most two of: untrusted input, private data or sensitive systems, and the power to change state or communicate. With all three, it needs supervision

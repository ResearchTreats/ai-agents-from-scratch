# Lesson 01 key terms

- **Agent** - A loop: LLM thinks, picks a tool, result feeds back, repeat until stop
- **ReAct** - Yao et al. 2022 — interleave Thought, Action, Observation in one stream
- **Tool call** - Structured output the runtime dispatches to an executable
- **Observation** - The string representation of tool output fed back into the next prompt
- **Stop condition** - Explicit `finish`, no tool calls emitted, max turns, max tokens, or guardrail trip
- **Turn budget** - Hard cap on loop iterations — agents run 40–400 steps per task in 2026
- **Trace** - Full record of thought, action, observation tuples for a run

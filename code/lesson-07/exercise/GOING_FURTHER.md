# Lesson 07: going further

Optional extensions, once the exercise passes.

1. Read the Claude Agent SDK overview (https://platform.claude.com/docs/en/agent-sdk/overview). For each part it describes (calling the model, running tools, feeding results back, stopping), point to the line in agent.py's run_agent that does the same job.
2. Pick a model from the Ollama library that supports thinking and send "think": true in OllamaBrain's request body. Print the reasoning field of the reply's message next to its content, and keep it out of the Action lines. Run one ticket and compare the transcript with the qwen2.5:3b run: where does the reasoning appear, and what did your code have to change?
3. Add coercion to the toolbox for a model that sends a number as a string ("49.99" or "3" where a float or int is expected). Run the tickets with a local model and list one case where coercing fixes a call and one where it would hide a real mistake. Where do you stop coercing?

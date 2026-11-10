# Lesson 11: going further

Optional extensions, once the exercise passes.

1. Extend Archive.search() to deduplicate its results: if two matching entries share more than 80% of their words, keep only the higher-scored one and drop the other.
2. OllamaBrain re-sends the whole history on every call. Give it a max_main_context_tokens cap, estimated as len(text.split()) * 1.3 over the messages to_ollama produces. When a ticket goes over the cap, fold the oldest messages after the system prompt into one summary message before sending, and keep each tool message with the tool call it answers. Run the same ticket with and without the cap and compare the replies.

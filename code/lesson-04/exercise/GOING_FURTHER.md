# Lesson 04: going further

Optional extensions, once the exercise passes.

1. Read OpenAI's function-calling guide top to bottom and find the one field on a tool definition that helpdesk_tools() in tools.py never sets: strict. Explain what strict: true buys you - the model's output is constrained to validate against the schema before it ever reaches you - and why validate() and coerce() in calling.py still have to do that check by hand instead of trusting it.

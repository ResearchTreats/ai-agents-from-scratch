# Lesson 02 key terms

- **Tool** - A triple of name + JSON-Schema-typed input + executor function
- **Pure tool** - No side effects; safe to re-run
- **Consequential tool** - Mutates external state; requires gate, audit, or user confirmation
- **Four-step loop** - describe → decide → execute → observe
- **Host** - The program that holds the tool registry, calls the model, and runs the executor

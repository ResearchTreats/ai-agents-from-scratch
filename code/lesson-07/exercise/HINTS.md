# Lesson 07 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Open ollama_brain.py and look at its demo block at the bottom. It resets the store, runs each ticket and checks result['stopped']. Your function does the same thing once per model name, keeping a count of tickets that stopped with 'final'.

</details>

<details><summary>Hint 2</summary>

Write compare_models(models, brain_for=...) in exercise_07.py. For each model, build a brain with brain_for(model), reset the store before every ticket with store.reset(), and call run_agent(t, brain, box) with t from TICKETS and a box from helpdesk_tools(). Save finished / len(TICKETS) in a dict under the model's name. The default brain_for should build OllamaBrain(helpdesk_tools(), model=model).

</details>

<details><summary>Hint 3</summary>

Imports: store, run_agent from agent, OllamaBrain from ollama_brain, TICKETS from tickets, helpdesk_tools from tools. Then:

def compare_models(
    models,
    brain_for=lambda model: OllamaBrain(helpdesk_tools(), model=model),
):
    rates = {}
    for model in models:
        box, brain, finished = helpdesk_tools(), brain_for(model), 0
        for t in TICKETS:
            store.reset()
            finished += run_agent(t, brain, box)["stopped"] == "final"
        rates[model] = finished / len(TICKETS)
    return rates

</details>

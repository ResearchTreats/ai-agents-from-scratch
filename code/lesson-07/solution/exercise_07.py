import store
from agent import run_agent
from ollama_brain import OllamaBrain
from tickets import TICKETS
from tools import helpdesk_tools


def compare_models(
    models, brain_for=lambda model: OllamaBrain(helpdesk_tools(), model=model)
):
    rates = {}
    for model in models:
        box, brain, finished = helpdesk_tools(), brain_for(model), 0
        for t in TICKETS:
            store.reset()
            finished += run_agent(t, brain, box)["stopped"] == "final"
        rates[model] = finished / len(TICKETS)
    return rates


if __name__ == "__main__":
    for model, rate in compare_models(["qwen2.5:3b", "llama3.2:3b"]).items():
        print(f"{model:<14} {rate:.0%} of tickets finished")

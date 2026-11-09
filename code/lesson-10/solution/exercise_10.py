import store
from brain import ScriptedBrain
from supervisor import TEAMS, Supervisor, classify
from tools import helpdesk_tools

RETURN_TICKET = {"id": "T7", "customer": "C1",
                 "text": "I want to return my jacket from order A17. It does not fit."}


def add_returns_team():
    TEAMS["returns"] = {"words": ["return", "fit", "exchange", "size"],
                        "tools": ["lookup_order", "search_help"]}


if __name__ == "__main__":
    add_returns_team()
    store.reset()
    print("classified as:", classify(RETURN_TICKET["text"]))
    print(Supervisor(ScriptedBrain(), helpdesk_tools()).handle(RETURN_TICKET)["team"])

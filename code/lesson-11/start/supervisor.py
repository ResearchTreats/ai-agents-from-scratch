import store
from agent import run_agent
from brain import ScriptedBrain
from tickets import TICKETS
from tools import ToolBox, helpdesk_tools

TEAMS = {
    "billing": {
        "words": ["charged", "refund", "invoice", "payment"],
        "tools": ["lookup_order", "lookup_customer", "refund"],
    },
    "shipping": {
        "words": ["order", "deliver", "arrive", "address"],
        "tools": ["lookup_order", "search_help"],
    },
    "tech": {
        "words": ["crash", "app", "error", "bug", "export"],
        "tools": ["search_help"],
    },
}


def classify(text):
    text = text.lower()
    scores = {
        team: sum(word in text for word in spec["words"])
        for team, spec in TEAMS.items()
    }
    team, score = max(scores.items(), key=lambda pair: pair[1])
    return team if score > 0 else "person"


def scoped(box, names):
    small = ToolBox(box.approve)
    for name in names:
        small.add(box.tools[name])
    return small


class Supervisor:
    def __init__(self, brain, box):
        self.brain = brain
        self.box = box

    def handle(self, ticket):
        team = classify(ticket["text"])
        if team == "person":
            return {"team": team, "answer": None, "stopped": "escalated"}
        result = run_agent(
            ticket, self.brain, scoped(self.box, TEAMS[team]["tools"])
        )
        return {"team": team, **result}


if __name__ == "__main__":
    store.reset()
    boss = Supervisor(
        ScriptedBrain(), helpdesk_tools(lambda n, a: float(a["amount"]) <= 50)
    )
    for t in TICKETS:
        result = boss.handle(t)
        print(
            f"{t['id']} -> {result['team']:<8} {result['stopped']:<9} "
            f"{str(result['answer'])[:40]}"
        )

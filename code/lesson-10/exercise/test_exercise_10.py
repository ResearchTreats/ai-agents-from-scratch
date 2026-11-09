import store
from brain import ScriptedBrain
from exercise_10 import RETURN_TICKET, add_returns_team
from supervisor import TEAMS, Supervisor, classify
from tools import helpdesk_tools


def test_a_returns_ticket_reaches_the_returns_team():
    add_returns_team()
    assert classify(RETURN_TICKET["text"]) == "returns"
    assert TEAMS["returns"]["tools"] == ["lookup_order", "search_help"]


def test_other_tickets_still_route_as_before():
    add_returns_team()
    assert classify("I was charged twice, please refund") == "billing"


def test_the_supervisor_runs_the_returns_specialist():
    add_returns_team()
    store.reset()
    result = Supervisor(ScriptedBrain(), helpdesk_tools()).handle(RETURN_TICKET)
    assert result["team"] == "returns"

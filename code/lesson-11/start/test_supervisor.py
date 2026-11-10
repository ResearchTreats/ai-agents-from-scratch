import store
from brain import ScriptedBrain
from supervisor import TEAMS, Supervisor, classify, scoped
from tickets import ticket
from tools import helpdesk_tools


def test_each_ticket_goes_to_the_right_team():
    assert classify(ticket("T1")["text"]) == "shipping"
    assert classify(ticket("T2")["text"]) == "billing"
    assert classify(ticket("T3")["text"]) == "tech"


def test_a_vague_ticket_goes_to_a_person():
    assert classify(ticket("T5")["text"]) == "person"


def test_scoped_box_holds_only_its_tools():
    box = scoped(helpdesk_tools(), TEAMS["tech"]["tools"])
    assert list(box.tools) == ["search_help"]
    assert box.run("refund", {"order_id": "B22", "amount": 1}).startswith(
        "error: unknown tool"
    )


def test_supervisor_runs_the_specialist():
    store.reset()
    boss = Supervisor(
        ScriptedBrain(), helpdesk_tools(approve=lambda n, a: True)
    )
    result = boss.handle(ticket("T1"))
    assert result["team"] == "shipping"
    assert "UPS" in result["answer"]


def test_supervisor_escalates_instead_of_guessing():
    boss = Supervisor(ScriptedBrain(), helpdesk_tools())
    assert boss.handle(ticket("T5")) == {
        "team": "person",
        "answer": None,
        "stopped": "escalated",
    }

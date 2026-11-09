import store
from agent import run_agent
from brain import ScriptedBrain
from guard import REWORDED, GuardedToolBox, scan
from tickets import ticket
from tools import helpdesk_tools

ALWAYS_APPROVE = helpdesk_tools(approve=lambda name, args: True)


def run_ticket(ticket_id):
    store.reset()
    t = ticket(ticket_id)
    return run_agent(t, ScriptedBrain(), GuardedToolBox(ALWAYS_APPROVE, t))


def refund(t, order_id, amount):
    store.reset()
    box = GuardedToolBox(ALWAYS_APPROVE, t)
    return box.run("refund", {"order_id": order_id, "amount": amount})


def test_scan_spots_instructions_aimed_at_the_agent():
    assert scan(ticket("T4")["text"]) != []
    assert scan(ticket("T2")["text"]) == []


def test_injected_ticket_cannot_refund_even_when_approved():
    run_ticket("T4")
    assert store.REFUNDS == []


def test_honest_refund_still_goes_through():
    run_ticket("T2")
    assert store.REFUNDS == [{"order_id": "B22", "amount": 25.0}]


def test_a_reworded_attack_gets_past_scan_but_not_the_policy():
    assert scan(REWORDED) == []
    reworded = {**ticket("T4"), "text": REWORDED}
    assert "larger than the order" in refund(reworded, "B22", 500)
    assert store.REFUNDS == []


def test_cannot_refund_someone_elses_order():
    assert "another customer" in refund(ticket("T1"), "B22", 5)
    assert store.REFUNDS == []


def test_arguments_it_cannot_check_are_refused():
    assert "cannot be checked" in refund(ticket("T2"), "B22", "lots")
    assert store.REFUNDS == []


def test_instructions_hidden_in_tool_output_are_removed():
    box = GuardedToolBox(ALWAYS_APPROVE, ticket("T3"))
    note = box.run("lookup_order", {"order_id": "C35"})
    assert "ignore previous instructions" not in note.lower()
    assert "[removed: instruction-like text]" in note

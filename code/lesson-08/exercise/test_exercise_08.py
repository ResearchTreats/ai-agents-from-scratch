import store
from exercise_08 import StricterGuard
from tickets import ticket
from tools import helpdesk_tools

YES = helpdesk_tools(approve=lambda name, args: True)


def test_no_refund_on_an_order_that_has_not_shipped():
    store.reset()
    message = StricterGuard(YES, ticket("T3")).run("refund", {"order_id": "C35", "amount": 5})
    assert "has not shipped" in message
    assert store.REFUNDS == []


def test_the_earlier_rules_still_apply_first():
    store.reset()
    message = StricterGuard(YES, ticket("T4")).run("refund", {"order_id": "B22", "amount": 5})
    assert "instructions aimed at the agent" in message


def test_a_shipped_order_can_still_be_refunded():
    store.reset()
    StricterGuard(YES, ticket("T2")).run("refund", {"order_id": "B22", "amount": 25})
    assert store.REFUNDS == [{"order_id": "B22", "amount": 25.0}]

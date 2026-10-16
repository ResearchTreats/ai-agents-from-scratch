import store
from exercise_02 import tools_with_cancel


def test_cancel_never_runs_without_approval():
    store.reset()
    message = tools_with_cancel().run("cancel_order", {"order_id": "C35"})
    assert "needs approval" in message
    assert store.ORDERS["C35"]["status"] == "processing"


def test_approved_cancel_changes_the_order():
    store.reset()
    tools_with_cancel(approve=lambda name, args: True).run("cancel_order", {"order_id": "C35"})
    assert store.ORDERS["C35"]["status"] == "cancelled"


def test_a_shipped_order_cannot_be_cancelled():
    store.reset()
    message = tools_with_cancel(approve=lambda n, a: True).run("cancel_order", {"order_id": "A17"})
    assert "already shipped" in message

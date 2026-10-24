import store
from exercise_03 import REFUND_STATUS, tools_with_refund_status
from schema_lint import lint_tool


def test_the_new_tool_passes_the_linter():
    assert lint_tool(REFUND_STATUS) == []


def test_it_reports_refunds_for_an_order():
    store.reset()
    box = tools_with_refund_status(approve=lambda n, a: True)
    assert box.run("get_refund_status", {"order_id": "B22"}) == "no refunds for B22"
    box.run("refund", {"order_id": "B22", "amount": 25})
    assert "25.00" in box.run("get_refund_status", {"order_id": "B22"})

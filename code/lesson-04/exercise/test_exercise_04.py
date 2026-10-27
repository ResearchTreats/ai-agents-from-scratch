from exercise_04 import call_all_capped
from tools import helpdesk_tools

CALLS = [("lookup_order", {"order_id": "A17"}), ("lookup_customer", {"customer_id": "C1"}),
         ("search_help", {"query": "refund"})]


def test_calls_over_the_cap_are_refused_not_dropped():
    results = call_all_capped(helpdesk_tools(), CALLS, max_calls=2)
    assert [r["id"] for r in results] == ["call_1", "call_2", "call_3"]
    assert not results[1]["observation"].startswith("error")
    assert results[2]["observation"].startswith("error: only 2 tool calls")


def test_under_the_cap_everything_runs():
    results = call_all_capped(helpdesk_tools(), CALLS[:1], max_calls=2)
    assert len(results) == 1 and '"UPS"' in results[0]["observation"]

import store
from agent import run_agent
from brain import ScriptedBrain
from tickets import ticket
from tools import Tool, ToolBox, helpdesk_tools


def small_refunds_only(name, args):
    return float(args.get("amount", 0)) <= 50


def test_toolbox_runs_a_pure_tool():
    box = helpdesk_tools()
    assert '"carrier": "UPS"' in box.run("lookup_order", {"order_id": "A17"})


def test_unknown_tool_lists_what_exists():
    message = helpdesk_tools().run("change_address", {})
    assert message.startswith("error: unknown tool")
    assert "lookup_order" in message


def test_side_effect_needs_approval():
    store.reset()
    message = helpdesk_tools().run("refund", {"order_id": "B22", "amount": 25})
    assert "needs approval" in message
    assert store.REFUNDS == []


def test_approved_refund_changes_the_store():
    store.reset()
    helpdesk_tools(approve=small_refunds_only).run(
        "refund", {"order_id": "B22", "amount": 25})
    assert store.REFUNDS == [{"order_id": "B22", "amount": 25.0}]


def test_a_crashing_tool_becomes_an_observation():
    box = ToolBox()
    box.add(Tool("boom", "Use when testing. Do not use for real work.",
                 {"type": "object", "properties": {}}, lambda: 1 / 0))
    assert box.run("boom", {}).startswith("error: ZeroDivisionError")


def test_toolbox_plugs_into_the_agent_loop():
    store.reset()
    box = helpdesk_tools(approve=small_refunds_only)
    result = run_agent(ticket("T2"), ScriptedBrain(), box)
    assert result["stopped"] == "final"
    assert store.REFUNDS == [{"order_id": "B22", "amount": 25.0}]


def test_big_refund_is_blocked_without_a_person():
    store.reset()
    box = helpdesk_tools(approve=small_refunds_only)
    run_agent(ticket("T4"), ScriptedBrain(), box)
    assert store.REFUNDS == []

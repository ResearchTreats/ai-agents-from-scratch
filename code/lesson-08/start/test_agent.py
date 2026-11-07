from agent import TOOLS, parse, run_agent
from brain import ScriptedBrain
from tickets import ticket


def test_parse_reads_a_final_answer():
    assert parse("Thought: done.\nFinal Answer: Hi there.") == ("final", "Hi there.")


def test_parse_reads_an_action():
    reply = 'Thought: look it up.\nAction: lookup_order {"order_id": "A17"}'
    assert parse(reply) == ("actions", [("lookup_order", {"order_id": "A17"})])


def test_agent_answers_an_order_question():
    result = run_agent(ticket("T1"), ScriptedBrain(), TOOLS)
    assert result["stopped"] == "final"
    assert "UPS" in result["answer"]


def test_unknown_tool_becomes_an_observation():
    result = run_agent(ticket("T6"), ScriptedBrain(), TOOLS)
    assert result["trace"][0]["observation"].startswith("error: unknown tool")


def test_turn_budget_stops_a_stuck_agent():
    result = run_agent(ticket("T5"), ScriptedBrain(), TOOLS, max_turns=3)
    assert result["stopped"] == "max_turns"
    assert result["turns"] == 3

import json

import pytest

from agent import TOOLS, run_agent
from brain import ScriptedBrain
from exercise_01 import run_agent_safely
from tickets import ticket

BROKEN_THEN_FIXED = {"T1": [
    'Thought: look it up.\nAction: lookup_order {"order_id": A17}',
    'Thought: fix the JSON.\nAction: lookup_order {"order_id": "A17"}',
    "Final Answer: Order A17 shipped with UPS.",
]}


def test_the_lesson_loop_crashes_on_broken_json():
    with pytest.raises(json.JSONDecodeError):
        run_agent(ticket("T1"), ScriptedBrain(BROKEN_THEN_FIXED), TOOLS)


def test_the_safe_loop_turns_broken_json_into_an_observation():
    result = run_agent_safely(ticket("T1"), ScriptedBrain(BROKEN_THEN_FIXED), TOOLS)
    assert result["trace"][0]["observation"].startswith("error: the Action arguments are not valid JSON")
    assert result["stopped"] == "final"
    assert "UPS" in result["answer"]


def test_the_safe_loop_still_answers_normal_tickets():
    assert run_agent_safely(ticket("T1"), ScriptedBrain(), TOOLS)["stopped"] == "final"

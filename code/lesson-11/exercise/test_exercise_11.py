from exercise_11 import memory_tools
from memory import Archive, MainContext
from schema_lint import lint_box


def test_the_agent_can_store_and_find_a_fact():
    box = memory_tools(MainContext(cap=4, archive=Archive()))
    assert box.run("remember", {"fact": "Asha prefers a phone call."}) == "remembered"
    assert "phone call" in box.run("recall", {"query": "phone or email"})


def test_recall_says_so_when_nothing_matches():
    box = memory_tools(MainContext(cap=4, archive=Archive()))
    assert box.run("recall", {"query": "weather"}) == "nothing remembered about that"


def test_memory_tools_pass_the_linter():
    assert all(p == [] for p in lint_box(memory_tools(MainContext(4, Archive()))).values())

from schema_lint import lint_box, lint_tool
from tools import Tool, helpdesk_tools

VAGUE = Tool(
    "doStuff",
    "Does stuff.",
    {"type": "object", "required": ["what"], "properties": {"thing": {}}},
    lambda thing="": thing,
)


def test_helpdesk_tools_are_clean():
    assert all(
        problems == [] for problems in lint_box(helpdesk_tools()).values()
    )


def test_vague_tool_gets_every_finding():
    problems = " | ".join(lint_tool(VAGUE))
    assert "snake_case" in problems
    assert "Use when" in problems
    assert "Do not use" in problems
    assert "'thing' has no type" in problems
    assert "'thing' has no description" in problems
    assert "'what' is required but not defined" in problems


def test_description_length_is_capped():
    long_tool = Tool(
        "long_one",
        "Use when x. Do not use for y. " + "z" * 1100,
        {"type": "object", "properties": {}},
        lambda: "",
    )
    assert any("1024" in p for p in lint_tool(long_tool))

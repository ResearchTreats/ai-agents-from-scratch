import re

from tools import Tool, helpdesk_tools

MAX_DESCRIPTION = 1024
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")


def lint_name_and_description(tool):
    problems = []
    if not SNAKE_CASE.match(tool.name):
        problems.append(f"name {tool.name!r} is not snake_case")
    if not tool.description.startswith("Use when"):
        problems.append("description should start with 'Use when ...'")
    if "Do not use" not in tool.description:
        problems.append("description should say 'Do not use for ...'")
    if len(tool.description) > MAX_DESCRIPTION:
        problems.append(f"description is over {MAX_DESCRIPTION} characters")
    return problems


def lint_parameters(tool):
    problems = []
    properties = tool.params.get("properties", {})
    for name, spec in properties.items():
        if "type" not in spec:
            problems.append(f"parameter {name!r} has no type")
        if not spec.get("description"):
            problems.append(f"parameter {name!r} has no description")
    for name in tool.params.get("required", []):
        if name not in properties:
            problems.append(f"parameter {name!r} is required but not defined")
    return problems


def lint_tool(tool):
    return lint_name_and_description(tool) + lint_parameters(tool)


def lint_box(box):
    return {name: lint_tool(tool) for name, tool in box.tools.items()}


if __name__ == "__main__":
    for name, problems in lint_box(helpdesk_tools()).items():
        print(f"{name}: {'clean' if not problems else problems}")
    vague = Tool(
        "doStuff",
        "Does stuff.",
        {"type": "object", "required": ["what"], "properties": {"thing": {}}},
        lambda thing="": thing,
    )
    print("doStuff:")
    for problem in lint_tool(vague):
        print(f"  - {problem}")

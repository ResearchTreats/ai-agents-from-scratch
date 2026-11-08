from agent import parse
from brain import SCRIPTS
from tools import helpdesk_tools

TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
}


def validate(args, schema):
    problems = []
    properties = schema.get("properties", {})
    for name in schema.get("required", []):
        if name not in args:
            problems.append(f"missing required argument {name!r}")
    for name, value in args.items():
        spec = properties.get(name)
        if spec is None:
            problems.append(f"unexpected argument {name!r}")
            continue
        wanted = spec.get("type")
        is_bool_as_number = isinstance(value, bool) and wanted in (
            "number",
            "integer",
        )
        if wanted in TYPES and (
            not isinstance(value, TYPES[wanted]) or is_bool_as_number
        ):
            problems.append(
                f"{name!r} should be {wanted}, got {type(value).__name__}"
            )
        if "enum" in spec and value not in spec["enum"]:
            problems.append(f"{name!r} must be one of {spec['enum']}")
    return problems


def coerce(args, schema):
    fixed = dict(args)
    for name, spec in schema.get("properties", {}).items():
        value = fixed.get(name)
        if isinstance(value, str) and spec.get("type") in (
            "number",
            "integer",
        ):
            try:
                fixed[name] = (
                    int(value) if spec["type"] == "integer" else float(value)
                )
            except ValueError:
                pass
    return fixed


def call_all(box, calls):
    results = []
    for number, (name, args) in enumerate(calls, start=1):
        tool = box.tools.get(name)
        if tool is None:
            observation = f"error: unknown tool {name!r}"
        else:
            args = coerce(args, tool.params)
            problems = validate(args, tool.params)
            observation = (
                "error: " + "; ".join(problems)
                if problems
                else box.run(name, args)
            )
        results.append(
            {"id": f"call_{number}", "tool": name, "observation": observation}
        )
    return results


if __name__ == "__main__":
    box = helpdesk_tools(approve=lambda name, args: args["amount"] <= 50)
    refund = box.tools["refund"].params
    print("raw:    ", validate({"order_id": "B22", "amount": "25"}, refund))
    print(
        "coerced:",
        validate(coerce({"order_id": "B22", "amount": "25"}, refund), refund),
    )
    for turn in SCRIPTS["T2"][:2]:
        _, calls = parse(turn)
        for result in call_all(box, calls):
            print(
                f"{result['id']} {result['tool']}: "
                f"{result['observation'][:60]}"
            )

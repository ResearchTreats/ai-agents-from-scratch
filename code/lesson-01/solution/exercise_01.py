import json

from agent import SYSTEM, TOOLS, parse, run_agent
from brain import ScriptedBrain
from tickets import TICKETS


def run_agent_safely(ticket, brain, tools, max_turns=6):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"[{ticket['id']}] {ticket['text']}"}]
    trace = []
    for turn in range(1, max_turns + 1):
        reply = brain.reply(messages)
        messages.append({"role": "assistant", "content": reply})
        try:
            kind, value = parse(reply)
        except json.JSONDecodeError as exc:
            observation = (f"error: the Action arguments are not valid JSON ({exc.msg}). "
                           "Reply again with valid JSON.")
            trace.append({"tool": None, "args": {}, "observation": observation})
            messages.append({"role": "tool", "content": f"Observation: {observation}"})
            continue
        if kind == "final":
            return {"answer": value, "turns": turn, "trace": trace, "stopped": "final"}
        for name, args in value:
            tool = tools.get(name)
            observation = tool(**args) if tool else f"error: unknown tool {name!r}"
            trace.append({"tool": name, "args": args, "observation": observation})
            messages.append({"role": "tool", "content": f"Observation: {observation}"})
    return {"answer": None, "turns": max_turns, "trace": trace, "stopped": "max_turns"}


if __name__ == "__main__":
    broken = ScriptedBrain({"T1": [
        'Thought: look it up.\nAction: lookup_order {"order_id": A17}',
        'Thought: fix the JSON.\nAction: lookup_order {"order_id": "A17"}',
        "Final Answer: Order A17 shipped with UPS."]})
    try:
        run_agent(TICKETS[0], broken, TOOLS)
    except json.JSONDecodeError as exc:
        print(f"lesson loop: crashed ({exc.msg})")
    result = run_agent_safely(TICKETS[0], broken, TOOLS)
    for step in result["trace"]:
        print(f"  {step['tool']} -> {step['observation'][:70]}")
    print(f"safe loop: {result['stopped']} after {result['turns']} turns: {result['answer']}")

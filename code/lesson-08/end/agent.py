import json
import re

import store
from brain import ScriptedBrain
from tickets import TICKETS

SYSTEM = ("You are a helpful support agent. Think step by step. "
          "To use a tool, write: Action: tool_name {json arguments}. "
          "When you know the answer, write: Final Answer: your reply.")

ACTION = re.compile(r"^Action:\s*(\w+)\s*(\{.*\})\s*$", re.MULTILINE)


def parse(reply):
    if "Final Answer:" in reply:
        return "final", reply.split("Final Answer:", 1)[1].strip()
    calls = [(name, json.loads(args)) for name, args in ACTION.findall(reply)]
    return "actions", calls


def lookup_order(order_id):
    order = store.ORDERS.get(order_id)
    if order is None:
        return f"error: there is no order {order_id!r}"
    return json.dumps(order)


TOOLS = {"lookup_order": lookup_order}


def run_agent(ticket, brain, tools, max_turns=6):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"[{ticket['id']}] {ticket['text']}"}]
    trace = []
    for turn in range(1, max_turns + 1):
        reply = brain.reply(messages)
        messages.append({"role": "assistant", "content": reply})
        kind, value = parse(reply)
        if kind == "final":
            return {"answer": value, "turns": turn, "trace": trace, "stopped": "final"}
        for name, args in value:
            tool = tools.get(name)
            observation = tool(**args) if tool else f"error: unknown tool {name!r}"
            trace.append({"tool": name, "args": args, "observation": observation})
            messages.append({"role": "tool", "content": f"Observation: {observation}"})
    return {"answer": None, "turns": max_turns, "trace": trace, "stopped": "max_turns"}


if __name__ == "__main__":
    brain = ScriptedBrain()
    for t in (TICKETS[0], TICKETS[4]):
        result = run_agent(t, brain, TOOLS)
        for step in result["trace"]:
            print(f"  {step['tool']}{step['args']} -> {step['observation'][:60]}")
        print(f"{t['id']}: {result['stopped']} after {result['turns']} turns: "
              f"{result['answer']}")

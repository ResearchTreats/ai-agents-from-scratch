import json
from dataclasses import dataclass
from typing import Callable

import store
from agent import lookup_order, run_agent
from brain import ScriptedBrain
from tickets import TICKETS


@dataclass
class Tool:
    name: str
    description: str
    params: dict
    fn: Callable
    side_effect: bool = False

    def schema(self):
        return {"name": self.name, "description": self.description,
                "parameters": self.params}


class ToolBox:
    def __init__(self, approve=None):
        self.tools = {}
        self.approve = approve or (lambda name, args: False)

    def add(self, tool):
        self.tools[tool.name] = tool

    def describe(self):
        return json.dumps([t.schema() for t in self.tools.values()], indent=2)

    def run(self, name, args):
        tool = self.tools.get(name)
        if tool is None:
            return f"error: unknown tool {name!r}. Tools: {', '.join(self.tools)}"
        if tool.side_effect and not self.approve(name, args):
            return f"error: {name} needs approval from a person"
        try:
            return tool.fn(**args)
        except Exception as exc:
            return f"error: {type(exc).__name__}: {exc}"

    def get(self, name):
        return lambda **args: self.run(name, args)


def lookup_customer(customer_id):
    customer = store.CUSTOMERS.get(customer_id)
    return json.dumps(customer) if customer else f"error: no customer {customer_id!r}"


def search_help(query):
    hits = [text for key, text in store.HELP_ARTICLES.items() if key in query.lower()]
    return " ".join(hits) or "no help article matches"


def refund(order_id, amount):
    order = store.ORDERS[order_id]
    store.REFUNDS.append({"order_id": order_id, "amount": float(amount)})
    return f"refunded {float(amount):.2f} on {order_id} (total {order['total']:.2f})"


def text_param(description):
    return {"type": "string", "description": description}


def helpdesk_tools(approve=None):
    box = ToolBox(approve)
    box.add(Tool("lookup_order",
                 "Use when you need an order's status, carrier or charges. "
                 "Do not use for customer details.",
                 {"type": "object", "required": ["order_id"],
                  "properties": {"order_id": text_param("Order id, like A17")}},
                 lookup_order))
    box.add(Tool("lookup_customer",
                 "Use when you need a customer's name or plan. "
                 "Do not use for orders.",
                 {"type": "object", "required": ["customer_id"],
                  "properties": {"customer_id": text_param("Customer id, like C1")}},
                 lookup_customer))
    box.add(Tool("search_help",
                 "Use when a question needs a help-center policy. "
                 "Do not use for a specific order.",
                 {"type": "object", "required": ["query"],
                  "properties": {"query": text_param("A few keywords")}},
                 search_help))
    box.add(Tool("refund",
                 "Use when an order was charged wrongly and money must go back. "
                 "Do not use for delivery problems.",
                 {"type": "object", "required": ["order_id", "amount"],
                  "properties": {"order_id": text_param("Order id, like B22"),
                                 "amount": {"type": "number",
                                            "description": "Dollars to refund"}}},
                 refund, side_effect=True))
    return box


if __name__ == "__main__":
    box = helpdesk_tools(approve=lambda name, args: float(args["amount"]) <= 50)
    for t in (TICKETS[1], TICKETS[3]):
        store.reset()
        result = run_agent(t, ScriptedBrain(), box)
        for step in result["trace"]:
            print(f"  {step['tool']}{step['args']} -> {step['observation'][:60]}")
        print(f"{t['id']}: refunds made: {store.REFUNDS}")

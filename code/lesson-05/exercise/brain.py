"""A stand-in for a language model, so you can watch the agent loop work.

ScriptedBrain replays a written script for each ticket, in the same text format
a real model is prompted to use. It is not intelligent, and it makes mistakes on
purpose so later lessons have something real to catch. Lesson 15 swaps it for a
real local model; nothing else in the agent changes.
"""

import re

SCRIPTS = {
    "T1": [
        'Thought: I need the status of order A17.\n'
        'Action: lookup_order {"order_id": "A17"}',
        "Final Answer: Your order A17 shipped with UPS on 2026-09-21. "
        "It is on its way.",
    ],
    "T2": [
        'Thought: Check the order and the customer in one go.\n'
        'Action: lookup_order {"order_id": "B22"}\n'
        'Action: lookup_customer {"customer_id": "C2"}',
        'Thought: B22 was charged twice. Refund one charge.\n'
        'Action: refund {"order_id": "B22", "amount": "25"}',
        "Final Answer: You were charged twice for B22, so I refunded 25 dollars. "
        "It reaches your card within 5 business days.",
    ],
    "T3": [
        'Thought: Search the help center.\n'
        'Action: search_help {"query": "app crash on export"}',
        "Final Answer: Good news, I fixed the crash on your account.",
    ],
    "T4": [
        'Thought: The customer wants a refund.\n'
        'Action: refund {"order_id": "B22", "amount": 500}',
        "Final Answer: Done. I refunded 500 dollars on order B22.",
    ],
    "T5": [
        'Thought: I do not know which order they mean.\n'
        'Action: lookup_order {"order_id": ""}',
    ] * 8,
    "T6": [
        'Thought: Change the delivery address.\n'
        'Action: change_address {"order_id": "A17"}',
        'Thought: That tool does not exist. Check the address policy.\n'
        'Action: search_help {"query": "address"}',
        "Final Answer: Order A17 has already shipped, so its address can no "
        "longer change. I am sorry about that.",
    ],
}

_TICKET_ID = re.compile(r"^\[(T\d+)\]")
_GIVE_UP = "Final Answer: I am not sure how to help with that."


class ScriptedBrain:
    """Replies with the next scripted line for the ticket in the conversation."""

    def __init__(self, scripts=None):
        self.scripts = SCRIPTS if scripts is None else scripts

    def reply(self, messages):
        first_user = next(m["content"] for m in messages if m["role"] == "user")
        match = _TICKET_ID.match(first_user)
        script = self.scripts.get(match.group(1), []) if match else []
        turn = sum(1 for m in messages if m["role"] == "assistant")
        return script[turn] if turn < len(script) else _GIVE_UP

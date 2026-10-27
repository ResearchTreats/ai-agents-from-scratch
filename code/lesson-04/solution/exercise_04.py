from calling import call_all
from tools import helpdesk_tools


def call_all_capped(box, calls, max_calls=2):
    results = call_all(box, calls[:max_calls])
    for number, (name, _) in enumerate(calls[max_calls:], start=max_calls + 1):
        results.append({"id": f"call_{number}", "tool": name,
                        "observation": f"error: only {max_calls} tool calls are allowed "
                                       f"per turn; ask for {name} next turn"})
    return results


if __name__ == "__main__":
    calls = [("lookup_order", {"order_id": "A17"}), ("lookup_customer", {"customer_id": "C1"}),
             ("search_help", {"query": "refund"})]
    for result in call_all_capped(helpdesk_tools(), calls):
        print(f"{result['id']} {result['tool']}: {result['observation'][:60]}")

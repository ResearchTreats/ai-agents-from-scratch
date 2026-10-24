import store
from schema_lint import lint_box
from tools import Tool, helpdesk_tools, text_param


def get_refund_status(order_id):
    refunds = [r["amount"] for r in store.REFUNDS if r["order_id"] == order_id]
    if not refunds:
        return f"no refunds for {order_id}"
    return f"{order_id} refunds: " + ", ".join(f"{amount:.2f}" for amount in refunds)


REFUND_STATUS = Tool("get_refund_status",
                     "Use when a customer asks whether a refund went through. "
                     "Do not use to make a refund.",
                     {"type": "object", "required": ["order_id"],
                      "properties": {"order_id": text_param("Order id, like B22")}},
                     get_refund_status)


def tools_with_refund_status(approve=None):
    box = helpdesk_tools(approve)
    box.add(REFUND_STATUS)
    return box


if __name__ == "__main__":
    for name, problems in lint_box(tools_with_refund_status()).items():
        print(f"{name}: {'clean' if not problems else problems}")

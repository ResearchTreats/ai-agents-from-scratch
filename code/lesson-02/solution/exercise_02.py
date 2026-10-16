import store
from tools import Tool, helpdesk_tools, text_param


def cancel_order(order_id):
    order = store.ORDERS[order_id]
    if order["status"] != "processing":
        return f"error: {order_id} has already shipped and cannot be cancelled"
    order["status"] = "cancelled"
    return f"cancelled {order_id}"


CANCEL = Tool("cancel_order",
              "Use when a customer asks to cancel an order that has not shipped yet. "
              "Do not use for refunds.",
              {"type": "object", "required": ["order_id"],
               "properties": {"order_id": text_param("Order id, like C35")}},
              cancel_order, side_effect=True)


def tools_with_cancel(approve=None):
    box = helpdesk_tools(approve)
    box.add(CANCEL)
    return box


if __name__ == "__main__":
    store.reset()
    print("no approval:  ", tools_with_cancel().run("cancel_order", {"order_id": "C35"}))
    print("with approval:", tools_with_cancel(lambda n, a: True).run("cancel_order", {"order_id": "C35"}))
    print("C35 is now:   ", store.ORDERS["C35"]["status"])

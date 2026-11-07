import store
from guard import GuardedToolBox
from tickets import TICKETS
from tools import helpdesk_tools


class StricterGuard(GuardedToolBox):
    def check(self, args):
        problem = super().check(args)
        if problem:
            return problem
        if store.ORDERS.get(args.get("order_id"), {}).get("status") == "processing":
            return "the order has not shipped yet - cancel it instead of refunding"
        return None


if __name__ == "__main__":
    store.reset()
    box = StricterGuard(helpdesk_tools(approve=lambda name, args: True), TICKETS[2])
    print(box.run("refund", {"order_id": "C35", "amount": 5}))

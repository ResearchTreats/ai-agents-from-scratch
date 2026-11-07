# Lesson 08 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Open exercise_08.py — you're extending guard.py's GuardedToolBox, not rewriting it. Subclass it as StricterGuard and look at what check() already returns: a string describing the problem, or None when the call is fine. Your job is to add one more condition that can return a string.

</details>

<details><summary>Hint 2</summary>

Call super().check(args) first and return its result immediately if it isn't None — the ticket-injection and cross-customer/over-amount checks from GuardedToolBox must still run before your new rule. Then look up the order the same way check() already does, with store.ORDERS.get(args.get('order_id'), {}), and inspect its 'status' field.

</details>

<details><summary>Hint 3</summary>

If store.ORDERS[...]['status'] == 'processing', return the string "the order has not shipped yet - cancel it instead of refunding" — test_no_refund_on_an_order_that_has_not_shipped checks for 'has not shipped' in that message, and C35 is the order fixture whose status is 'processing'. Otherwise fall through and return None so a shipped order like B22 can still be refunded.

</details>

# Lesson 02 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Open exercise_02.py. You already have everything you need in tools.py - cancel_order needs the same shape as refund: a plain function, then a Tool that wraps it and gets added to a fresh toolbox.

</details>

<details><summary>Hint 2</summary>

Write a cancel_order(order_id) function that reads store.ORDERS[order_id], and only sets its status to cancelled if it isn't already shipped - otherwise return an error string that mentions already shipped. Wrap it in a Tool with side_effect=True, same as refund, and write a tools_with_cancel(approve=None) function that starts from helpdesk_tools(approve) and adds your new tool with box.add(...).

</details>

<details><summary>Hint 3</summary>

Your cancel_order(order_id) should look up store.ORDERS[order_id]; if its status isn't processing, return an error string that contains the words already shipped (that's what makes the A17 test pass, since A17 ships already); otherwise set status to cancelled and return a string like f'cancelled {order_id}'. Build CANCEL = Tool('cancel_order', 'Use when a customer asks to cancel an order that has not shipped yet. Do not use for refunds.', {'type': 'object', 'required': ['order_id'], 'properties': {'order_id': text_param('Order id, like C35')}}, cancel_order, side_effect=True), then write tools_with_cancel(approve=None) as a function that calls helpdesk_tools(approve), adds CANCEL to it with .add(CANCEL), and returns the box - that combination is exactly what makes all three tests in test_exercise_02.py pass.

</details>

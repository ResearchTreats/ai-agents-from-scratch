# Lesson 03 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Open exercise_03.py. You need a plain function get_refund_status(order_id) that reads store.REFUNDS - the same list refund appends to - and reports what it finds for that order; then wrap it in a Tool, the same shape as the tools in tools.py, and check it against lint_tool before you even add it to a box.

</details>

<details><summary>Hint 2</summary>

Write get_refund_status(order_id) to filter store.REFUNDS for entries whose order_id matches, returning 'no refunds for {order_id}' when there are none, or a string listing each amount formatted to two decimals when there are some. Build REFUND_STATUS as a Tool named get_refund_status with a description that starts with 'Use when' and contains 'Do not use' (so it passes lint_tool), a required order_id parameter built with text_param, and get_refund_status as its executor. Then write tools_with_refund_status(approve=None) that starts from helpdesk_tools(approve) and adds REFUND_STATUS with box.add(...).

</details>

<details><summary>Hint 3</summary>

Your get_refund_status(order_id) should be: refunds = [r['amount'] for r in store.REFUNDS if r['order_id'] == order_id]; return f'no refunds for {order_id}' if not refunds else f'{order_id} refunds: ' + ', '.join(f'{amount:.2f}' for amount in refunds). Build REFUND_STATUS = Tool('get_refund_status', 'Use when a customer asks whether a refund went through. Do not use to make a refund.', {'type': 'object', 'required': ['order_id'], 'properties': {'order_id': text_param('Order id, like B22')}}, get_refund_status), and write tools_with_refund_status(approve=None) as box = helpdesk_tools(approve); box.add(REFUND_STATUS); return box - that combination is exactly what makes both tests in test_exercise_03.py pass.

</details>

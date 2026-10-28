# Lesson 05 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

Look at how handle() in mcp_server.py already falls through to error(request_id, -32601, ...) when it doesn't recognize a method - resources/list hits that exact fallback today. Your handle_with_resources() in exercise_05.py needs to catch that one case and turn it into a real listing instead of leaving it as an error.

</details>

<details><summary>Hint 2</summary>

Call the existing handle() first. If request.get('method') == 'resources/list' and the reply came back as that -32601 error, build your own reply with the result() helper imported from mcp_server - one entry per article, each with a 'help://<key>' uri. Put the article keys in a new store.py module next to mcp_server.py as HELP_ARTICLES. Also patch the server/discover reply so its capabilities dict gets a 'resources' key, the same way it already has 'tools'.

</details>

<details><summary>Hint 3</summary>

In exercise_05.py: `reply = handle(request, box)`; if the method is 'resources/list' and `reply.get('error', {}).get('code') == -32601`, return `result(request['id'], {'resources': [{'uri': f'help://{key}', 'name': key, 'mimeType': 'text/plain'} for key in store.HELP_ARTICLES]})`; if the method is 'server/discover' and 'result' in reply, set `reply['result']['capabilities']['resources'] = {}`; otherwise return reply unchanged. In store.py, define HELP_ARTICLES with its keys in the order export, refund, address so test_resources_list_names_every_help_article sees ['help://export', 'help://refund', 'help://address'].

</details>

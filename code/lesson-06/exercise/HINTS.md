# Lesson 06 exercise: hints

Open one hint at a time, only when you are stuck.

<details><summary>Hint 1</summary>

MCPClient already has request. Calling request('tools/list') returns a dict with a 'tools' list, and each tool in it carries an 'inputSchema'. Start by turning that list into a dict from tool name to schema.

</details>

<details><summary>Hint 2</summary>

In exercise_06.py, make CheckedClient a subclass of MCPClient and override call(name, arguments). Look up the tool's schema, run validate (imported from calling) on the arguments and that schema, and if it returns any problems, return a string starting 'error: ' without sending anything. Otherwise hand over to super().call. An unknown tool has no schema, so let the server reject it.

</details>

<details><summary>Hint 3</summary>

from calling import validate
from mcp_client import MCPClient


class CheckedClient(MCPClient):
    def schemas(self):
        return {
            t['name']: t['inputSchema']
            for t in self.request('tools/list')['tools']
        }

    def call(self, name, arguments):
        schema = self.schemas().get(name)
        problems = validate(arguments, schema) if schema else []
        if problems:
            return 'error: ' + '; '.join(problems)
        return super().call(name, arguments)

</details>

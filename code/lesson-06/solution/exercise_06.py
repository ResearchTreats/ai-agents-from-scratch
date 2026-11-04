from calling import validate
from mcp_client import MCPClient


class CheckedClient(MCPClient):
    def schemas(self):
        return {
            t["name"]: t["inputSchema"]
            for t in self.request("tools/list")["tools"]
        }

    def call(self, name, arguments):
        schema = self.schemas().get(name)
        problems = validate(arguments, schema) if schema else []
        if problems:
            return "error: " + "; ".join(problems)
        return super().call(name, arguments)


if __name__ == "__main__":
    client = CheckedClient()
    client.connect()
    print(client.call("refund", {"order_id": "B22", "amount": "25"}))
    print(client.call("lookup_order", {"order_id": "A17"})[:40])
    client.close()

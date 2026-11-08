import json
import subprocess
import sys

from agent import run_agent
from brain import ScriptedBrain
from mcp_server import MODERN, VERSION_KEY
from tickets import TICKETS

KNOWN_VERSIONS = [MODERN]


class MCPError(Exception):
    def __init__(self, error):
        super().__init__(f"{error['code']} {error['message']}")
        self.code = error["code"]
        self.data = error.get("data") or {}


class MCPClient:
    def __init__(self, version=MODERN):
        self.server = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        self.version = version
        self.next_id = 0

    def request(self, method, params=None):
        self.next_id += 1
        params = {**(params or {}), "_meta": {VERSION_KEY: self.version}}
        message = {
            "jsonrpc": "2.0",
            "id": self.next_id,
            "method": method,
            "params": params,
        }
        self.server.stdin.write(json.dumps(message) + "\n")
        self.server.stdin.flush()
        reply = json.loads(self.server.stdout.readline())
        if "error" in reply:
            raise MCPError(reply["error"])
        return reply["result"]

    def connect(self):
        try:
            return self.request("server/discover")
        except MCPError as e:
            shared = [
                v for v in e.data.get("supported", []) if v in KNOWN_VERSIONS
            ]
            if e.code != -32022 or not shared:
                raise
            self.version = shared[0]
            return self.request("server/discover")

    def list_tools(self):
        return [tool["name"] for tool in self.request("tools/list")["tools"]]

    def call(self, name, arguments):
        result = self.request(
            "tools/call", {"name": name, "arguments": arguments}
        )
        return "".join(
            c["text"] for c in result["content"] if c["type"] == "text"
        )

    def close(self):
        self.server.stdin.close()
        self.server.wait(timeout=5)


def mcp_tools(client):
    def remote(name):
        return lambda **arguments: client.call(name, arguments)

    return {name: remote(name) for name in client.list_tools()}


if __name__ == "__main__":
    client = MCPClient()
    print(
        "server:",
        client.connect()["_meta"]["io.modelcontextprotocol/serverInfo"],
    )
    print("tools:", client.list_tools())
    result = run_agent(TICKETS[0], ScriptedBrain(), mcp_tools(client))
    for step in result["trace"]:
        print(f"  {step['tool']}{step['args']} -> {step['observation'][:60]}")
    print(f"{TICKETS[0]['id']}: {result['answer']}")
    client.close()

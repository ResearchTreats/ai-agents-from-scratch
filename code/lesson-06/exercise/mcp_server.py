import json
import sys

from tools import helpdesk_tools

MODERN = "2026-07-28"
LEGACY = "2025-11-25"
VERSION_KEY = "io.modelcontextprotocol/protocolVersion"
SERVER_INFO = {"name": "helpdesk", "version": "1.0.0"}


def result(request_id, body):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"resultType": "complete", **body},
    }


def error(request_id, code, message, data=None):
    body = {"code": code, "message": message}
    if data is not None:
        body["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": body}


def handle(request, box):
    request_id, method = request.get("id"), request.get("method")
    params = request.get("params") or {}
    if request_id is None:
        return None
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": LEGACY,
                "serverInfo": SERVER_INFO,
                "capabilities": {"tools": {}},
            },
        }
    version = params.get("_meta", {}).get(VERSION_KEY)
    if version not in (None, MODERN):
        return error(
            request_id,
            -32022,
            "Unsupported protocol version",
            {"supported": [MODERN, LEGACY], "requested": version},
        )
    if method == "server/discover":
        return result(
            request_id,
            {
                "supportedVersions": [MODERN, LEGACY],
                "capabilities": {"tools": {}},
                "_meta": {"io.modelcontextprotocol/serverInfo": SERVER_INFO},
            },
        )
    if method == "tools/list":
        return result(
            request_id,
            {
                "tools": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.params,
                    }
                    for t in box.tools.values()
                ]
            },
        )
    if method == "tools/call":
        name = params.get("name")
        if name not in box.tools:
            return error(request_id, -32602, f"Unknown tool: {name}")
        text = box.run(name, params.get("arguments") or {})
        return result(
            request_id,
            {
                "content": [{"type": "text", "text": text}],
                "isError": text.startswith("error:"),
            },
        )
    return error(request_id, -32601, f"Method not found: {method}")


def serve(box, stdin=sys.stdin, stdout=sys.stdout):
    for line in stdin:
        if not line.strip():
            continue
        try:
            reply = handle(json.loads(line), box)
        except json.JSONDecodeError:
            reply = error(None, -32700, "Parse error")
        if reply is not None:
            stdout.write(json.dumps(reply) + "\n")
            stdout.flush()


if __name__ == "__main__":
    serve(
        helpdesk_tools(approve=lambda name, args: float(args["amount"]) <= 50)
    )

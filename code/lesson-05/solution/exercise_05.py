import store
from mcp_server import MODERN, handle, result
from tools import helpdesk_tools


def handle_with_resources(request, box):
    reply = handle(request, box)
    method = request.get("method")
    if method == "resources/list" and reply and reply.get("error", {}).get("code") == -32601:
        return result(request["id"], {"resources": [
            {"uri": f"help://{key}", "name": key, "mimeType": "text/plain"}
            for key in store.HELP_ARTICLES]})
    if method == "server/discover" and reply and "result" in reply:
        reply["result"]["capabilities"]["resources"] = {}
    return reply


if __name__ == "__main__":
    meta = {"_meta": {"io.modelcontextprotocol/protocolVersion": MODERN}}
    for method in ("server/discover", "resources/list"):
        reply = handle_with_resources({"jsonrpc": "2.0", "id": 1, "method": method,
                                       "params": meta}, helpdesk_tools())
        print(method, "->", reply["result"].get("capabilities") or reply["result"]["resources"])

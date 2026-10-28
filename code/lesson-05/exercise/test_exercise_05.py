from exercise_05 import handle_with_resources
from mcp_server import MODERN
from tools import helpdesk_tools

META = {"_meta": {"io.modelcontextprotocol/protocolVersion": MODERN}}


def ask(method):
    return handle_with_resources({"jsonrpc": "2.0", "id": 1, "method": method,
                                  "params": META}, helpdesk_tools())


def test_resources_list_names_every_help_article():
    resources = ask("resources/list")["result"]["resources"]
    assert [r["uri"] for r in resources] == ["help://export", "help://refund", "help://address"]


def test_discover_now_advertises_resources():
    assert "resources" in ask("server/discover")["result"]["capabilities"]


def test_tools_still_work():
    assert len(ask("tools/list")["result"]["tools"]) == 4

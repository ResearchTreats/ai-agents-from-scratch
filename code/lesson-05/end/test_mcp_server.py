import io
import json

from mcp_server import LEGACY, MODERN, handle, serve
from tools import helpdesk_tools

META = {"_meta": {"io.modelcontextprotocol/protocolVersion": MODERN}}


def ask(method, params=None, box=None):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {**META, **(params or {})},
    }
    return handle(request, box or helpdesk_tools())


def test_discover_names_versions_and_tools_capability():
    result = ask("server/discover")["result"]
    assert result["supportedVersions"] == [MODERN, LEGACY]
    assert "tools" in result["capabilities"]


def test_tools_list_uses_the_toolbox_schemas():
    tools = ask("tools/list")["result"]["tools"]
    assert [t["name"] for t in tools] == [
        "lookup_order",
        "lookup_customer",
        "search_help",
        "refund",
    ]
    assert tools[0]["inputSchema"]["required"] == ["order_id"]


def test_tools_call_returns_text_content():
    result = ask(
        "tools/call",
        {"name": "lookup_order", "arguments": {"order_id": "A17"}},
    )["result"]
    assert result["resultType"] == "complete"
    assert result["isError"] is False
    assert "UPS" in result["content"][0]["text"]


def test_tool_failure_is_a_result_not_a_protocol_error():
    result = ask(
        "tools/call",
        {"name": "refund", "arguments": {"order_id": "B22", "amount": 5}},
    )["result"]
    assert result["isError"] is True


def test_unknown_tool_is_a_protocol_error():
    assert (
        ask("tools/call", {"name": "nope", "arguments": {}})["error"]["code"]
        == -32602
    )


def test_unknown_method():
    assert ask("resources/list")["error"]["code"] == -32601


def test_wrong_version_lists_what_is_supported():
    request = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/list",
        "params": {
            "_meta": {"io.modelcontextprotocol/protocolVersion": "1900-01-01"}
        },
    }
    error = handle(request, helpdesk_tools())["error"]
    assert error["code"] == -32022
    assert error["data"] == {
        "supported": [MODERN, LEGACY],
        "requested": "1900-01-01",
    }


def test_legacy_initialize_still_works():
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {},
    }
    assert (
        handle(request, helpdesk_tools())["result"]["protocolVersion"]
        == LEGACY
    )


def test_notifications_get_no_reply():
    assert (
        handle(
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            helpdesk_tools(),
        )
        is None
    )


def test_serve_speaks_one_json_message_per_line():
    lines = [
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": META,
            }
        ),
        "not json",
    ]
    out = io.StringIO()
    serve(helpdesk_tools(), io.StringIO("\n".join(lines) + "\n"), out)
    replies = [json.loads(line) for line in out.getvalue().splitlines()]
    assert len(replies[0]["result"]["tools"]) == 4
    assert replies[1]["error"]["code"] == -32700

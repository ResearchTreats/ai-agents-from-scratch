import pytest

from agent import run_agent
from brain import ScriptedBrain
from mcp_client import MCPClient, MCPError, mcp_tools
from tickets import TICKETS


@pytest.fixture
def client():
    c = MCPClient()
    yield c
    c.close()


def test_connect_finds_the_server(client):
    assert "2026-07-28" in client.connect()["supportedVersions"]


def test_an_unknown_version_switches_to_one_both_speak():
    c = MCPClient(version="1900-01-01")
    try:
        c.connect()
        assert c.version == "2026-07-28"
    finally:
        c.close()


def test_a_tool_runs_inside_the_server(client):
    assert '"carrier": "UPS"' in client.call(
        "lookup_order", {"order_id": "A17"}
    )


def test_an_unknown_tool_is_an_error(client):
    with pytest.raises(MCPError) as e:
        client.call("change_address", {"order_id": "A17"})
    assert e.value.code == -32602


def test_the_agent_answers_through_mcp(client):
    result = run_agent(TICKETS[0], ScriptedBrain(), mcp_tools(client))
    assert result["stopped"] == "final"
    assert result["trace"][0]["tool"] == "lookup_order"

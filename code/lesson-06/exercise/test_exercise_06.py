import pytest

from exercise_06 import CheckedClient
from mcp_client import MCPError


@pytest.fixture
def client():
    c = CheckedClient()
    c.connect()
    yield c
    c.close()


def test_a_bad_argument_never_reaches_the_server(client):
    assert client.call("refund", {"order_id": "B22", "amount": "25"}) == (
        "error: 'amount' should be number, got str"
    )


def test_a_good_call_still_runs(client):
    assert '"carrier": "UPS"' in client.call(
        "lookup_order", {"order_id": "A17"}
    )


def test_an_unknown_tool_is_still_the_servers_error(client):
    with pytest.raises(MCPError):
        client.call("change_address", {"order_id": "A17"})

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from agent import run_agent
from ollama_brain import OllamaBrain
from tickets import ticket
from tools import helpdesk_tools


def fake_ollama(replies):
    seen = []
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            size = int(self.headers["Content-Length"])
            seen.append(json.loads(self.rfile.read(size)))
            body = json.dumps({"message": replies[len(seen) - 1]}).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_port}/api/chat", seen, server


CALL = {"name": "lookup_order", "arguments": {"order_id": "A17"}}
TOOL_CALL = {"role": "assistant", "tool_calls": [{"function": CALL}]}
ANSWER = {"role": "assistant", "content": "Your order A17 shipped with UPS."}


def test_a_tool_call_becomes_an_action_line():
    url, _, server = fake_ollama([TOOL_CALL])
    brain = OllamaBrain(helpdesk_tools(), url=url)
    reply = brain.reply([{"role": "user", "content": "[T1] where is A17?"}])
    server.shutdown()
    assert reply == 'Action: lookup_order {"order_id": "A17"}'


def test_the_same_agent_loop_runs_on_a_real_model_shape():
    url, seen, server = fake_ollama([TOOL_CALL, ANSWER])
    brain = OllamaBrain(helpdesk_tools(), url=url)
    result = run_agent(ticket("T1"), brain, helpdesk_tools())
    server.shutdown()
    assert result["stopped"] == "final"
    assert "UPS" in result["answer"]
    assert seen[0]["stream"] is False
    assert seen[0]["options"]["temperature"] == 0

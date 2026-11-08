import json
import urllib.error
import urllib.request

import store
from agent import parse, run_agent
from tickets import TICKETS
from tools import helpdesk_tools

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"


def to_ollama(messages):
    converted, pending = [], []
    for message in messages:
        if message["role"] == "assistant":
            kind, value = parse(message["content"])
            if kind == "actions" and value:
                pending = [name for name, _ in value]
                converted.append(
                    {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [
                            {"function": {"name": name, "arguments": args}}
                            for name, args in value
                        ],
                    }
                )
                continue
        if message["role"] == "tool":
            text = message["content"].removeprefix("Observation: ")
            converted.append(
                {
                    "role": "tool",
                    "content": text,
                    "tool_name": pending.pop(0) if pending else "",
                }
            )
            continue
        converted.append(
            {"role": message["role"], "content": message["content"]}
        )
    return converted


class OllamaBrain:
    def __init__(self, box, model=MODEL, url=OLLAMA_URL):
        self.tools = [
            {"type": "function", "function": t.schema()}
            for t in box.tools.values()
        ]
        self.model = model
        self.url = url

    def reply(self, messages):
        body = {
            "model": self.model,
            "messages": to_ollama(messages),
            "tools": self.tools,
            "stream": False,
            "options": {"temperature": 0, "seed": 7},
        }
        request = urllib.request.Request(
            self.url,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                message = json.load(response)["message"]
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise LookupError(
                    f"Ollama has no model {self.model!r} (404). "
                    f"Run: ollama pull {self.model}"
                ) from None
            raise
        except urllib.error.URLError:
            raise ConnectionError(
                f"cannot reach Ollama at {self.url}. Run: ollama serve"
            ) from None
        calls = message.get("tool_calls") or []
        if calls:
            return "\n".join(
                f"Action: {c['function']['name']} "
                f"{json.dumps(c['function']['arguments'])}"
                for c in calls
            )
        text = message.get("content", "").strip()
        return (
            text
            if "Final Answer:" in text or "Action:" in text
            else f"Final Answer: {text}"
        )


if __name__ == "__main__":
    box = helpdesk_tools()
    brain = OllamaBrain(box)
    for t in TICKETS:
        store.reset()
        result = run_agent(t, brain, box)
        tools = [step["tool"] for step in result["trace"]]
        print(f"{t['id']}: {result['stopped']} {tools}")

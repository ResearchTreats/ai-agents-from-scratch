from memory import Archive, MainContext
from tools import Tool, ToolBox, text_param


def memory_tools(context):
    def remember(fact):
        context.archive.add(fact)
        return "remembered"

    def recall(query):
        found = context.recall(query)
        return " | ".join(found) if found else "nothing remembered about that"

    box = ToolBox()
    box.add(Tool("remember",
                 "Use when the customer states a lasting fact or preference. "
                 "Do not use for order details you can look up.",
                 {"type": "object", "required": ["fact"],
                  "properties": {"fact": text_param("The fact, in one sentence")}},
                 remember))
    box.add(Tool("recall",
                 "Use when you need something the customer said earlier. "
                 "Do not use for order status.",
                 {"type": "object", "required": ["query"],
                  "properties": {"query": text_param("A few keywords")}},
                 recall))
    return box


if __name__ == "__main__":
    box = memory_tools(MainContext(cap=4, archive=Archive()))
    print(box.run("remember", {"fact": "Asha prefers a phone call, never email."}))
    print(box.run("recall", {"query": "email or phone?"}))

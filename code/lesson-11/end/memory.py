import re


def words(text):
    return set(re.findall(r"\w+", text.lower()))


class Archive:
    def __init__(self):
        self.records = []

    def add(self, text):
        self.records.append(text)

    def search(self, query, k=2):
        scored = [
            (len(words(query) & words(text)), text) for text in self.records
        ]
        ranked = sorted(scored, key=lambda pair: -pair[0])
        return [text for score, text in ranked if score > 0][:k]


class MainContext:
    def __init__(self, cap, archive):
        self.cap = cap
        self.archive = archive
        self.core = {}
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        while len(self.messages) > self.cap:
            evicted = self.messages.pop(0)
            self.archive.add(evicted["content"])

    def recall(self, query):
        return self.archive.search(query)

    def prompt(self):
        facts = "\n".join(
            f"- {key}: {value}" for key, value in self.core.items()
        )
        return f"Core facts:\n{facts}"


if __name__ == "__main__":
    context = MainContext(cap=4, archive=Archive())
    context.core["customer"] = "Asha (C1), pro plan"
    context.add("user", "Asha prefers a phone call, never email.")
    for i in range(1, 7):
        context.add("user", f"Asha asks again about order A17, message {i}.")
    print(context.prompt())
    print("Main context:")
    for message in context.messages:
        print(f"- {message['content']}")
    print(f"in main context: {len(context.messages)} messages")
    print(f"archived:        {len(context.archive.records)} messages")
    print(f"recall('email or phone?') -> {context.recall('email or phone?')}")

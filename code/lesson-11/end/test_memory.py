from memory import Archive, MainContext


def test_archive_finds_the_best_overlap_first():
    archive = Archive()
    archive.add("Asha's order A17 shipped with UPS.")
    archive.add("Asha prefers a phone call, never email.")
    assert archive.search("should I email or phone Asha?")[0].startswith(
        "Asha prefers"
    )


def test_archive_ignores_punctuation_and_case():
    archive = Archive()
    archive.add("Refunds take FIVE days.")
    assert archive.search("How many DAYS?") == ["Refunds take FIVE days."]


def test_archive_returns_nothing_for_no_overlap():
    archive = Archive()
    archive.add("Order A17 shipped with UPS.")
    assert archive.search("weather tomorrow") == []


def test_main_context_pages_out_instead_of_forgetting():
    context = MainContext(cap=3, archive=Archive())
    context.add("user", "Asha prefers a phone call, never email.")
    for i in range(5):
        context.add("user", f"filler message {i}")
    assert len(context.messages) == 3
    assert "phone call" not in " ".join(
        m["content"] for m in context.messages
    )
    assert context.recall("phone or email?") == [
        "Asha prefers a phone call, never email."
    ]


def test_core_facts_are_never_evicted():
    context = MainContext(cap=2, archive=Archive())
    context.core["customer"] = "Asha, pro plan"
    for i in range(10):
        context.add("user", f"message {i}")
    assert context.core == {"customer": "Asha, pro plan"}
    assert context.prompt().startswith(
        "Core facts:\n- customer: Asha, pro plan"
    )

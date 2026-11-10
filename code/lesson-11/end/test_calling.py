import store
from agent import parse
from brain import SCRIPTS
from calling import call_all, coerce, validate
from tools import helpdesk_tools

REFUND = helpdesk_tools().tools["refund"].params


def test_valid_arguments_have_no_problems():
    assert validate({"order_id": "B22", "amount": 25}, REFUND) == []


def test_string_number_is_a_problem():
    assert validate({"order_id": "B22", "amount": "25"}, REFUND) == [
        "'amount' should be number, got str"
    ]


def test_missing_and_unexpected_arguments():
    problems = validate({"amount": 5, "note": "x"}, REFUND)
    assert "missing required argument 'order_id'" in problems
    assert "unexpected argument 'note'" in problems


def test_a_boolean_is_not_a_number():
    assert validate({"order_id": "B22", "amount": True}, REFUND) != []


def test_coerce_fixes_a_string_number():
    assert coerce({"order_id": "B22", "amount": "25"}, REFUND) == {
        "order_id": "B22",
        "amount": 25.0,
    }


def test_coerce_leaves_words_alone():
    assert coerce({"amount": "lots"}, REFUND) == {"amount": "lots"}


def test_two_calls_in_one_turn_keep_their_ids():
    _, calls = parse(SCRIPTS["T2"][0])
    results = call_all(helpdesk_tools(), calls)
    assert [r["id"] for r in results] == ["call_1", "call_2"]
    assert [r["tool"] for r in results] == ["lookup_order", "lookup_customer"]


def test_bad_call_is_rejected_before_it_runs():
    store.reset()
    box = helpdesk_tools(approve=lambda name, args: True)
    results = call_all(
        box, [("refund", {"order_id": "B22", "amount": "lots"})]
    )
    assert results[0]["observation"].startswith(
        "error: 'amount' should be number"
    )
    assert store.REFUNDS == []

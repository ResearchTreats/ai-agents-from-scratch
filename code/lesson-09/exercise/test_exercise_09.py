from exercise_09 import regression_gate


def results(passed, total):
    return [{"passed": i < passed} for i in range(total)]


def test_first_run_sets_the_baseline(tmp_path):
    assert regression_gate(results(3, 6), tmp_path / "rate.json") is True


def test_a_drop_below_the_last_rate_fails(tmp_path):
    path = tmp_path / "rate.json"
    regression_gate(results(4, 6), path)
    assert regression_gate(results(3, 6), path) is False


def test_holding_or_improving_passes(tmp_path):
    path = tmp_path / "rate.json"
    regression_gate(results(3, 6), path)
    assert regression_gate(results(3, 6), path) is True
    assert regression_gate(results(5, 6), path) is True

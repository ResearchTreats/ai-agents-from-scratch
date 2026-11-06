from brain import ScriptedBrain
from exercise_07 import compare_models


def test_each_model_gets_its_own_finish_rate():
    rates = compare_models(
        ["scripted-a", "scripted-b"], brain_for=lambda model: ScriptedBrain()
    )
    assert rates == {"scripted-a": 5 / 6, "scripted-b": 5 / 6}

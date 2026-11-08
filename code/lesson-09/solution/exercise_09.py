import json
from pathlib import Path

from brain import ScriptedBrain
from evals import CASES, make_helpdesk, run_suite


def regression_gate(results, path):
    path = Path(path)
    rate = sum(r["passed"] for r in results) / len(results)
    best = json.loads(path.read_text(encoding="utf-8"))["rate"] if path.exists() else 0.0
    if rate < best:
        return False
    path.write_text(json.dumps({"rate": rate}), encoding="utf-8")
    return True


if __name__ == "__main__":
    results = run_suite(CASES, make_helpdesk(ScriptedBrain()))
    rate = sum(r["passed"] for r in results) / len(results)
    ok = regression_gate(results, "pass_rate.json")
    print(f"pass rate {rate:.0%}: {'no regression' if ok else 'REGRESSION - blocked'}")

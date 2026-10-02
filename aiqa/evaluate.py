import json
from pathlib import Path
from .evaluator import evaluate_proposals

def load_reference():
    return json.loads(Path("REFERENCE_TESTS.json").read_text())

def evaluate(proposals):
    references = load_reference()
    result = evaluate_proposals(proposals, references)
    return {
        "validity": result.validity,
        "reference_coverage": result.reference_coverage,
        "duplicate_rate": result.duplicate_rate,
        "total": result.total,
    }

if __name__ == "__main__":
    print(evaluate(load_reference()))

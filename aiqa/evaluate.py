import json
from pathlib import Path
from .models import validate

def load_reference():
    return json.loads(Path("REFERENCE_TESTS.json").read_text())

def evaluate(proposals):
    valid=0; scenarios=set()
    for item in proposals:
        try:
            p=validate(item); valid+=1; scenarios.add(p.scenario.lower())
        except ValueError:
            pass
    refs=load_reference()
    covered=sum(r["scenario"].lower() in scenarios for r in refs)
    return {"validity": valid/len(proposals) if proposals else 0, "reference_coverage": covered/len(refs) if refs else 0}

if __name__ == "__main__":
    print(evaluate(load_reference()))

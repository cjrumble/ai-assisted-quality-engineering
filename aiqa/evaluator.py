from dataclasses import dataclass
from collections import Counter

@dataclass(frozen=True)
class Evaluation:
    validity: float
    reference_coverage: float
    duplicate_rate: float
    total: int

def evaluate_proposals(proposals, references):
    total=len(proposals)
    valid=[p for p in proposals if isinstance(p,dict) and p.get("scenario") and p.get("expected")]
    scenarios=[p["scenario"].strip().lower() for p in valid]
    unique=set(scenarios)
    ref_set={r["scenario"].strip().lower() for r in references}
    coverage=(len(unique & ref_set)/len(ref_set)) if ref_set else 0.0
    duplicates=(1-len(unique)/len(scenarios)) if scenarios else 0.0
    return Evaluation(
        validity=len(valid)/total if total else 0.0,
        reference_coverage=coverage,
        duplicate_rate=duplicates,
        total=total,
    )

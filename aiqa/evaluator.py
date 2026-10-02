from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    validity: float
    reference_coverage: float
    duplicate_rate: float
    total: int
    risk_coverage: float
    requirement_id_validity: float


def evaluate_proposals(proposals, references=None, requirement_ids=None):
    """Measure deterministic quality signals without making a model call."""
    references = references or []
    requirement_ids = set(requirement_ids or [])
    total = len(proposals)
    valid = [p for p in proposals if isinstance(p, dict) and p.get("scenario") and p.get("expected")]
    scenarios = [p["scenario"].strip().lower() for p in valid]
    unique = set(scenarios)
    ref_set = {r["scenario"].strip().lower() for r in references if r.get("scenario")}
    coverage = (len(unique & ref_set) / len(ref_set)) if ref_set else 0.0
    duplicates = (1 - len(unique) / len(scenarios)) if scenarios else 0.0
    risky = {"high", "critical"}
    risks_present = {str(p.get("risk", "")).lower() for p in valid}
    risk_coverage = len(risks_present & risky) / len(risky) if risky else 0.0
    ids_present = [p.get("requirement_id") for p in valid]
    id_validity = (sum(1 for rid in ids_present if rid in requirement_ids) / len(ids_present)) if ids_present and requirement_ids else 0.0
    return Evaluation(
        validity=len(valid) / total if total else 0.0,
        reference_coverage=coverage,
        duplicate_rate=duplicates,
        total=total,
        risk_coverage=risk_coverage,
        requirement_id_validity=id_validity,
    )

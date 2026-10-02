"""Requirement-to-test traceability and coverage analysis."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TraceabilityResult:
    requirements: int
    covered_requirements: int
    uncovered_requirements: tuple[str, ...]
    orphan_tests: tuple[str, ...]
    coverage: float


def build_traceability(requirements: list[dict], proposals: list[dict]) -> TraceabilityResult:
    requirement_ids = {r["id"] for r in requirements}
    covered = {
        p.get("requirement_id")
        for p in proposals
        if p.get("requirement_id") in requirement_ids
    }
    uncovered = tuple(sorted(requirement_ids - covered))
    orphans = tuple(
        sorted(
            str(p.get("scenario", ""))
            for p in proposals
            if p.get("requirement_id") not in requirement_ids
        )
    )
    coverage = len(covered) / len(requirement_ids) if requirement_ids else 0.0
    return TraceabilityResult(
        requirements=len(requirement_ids),
        covered_requirements=len(covered),
        uncovered_requirements=uncovered,
        orphan_tests=orphans,
        coverage=coverage,
    )


def to_matrix(requirements: list[dict], proposals: list[dict]) -> list[dict]:
    """Return an auditable requirement/test matrix suitable for JSON or CSV."""
    by_requirement: dict[str, list[str]] = {}
    for proposal in proposals:
        by_requirement.setdefault(proposal.get("requirement_id", ""), []).append(
            proposal.get("scenario", "")
        )

    return [
        {
            "requirement_id": requirement["id"],
            "requirement": requirement["text"],
            "tests": by_requirement.get(requirement["id"], []),
            "covered": bool(by_requirement.get(requirement["id"])),
        }
        for requirement in requirements
    ]

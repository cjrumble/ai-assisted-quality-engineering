"""Run the live model adapter and write an auditable sample report."""
import json
import os
from pathlib import Path

from aiqa.evaluator import evaluate_proposals
from aiqa.model_adapter import LiveModelAdapter
from aiqa.traceability import build_traceability, to_matrix


def main():
    requirements = json.loads(Path("REQUIREMENTS_TRACEABILITY.json").read_text())
    references = json.loads(Path("REFERENCE_TESTS.json").read_text())
    requirement_text = "\\n".join(f'{r["id"]}: {r["text"]}' for r in requirements)
    proposals = LiveModelAdapter().generate(requirement_text)
    evaluation = evaluate_proposals(proposals, references=references, requirement_ids=[r["id"] for r in requirements])
    trace = build_traceability(requirements, proposals)

    output = {
        "model": os.getenv("AI_MODEL_NAME", "configured-model"),
        "evaluation": {
            "validity": evaluation.validity,
            "reference_coverage": evaluation.reference_coverage,
            "duplicate_rate": evaluation.duplicate_rate,
            "risk_coverage": evaluation.risk_coverage,
            "requirement_id_validity": evaluation.requirement_id_validity,
            "total": evaluation.total,
        },
        "traceability": {
            "requirements": trace.requirements,
            "covered_requirements": trace.covered_requirements,
            "coverage": trace.coverage,
            "uncovered_requirements": list(trace.uncovered_requirements),
            "orphan_tests": list(trace.orphan_tests),
        },
        "matrix": to_matrix(requirements, proposals),
        "proposals": proposals,
    }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/live-model-sample.json").write_text(json.dumps(output, indent=2) + "\\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

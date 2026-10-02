"""Optional live-model demo.

Run only when AI_MODEL_API_KEY is configured. The default CI suite remains
offline and deterministic.
"""
import json
import os
from pathlib import Path

from aiqa.model_adapter import LiveModelAdapter
from aiqa.traceability import build_traceability, to_matrix


def main():
    requirements = json.loads(Path("REQUIREMENTS_TRACEABILITY.json").read_text())
    requirement_text = "\n".join(
        f'{r["id"]}: {r["text"]}' for r in requirements
    )
    proposals = LiveModelAdapter().generate(requirement_text)
    trace = build_traceability(requirements, proposals)

    output = {
        "model": os.getenv("AI_MODEL_NAME", "gpt-4o-mini"),
        "traceability": {
            "coverage": trace.coverage,
            "uncovered_requirements": trace.uncovered_requirements,
            "orphan_tests": trace.orphan_tests,
        },
        "matrix": to_matrix(requirements, proposals),
        "proposals": proposals,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

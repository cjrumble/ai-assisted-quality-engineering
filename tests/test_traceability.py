from aiqa.traceability import build_traceability, to_matrix


REQUIREMENTS = [
    {"id": "REQ-001", "text": "Valid login works"},
    {"id": "REQ-002", "text": "Invalid login is rejected"},
]


def test_traceability_calculates_coverage_and_uncovered_requirements():
    proposals = [{"requirement_id": "REQ-001", "scenario": "Valid login", "expected": "Success"}]
    result = build_traceability(REQUIREMENTS, proposals)

    assert result.requirements == 2
    assert result.covered_requirements == 1
    assert result.coverage == 0.5
    assert result.uncovered_requirements == ("REQ-002",)


def test_traceability_detects_orphan_tests():
    proposals = [
        {"requirement_id": "REQ-999", "scenario": "Unknown requirement", "expected": "No behavior"}
    ]
    result = build_traceability(REQUIREMENTS, proposals)

    assert result.orphan_tests == ("Unknown requirement",)


def test_matrix_is_auditable():
    proposals = [{"requirement_id": "REQ-001", "scenario": "Valid login", "expected": "Success"}]
    matrix = to_matrix(REQUIREMENTS, proposals)

    assert matrix[0]["covered"] is True
    assert matrix[1]["covered"] is False

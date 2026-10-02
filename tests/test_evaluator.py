from aiqa.evaluator import evaluate_proposals

def test_evaluator_measures_validity_coverage_and_duplicates():
    refs=[{"scenario":"valid login"},{"scenario":"invalid password"}]
    proposals=[
        {"scenario":"Valid Login","expected":"dashboard"},
        {"scenario":"Valid Login","expected":"dashboard"},
        {"scenario":"Invalid Password","expected":"error"},
        {"scenario":"","expected":"missing scenario"},
    ]
    result=evaluate_proposals(proposals, refs)
    assert result.validity == 0.75
    assert result.reference_coverage == 1.0
    assert result.duplicate_rate > 0

def test_empty_inputs_are_safe():
    result=evaluate_proposals([], [])
    assert result.validity == 0
    assert result.reference_coverage == 0

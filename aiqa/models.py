from dataclasses import dataclass

@dataclass
class TestProposal:
    scenario: str
    expected: str

def validate(proposal: dict) -> TestProposal:
    if not isinstance(proposal, dict) or not proposal.get("scenario") or not proposal.get("expected"):
        raise ValueError("Proposal must contain scenario and expected")
    return TestProposal(proposal["scenario"], proposal["expected"])

# AI-Assisted Quality Engineering

A controlled evaluation harness for using LLMs to propose software tests while measuring **validity, reference coverage, duplication, and review readiness**.

## Architecture

```
Requirement
   ↓
Prompt / Model Adapter
   ↓
Structured JSON proposals
   ↓
Schema validation
   ↓
Duplicate detection
   ↓
Reference coverage
   ↓
Human review
   ↓
Approved test assets
```

## Senior-engineering practices demonstrated
- deterministic evaluation independent of model output
- explicit structured-output contract
- prompt isolation and versioning
- reference-test baselines
- validity/coverage/duplication metrics
- safe parser behavior for malformed model responses
- offline tests that do not require an API key
- separation between AI generation and quality decisions

## Safety and governance
AI output is treated as a **proposal**, never as an authoritative test oracle. Production credentials and sensitive customer data are excluded from prompts. A human reviewer remains accountable for approving generated tests.

## Run
```bash
pip install -r requirements.txt
pytest -v
python -m aiqa.evaluate
```

## Extension path
A production implementation can add model adapters, prompt/version experiments, mutation testing, requirement-to-test traceability, cost/latency measurement, hallucination checks, and human-review persistence without changing the deterministic evaluation core.

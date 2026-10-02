# AI-Assisted Quality Engineering

A controlled evaluation harness for using AI/LLMs to propose software tests while measuring **validity, reference coverage, duplication, requirement coverage, and review readiness**.

## Architecture

```
Requirements with stable IDs
        ↓
Prompt / Live Model Adapter
        ↓
Structured JSON test proposals
        ↓
Schema + deterministic evaluation
        ↓
Requirement-to-test traceability
        ↓
Human review
        ↓
Approved test assets
```

## Senior-engineering practices demonstrated

- provider-neutral live-model adapter using an OpenAI-compatible API contract
- API credentials supplied only through environment variables
- deterministic offline CI; live-model execution is opt-in
- explicit structured-output contract
- stable requirement IDs and auditable requirement-to-test mapping
- validity, reference coverage, duplicate-rate, and traceability metrics
- malformed-output protection and isolated unit tests
- separation between AI generation and quality decisions
- human review and governance as part of the quality workflow

## Live model

Configure the adapter without committing credentials:

```bash
export AI_MODEL_API_KEY="..."
export AI_MODEL_NAME="gpt-4o-mini"
export AI_MODEL_API_URL="https://api.openai.com/v1/chat/completions"
python scripts/generate_live.py
```

The endpoint and model are configurable so the harness can be used with compatible model providers. The live demo reads `REQUIREMENTS_TRACEABILITY.json`, generates structured proposals, and emits an auditable traceability matrix.

**Never commit an API key or customer-sensitive data.**

## Requirement-to-test traceability

Requirements are assigned stable IDs such as `REQ-001`. Generated tests carry the corresponding `requirement_id`. The traceability evaluator identifies:

- total requirements
- covered requirements
- coverage percentage
- uncovered requirements
- orphan tests referencing unknown requirements

See [docs/TRACEABILITY.md](docs/TRACEABILITY.md).

## Deterministic evaluation

The core evaluator remains independent of the model. Run it locally or in CI:

```bash
pip install -r requirements.txt
pytest -v
python -m aiqa.evaluate
```

CI does **not** call a live model, which keeps builds reproducible and prevents secrets from being required for normal testing.

## Safety and governance

AI output is treated as a **proposal**, never as an authoritative test oracle. Production credentials and sensitive customer data are excluded from prompts. A human reviewer remains accountable for approving generated tests.

## Extension path

The project can be extended with prompt/model version comparison, mutation testing, hallucination detection, cost/latency telemetry, persisted human-review decisions, and generated-test execution without changing the deterministic evaluation core.

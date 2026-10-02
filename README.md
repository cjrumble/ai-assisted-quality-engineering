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


## Example traceability report

The following is a representative offline report using the repository's deterministic reference proposals. It demonstrates the evidence a reviewer can inspect before any live-model output is accepted.

| Requirement | Risk | Test proposals | Covered | Review status |
|---|---|---:|---|---|
| REQ-001 — Valid credentials allow sign-in | High | 1 | Yes | Requires human approval |
| REQ-002 — Invalid credentials are rejected without sensitive details | High | 1 | Yes | Requires human approval |
| REQ-003 — Sign-out invalidates the session | Medium | 1 | Yes | Requires human approval |

**Traceability metrics**

- Requirements: **3**
- Covered: **3**
- Traceability coverage: **100%**
- Uncovered requirements: **0**
- Orphan tests: **0**
- Generated proposals are still **untrusted** until schema validation and human review are complete.

### What this report proves

This is intentionally more than a list of AI-generated test cases. The harness establishes an auditable chain:

`Requirement → Requirement ID → Generated test proposal → Deterministic validation → Coverage result → Human review`

A model can produce syntactically valid tests while still missing important requirements. The traceability layer makes those gaps measurable and prevents a high volume of generated tests from being mistaken for complete coverage.

### Live-model sample

A live run is **not executed in CI** because it requires an external model credential and produces non-deterministic output. To run the repository's live demonstration locally:

```bash
export AI_MODEL_API_KEY="YOUR_KEY"
export AI_MODEL_NAME="gpt-4o-mini"
export AI_MODEL_API_URL="https://api.openai.com/v1/chat/completions"

python scripts/generate_live.py
```

The command reads `REQUIREMENTS_TRACEABILITY.json`, invokes the configured model, validates the returned structure through the project's evaluation pipeline, and prints JSON containing the model name, traceability metrics, requirement/test matrix, and proposals.

For a portfolio repository, the important engineering distinction is that **the model generates proposals; deterministic code measures them; humans approve them**. No live API key or customer data belongs in the repository.


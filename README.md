# AI-Assisted Quality Engineering

[![CI](https://github.com/cjrumble/ai-assisted-quality-engineering/actions/workflows/test.yml/badge.svg)](https://github.com/cjrumble/ai-assisted-quality-engineering/actions/workflows/test.yml)

**AI proposes tests. Deterministic engineering metrics decide what needs review.**

A controlled evaluation harness for using AI/LLMs to propose software tests while measuring **validity, requirement traceability, reference coverage, duplication, risk coverage, and review readiness**.

## Architecture at a Glance

### 30-second recruiter / hiring-manager view

```
  REQUIREMENTS             AI MODEL                 QUALITY GATES
┌────────────────┐     ┌────────────────┐       ┌────────────────────┐
│ REQ-001        │     │ Structured     │       │ Validity           │
│ REQ-002   ─────┼────▶│ test proposals │──────▶│ Requirement-ID      │
│ REQ-003        │     │ JSON contract  │       │ Duplicate rate     │
└────────────────┘     └────────────────┘       │ Reference coverage │
          │                                     │ Risk coverage      │
          │                                     └─────────┬──────────┘
          │                                               │
          │                                               ▼
          │                                    ┌────────────────────┐
          └───────────────────────────────────▶│ TRACEABILITY       │
                                               │ Requirement → Test │
                                               │ Coverage → Review  │
                                               └─────────┬──────────┘
                                                         │
                                                         ▼
                                               ┌────────────────────┐
                                               │ HUMAN APPROVAL      │
                                               │ Approved test asset │
                                               └────────────────────┘
```

**Engineering story:** the model generates proposals; deterministic code measures their quality; traceability exposes gaps; humans make the final quality decision.

## Recruiter / Hiring-Manager Snapshot

| Engineering signal | Evidence in this repo |
|---|---|
| **AI engineering** | Provider-neutral live-model adapter + structured JSON contract |
| **Quality engineering** | Deterministic evaluation, schema checks, traceability, human approval |
| **Test automation** | Python + pytest + API/UI test patterns + CI |
| **Release governance** | Requirement coverage and orphan-test detection |
| **Engineering metrics** | Validity, reference coverage, duplicate rate, risk coverage, ID validity |
| **Production discipline** | Secrets via environment variables; live model is opt-in; CI stays deterministic |

## End-to-End Flow

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

## Engineering Metrics

These are deterministic engineering signals—not model-generated quality claims.

| Metric | Definition | Engineering use |
|---|---|---|
| **Validity** | Proposals containing required scenario/expected fields ÷ total | Detect malformed or incomplete output |
| **Requirement-ID validity** | Valid proposals tied to known requirement IDs ÷ valid proposals | Detect invented or broken trace links |
| **Traceability coverage** | Requirements with ≥1 linked proposal ÷ total requirements | Show whether requirements are represented by tests |
| **Reference coverage** | Known reference scenarios represented by generated scenarios ÷ reference scenarios | Measure alignment with expected test intent |
| **Duplicate rate** | 1 − unique scenarios ÷ valid scenarios | Prevent inflated test counts from repetition |
| **Risk coverage** | Presence of High/Critical risk signals in generated proposals | Make risk prioritization measurable |
| **Orphan tests** | Proposals pointing to unknown requirement IDs | Identify unauditable output |

The evaluator runs without a model credential and is suitable for deterministic CI.

## Example Traceability Report

The repository includes a representative offline report so a reviewer can understand the evidence before running a live model.

### Executive metrics

| KPI | Result | Interpretation |
|---|---:|---|
| Requirements | **3** | Stable requirement inventory |
| Requirements covered | **3 / 3** | Every requirement has a linked proposal |
| Traceability coverage | **100%** | No uncovered requirements |
| Orphan tests | **0** | No unknown requirement references |
| Duplicate rate | **0%** | No duplicate scenarios in the sample |
| Validity | **100%** | All sample proposals meet required fields |
| Requirement-ID validity | **100%** | All sample proposals use known IDs |
| Review state | **Human review required** | AI output remains untrusted |

### Requirement → Test visual matrix

| ID | Risk | Requirement | Proposed test | Status |
|---|---|---|---|---|
| **REQ-001** | High | Valid credentials allow sign-in | Valid credentials permit sign-in | ✅ Covered |
| **REQ-002** | High | Invalid credentials are rejected without sensitive details | Invalid credentials are rejected without sensitive details | ✅ Covered |
| **REQ-003** | Medium | Sign-out invalidates the session | Sign-out invalidates the authenticated session | ✅ Covered |

**Audit chain:**

`Requirement → Stable ID → AI proposal → Deterministic validation → Engineering metrics → Traceability result → Human approval`

Generating many test cases is not the same as demonstrating coverage. The traceability layer makes missing, duplicated, or unauditable output visible.

See the [representative JSON report](reports/live-model-sample.json) and [traceability design](docs/TRACEABILITY.md).

## Senior-engineering practices demonstrated

- provider-neutral live-model adapter using an OpenAI-compatible API contract
- API credentials supplied only through environment variables
- deterministic offline CI; live-model execution is opt-in
- explicit structured-output contract
- stable requirement IDs and auditable requirement-to-test mapping
- validity, reference coverage, duplicate-rate, risk, and traceability metrics
- malformed-output protection and isolated unit tests
- separation between AI generation and quality decisions
- human review and governance as part of the quality workflow

## Live Model

Configure the adapter without committing credentials:

```bash
export AI_MODEL_API_KEY="YOUR_KEY"
export AI_MODEL_NAME="gpt-4o-mini"
export AI_MODEL_API_URL="https://api.openai.com/v1/chat/completions"
python scripts/generate_live.py
```

The live demonstration reads `REQUIREMENTS_TRACEABILITY.json`, generates structured proposals, evaluates them, and emits an auditable requirement/test matrix.

**Never commit an API key or customer-sensitive data.**

## Deterministic Evaluation

```bash
pip install -r requirements.txt
pytest -v
python -m aiqa.evaluate
```

CI does **not** call a live model, which keeps builds reproducible and prevents secrets from being required for normal testing.

## Safety and Governance

AI output is treated as a **proposal**, never as an authoritative test oracle. Production credentials and sensitive customer data are excluded from prompts. A human reviewer remains accountable for approving generated tests.

## Extension Path

Next engineering increments can include prompt/model version comparison, mutation testing, hallucination detection, cost/latency telemetry, persisted human-review decisions, and generated-test execution without changing the deterministic evaluation core.

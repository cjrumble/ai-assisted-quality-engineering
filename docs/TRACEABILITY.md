# Requirement-to-Test Traceability

The project treats traceability as an explicit quality artifact rather than a
side effect of prompt generation.

## Flow

```
Requirement IDs
     |
     v
Prompt / Live Model
     |
     v
Structured Test Proposals
     |
     +----> Schema + duplicate evaluation
     |
     v
Requirement-to-test matrix
     |
     v
Human review / approval
```

Each requirement has a stable ID such as `REQ-001`. A generated proposal must
carry `requirement_id`. The traceability evaluator reports:

- requirement count
- covered requirement count
- coverage percentage
- uncovered requirements
- orphan tests that reference unknown requirements

This makes missing coverage visible and prevents a generated test from being
treated as useful merely because it is syntactically valid.

## Live model configuration

The adapter uses an OpenAI-compatible chat-completions endpoint and reads:

- `AI_MODEL_API_URL`
- `AI_MODEL_NAME`
- `AI_MODEL_API_KEY`
- `AI_MODEL_TIMEOUT_SECONDS`

No API key is committed to the repository. CI stays offline; live-model
execution is an explicit local operation through `scripts/generate_live.py`.

The endpoint is intentionally configurable so the same quality harness can be
used with different compatible model providers.

## Governance

Live output is untrusted proposal data. The deterministic evaluator and human
review process remain outside the model boundary. Production use should also
persist prompt/model versions, latency, token/cost metadata, and reviewer
decisions.

# AI-Assisted Quality Engineering

A controlled evaluation harness for using an LLM to propose software tests from requirements while measuring validity, coverage, duplication, and human-review outcomes.

## Design principles
1. AI proposes; deterministic validators decide whether output is structurally valid.
2. Reference tests remain human-authored.
3. Evaluation uses a fixed dataset so model/prompt changes can be compared.
4. Sensitive production data is excluded from prompts.
5. The project reports limitations instead of treating generated tests as automatically correct.

## Pipeline
`requirements -> structured test proposals -> schema validation -> deduplication -> evaluation -> review queue`

## Run offline
```bash
pip install -r requirements.txt
pytest -v
python -m aiqa.evaluate
```

Set `OPENAI_API_KEY` only when testing a live model adapter. The default evaluator is offline.

import json

SYSTEM_PROMPT = """You are a software quality engineer.
Convert a requirement into structured test proposals.
Return JSON only. Never invent unavailable product behavior.
Each proposal must contain scenario and expected."""

def build_prompt(requirement: str) -> str:
    return f"{SYSTEM_PROMPT}\n\nRequirement:\n{requirement.strip()}"

def parse_response(raw: str):
    data=json.loads(raw)
    if not isinstance(data,list):
        raise ValueError("Model response must be a JSON array")
    return data

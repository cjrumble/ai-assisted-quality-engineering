import json

SYSTEM_PROMPT = """You are a software quality engineer.
Convert requirements into structured test proposals.
Return JSON only as an array.
Every proposal must contain requirement_id, scenario, expected, and risk.
Use only requirement IDs supplied by the user. Never invent product behavior."""

def build_prompt(requirement: str) -> str:
    return f"{SYSTEM_PROMPT}\n\nRequirements:\n{requirement.strip()}"

def parse_response(raw: str):
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("Model response must be a JSON array")
    return data

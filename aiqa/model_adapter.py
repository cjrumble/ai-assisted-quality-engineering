"""Live-model adapter with an OpenAI-compatible HTTP interface.

The adapter is intentionally provider-neutral: configure an OpenAI-compatible
endpoint, model name, and API key through environment variables. No credentials
are stored in source code.
"""
from dataclasses import dataclass
import json
import os
from urllib import request


@dataclass(frozen=True)
class ModelConfig:
    endpoint: str
    model: str
    api_key: str
    timeout_seconds: int = 60


class LiveModelAdapter:
    def __init__(self, config: ModelConfig | None = None):
        self.config = config or ModelConfig(
            endpoint=os.getenv("AI_MODEL_API_URL", "https://api.openai.com/v1/chat/completions"),
            model=os.getenv("AI_MODEL_NAME", "gpt-4o-mini"),
            api_key=os.getenv("AI_MODEL_API_KEY", ""),
            timeout_seconds=int(os.getenv("AI_MODEL_TIMEOUT_SECONDS", "60")),
        )

    def generate(self, requirement: str) -> list[dict]:
        if not self.config.api_key:
            raise RuntimeError("AI_MODEL_API_KEY is required for live-model execution")

        payload = {
            "model": self.config.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": "You are a software quality engineer. Return JSON only. Produce an array of test proposals with requirement_id, scenario, expected, and risk."},
                {"role": "user", "content": requirement.strip()},
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.config.endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=self.config.timeout_seconds) as response:
            result = json.loads(response.read().decode("utf-8"))

        content = result["choices"][0]["message"]["content"]
        return json.loads(content)

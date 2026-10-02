import json
from unittest.mock import patch

from aiqa.model_adapter import LiveModelAdapter, ModelConfig


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps({
            "choices": [{
                "message": {
                    "content": '[{"requirement_id":"REQ-001","scenario":"Valid login","expected":"Access granted","risk":"high"}]'
                }
            }]
        }).encode()


def test_live_adapter_uses_configured_endpoint_without_real_network_call():
    config = ModelConfig("https://example.test/v1/chat/completions", "test-model", "test-key")
    adapter = LiveModelAdapter(config)

    with patch("aiqa.model_adapter.request.urlopen", return_value=FakeResponse()) as mocked:
        proposals = adapter.generate("REQ-001: valid login")

    assert proposals[0]["requirement_id"] == "REQ-001"
    assert mocked.call_args.kwargs["timeout"] == 60


def test_live_adapter_requires_api_key():
    config = ModelConfig("https://example.test", "test-model", "")
    adapter = LiveModelAdapter(config)

    try:
        adapter.generate("test")
        assert False, "Expected missing API key failure"
    except RuntimeError as exc:
        assert "AI_MODEL_API_KEY" in str(exc)

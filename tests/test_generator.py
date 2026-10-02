import pytest
from aiqa.generator import build_prompt, parse_response

def test_prompt_is_explicit_about_structured_output():
    prompt=build_prompt("Users can reset their password.")
    assert "JSON only" in prompt
    assert "reset their password" in prompt

def test_parser_rejects_non_array():
    with pytest.raises(ValueError):
        parse_response('{"scenario":"x"}')

def test_parser_accepts_array():
    assert parse_response('[{"scenario":"x","expected":"y"}]')[0]["scenario"]=="x"

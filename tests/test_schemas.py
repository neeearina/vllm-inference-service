import pytest
from pydantic import ValidationError

from app.schemas import GenerateRequest, GenerateResponse


def test_generate_request_defaults():
    r = GenerateRequest.model_validate({"prompt": "hello"})
    assert r.prompt == "hello"
    assert r.max_tokens == 100
    assert r.temperature == 0.7


def test_generate_request_full():
    r = GenerateRequest.model_validate(
        {"prompt": "x", "max_tokens": 512, "temperature": 2.0}
    )
    assert r.max_tokens == 512
    assert r.temperature == 2.0


@pytest.mark.parametrize(
    "payload",
    [
        {"prompt": ""},
        {"prompt": "ok", "max_tokens": 0},
        {"prompt": "ok", "max_tokens": 513},
        {"prompt": "ok", "temperature": -0.01},
        {"prompt": "ok", "temperature": 2.01},
    ],
)
def test_generate_request_validation_errors(payload):
    with pytest.raises(ValidationError):
        GenerateRequest.model_validate(payload)


def test_generate_response():
    r = GenerateResponse(response="hi", latency_ms=12.5)
    assert r.response == "hi"
    assert r.latency_ms == 12.5

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_generate_ok(client):
    resp = client.post(
        "/generate",
        json={"prompt": "hello world", "max_tokens": 50, "temperature": 0.5},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["response"] == "mocked generated text"
    assert "latency_ms" in data
    assert isinstance(data["latency_ms"], (int, float))
    assert data["latency_ms"] >= 0


def test_generate_uses_request_params(client):
    fake_seq = MagicMock()
    fake_seq.outputs = [MagicMock(text="custom", token_ids=[7])]
    fake_seq.prompt_token_ids = [1, 2]

    with patch("app.main.generate_with_vllm") as gen:
        gen.return_value = fake_seq
        r = client.post(
            "/generate",
            json={"prompt": "p", "max_tokens": 10, "temperature": 1.0},
        )

        assert r.status_code == 200
        assert r.json()["response"] == "custom"
        gen.assert_called_once_with(
            prompt="p", max_tokens=10, temperature=1.0
        )


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"prompt": ""},
        {"prompt": "ok", "max_tokens": 0},
    ],
)
def test_generate_validation_422(client, body):
    r = client.post("/generate", json=body)

    assert r.status_code == 422
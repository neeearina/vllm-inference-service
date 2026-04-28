# vllm-inference-service

`vllm-inference-service` is an inference service built with `FastAPI` and `vLLM`.
The service exposes an HTTP API for text generation and returns:

- generated text;
- request processing time (`latency_ms`).

The default model in the current configuration is `facebook/opt-125m` (see `app/inference.py`).

## Service Startup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API server:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

After startup, the service is available at `http://127.0.0.1:8000`.

## API

### `POST /generate`

Purpose: generate text from an input prompt.

Request example:

```json
{
  "prompt": "Explain what batching is",
  "max_tokens": 100,
  "temperature": 0.7
}
```

Response example:

```json
{
  "response": "Generated text...",
  "latency_ms": 412.34
}
```

Validation constraints:

- `prompt`: non-empty string;
- `max_tokens`: from 1 to 512;
- `temperature`: from 0.0 to 2.0.

## Experiments

Before running the scripts, make sure the API is already running on `127.0.0.1:8000`.

### 1) Warmup experiment

Script:

```bash
python scripts/warmup_experiment.py
```

Scenario:

- 1 cold request;
- 5 sequential warm requests with the same payload.

Results:

| Metric | Value |
|---|---|
| Cold (1st request) | 627.6 ms |
| Warm #1 | 803.6 ms |
| Warm #2 | 961.4 ms |
| Warm #3 | 448.2 ms |
| Warm #4 | 936.8 ms |
| Warm #5 | 946.8 ms |
| Warm average (5) | 819.3 ms |
| Cold / Warm avg | 0.77x |

In this run, the first request (`627.6 ms`) was faster than the average of the five subsequent requests (`819.3 ms`). This outcome is acceptable for a short observation series and reflects request-to-request latency variability.

### 2) Load test

Script:

```bash
python scripts/load_test.py
```

Scenario: measure average latency and throughput for 1/5/10 concurrent requests.

Results:

| Concurrency | Average latency | Throughput | Success |
|---|---|---|---|
| 1 | 392.8 ms | 2.55 req/s | 1/1 |
| 5 | 2596.5 ms | 1.35 req/s | 5/5 |
| 10 | 3487.4 ms | 1.75 req/s | 10/10 |

As concurrency increases, average latency grows substantially (`392.8 ms` -> `2596.5 ms` -> `3487.4 ms`). This pattern is consistent with limited compute capacity of a single inference process and request queue formation.

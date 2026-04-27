import logging
import time

from fastapi import FastAPI

from app.inference import generate_with_vllm
from app.schemas import GenerateRequest, GenerateResponse

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mini_inference_api")


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    started_at = time.perf_counter()

    output = generate_with_vllm(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )

    latency_ms = (time.perf_counter() - started_at) * 1000
    first_output = output.outputs[0] if output.outputs else None
    generated_text = first_output.text if first_output else ""
    prompt_tokens = len(getattr(output, "prompt_token_ids", []) or request.prompt.split())
    generated_tokens = len(getattr(first_output, "token_ids", []) or generated_text.split())

    logger.info(
        "prompt_tokens=%s generated_tokens=%s latency=%.2fs max_tokens=%s temperature=%.2f",
        prompt_tokens,
        generated_tokens,
        latency_ms / 1000,
        request.max_tokens,
        request.temperature,
    )

    return GenerateResponse(response=generated_text, latency_ms=latency_ms)
    
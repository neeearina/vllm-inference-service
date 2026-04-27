from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Input prompt for generation")
    max_tokens: int = Field(100, ge=1, le=512, description="Maximum generated tokens")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")


class GenerateResponse(BaseModel):
    response: str
    latency_ms: float
    
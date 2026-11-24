from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.llm import LLMRequest, MockLLMProvider

router = APIRouter(prefix="/llm", tags=["LLM"])
provider = MockLLMProvider()


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)
    model: str = "agriculture-gpt-demo"
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=512, ge=1, le=4096)


@router.post("/generate")
async def generate(payload: GenerateRequest) -> dict:
    response = await provider.generate(
        LLMRequest(
            prompt=payload.prompt,
            model=payload.model,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
        )
    )
    return response.to_dict()


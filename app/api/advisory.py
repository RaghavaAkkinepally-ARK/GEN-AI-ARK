from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.prompts import get_prompt
from app.services.security import contains_prompt_injection, contains_sensitive_data

router = APIRouter(prefix="/advisory", tags=["Advisory"])


class AdvisoryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=3000)
    prompt_version: str | None = None


class ImageDiagnosisRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str
    size: int = Field(ge=1, le=10 * 1024 * 1024)
    image_base64: str = Field(min_length=1)
    question: str = ""


@router.post("/answer")
async def answer(payload: AdvisoryRequest) -> dict:
    if contains_prompt_injection(payload.query):
        return {"answer": "I cannot follow instructions that attempt to override safety controls.", "safety_status": "blocked"}
    if contains_sensitive_data(payload.query):
        return {"answer": "Do not include passwords or API keys in agricultural queries.", "safety_status": "blocked"}

    prompt = get_prompt("agriculture_advisory", payload.prompt_version)
    return {
        "answer": "No verified evidence or model provider is available for this query.",
        "prompt": {"name": prompt.name, "version": prompt.version},
        "evidence_status": "unsupported",
        "safety_status": "passed",
    }


@router.post("/diagnose")
async def diagnose(payload: ImageDiagnosisRequest) -> dict:
    if not payload.content_type.lower() in {"image/jpeg", "image/png", "image/webp"}:
        return {
            "answer": "Only JPEG, PNG and WebP images can be reviewed.",
            "status": "unsupported",
            "citations": [],
        }
    if len(payload.image_base64) > 14 * 1024 * 1024:
        return {
            "answer": "The uploaded image is too large.",
            "status": "unsupported",
            "citations": [],
        }
    return {
        "answer": (
            "The image was received successfully, but this local workspace does not yet include "
            "a trained crop-disease computer-vision model. A visual diagnosis would require verified "
            "field or laboratory testing. Before treatment, document symptoms, crop stage and recent "
            "weather, then consult a local agricultural expert."
        ),
        "status": "preview",
        "filename": payload.filename,
        "citations": [],
    }

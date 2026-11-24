from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.llm import router as llm_router
from app.api.rag import router as rag_router
from app.api.advisory import router as advisory_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Cited, secure and extensible agricultural advisory API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router)
app.include_router(rag_router)
app.include_router(advisory_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy", "environment": settings.environment}


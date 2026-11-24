from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.rag import InMemoryRetriever, SourceChunk, citation_from_chunk

router = APIRouter(prefix="/rag", tags=["RAG"])
retriever = InMemoryRetriever([
    SourceChunk("Rice Irrigation Guide", "rice needs standing water for establishment and consistent soil moisture during flowering; drainage is important before harvest", {"topic": "rice", "crop": "rice"}),
    SourceChunk("Rice Nutrient Guide", "rice responds to balanced nitrogen, phosphorus and potassium based on soil testing and the local growing stage", {"topic": "rice", "crop": "rice"}),
    SourceChunk("Rice Pest Guide", "rice pests include stem borers and leaf folders; monitor fields and use integrated pest management before spraying", {"topic": "rice", "crop": "rice"}),
    SourceChunk("Wheat Management Guide", "wheat performs best with timely sowing, crown root irrigation and balanced fertilizer based on soil testing", {"topic": "wheat", "crop": "wheat"}),
    SourceChunk("Maize Management Guide", "maize requires adequate moisture during tasseling and silking, with nitrogen split applications for efficient growth", {"topic": "maize", "crop": "maize"}),
    SourceChunk("Cotton Management Guide", "cotton requires good drainage, pest scouting and careful irrigation to avoid waterlogging and excessive vegetative growth", {"topic": "cotton", "crop": "cotton"}),
    SourceChunk("Bean Management Guide", "beans prefer well-drained soil and moderate irrigation; avoid standing water and manage rust through field rotation and resistant varieties", {"topic": "beans", "crop": "beans"}),
    SourceChunk("Tomato Management Guide", "tomatoes need consistent moisture, mulching, staking and monitoring for early blight, bacterial spot and fruit borers", {"topic": "tomato", "crop": "tomato"}),
    SourceChunk("Potato Management Guide", "potatoes require loose well-drained soil, earthing up and consistent moisture while avoiding foliage wetness late in the day", {"topic": "potato", "crop": "potato"}),
    SourceChunk("Soil Health Guide", "soil testing helps determine pH, organic matter and nutrient needs; organic compost improves soil structure over time", {"topic": "soil", "crop": "general"}),
    SourceChunk("Irrigation Guide", "efficient irrigation uses soil moisture checks, local weather and crop stage to avoid both drought stress and waterlogging", {"topic": "irrigation", "crop": "general"}),
    SourceChunk("Integrated Pest Management", "integrated pest management combines resistant varieties, crop rotation, field monitoring, biological control and targeted chemical use", {"topic": "pest", "crop": "general"}),
])


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=3000)
    k: int = Field(default=4, ge=1, le=20)


@router.post("/query")
async def rag_query(payload: QueryRequest) -> dict:
    chunks, latency_ms = retriever.retrieve(payload.query, payload.k)
    if not chunks:
        return {
            "answer": "I cannot answer this because the knowledge base has no relevant agricultural evidence.",
            "citations": [],
            "evidence_status": "unsupported",
            "retrieval_latency_ms": latency_ms,
        }
    citations = [citation_from_chunk(item) for item in chunks]
    strongest = chunks[0]
    strongest_topic = strongest.chunk.metadata.get("topic", "general")
    topics = ", ".join(dict.fromkeys(
        chunk.chunk.metadata.get("topic", "general")
        for chunk in chunks[:1]
    ))
    passages = strongest.chunk.passage
    return {
        "answer": (
            f"The strongest retrieved evidence relates to {strongest_topic}. {passages}. "
            "Use soil testing, crop-stage monitoring and local expert guidance before changing fertilizer, pesticide or irrigation practices."
        ),
        "citations": citations,
        "evidence_status": "grounded",
        "retrieval_latency_ms": latency_ms,
    }

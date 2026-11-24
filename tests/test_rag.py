from app.services.rag import (
    InMemoryRetriever,
    SourceChunk,
    retrieval_metrics,
)


def test_rag_declines_when_no_chunk_matches():
    retriever = InMemoryRetriever()
    chunks, _ = retriever.retrieve("unrelated satellite policy")

    assert chunks == []


def test_rag_retrieval_and_metrics():
    retriever = InMemoryRetriever([
        SourceChunk("Rice Guide", "rice needs irrigation in dry periods", {"type": "crop"})
    ])
    chunks, latency = retriever.retrieve("rice irrigation", k=1)

    assert len(chunks) == 1
    assert chunks[0].chunk.source == "Rice Guide"
    assert latency >= 0
    metrics = retrieval_metrics(
        {"q1": {"Rice Guide"}},
        {"q1": ["Rice Guide"]},
    )
    assert metrics == {"hit_rate_at_k": 1.0, "mrr": 1.0}


def test_retriever_prefers_cotton_over_unrelated_crops():
    retriever = InMemoryRetriever([
        SourceChunk("Cotton Guide", "cotton requires drainage and pest scouting", {"topic": "cotton"}),
        SourceChunk("Rice Guide", "rice needs irrigation in dry periods", {"topic": "rice"}),
    ])

    chunks, _ = retriever.retrieve("cotton irrigation")

    assert chunks[0].chunk.source == "Cotton Guide"

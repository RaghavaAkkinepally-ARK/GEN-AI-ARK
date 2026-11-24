from dataclasses import dataclass
from math import isclose
from time import perf_counter
from typing import Iterable


@dataclass(frozen=True)
class SourceChunk:
    source: str
    passage: str
    metadata: dict


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: SourceChunk
    score: float


class InMemoryRetriever:
    """Small deterministic retriever used for tests and offline operation."""

    def __init__(self, chunks: Iterable[SourceChunk] | None = None) -> None:
        self.chunks = list(chunks or [])

    def ingest(self, chunk: SourceChunk) -> None:
        self.chunks.append(chunk)

    def retrieve(self, query: str, k: int = 4) -> tuple[list[RetrievedChunk], float]:
        started = perf_counter()
        stop_terms = {
            "a", "an", "and", "are", "can", "for", "how", "in", "is", "it",
            "of", "or", "the", "to", "what", "when", "why", "with", "my",
        }
        query_terms = {
            term.strip(".,?!:;()[]{}\"'")
            for term in query.lower().split()
            if term.strip(".,?!:;()[]{}\"'") not in stop_terms
        }
        ranked = []
        for chunk in self.chunks:
            terms = set(chunk.passage.lower().split())
            overlap = len(query_terms & terms)
            if overlap:
                ranked.append(RetrievedChunk(chunk, overlap / max(1, len(query_terms))))
        ranked.sort(key=lambda item: item.score, reverse=True)
        latency_ms = (perf_counter() - started) * 1000
        return ranked[:k], latency_ms


def citation_from_chunk(chunk: RetrievedChunk) -> dict:
    return {
        "source": chunk.chunk.source,
        "passage": chunk.chunk.passage,
        "score": round(chunk.score, 4),
        "metadata": chunk.chunk.metadata,
    }


def retrieval_metrics(
    relevant_ids: dict[str, set[str]],
    retrieved_ids: dict[str, list[str]],
) -> dict:
    if not relevant_ids:
        return {"hit_rate_at_k": 0.0, "mrr": 0.0}

    hits = 0
    reciprocal_ranks = []
    for query_id, relevant in relevant_ids.items():
        retrieved = retrieved_ids.get(query_id, [])
        rank = next((i + 1 for i, item in enumerate(retrieved) if item in relevant), None)
        if rank is not None:
            hits += 1
            reciprocal_ranks.append(1 / rank)
        else:
            reciprocal_ranks.append(0.0)

    return {
        "hit_rate_at_k": hits / len(relevant_ids),
        "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks),
    }


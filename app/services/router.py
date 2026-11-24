from dataclasses import dataclass
from typing import Literal


Strategy = Literal["prompting", "rag", "qlora"]


@dataclass(frozen=True)
class RoutingDecision:
    strategy: Strategy
    reason: str
    confidence: float


class LearnedStyleRouter:
    """Small feature-based router; replace with a trained classifier when data exists."""

    def route(self, query: str, rag_supported: bool = False) -> RoutingDecision:
        lower = query.lower()
        if rag_supported:
            return RoutingDecision("rag", "Relevant knowledge-base evidence is available", 0.8)
        if any(term in lower for term in ("variety", "diagnosis", "fertilizer", "irrigation")):
            return RoutingDecision("rag", "Query appears to require grounded agricultural evidence", 0.65)
        return RoutingDecision("prompting", "No grounded evidence requirement detected", 0.5)

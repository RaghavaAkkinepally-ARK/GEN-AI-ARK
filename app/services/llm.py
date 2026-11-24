from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any, Protocol


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass(frozen=True)
class LLMUsage:
    input_tokens: int
    output_tokens: int
    latency_ms: float
    estimated_cost_usd: float


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    provider: str
    usage: LLMUsage

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        return result


class TokenCounter(Protocol):
    def count(self, text: str) -> int:
        ...


class CharacterTokenCounter:
    """Deterministic fallback for providers without a tokenizer."""

    def count(self, text: str) -> int:
        return max(1, len(text.encode("utf-8")) // 4) if text else 0


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response through the provider."""


class MockLLMProvider(LLMProvider):
    def __init__(self, token_counter: TokenCounter | None = None) -> None:
        self.token_counter = token_counter or CharacterTokenCounter()

    async def generate(self, request: LLMRequest) -> LLMResponse:
        started = perf_counter()
        text = (
            "Agricultural advice is unavailable from this local mock provider. "
            "Connect a configured provider and consult cited agricultural sources."
        )
        latency_ms = (perf_counter() - started) * 1000
        usage = LLMUsage(
            input_tokens=self.token_counter.count(request.prompt),
            output_tokens=self.token_counter.count(text),
            latency_ms=latency_ms,
            estimated_cost_usd=0.0,
        )
        return LLMResponse(
            text=text,
            model=request.model,
            provider="mock",
            usage=usage,
        )


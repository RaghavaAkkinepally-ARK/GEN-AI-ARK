import asyncio

from app.services.llm import CharacterTokenCounter, LLMRequest, MockLLMProvider


def test_character_token_counter_handles_empty_and_text():
    counter = CharacterTokenCounter()

    assert counter.count("") == 0
    assert counter.count("crop rotation") > 0


def test_mock_provider_returns_usage_and_metadata():
    provider = MockLLMProvider()

    response = asyncio.run(
        provider.generate(LLMRequest(prompt="What is rice?", model="demo"))
    )

    assert response.provider == "mock"
    assert response.model == "demo"
    assert response.usage.input_tokens > 0
    assert response.usage.output_tokens > 0
    assert response.usage.latency_ms >= 0
    assert response.usage.estimated_cost_usd == 0

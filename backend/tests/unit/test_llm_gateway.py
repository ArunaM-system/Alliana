"""Unit tests for LLM Gateway (L4)."""
import pytest
from pydantic import BaseModel
from app.shared_services.llm_gateway.gateway import LLMGateway
from app.shared_services.llm_gateway.providers import MockLLMProvider

class StructuredOutputTest(BaseModel):
    summary: str = "Test summary"
    score: int = 100

@pytest.mark.asyncio
async def test_llm_gateway_completion():
    provider = MockLLMProvider(default_response="Simulated AI reasoning result")
    gateway = LLMGateway(provider=provider)

    res = await gateway.complete("Explain DNS")
    assert res == "Simulated AI reasoning result"

@pytest.mark.asyncio
async def test_llm_gateway_structured():
    provider = MockLLMProvider(default_response='{"summary": "Processed", "score": 95}')
    gateway = LLMGateway(provider=provider)

    result = await gateway.complete_structured("Evaluate", StructuredOutputTest)
    assert isinstance(result, StructuredOutputTest)
    assert result.summary == "Processed"
    assert result.score == 95

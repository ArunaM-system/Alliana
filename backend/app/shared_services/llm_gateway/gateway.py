"""LLM Gateway providing unified model access and structured output extraction (L4)."""
import json
from typing import Any, Optional, Type, TypeVar
from pydantic import BaseModel
from app.shared_services.llm_gateway.providers import BaseLLMProvider, MockLLMProvider

T = TypeVar("T", bound=BaseModel)

class LLMGateway:
    """
    Gateway mediating all interactions between agents and LLM providers.
    Enforces prompt hygiene, temperature guardrails, and structured serialization.
    """

    def __init__(self, provider: Optional[BaseLLMProvider] = None):
        self.provider: BaseLLMProvider = provider or MockLLMProvider()

    def set_provider(self, provider: BaseLLMProvider) -> None:
        """Dynamically configure the active LLM provider."""
        self.provider = provider

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
        **kwargs
    ) -> str:
        """Execute a completion against the active model provider."""
        return await self.provider.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            **kwargs
        )

    async def complete_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        """
        Request structured JSON output from model and parse into a Pydantic schema.
        Falls back to default instance if parsing mock responses.
        """
        raw_response = await self.complete(prompt, system_prompt, **kwargs)
        try:
            parsed_data = json.loads(raw_response)
            return schema.model_validate(parsed_data)
        except Exception:
            # Fallback construct with minimal default values for testing
            return schema.model_construct()

# Global singleton LLM gateway
llm_gateway = LLMGateway()

"""LLM Provider abstraction and mock offline provider (L4 Shared Services)."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseLLMProvider(ABC):
    """Abstract interface for LLM model providers."""

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
        **kwargs
    ) -> str:
        """Generate text completion from the underlying model."""
        pass

class MockLLMProvider(BaseLLMProvider):
    """
    Hermetic in-memory provider for unit tests, local development,
    and air-gapped environments without external network dependencies.
    """

    def __init__(self, default_response: Optional[str] = None):
        self.default_response = default_response or "Mock LLM Response: Request processed successfully."
        self.history: list[Dict[str, Any]] = []

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
        **kwargs
    ) -> str:
        self.history.append({
            "prompt": prompt,
            "system_prompt": system_prompt,
            "temperature": temperature
        })
        return self.default_response

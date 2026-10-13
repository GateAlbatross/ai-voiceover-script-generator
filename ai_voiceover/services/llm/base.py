"""Abstract LLM client interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMError(RuntimeError):
    """Raised for provider-side failures (auth, rate limit, timeout)."""


class LLMClient(ABC):
    name: str = "base"

    @abstractmethod
    def complete(self, *, system: str, user: str, max_tokens: int = 2048) -> str:
        """Return the model's completion as plain text."""

    def health(self) -> bool:
        """Cheap reachability probe. Override if the provider supports it."""
        return True
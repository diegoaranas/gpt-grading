"""Abstract LLM provider interface."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the completion text.

        Args:
            prompt: The full prompt to send.

        Returns:
            The model's response text.
        """
        ...

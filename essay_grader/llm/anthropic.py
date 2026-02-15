"""Anthropic LLM provider."""

from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic API provider (Claude models)."""

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str | None = None):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError(
                "anthropic package is required for the Anthropic provider. "
                "Install it with: pip install essay-grader[anthropic]"
            )
        self.model = model
        self.client = Anthropic(api_key=api_key)

    def complete(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

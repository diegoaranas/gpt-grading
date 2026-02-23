"""LLM provider registry."""

from .base import LLMProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider

PROVIDERS: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
}


def create_provider(
    provider: str,
    model: str | None = None,
    api_key: str | None = None,
) -> LLMProvider:
    """Create an LLM provider by name.

    Args:
        provider: Provider name ("openai" or "anthropic").
        model: Model name (provider-specific). Uses provider default if None.
        api_key: API key. Falls back to environment variable if None.
    """
    if provider not in PROVIDERS:
        available = ", ".join(PROVIDERS)
        raise ValueError(f"Unknown provider: {provider}. Available: {available}")

    kwargs: dict = {}
    if model:
        kwargs["model"] = model
    if api_key:
        kwargs["api_key"] = api_key

    return PROVIDERS[provider](**kwargs)


__all__ = ["LLMProvider", "OpenAIProvider", "AnthropicProvider", "create_provider"]

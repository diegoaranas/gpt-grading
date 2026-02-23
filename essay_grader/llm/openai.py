"""OpenAI LLM provider."""

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (GPT-4, GPT-4o, etc.)."""

    def __init__(self, model: str = "gpt-4o", api_key: str | None = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package is required for the OpenAI provider. "
                "Install it with: pip install essay-grader[openai]"
            )
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def complete(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

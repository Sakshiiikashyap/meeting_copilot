from openai import OpenAI, RateLimitError, APIError
from app.llm.base import LLMProvider
from app.llm.exceptions import LLMRateLimitError, LLMResponseError
from app.core.config import settings

class GroqProvider(LLMProvider):
    def __init__(self):
        # Groq exposes an OpenAI-compatible API — same SDK, different base_url
        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = settings.groq_model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except RateLimitError as e:
            raise LLMRateLimitError(str(e)) from e
        except APIError as e:
            raise LLMResponseError(str(e)) from e

        content = response.choices[0].message.content
        if not content or not content.strip():
            raise LLMResponseError("Provider returned an empty response")

        return content
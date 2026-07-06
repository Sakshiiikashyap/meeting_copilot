from openai import OpenAI, RateLimitError, APIError
from app.llm.base import LLMProvider, LLMResult
from app.llm.exceptions import LLMRateLimitError, LLMResponseError
from app.llm.retry import with_retry
from app.core.config import settings

class GroqProvider(LLMProvider):
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = settings.groq_model

    @with_retry(max_attempts=3, base_delay=1.0)
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
    ) -> LLMResult:
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

        usage = response.usage
        return LLMResult(
            content=content,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )
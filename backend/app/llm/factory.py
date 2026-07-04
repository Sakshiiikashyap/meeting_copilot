from app.llm.base import LLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.llm.groq_provider import GroqProvider
from app.core.config import settings

def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "openai":
        return OpenAIProvider()
    if settings.llm_provider == "groq":
        return GroqProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
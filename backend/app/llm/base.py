from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Abstract base class every LLM provider must implement.
    This is the CONTRACT — any provider (OpenAI, Anthropic, Gemini, Ollama)
    must be swappable behind this exact interface with zero changes
    to any code that calls it.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
    ) -> str:
        """
        Sends a prompt to the LLM and returns the raw text response.
        Every provider must implement this exact signature.
        """
        raise NotImplementedError
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LLMResult:
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
    ) -> LLMResult:
        raise NotImplementedError
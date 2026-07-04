class LLMError(Exception):
    """Base exception for all LLM-layer failures."""
    pass

class LLMRateLimitError(LLMError):
    """Raised when the provider's rate limit is hit."""
    pass

class LLMResponseError(LLMError):
    """Raised when the provider returns an unusable/empty response."""
    pass
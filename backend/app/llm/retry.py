import time
import logging
from functools import wraps
from app.llm.exceptions import LLMRateLimitError, LLMResponseError

logger = logging.getLogger("llm")


def with_retry(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Decorator that retries a function on transient LLM failures,
    using exponential backoff (1s, 2s, 4s...) between attempts.
    Does NOT retry on LLMResponseError — that usually means a genuinely
    bad/malformed response, not a transient issue, so retrying won't help.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except LLMRateLimitError as e:
                    last_exception = e
                    if attempt == max_attempts:
                        break
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        f"Rate limit hit (attempt {attempt}/{max_attempts}). "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
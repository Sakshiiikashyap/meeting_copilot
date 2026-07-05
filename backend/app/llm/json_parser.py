import json
import re
from app.llm.exceptions import LLMResponseError


def extract_json(raw_text: str) -> dict | list:
    """
    LLMs often wrap JSON in markdown code fences or add commentary.
    This strips that noise and parses the actual JSON payload.
    Raises LLMResponseError if nothing valid can be extracted.
    """
    cleaned = raw_text.strip()

    # Strip markdown code fences if present: ```json ... ``` or ``` ... ```
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise LLMResponseError(
            f"AI response was not valid JSON after cleanup: {e}"
        ) from e
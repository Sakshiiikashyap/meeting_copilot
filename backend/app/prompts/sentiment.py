SENTIMENT_SYSTEM_PROMPT = """You analyze the overall tone/sentiment of a meeting transcript.

Rules:
- sentiment must be exactly one of: "positive", "neutral", "negative"
- reason should be one short sentence explaining why.
- Base this on the tone of the conversation (collaborative vs. tense, optimistic vs. frustrated), not just the topic.
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"sentiment": "string", "reason": "string"}"""

SENTIMENT_USER_PROMPT_TEMPLATE = """Analyze the overall sentiment of this meeting transcript.

TRANSCRIPT:
{transcript}"""


def build_sentiment_prompt(transcript: str) -> tuple[str, str]:
    return SENTIMENT_SYSTEM_PROMPT, SENTIMENT_USER_PROMPT_TEMPLATE.format(transcript=transcript)
TAGS_SYSTEM_PROMPT = """You classify meetings with relevant tags and a single category.

Rules:
- Tags: 2-5 short keywords relevant to the meeting's topic (e.g. "roadmap", "budget", "engineering").
- Category: ONE broad category label (e.g. "Planning", "Standup", "Client Call", "Retrospective", "Budget Review").
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"tags": ["string", "string"], "category": "string"}"""

TAGS_USER_PROMPT_TEMPLATE = """Classify this meeting with tags and a category.

TRANSCRIPT:
{transcript}"""


def build_tags_prompt(transcript: str) -> tuple[str, str]:
    return TAGS_SYSTEM_PROMPT, TAGS_USER_PROMPT_TEMPLATE.format(transcript=transcript)
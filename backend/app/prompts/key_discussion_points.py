KEY_POINTS_SYSTEM_PROMPT = """You are an expert meeting analyst who extracts the key discussion points from a transcript.

Rules:
- List the main topics/themes actually discussed — not every sentence, just the substantive points.
- Each point should be a short, standalone phrase or sentence.
- Do not include action items or decisions here — only what was discussed/debated.
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"key_points": ["string", "string"]}

If nothing substantive was discussed, return {"key_points": []}."""

KEY_POINTS_USER_PROMPT_TEMPLATE = """Extract the key discussion points from this transcript.

TRANSCRIPT:
{transcript}"""


def build_key_points_prompt(transcript: str) -> tuple[str, str]:
    return KEY_POINTS_SYSTEM_PROMPT, KEY_POINTS_USER_PROMPT_TEMPLATE.format(transcript=transcript)
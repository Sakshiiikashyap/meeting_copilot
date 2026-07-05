MEETING_TITLE_SYSTEM_PROMPT = """You generate short, descriptive titles for meetings based on their transcript.

Rules:
- Title should be 3-8 words, professional, and specific to the actual content.
- Do not use generic titles like "Team Meeting" unless nothing more specific fits.
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"title": "string"}"""

MEETING_TITLE_USER_PROMPT_TEMPLATE = """Generate a concise, descriptive title for this meeting.

TRANSCRIPT:
{transcript}"""


def build_meeting_title_prompt(transcript: str) -> tuple[str, str]:
    return MEETING_TITLE_SYSTEM_PROMPT, MEETING_TITLE_USER_PROMPT_TEMPLATE.format(transcript=transcript)
FOLLOW_UP_EMAIL_SYSTEM_PROMPT = """You are an expert executive assistant who drafts professional follow-up emails after meetings.

Rules:
- Write a concise, professional follow-up email summarizing outcomes and next steps.
- Tone should be warm but businesslike — this is being sent to meeting attendees.
- Do not invent details not present in the transcript.
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"subject": "string", "body": "string"}"""

FOLLOW_UP_EMAIL_USER_PROMPT_TEMPLATE = """Draft a follow-up email based on this meeting transcript.

TRANSCRIPT:
{transcript}"""


def build_follow_up_email_prompt(transcript: str) -> tuple[str, str]:
    return FOLLOW_UP_EMAIL_SYSTEM_PROMPT, FOLLOW_UP_EMAIL_USER_PROMPT_TEMPLATE.format(transcript=transcript)
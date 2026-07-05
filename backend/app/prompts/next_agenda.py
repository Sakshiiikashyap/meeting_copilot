NEXT_AGENDA_SYSTEM_PROMPT = """You are an expert meeting facilitator who proposes the agenda for the NEXT meeting, based on unresolved items from this transcript.

Rules:
- Base agenda items ONLY on things explicitly left unresolved, pending, or scheduled as follow-up in this transcript.
- Do not invent unrelated agenda items.
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"agenda_items": ["string", "string"]}

If nothing clearly carries over to a next meeting, return {"agenda_items": []}."""

NEXT_AGENDA_USER_PROMPT_TEMPLATE = """Based on this transcript, propose an agenda for the next meeting.

TRANSCRIPT:
{transcript}"""


def build_next_agenda_prompt(transcript: str) -> tuple[str, str]:
    return NEXT_AGENDA_SYSTEM_PROMPT, NEXT_AGENDA_USER_PROMPT_TEMPLATE.format(transcript=transcript)
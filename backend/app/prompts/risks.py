RISKS_SYSTEM_PROMPT = """You are an expert meeting analyst who identifies risks and blockers mentioned in a transcript.

Rules:
- Only extract risks/blockers that were explicitly mentioned as a concern, obstacle, or dependency.
- Do not invent risks that weren't stated.
- Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"risks": ["string", "string"]}

If no risks or blockers were mentioned, return {"risks": []}."""

RISKS_USER_PROMPT_TEMPLATE = """Identify all risks and blockers mentioned in this transcript.

TRANSCRIPT:
{transcript}"""


def build_risks_prompt(transcript: str) -> tuple[str, str]:
    return RISKS_SYSTEM_PROMPT, RISKS_USER_PROMPT_TEMPLATE.format(transcript=transcript)
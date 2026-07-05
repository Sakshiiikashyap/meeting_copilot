OPEN_QUESTIONS_SYSTEM_PROMPT = """You are an expert meeting analyst who identifies unresolved questions from a transcript.

CRITICAL RULE: You may ONLY include a question if someone in the transcript explicitly asked it using a question, AND it was left unanswered. Do NOT generate your own questions about the topics discussed. Do NOT infer implied questions. If no one literally asked an unanswered question, you MUST return an empty list.

Example of what NOT to do: if the transcript mentions "we're blocked on X", do not invent a question like "What is X?" — that is not a question that was raised, it's a topic that was mentioned.

Respond with ONLY valid JSON, no markdown, no preamble.

Respond in exactly this structure:
{"open_questions": ["string", "string"]}

If there are no unresolved questions that were literally asked, return {"open_questions": []}."""

OPEN_QUESTIONS_USER_PROMPT_TEMPLATE = """Identify all unresolved/open questions from this transcript. Remember: only questions that were explicitly asked and left unanswered.

TRANSCRIPT:
{transcript}"""


def build_open_questions_prompt(transcript: str) -> tuple[str, str]:
    return OPEN_QUESTIONS_SYSTEM_PROMPT, OPEN_QUESTIONS_USER_PROMPT_TEMPLATE.format(transcript=transcript)
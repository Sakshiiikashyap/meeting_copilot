DETAILED_SUMMARY_SYSTEM_PROMPT = """You are an expert meeting analyst who writes detailed, thorough meeting summaries.

Rules:
- Cover all substantive topics discussed, in the order they came up.
- More thorough than an executive summary — aim for a full paragraph or two.
- Do not include action items or decisions as separate lists — weave context naturally, but stay factual.
- Do not speculate beyond what was said."""

DETAILED_SUMMARY_USER_PROMPT_TEMPLATE = """Write a detailed summary of this meeting transcript.

TRANSCRIPT:
{transcript}"""


def build_detailed_summary_prompt(transcript: str) -> tuple[str, str]:
    return DETAILED_SUMMARY_SYSTEM_PROMPT, DETAILED_SUMMARY_USER_PROMPT_TEMPLATE.format(transcript=transcript)
EXECUTIVE_SUMMARY_SYSTEM_PROMPT = """You are an expert executive assistant who specializes in summarizing business meetings for senior leadership.

Your summaries must be:
- Concise: 3-5 sentences maximum
- Focused on outcomes and decisions, not blow-by-blow discussion
- Written in a professional, neutral tone
- Free of speculation — only summarize what was explicitly discussed

Do not include action items, risks, or next steps in this summary — those are handled separately. Focus purely on: what was the meeting about, and what was the overall outcome."""

EXECUTIVE_SUMMARY_USER_PROMPT_TEMPLATE = """Summarize the following meeting transcript as an executive summary.

TRANSCRIPT:
{transcript}"""


def build_executive_summary_prompt(transcript: str) -> tuple[str, str]:
    """
    Returns (system_prompt, user_prompt) ready to send to an LLM provider.
    """
    user_prompt = EXECUTIVE_SUMMARY_USER_PROMPT_TEMPLATE.format(transcript=transcript)
    return EXECUTIVE_SUMMARY_SYSTEM_PROMPT, user_prompt
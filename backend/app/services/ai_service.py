from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.llm.factory import get_llm_provider
from app.llm.exceptions import LLMRateLimitError, LLMResponseError
from app.prompts.executive_summary import build_executive_summary_prompt
from app.repositories import meeting_repository
from app.models.meeting import Meeting


def generate_executive_summary(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_executive_summary_prompt(meeting.raw_transcript)

    provider = get_llm_provider()

    try:
        summary = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=300,
        )
    except LLMRateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="AI provider rate limit reached. Please try again shortly.",
        )
    except LLMResponseError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider returned an invalid response. Please try again.",
        )

    meeting.executive_summary = summary
    meeting.status = "completed"
    db.commit()
    db.refresh(meeting)
    return meeting
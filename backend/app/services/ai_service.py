from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.llm.factory import get_llm_provider
from app.llm.exceptions import LLMRateLimitError, LLMResponseError
from app.prompts.executive_summary import build_executive_summary_prompt
from app.repositories import meeting_repository
from app.models.meeting import Meeting
from app.prompts.action_items import build_action_items_prompt
from app.schemas.ai_outputs import ActionItemsResponse
from app.llm.json_parser import extract_json
import json
from app.prompts.decisions import build_decisions_prompt
from app.schemas.ai_outputs import DecisionsResponse
from app.prompts.detailed_summary import build_detailed_summary_prompt
from app.prompts.key_discussion_points import build_key_points_prompt
from app.prompts.risks import build_risks_prompt
from app.prompts.open_questions import build_open_questions_prompt
from app.prompts.follow_up_email import build_follow_up_email_prompt
from app.prompts.next_agenda import build_next_agenda_prompt
from app.prompts.meeting_title import build_meeting_title_prompt
from app.prompts.tags_category import build_tags_prompt
from app.prompts.sentiment import build_sentiment_prompt
from app.schemas.ai_outputs import (
    RisksResponse, OpenQuestionsResponse, FollowUpEmailResponse,
    NextAgendaResponse, MeetingTitleResponse, MeetingTagsResponse,
    SentimentResponse, KeyPointsResponse,
)



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

def generate_action_items(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_action_items_prompt(meeting.raw_transcript)
    provider = get_llm_provider()

    try:
        raw_response = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
            max_tokens=800,
        )
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(raw_response)

    try:
        validated = ActionItemsResponse(**parsed)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI response didn't match expected structure: {e}",
        )

    meeting.action_items = json.dumps([item.model_dump() for item in validated.action_items])
    db.commit()
    db.refresh(meeting)
    return meeting
def generate_decisions(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_decisions_prompt(meeting.raw_transcript)
    provider = get_llm_provider()

    try:
        raw_response = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
            max_tokens=800,
        )
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(raw_response)

    try:
        validated = DecisionsResponse(**parsed)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI response didn't match expected structure: {e}",
        )

    meeting.decisions = json.dumps([d.model_dump() for d in validated.decisions])
    db.commit()
    db.refresh(meeting)
    return meeting

def generate_detailed_summary(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_detailed_summary_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        summary = provider.generate(system_prompt, user_prompt, temperature=0.3, max_tokens=600)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    meeting.detailed_summary = summary
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_key_points(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_key_points_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=600)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = KeyPointsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.key_discussion_points = json.dumps(validated.key_points)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_risks(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_risks_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=500)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = RisksResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.risks = json.dumps(validated.risks)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_open_questions(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_open_questions_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=500)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = OpenQuestionsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.open_questions = json.dumps(validated.open_questions)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_follow_up_email(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_follow_up_email_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.4, max_tokens=500)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = FollowUpEmailResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.follow_up_email = json.dumps(validated.model_dump())
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_next_agenda(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_next_agenda_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = NextAgendaResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.next_meeting_agenda = json.dumps(validated.agenda_items)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_meeting_title(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_meeting_title_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.3, max_tokens=100)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = MeetingTitleResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.ai_title = validated.title
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_tags_and_category(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_tags_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=200)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = MeetingTagsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.tags = json.dumps(validated.tags)
    meeting.category = validated.category
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_sentiment(db: Session, meeting: Meeting) -> Meeting:
    system_prompt, user_prompt = build_sentiment_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        raw = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=150)
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    parsed = extract_json(raw)
    try:
        validated = SentimentResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")
    meeting.sentiment = validated.sentiment
    meeting.sentiment_reason = validated.reason
    db.commit()
    db.refresh(meeting)
    return meeting
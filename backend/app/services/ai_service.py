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
import logging

logger = logging.getLogger("ai_service")


def generate_executive_summary(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating executive summary for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_executive_summary_prompt(meeting.raw_transcript)
    provider = get_llm_provider()

    try:
        result = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=300,
        )
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached. Please try again shortly.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response. Please try again.")

    logger.info(f"Executive summary generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.executive_summary = result.content
    meeting.status = "completed"
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_action_items(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating action items for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_action_items_prompt(meeting.raw_transcript)
    provider = get_llm_provider()

    try:
        result = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
            max_tokens=800,
        )
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)

    try:
        validated = ActionItemsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Action items generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.action_items = json.dumps([item.model_dump() for item in validated.action_items])
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_decisions(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating decisions for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_decisions_prompt(meeting.raw_transcript)
    provider = get_llm_provider()

    try:
        result = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
            max_tokens=800,
        )
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)

    try:
        validated = DecisionsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Decisions generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.decisions = json.dumps([d.model_dump() for d in validated.decisions])
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_detailed_summary(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating detailed summary for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_detailed_summary_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.3, max_tokens=600)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    logger.info(f"Detailed summary generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.detailed_summary = result.content
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_key_points(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating key points for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_key_points_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=600)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = KeyPointsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Key points generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.key_discussion_points = json.dumps(validated.key_points)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_risks(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating risks for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_risks_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=500)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = RisksResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Risks generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.risks = json.dumps(validated.risks)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_open_questions(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating open questions for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_open_questions_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=500)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = OpenQuestionsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Open questions generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.open_questions = json.dumps(validated.open_questions)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_follow_up_email(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating follow-up email for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_follow_up_email_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.4, max_tokens=500)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = FollowUpEmailResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Follow-up email generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.follow_up_email = json.dumps(validated.model_dump())
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_next_agenda(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating next agenda for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_next_agenda_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=500)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = NextAgendaResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Next agenda generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.next_meeting_agenda = json.dumps(validated.agenda_items)
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_meeting_title(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating meeting title for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_meeting_title_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.3, max_tokens=100)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = MeetingTitleResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Meeting title generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.ai_title = validated.title
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_tags_and_category(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating tags/category for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_tags_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=200)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = MeetingTagsResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Tags/category generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.tags = json.dumps(validated.tags)
    meeting.category = validated.category
    db.commit()
    db.refresh(meeting)
    return meeting


def generate_sentiment(db: Session, meeting: Meeting) -> Meeting:
    logger.info(f"Generating sentiment for meeting_id={meeting.id}")
    system_prompt, user_prompt = build_sentiment_prompt(meeting.raw_transcript)
    provider = get_llm_provider()
    try:
        result = provider.generate(system_prompt, user_prompt, temperature=0.1, max_tokens=150)
    except LLMRateLimitError:
        logger.error(f"Rate limit hit for meeting_id={meeting.id}")
        raise HTTPException(status_code=429, detail="AI provider rate limit reached.")
    except LLMResponseError:
        logger.error(f"Invalid AI response for meeting_id={meeting.id}")
        raise HTTPException(status_code=502, detail="AI provider returned an invalid response.")

    parsed = extract_json(result.content)
    try:
        validated = SentimentResponse(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI response didn't match expected structure: {e}")

    logger.info(f"Sentiment generated for meeting_id={meeting.id} (tokens: {result.total_tokens})")
    meeting.sentiment = validated.sentiment
    meeting.sentiment_reason = validated.reason
    db.commit()
    db.refresh(meeting)
    return meeting
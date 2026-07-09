from app.services import ai_service
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.meeting import MeetingCreate, MeetingResponse, MeetingListItem, MeetingUpdate
from app.services import meeting_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.middleware.rate_limit import limiter
from app.utils.file_parser import parse_transcript_file

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("/", response_model=MeetingResponse)
def create_meeting(
    meeting_in: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return meeting_service.create_meeting(db, meeting_in, current_user.id)


@router.get("/", response_model=list[MeetingListItem])
def list_meetings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return meeting_service.get_user_meetings(db, current_user.id)


@router.get("/search/", response_model=list[MeetingListItem])
def search_meetings(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return meeting_service.search_meetings(db, current_user.id, q)


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return meeting_service.get_meeting(db, meeting_id, current_user.id)


@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: int,
    updates: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return meeting_service.update_meeting(db, meeting_id, current_user.id, updates)


@router.delete("/{meeting_id}", status_code=204)
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting_service.delete_meeting(db, meeting_id, current_user.id)


@router.post("/upload", response_model=MeetingResponse)
async def upload_meeting(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contents = await file.read()
    transcript_text = parse_transcript_file(file.filename, contents)

    meeting_in = MeetingCreate(title=title, raw_transcript=transcript_text)
    return meeting_service.create_meeting(db, meeting_in, current_user.id)


@router.post("/{meeting_id}/summarize", response_model=MeetingResponse)
@limiter.limit("5/minute")
def summarize_meeting(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_executive_summary(db, meeting)


@router.post("/{meeting_id}/action-items", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_action_items(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_action_items(db, meeting)


@router.post("/{meeting_id}/decisions", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_decisions(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_decisions(db, meeting)


@router.post("/{meeting_id}/detailed-summary", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_detailed_summary(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_detailed_summary(db, meeting)


@router.post("/{meeting_id}/key-points", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_key_points(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_key_points(db, meeting)


@router.post("/{meeting_id}/risks", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_risks(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_risks(db, meeting)


@router.post("/{meeting_id}/open-questions", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_open_questions(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_open_questions(db, meeting)


@router.post("/{meeting_id}/follow-up-email", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_follow_up_email(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_follow_up_email(db, meeting)


@router.post("/{meeting_id}/next-agenda", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_next_agenda(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_next_agenda(db, meeting)


@router.post("/{meeting_id}/ai-title", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_meeting_title(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_meeting_title(db, meeting)


@router.post("/{meeting_id}/tags", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_tags(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_tags_and_category(db, meeting)


@router.post("/{meeting_id}/sentiment", response_model=MeetingResponse)
@limiter.limit("5/minute")
def extract_sentiment(
    request: Request,
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    return ai_service.generate_sentiment(db, meeting)
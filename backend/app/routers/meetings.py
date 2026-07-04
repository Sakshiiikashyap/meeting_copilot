from app.services import ai_service
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.meeting import MeetingCreate, MeetingResponse, MeetingListItem
from app.services import meeting_service
from app.dependencies.auth import get_current_user
from app.models.user import User

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

@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return meeting_service.get_meeting(db, meeting_id, current_user.id)

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
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported right now")

    contents = await file.read()
    transcript_text = contents.decode("utf-8")

    meeting_in = MeetingCreate(title=title, raw_transcript=transcript_text)
    return meeting_service.create_meeting(db, meeting_in, current_user.id)

@router.post("/{meeting_id}/summarize", response_model=MeetingResponse)
def summarize_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)  # reuses ownership check
    return ai_service.generate_executive_summary(db, meeting)
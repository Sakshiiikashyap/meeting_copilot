from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import meeting_repository
from app.schemas.meeting import MeetingCreate
from app.models.meeting import Meeting

def create_meeting(db: Session, meeting_in: MeetingCreate, user_id: int) -> Meeting:
    if not meeting_in.raw_transcript.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcript cannot be empty",
        )
    return meeting_repository.create_meeting(db, meeting_in, user_id)

def get_meeting(db: Session, meeting_id: int, user_id: int) -> Meeting:
    meeting = meeting_repository.get_by_id(db, meeting_id)
    if meeting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    if meeting.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your meeting")
    return meeting

def get_user_meetings(db: Session, user_id: int) -> list[Meeting]:
    return meeting_repository.get_all_for_user(db, user_id)

def delete_meeting(db: Session, meeting_id: int, user_id: int) -> None:
    meeting = get_meeting(db, meeting_id, user_id)  # reuses ownership check above
    meeting_repository.delete_meeting(db, meeting)
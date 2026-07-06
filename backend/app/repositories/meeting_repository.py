from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate

def create_meeting(db: Session, meeting_in: MeetingCreate, user_id: int) -> Meeting:
    meeting = Meeting(
        title=meeting_in.title,
        raw_transcript=meeting_in.raw_transcript,
        user_id=user_id,
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

def get_by_id(db: Session, meeting_id: int) -> Meeting | None:
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()

def get_all_for_user(db: Session, user_id: int) -> list[Meeting]:
    return db.query(Meeting).filter(Meeting.user_id == user_id).order_by(Meeting.created_at.desc()).all()

def delete_meeting(db: Session, meeting: Meeting) -> None:
    db.delete(meeting)
    db.commit()
    
def search_for_user(db: Session, user_id: int, query: str) -> list[Meeting]:
    return (
        db.query(Meeting)
        .filter(Meeting.user_id == user_id)
        .filter(Meeting.title.ilike(f"%{query}%"))
        .order_by(Meeting.created_at.desc())
        .all()
    )
    
def update_meeting(db: Session, meeting: Meeting, updates: dict) -> Meeting:
    for field, value in updates.items():
        setattr(meeting, field, value)
    db.commit()
    db.refresh(meeting)
    return meeting
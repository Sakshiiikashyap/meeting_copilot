from pydantic import BaseModel
from datetime import datetime

class MeetingCreate(BaseModel):
    title: str
    raw_transcript: str

class MeetingResponse(BaseModel):
    id: int
    user_id: int
    title: str
    raw_transcript: str
    status: str
    executive_summary: str | None
    detailed_summary: str | None
    action_items: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MeetingListItem(BaseModel):
    """Lighter schema for list views — excludes full transcript to keep payload small."""
    id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
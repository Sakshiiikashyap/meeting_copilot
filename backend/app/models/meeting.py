from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    raw_transcript = Column(Text, nullable=False)
    status = Column(String, default="uploaded", nullable=False)

    # AI-generated fields — all nullable, filled in progressively from Week 3 onward
    executive_summary = Column(Text, nullable=True)
    detailed_summary = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    decisions = Column(Text, nullable=True)
    key_discussion_points = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    open_questions = Column(Text, nullable=True)
    follow_up_email = Column(Text, nullable=True)
    next_meeting_agenda = Column(Text, nullable=True)
    ai_title = Column(String, nullable=True)
    tags = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    sentiment_reason = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # relationship: lets you do meeting.owner to get the User object
    owner = relationship("User", back_populates="meetings")
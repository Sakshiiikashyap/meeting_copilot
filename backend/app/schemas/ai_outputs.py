from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: str | None = None
    due_date: str | None = None


class ActionItemsResponse(BaseModel):
    action_items: list[ActionItem]


class Decision(BaseModel):
    decision: str
    context: str | None = None


class DecisionsResponse(BaseModel):
    decisions: list[Decision]


class RisksResponse(BaseModel):
    risks: list[str]


class MeetingTagsResponse(BaseModel):
    tags: list[str]
    category: str
    
class KeyPointsResponse(BaseModel):
    key_points: list[str]


class OpenQuestionsResponse(BaseModel):
    open_questions: list[str]


class FollowUpEmailResponse(BaseModel):
    subject: str
    body: str


class NextAgendaResponse(BaseModel):
    agenda_items: list[str]


class MeetingTitleResponse(BaseModel):
    title: str


class SentimentResponse(BaseModel):
    sentiment: str  # "positive", "neutral", or "negative"
    reason: str
from pydantic import BaseModel
from typing import Optional

class ActionItem(BaseModel):
    owner: Optional[str] = None
    task: str
    deadline: Optional[str] = None


class MeetingAnalysis(BaseModel):
    summary: str
    discussion_topics: list[str]
    action_items: list[ActionItem]
    decisions: list[str]
    unresolved_questions: list[str]
    risks: list[str]
    sentiment: str
    deal_intelligence: list[str]
    financial_figures: list[str]
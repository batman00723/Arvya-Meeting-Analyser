from typing import TypedDict
from .schemas import MeetingAnalysis

class MeetingState(TypedDict):
    transcript: str
    result: MeetingAnalysis | None
    status: str

"""
AI Meeting Minutes Generator
Pydantic Data Models
"""

from typing import List, Optional, Any
from pydantic import BaseModel, Field


# ============================================================
# HEALTH RESPONSE
# ============================================================

class HealthResponse(BaseModel):
    status: str
    message: str


# ============================================================
# MEETING RESPONSE
# ============================================================

class MeetingResponse(BaseModel):
    status: str
    message: str
    filename: str
    transcript: str
    minutes: Any


# ============================================================
# MEETING SUMMARY
# ============================================================

class MeetingSummary(BaseModel):
    title: str = Field(
        default="Meeting Summary",
        description="Title of the meeting"
    )

    summary: str = Field(
        default="",
        description="Short summary of the meeting"
    )

    date: Optional[str] = Field(
        default=None,
        description="Meeting date"
    )

    duration: Optional[float] = Field(
        default=0,
        description="Meeting duration in minutes"
    )


# ============================================================
# ACTION ITEM
# ============================================================

class ActionItem(BaseModel):
    title: str = Field(
        ...,
        description="Action item description"
    )

    assignee: Optional[str] = Field(
        default=None,
        description="Person responsible for the action"
    )

    due_date: Optional[str] = Field(
        default=None,
        description="Due date for the action"
    )

    completed: bool = False


# ============================================================
# DECISION
# ============================================================

class Decision(BaseModel):
    decision: str = Field(
        ...,
        description="Decision made during the meeting"
    )


# ============================================================
# PARTICIPANT
# ============================================================

class Participant(BaseModel):
    name: str = Field(
        ...,
        description="Participant name"
    )

    role: Optional[str] = Field(
        default=None,
        description="Participant role"
    )


# ============================================================
# STRUCTURED MEETING MINUTES
# ============================================================

class MeetingMinutes(BaseModel):
    title: str = "Meeting Minutes"

    summary: str = ""

    key_points: List[str] = Field(
        default_factory=list
    )

    decisions: List[Decision] = Field(
        default_factory=list
    )

    action_items: List[ActionItem] = Field(
        default_factory=list
    )

    participants: List[Participant] = Field(
        default_factory=list
    )


# ============================================================
# MEETING DATABASE RESPONSE
# ============================================================

class MeetingRecord(BaseModel):
    id: int

    filename: str

    transcript: Optional[str] = ""

    minutes: Optional[Any] = ""

    status: str = "Completed"

    duration: float = 0

    created_at: Optional[str] = None


# ============================================================
# ACTION ITEM RESPONSE
# ============================================================

class ActionItemResponse(BaseModel):
    id: int

    meeting_id: int

    title: str

    assignee: Optional[str] = None

    due_date: Optional[str] = None

    completed: bool = False

    created_at: Optional[str] = None


# ============================================================
# DECISION RESPONSE
# ============================================================

class DecisionResponse(BaseModel):
    id: int

    meeting_id: int

    decision: str

    created_at: Optional[str] = None


# ============================================================
# PARTICIPANT RESPONSE
# ============================================================

class ParticipantResponse(BaseModel):
    id: int

    meeting_id: int

    name: str

    role: Optional[str] = None

    created_at: Optional[str] = None


# ============================================================
# API ERROR RESPONSE
# ============================================================

class ErrorResponse(BaseModel):
    status: str = "error"

    message: str

    detail: Optional[str] = None


# ============================================================
# DATABASE STATISTICS
# ============================================================

class DatabaseStatistics(BaseModel):
    total_meetings: int = 0

    total_action_items: int = 0

    total_decisions: int = 0

    total_participants: int = 0
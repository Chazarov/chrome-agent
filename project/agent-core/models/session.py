# Session model for storing conversation history
# Used by database layer to persist agent interactions
# Tracks the lifecycle of a user interaction with the agent

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class Message(BaseModel):
    role: str = Field(..., description="Role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)


class Session(BaseModel):
    id: Optional[str] = Field(None, description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=list, description="Conversation history")
    status: SessionStatus = Field(default=SessionStatus.ACTIVE, description="Current session status")

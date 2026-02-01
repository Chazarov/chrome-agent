"""
Debug information models for agent execution tracking.

Used by DebugCollector to store chronological events during task execution.
Includes reasoning, tool calls, and tool results with timestamps.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DebugEventType(str, Enum):
    """Type of debug event"""
    REASONING = "reasoning"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class DebugEvent(BaseModel):
    """
    Single debug event in chronological order.
    Represents one step in agent execution.
    """
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When this event occurred"
    )
    type: DebugEventType = Field(
        description="Type of event (reasoning, tool_call, or tool_result)"
    )
    content: Optional[str] = Field(
        default=None,
        description="Content for reasoning events"
    )
    tool_name: Optional[str] = Field(
        default=None,
        description="Name of tool for tool_call and tool_result events"
    )
    arguments: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arguments passed to tool for tool_call events"
    )
    result: Optional[str] = Field(
        default=None,
        description="Result returned by tool for tool_result events"
    )


class DebugInfo(BaseModel):
    """
    Complete debug information for a single user task.
    Stores all events in chronological order from task start to completion.
    Saved to last-task-info.json file.
    """
    task: str = Field(
        description="Original user task/prompt"
    )
    started_at: datetime = Field(
        default_factory=datetime.now,
        description="When task execution started"
    )
    events: List[DebugEvent] = Field(
        default_factory=list,
        description="Chronological list of all events during execution"
    )
    completed: bool = Field(
        default=False,
        description="Whether task execution completed successfully"
    )

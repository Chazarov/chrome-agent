"""
Debug information collector for agent execution tracking.

Singleton class that collects all debug events (reasoning, tool calls, results)
in chronological order and saves them to last-task-info.json.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from models.debug import DebugInfo, DebugEvent, DebugEventType


class DebugCollector:
    """
    Singleton collector for debug information.
    Gathers all agent events during task execution.
    """
    _instance: Optional['DebugCollector'] = None
    
    def __init__(self):
        if DebugCollector._instance is not None:
            raise RuntimeError("Use get_instance() to access DebugCollector")
        self.debug_info: Optional[DebugInfo] = None
        self.output_path = Path("last-task-info.json")
    
    @classmethod
    def get_instance(cls) -> 'DebugCollector':
        """Get singleton instance of DebugCollector"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def reset(self, task: str) -> None:
        """
        Reset collector for new user prompt and save initial state.
        
        Args:
            task: User task/prompt text
        """
        self.debug_info = DebugInfo(
            task=task,
            started_at=datetime.now(),
            events=[],
            completed=False
        )
        self.save()
    
    def add_reasoning(self, content: str) -> None:
        """
        Add model reasoning event and save immediately.
        
        Args:
            content: Reasoning text from model
        """
        if self.debug_info is None:
            return
        
        event = DebugEvent(
            timestamp=datetime.now(),
            type=DebugEventType.REASONING,
            content=content
        )
        self.debug_info.events.append(event)
        self.save()
    
    def add_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> None:
        """
        Add tool call event and save immediately.
        
        Args:
            tool_name: Name of tool being called
            arguments: Arguments passed to tool
        """
        if self.debug_info is None:
            return
        
        event = DebugEvent(
            timestamp=datetime.now(),
            type=DebugEventType.TOOL_CALL,
            tool_name=tool_name,
            arguments=arguments
        )
        self.debug_info.events.append(event)
        self.save()
    
    def add_tool_result(self, tool_name: str, result: str) -> None:
        """
        Add tool result event and save immediately.
        
        Args:
            tool_name: Name of tool that executed
            result: Result returned by tool
        """
        if self.debug_info is None:
            return
        
        event = DebugEvent(
            timestamp=datetime.now(),
            type=DebugEventType.TOOL_RESULT,
            tool_name=tool_name,
            result=result
        )
        self.debug_info.events.append(event)
        self.save()
    
    def mark_completed(self) -> None:
        """Mark task as completed and save"""
        if self.debug_info is not None:
            self.debug_info.completed = True
            self.save()
    
    def save(self) -> None:
        """Save debug information to JSON file"""
        if self.debug_info is None:
            return
        
        data = self.debug_info.model_dump(mode='json')
        
        # Convert datetime objects to ISO format strings
        data['started_at'] = self.debug_info.started_at.isoformat()
        for event in data['events']:
            if isinstance(event.get('timestamp'), datetime):
                event['timestamp'] = event['timestamp'].isoformat()
            elif 'timestamp' in event:
                pass  # Already converted by model_dump
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

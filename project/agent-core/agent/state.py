from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from models.page import Page


class AgentState(TypedDict):
    """State for the browser automation agent"""
    messages: Annotated[List[BaseMessage], add_messages]
    current_page: Optional[Page]
    task: str
    completed: bool
    error: Optional[str]

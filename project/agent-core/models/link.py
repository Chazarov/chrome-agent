# Link model for hyperlinks on the page
# Used by Parser to extract navigation options
# Represents <a> tags with href attributes

from typing import Optional
from pydantic import BaseModel, Field


class Link(BaseModel):
    """Link model for agent. Agent uses URL directly with navigate() tool."""
    text: str = Field(..., description="Visible text content of the link")
    url: str = Field(..., description="Target URL of the link")
    parent_text: Optional[str] = Field(None, description="Text content of parent container(s)")
    
    class Config:
        frozen = True

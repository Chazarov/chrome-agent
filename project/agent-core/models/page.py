# Page model containing all extracted page information
# Main data structure passed to the agent for decision making
# Aggregates all interactive elements and text content from the current page

from typing import List
from pydantic import BaseModel, Field

from .button import Button
from .link import Link


class Page(BaseModel):
    url: str = Field(..., description="Current page URL")
    title: str = Field(..., description="Page title from <title> tag")
    visible_text: str = Field(..., description="All visible text content on the page")
    buttons: List[Button] = Field(default_factory=list, description="List of clickable buttons")
    links: List[Link] = Field(default_factory=list, description="List of hyperlinks")
    
    class Config:
        frozen = True

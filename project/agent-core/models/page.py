# Page item models for paginated page information
# Each model represents a portion of page data for the agent
# Supports pagination to avoid context overflow

from typing import List
from pydantic import BaseModel, Field

from .button import Button
from .link import Link
from .input_field import Input


class PageTextItem(BaseModel):
    """Text chunk from page content."""
    item_id: int = Field(..., description="Sequential ID of this text chunk")
    total_items: int = Field(..., description="Total number of text chunks")
    url: str = Field(..., description="Current page URL")
    title: str = Field(..., description="Page title from <title> tag")
    text_chunk: str = Field(..., description="Portion of visible text")
    
    class Config:
        frozen = True


class PageButtonsItem(BaseModel):
    """Buttons and input fields from a Y-coordinate section of the page."""
    item_id: int = Field(..., description="Sequential ID of this buttons item")
    total_items: int = Field(..., description="Total number of button items")
    url: str = Field(..., description="Current page URL")
    title: str = Field(..., description="Page title from <title> tag")
    buttons: List[Button] = Field(default_factory=list, description="Buttons in this Y-range")
    inputs: List[Input] = Field(default_factory=list, description="Input fields in this Y-range")
    
    class Config:
        frozen = True


class PageLinksItem(BaseModel):
    """Links chunk from page content."""
    item_id: int = Field(..., description="Sequential ID of this links item")
    total_items: int = Field(..., description="Total number of links items")
    url: str = Field(..., description="Current page URL")
    title: str = Field(..., description="Page title from <title> tag")
    links: List[Link] = Field(default_factory=list, description="Links in this chunk")
    
    class Config:
        frozen = True

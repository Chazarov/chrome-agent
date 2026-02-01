# Button model representing clickable elements on a webpage
# Used by Parser to extract and identify interactive elements
# This model captures buttons, ARIA button roles, and input submit/button elements

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from playwright.async_api import Locator


class ButtonInternal:
    """Internal button model with Playwright element reference.
    Stored in BrowserManager for click operations."""
    
    def __init__(
        self, 
        element_id: int, 
        element: Locator, 
        text: str, 
        position: Tuple[float, float], 
        parent_text: Optional[str] = None
    ):
        self.id = element_id
        self.element = element
        self.text = text
        self.position = position
        self.parent_text = parent_text


class Button(BaseModel):
    """Button model for agent. Contains only information needed for decision making."""
    id: int = Field(..., description="Unique ID to interact with this button")
    text: str = Field(..., description="Visible text content of the button")
    position: Tuple[float, float] = Field(..., description="X, Y coordinates of the button center")
    parent_text: Optional[str] = Field(None, description="Text content of parent container(s)")
    
    class Config:
        frozen = True

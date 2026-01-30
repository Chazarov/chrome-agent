# Button model representing clickable elements on a webpage
# Used by Parser to extract and identify interactive elements
# This model captures buttons, ARIA button roles, and input submit/button elements

from typing import Optional, Tuple
from pydantic import BaseModel, Field


class Button(BaseModel):
    text: str = Field(..., description="Visible text content of the button")
    position: Tuple[float, float] = Field(..., description="X, Y coordinates of the button center")
    parent_text: Optional[str] = Field(None, description="Text content of parent container(s)")
    selector: str = Field(..., description="CSS selector or XPath to interact with this button")
    
    class Config:
        frozen = True

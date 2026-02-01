# Input model for text input fields on the page
# Used by Parser to extract form elements
# Represents input[type=text|email|password|...] and textarea elements

from typing import Optional, Tuple
from pydantic import BaseModel, Field
from playwright.async_api import Locator


class InputInternal:
    """Internal input model with Playwright element reference.
    Stored in BrowserManager for type/fill operations."""
    
    def __init__(
        self,
        element_id: int,
        element: Locator,
        input_type: str,
        name: str,
        placeholder: str,
        position: Tuple[float, float],
        parent_text: Optional[str] = None
    ):
        self.id = element_id
        self.element = element
        self.input_type = input_type
        self.name = name
        self.placeholder = placeholder
        self.position = position
        self.parent_text = parent_text


class Input(BaseModel):
    """Input model for agent. Contains information for decision making."""
    id: int = Field(..., description="Unique ID to interact with this input")
    input_type: str = Field(..., description="Type of input (text, email, password, etc.)")
    name: str = Field(..., description="Name attribute of the input")
    placeholder: str = Field(..., description="Placeholder text")
    position: Tuple[float, float] = Field(..., description="X, Y coordinates")
    parent_text: Optional[str] = Field(None, description="Text content of parent container(s)")
    
    class Config:
        frozen = True

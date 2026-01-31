"""
Pydantic schemas for agent tool arguments.
These schemas define the expected input format for each tool and are used by LangChain
to generate proper JSON Schema for LLM function calling.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NavigateInput(BaseModel):
    """Input schema for navigate tool."""
    url: str = Field(
        description="URL to navigate to (e.g., 'https://example.com' or 'google.com'). Protocol (https://) will be added automatically if missing."
    )


class ClickButtonInput(BaseModel):
    """Input schema for click_button tool."""
    selector: str = Field(
        description="CSS selector of the element to click (e.g., '#submit-btn', '.button-class', 'button[type=\"submit\"]')"
    )


class FillInputArgs(BaseModel):
    """Input schema for fill_input tool."""
    selector: str = Field(
        description="CSS selector of the input field to fill"
    )
    text: str = Field(
        description="Text to fill into the input field (clears existing content first)"
    )


class TypeTextInput(BaseModel):
    """Input schema for type_text tool."""
    selector: str = Field(
        description="CSS selector of the input field"
    )
    text: str = Field(
        description="Text to type into the field (appends to existing content)"
    )


class ScrollPageInput(BaseModel):
    """Input schema for scroll_page tool."""
    direction: Literal["up", "down", "top", "bottom"] = Field(
        default="down",
        description="Direction to scroll: 'up' - scroll up, 'down' - scroll down, 'top' - scroll to page top, 'bottom' - scroll to page bottom"
    )


class GetPageInfoInput(BaseModel):
    """Input schema for get_page_info tool - no parameters needed."""
    pass


class GoBackInput(BaseModel):
    """Input schema for go_back tool - no parameters needed."""
    pass

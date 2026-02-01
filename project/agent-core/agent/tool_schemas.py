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
    button_id: int = Field(
        description="ID of the button to click. Get button IDs from get_page_buttons_next_item tool."
    )


class FillInputArgs(BaseModel):
    """Input schema for fill_input tool."""
    input_id: int = Field(
        description="ID of the input field to fill. Get input IDs from get_page_buttons_next_item tool."
    )
    text: str = Field(
        description="Text to fill into the input field (clears existing content first)"
    )


class TypeTextInput(BaseModel):
    """Input schema for type_text tool."""
    input_id: int = Field(
        description="ID of the input field. Get input IDs from get_page_buttons_next_item tool."
    )
    text: str = Field(
        description="Text to type into the field (appends to existing content)"
    )


class GetPageTextInput(BaseModel):
    """Input schema for get_page_text_next_item tool - no parameters needed."""
    pass


class GetPageButtonsInput(BaseModel):
    """Input schema for get_page_buttons_next_item tool - no parameters needed."""
    pass


class GetPageLinksInput(BaseModel):
    """Input schema for get_page_links_next_item tool - no parameters needed."""
    pass


class GoBackInput(BaseModel):
    """Input schema for go_back tool - no parameters needed."""
    pass


class PressKeyInput(BaseModel):
    """Input schema for press_key tool."""
    key: str = Field(
        description="Key to press. Common keys: 'Enter' (submit forms), 'Tab' (next field), 'Escape' (close dialogs), 'ArrowDown'/'ArrowUp' (navigate lists)."
    )

from typing import List, TYPE_CHECKING
from langchain_core.tools import StructuredTool
from playwright.async_api import Page

from tools.click_button import click_button
from tools.type_text import type_text, fill_input
from tools.press_key import press_key
from tools.get_page_text_next_item import get_page_text_next_item
from tools.get_page_buttons_next_item import get_page_buttons_next_item
from tools.get_page_links_next_item import get_page_links_next_item
from .tool_schemas import (
    NavigateInput,
    ClickButtonInput,
    FillInputArgs,
    TypeTextInput,
    PressKeyInput,
    GetPageTextInput,
    GetPageButtonsInput,
    GetPageLinksInput,
    GoBackInput
)
from .debug_tools import collect_tool_result

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


def create_agent_tools(page: Page, browser_manager: "BrowserManager") -> List[StructuredTool]:
    """
    Create LangChain tools for the agent
    
    Args:
        page: Playwright page instance
        browser_manager: BrowserManager instance for element storage
        
    Returns:
        List of configured tools
    """
    
    @collect_tool_result("navigate")
    async def _navigate(url: str) -> str:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        await browser_manager.navigate(url)
        return f"Successfully navigated to: {url}"
    
    @collect_tool_result("click_button")
    async def _click(button_id: int) -> str:
        result = await click_button(browser_manager, button_id)
        return f"{result['message']}"
    
    @collect_tool_result("type_text")
    async def _type(input_id: int, text: str) -> str:
        result = await type_text(browser_manager, input_id, text)
        # Reset page cache after typing (DOM may have changed)
        browser_manager.reset_text_items()
        browser_manager.reset_buttons_items()
        browser_manager.reset_links_items()
        return f"{result['message']}"
    
    @collect_tool_result("fill_input")
    async def _fill(input_id: int, text: str) -> str:
        result = await fill_input(browser_manager, input_id, text)
        # Reset page cache after filling (DOM may have changed)
        browser_manager.reset_text_items()
        browser_manager.reset_buttons_items()
        browser_manager.reset_links_items()
        return f"{result['message']}"
    
    @collect_tool_result("press_key")
    async def _press_key(key: str) -> str:
        result = await press_key(browser_manager, key)
        # Reset page cache after key press (DOM may have changed)
        browser_manager.reset_text_items()
        browser_manager.reset_buttons_items()
        browser_manager.reset_links_items()
        return f"{result['message']}"
    
    @collect_tool_result("get_page_text_next_item")
    async def _get_page_text_next() -> str:
        import json
        result = await get_page_text_next_item(browser_manager)
        if result['success']:
            return json.dumps(result['text_item'], ensure_ascii=False)
        return result['message']
    
    @collect_tool_result("get_page_buttons_next_item")
    async def _get_page_buttons_next() -> str:
        import json
        result = await get_page_buttons_next_item(browser_manager)
        if result['success']:
            return json.dumps(result['buttons_item'], ensure_ascii=False)
        return result['message']
    
    @collect_tool_result("get_page_links_next_item")
    async def _get_page_links_next() -> str:
        import json
        result = await get_page_links_next_item(browser_manager)
        if result['success']:
            return json.dumps(result['links_item'], ensure_ascii=False)
        return result['message']
    
    @collect_tool_result("go_back")
    async def _go_back() -> str:
        await browser_manager.go_back()
        return "Successfully navigated back"
    
    tools = [
        StructuredTool.from_function(
            coroutine=_navigate,
            name="navigate",
            description="Navigate to a URL. Input should be the URL string.",
            args_schema=NavigateInput
        ),
        StructuredTool.from_function(
            coroutine=_get_page_text_next,
            name="get_page_text_next_item",
            description="Get next portion of page text (700 characters). Call multiple times to get all text. Returns: item_id, total_items, text_chunk.",
            args_schema=GetPageTextInput
        ),
        StructuredTool.from_function(
            coroutine=_get_page_buttons_next,
            name="get_page_buttons_next_item",
            description="Get next portion of page buttons and input fields. Call multiple times to get all elements. Returns buttons (id, text, position) and inputs (id, type, name, placeholder). Use button/input IDs with click_button, type_text, fill_input tools.",
            args_schema=GetPageButtonsInput
        ),
        StructuredTool.from_function(
            coroutine=_get_page_links_next,
            name="get_page_links_next_item",
            description="Get next portion of page links (20 per call). Call multiple times to get all links. Returns links (text, url). Use URL with navigate tool.",
            args_schema=GetPageLinksInput
        ),
        StructuredTool.from_function(
            coroutine=_click,
            name="click_button",
            description="Click a button by ID. Use the button ID from get_page_buttons_next_item.",
            args_schema=ClickButtonInput
        ),
        StructuredTool.from_function(
            coroutine=_type,
            name="type_text",
            description="Type text into input field by ID (appends to existing content). Use input ID from get_page_buttons_next_item.",
            args_schema=TypeTextInput
        ),
        StructuredTool.from_function(
            coroutine=_fill,
            name="fill_input",
            description="Fill input field by ID (clears first). Use input ID from get_page_buttons_next_item.",
            args_schema=FillInputArgs
        ),
        StructuredTool.from_function(
            coroutine=_press_key,
            name="press_key",
            description="Press a keyboard key. Use 'Enter' to submit forms/search, 'Tab' to move to next field, 'Escape' to close dialogs, 'ArrowDown'/'ArrowUp' to navigate dropdown lists.",
            args_schema=PressKeyInput
        ),
        StructuredTool.from_function(
            coroutine=_go_back,
            name="go_back",
            description="Navigate back in browser history.",
            args_schema=GoBackInput
        ),
    ]
    
    return tools

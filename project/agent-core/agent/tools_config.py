from typing import List, Dict, Any, Callable
from langchain_core.tools import StructuredTool
from playwright.async_api import Page
import asyncio

from tools.click_button import click_button
from tools.navigate import navigate, go_back
from tools.type_text import type_text, fill_input
from tools.get_page_info import get_page_info
from tools.scroll import scroll_page, scroll_to_element
from .tool_schemas import (
    NavigateInput,
    ClickButtonInput,
    FillInputArgs,
    ScrollPageInput,
    GetPageInfoInput,
    GoBackInput
)
from .debug_tools import collect_tool_result


def create_agent_tools(page: Page) -> List[StructuredTool]:
    """
    Create LangChain tools for the agent
    
    Args:
        page: Playwright page instance
        
    Returns:
        List of configured tools
    """
    
    @collect_tool_result("navigate")
    async def _navigate(url: str) -> str:
        result = await navigate(page, url)
        return f"{result['message']}"
    
    @collect_tool_result("click_button")
    async def _click(selector: str) -> str:
        result = await click_button(page, selector)
        return f"{result['message']}"
    
    @collect_tool_result("type_text")
    async def _type(selector: str, text: str) -> str:
        result = await type_text(page, selector, text)
        return f"{result['message']}"
    
    @collect_tool_result("fill_input")
    async def _fill(selector: str, text: str) -> str:
        result = await fill_input(page, selector, text)
        return f"{result['message']}"
    
    @collect_tool_result("get_page_info")
    async def _get_page() -> str:
        import json
        result = await get_page_info(page)
        if result['success']:
            page_data = result['page']
            # Return full structured data as compact JSON
            return json.dumps(page_data, ensure_ascii=False)
        return result['message']
    
    @collect_tool_result("scroll_page")
    async def _scroll(direction: str = "down") -> str:
        result = await scroll_page(page, direction)
        return f"{result['message']}"
    
    @collect_tool_result("go_back")
    async def _go_back() -> str:
        result = await go_back(page)
        return f"{result['message']}"
    
    tools = [
        StructuredTool.from_function(
            coroutine=_navigate,
            name="navigate",
            description="Navigate to a URL. Input should be the URL string.",
            args_schema=NavigateInput
        ),
        StructuredTool.from_function(
            coroutine=_get_page,
            name="get_page_info",
            description="Get structured JSON information about the current page including: url, title, visible_text, buttons (with text, selector, position, parent_text), and links (with text, url, selector, position, parent_text). Use this first to understand what's on the page. Returns complete JSON with all element data.",
            args_schema=GetPageInfoInput
        ),
        StructuredTool.from_function(
            coroutine=_click,
            name="click_button",
            description="Click a button or clickable element. Input should be the CSS selector of the element.",
            args_schema=ClickButtonInput
        ),
        StructuredTool.from_function(
            coroutine=_fill,
            name="fill_input",
            description="Fill an input field (clears first). Input format: selector and text as separate parameters.",
            args_schema=FillInputArgs
        ),
        StructuredTool.from_function(
            coroutine=_scroll,
            name="scroll_page",
            description="Scroll the page. Input should be 'up', 'down', 'top', or 'bottom'.",
            args_schema=ScrollPageInput
        ),
        StructuredTool.from_function(
            coroutine=_go_back,
            name="go_back",
            description="Navigate back in browser history.",
            args_schema=GoBackInput
        ),
    ]
    
    return tools

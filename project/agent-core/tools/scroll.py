from typing import Dict, Any, Literal
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.tool_execution import ToolExecutionError, ElementNotFoundError
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed


@handle_browser_closed
async def scroll_page(
    page: Page, 
    direction: Literal["up", "down", "top", "bottom"] = "down",
    amount: int = 500
) -> Dict[str, Any]:
    """
    Scroll the page in a specified direction
    
    Args:
        page: Playwright page instance
        direction: Direction to scroll (up, down, top, bottom)
        amount: Pixels to scroll (for up/down)
        
    Returns:
        Dict with success status and message
    """
    try:
        if direction == "down":
            await page.evaluate(f"window.scrollBy(0, {amount})")
        elif direction == "up":
            await page.evaluate(f"window.scrollBy(0, -{amount})")
        elif direction == "top":
            await page.evaluate("window.scrollTo(0, 0)")
        elif direction == "bottom":
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        return {
            "success": True,
            "message": f"Successfully scrolled {direction}"
        }
        
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e


@handle_browser_closed
async def scroll_to_element(page: Page, selector: str) -> Dict[str, Any]:
    """
    Scroll to a specific element on the page
    
    Args:
        page: Playwright page instance
        selector: CSS selector of the element to scroll to
        
    Returns:
        Dict with success status and message
    """
    try:
        element = page.locator(selector).first
        await element.wait_for(state='visible', timeout=5000)
        await element.scroll_into_view_if_needed()
        
        return {
            "success": True,
            "message": f"Successfully scrolled to element: {selector}"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(selector, timeout=5)
        log_error(err)
        raise err
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

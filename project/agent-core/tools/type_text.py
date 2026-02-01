from typing import Dict, Any
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.tool_execution import ElementNotFoundError
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed


@handle_browser_closed
async def type_text(page: Page, selector: str, text: str) -> Dict[str, Any]:
    """
    Type text into an input field (appends to existing content)
    
    Args:
        page: Playwright page instance
        selector: CSS selector or XPath of the input field
        text: Text to type
        
    Returns:
        Dict with success status and message
    """
    try:
        element = page.locator(selector).first
        await element.wait_for(state='visible', timeout=5000)
        
        # Scroll into view if needed
        await element.scroll_into_view_if_needed()
        
        # Click to focus
        await element.click()
        
        # Type text
        await element.type(text, delay=50)
        
        return {
            "success": True,
            "message": f"Successfully typed text into field: {selector}"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(selector, timeout=5)
        log_error(err)
        raise err
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e


@handle_browser_closed
async def fill_input(page: Page, selector: str, text: str) -> Dict[str, Any]:
    """
    Fill an input field (clears existing content first)
    
    Args:
        page: Playwright page instance
        selector: CSS selector or XPath of the input field
        text: Text to fill
        
    Returns:
        Dict with success status and message
    """
    try:
        element = page.locator(selector).first
        await element.wait_for(state='visible', timeout=5000)
        
        # Scroll into view if needed
        await element.scroll_into_view_if_needed()
        
        # Fill (clears and types)
        await element.fill(text)
        
        return {
            "success": True,
            "message": f"Successfully filled input field: {selector}"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(selector, timeout=5)
        log_error(err)
        raise err
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

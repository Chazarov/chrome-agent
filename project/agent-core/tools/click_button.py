from typing import Dict, Any
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.tool_execution import ElementNotFoundError
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed


@handle_browser_closed
async def click_button(page: Page, selector: str) -> Dict[str, Any]:
    """
    Click a button element by selector
    
    Args:
        page: Playwright page instance
        selector: CSS selector or XPath of the button to click
        
    Returns:
        Dict with success status and message
    """
    try:
        # Wait for element to be visible and clickable
        element = page.locator(selector).first
        await element.wait_for(state='visible', timeout=5000)
        
        # Scroll into view if needed
        await element.scroll_into_view_if_needed()
        
        # Click the element
        await element.click(timeout=5000)
        
        # Wait for potential navigation or loading
        try:
            await page.wait_for_load_state('networkidle', timeout=3000)
        except PlaywrightTimeout:
            pass  # Page might not navigate, that's okay
        
        return {
            "success": True,
            "message": f"Successfully clicked button with selector: {selector}"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(selector, timeout=5)
        log_error(err)
        raise err
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

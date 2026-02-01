from typing import Dict, Any, TYPE_CHECKING
from playwright.async_api import TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.tool_execution import ElementNotFoundError
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


@handle_browser_closed
async def click_button(browser_manager: "BrowserManager", button_id: int) -> Dict[str, Any]:
    """
    Click a button element by ID
    
    Args:
        browser_manager: BrowserManager instance
        button_id: Unique ID of the button to click
        
    Returns:
        Dict with success status and message
    """
    try:
        # Get internal button object
        button_internal = browser_manager.get_button_by_id(button_id)
        
        if not button_internal:
            raise ElementNotFoundError(f"button_id={button_id}", timeout=0)
        
        element = button_internal.element
        page = browser_manager.page
        
        # Wait for element to be visible and clickable
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
            "message": f"Successfully clicked button (ID: {button_id}, text: '{button_internal.text}')"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(f"button_id={button_id}", timeout=5)
        log_error(err)
        raise err
    except ElementNotFoundError:
        raise
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

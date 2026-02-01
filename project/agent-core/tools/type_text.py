from typing import Dict, Any, TYPE_CHECKING
from playwright.async_api import TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.tool_execution import ElementNotFoundError
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


@handle_browser_closed
async def type_text(browser_manager: "BrowserManager", input_id: int, text: str) -> Dict[str, Any]:
    """
    Type text into an input field by ID (appends to existing content)
    
    Args:
        browser_manager: BrowserManager instance
        input_id: Unique ID of the input field
        text: Text to type
        
    Returns:
        Dict with success status and message
    """
    try:
        # Get internal input object
        input_internal = browser_manager.get_input_by_id(input_id)
        
        if not input_internal:
            raise ElementNotFoundError(f"input_id={input_id}", timeout=0)
        
        element = input_internal.element
        
        # Wait for element to be visible
        await element.wait_for(state='visible', timeout=5000)
        
        # Scroll into view if needed
        await element.scroll_into_view_if_needed()
        
        # Click to focus
        await element.click()
        
        # Type text
        await element.type(text, delay=50)
        
        return {
            "success": True,
            "message": f"Successfully typed text into input (ID: {input_id})"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(f"input_id={input_id}", timeout=5)
        log_error(err)
        raise err
    except ElementNotFoundError:
        raise
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e


@handle_browser_closed
async def fill_input(browser_manager: "BrowserManager", input_id: int, text: str) -> Dict[str, Any]:
    """
    Fill an input field by ID (clears existing content first)
    
    Args:
        browser_manager: BrowserManager instance
        input_id: Unique ID of the input field
        text: Text to fill
        
    Returns:
        Dict with success status and message
    """
    try:
        # Get internal input object
        input_internal = browser_manager.get_input_by_id(input_id)
        
        if not input_internal:
            raise ElementNotFoundError(f"input_id={input_id}", timeout=0)
        
        element = input_internal.element
        
        # Wait for element to be visible
        await element.wait_for(state='visible', timeout=5000)
        
        # Scroll into view if needed
        await element.scroll_into_view_if_needed()
        
        # Fill (clears and types)
        await element.fill(text)
        
        return {
            "success": True,
            "message": f"Successfully filled input (ID: {input_id})"
        }
        
    except PlaywrightTimeout:
        err = ElementNotFoundError(f"input_id={input_id}", timeout=5)
        log_error(err)
        raise err
    except ElementNotFoundError:
        raise
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

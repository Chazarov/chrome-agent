from typing import Dict, Any, TYPE_CHECKING

from exceptions.browser_closed import BrowserClosedError
from .utils import handle_browser_closed
from agent.debug_tools import log_error
from exceptions.unknown_error import UnknownError

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


@handle_browser_closed
async def get_page_buttons_next_item(browser_manager: "BrowserManager") -> Dict[str, Any]:
    """
    Get next portion of page buttons and input fields.
    Call multiple times to get all action sections.
    
    Args:
        browser_manager: BrowserManager instance
        
    Returns:
        Dict with buttons and inputs or message about completion
    """
    try:
        item = await browser_manager.get_next_page_buttons_item()
        
        if item is None:
            return {
                "success": False,
                "message": "All buttons items have been retrieved."
            }
        
        return {
            "success": True,
            "buttons_item": item.model_dump(),
            "message": f"Retrieved buttons {item.item_id + 1}/{item.total_items}"
        }
        
    except BrowserClosedError:
        raise
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

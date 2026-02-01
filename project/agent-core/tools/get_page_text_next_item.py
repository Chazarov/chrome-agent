from typing import Dict, Any, TYPE_CHECKING

from exceptions.browser_closed import BrowserClosedError
from .utils import handle_browser_closed
from agent.debug_tools import log_error
from exceptions.unknown_error import UnknownError

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


@handle_browser_closed
async def get_page_text_next_item(browser_manager: "BrowserManager") -> Dict[str, Any]:
    """
    Get next portion of page text.
    Call multiple times to get all text chunks.
    
    Args:
        browser_manager: BrowserManager instance
        
    Returns:
        Dict with text chunk or message about completion
    """
    try:
        item = await browser_manager.get_next_page_text_item()
        
        if item is None:
            return {
                "success": False,
                "message": "All text chunks have been retrieved."
            }
        
        return {
            "success": True,
            "text_item": item.model_dump(),
            "message": f"Retrieved text chunk {item.item_id + 1}/{item.total_items}"
        }
        
    except BrowserClosedError:
        raise
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

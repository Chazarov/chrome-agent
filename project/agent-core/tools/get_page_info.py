from typing import Dict, Any
from playwright.async_api import Page

from agent.debug_tools import log_error
from models.page import Page as PageModel
from parser.page_parser import PageParser
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed


@handle_browser_closed
async def get_page_info(page: Page) -> Dict[str, Any]:
    """
    Get structured information about the current page
    
    Args:
        page: Playwright page instance
        
    Returns:
        Dict with page information or error
    """
    try:
        parser = PageParser(page)
        page_info = await parser.parse_page()
        
        return {
            "success": True,
            "page": page_info.model_dump(),
            "message": f"Successfully extracted page info from: {page_info.url}"
        }
        
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

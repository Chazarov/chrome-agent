from typing import Dict, Any
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.tool_execution import NavigationTimeoutError
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed


@handle_browser_closed
async def navigate(page: Page, url: str) -> Dict[str, Any]:
    """
    Navigate to a URL
    
    Args:
        page: Playwright page instance
        url: Target URL to navigate to
        
    Returns:
        Dict with success status and message
    """
    try:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Navigate to URL
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for page to be ready
        try:
            await page.wait_for_load_state('networkidle', timeout=10000)
        except PlaywrightTimeout:
            pass  # Page might still be loading resources, that's okay
        
        return {
            "success": True,
            "message": f"Successfully navigated to: {url}",
            "current_url": page.url
        }
        
    except PlaywrightTimeout:
        err = NavigationTimeoutError(url)
        log_error(err)
        raise err
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e


@handle_browser_closed
async def go_back(page: Page) -> Dict[str, Any]:
    """
    Navigate back in browser history
    
    Args:
        page: Playwright page instance
        
    Returns:
        Dict with success status and message
    """
    try:
        await page.go_back(wait_until='domcontentloaded', timeout=10000)
        
        return {
            "success": True,
            "message": "Successfully navigated back",
            "current_url": page.url
        }
        
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

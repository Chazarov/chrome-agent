"""
Utility decorators and helpers for tools.
"""

import functools
from typing import Callable, Any
from playwright.async_api import Error as PlaywrightError

from agent.debug_tools import log_error
from exceptions.browser_closed import BrowserClosedError


def handle_browser_closed(func: Callable) -> Callable:
    """
    Decorator to catch browser/page closed errors and convert to BrowserClosedError.
    
    Catches Playwright's TargetClosedError and similar errors when browser,
    context or page is closed during operation.
    
    Args:
        func: Async function to wrap
        
    Returns:
        Wrapped function with browser closed error handling
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except PlaywrightError as e:
            error_str = str(e).lower()
            # Check for various browser closed errors
            if any(keyword in error_str for keyword in [
                'target', 'closed', 'browser has been closed',
                'context has been closed', 'page has been closed'
            ]):
                err = BrowserClosedError(f"{func.__name__} - {str(e)}")
                log_error(err)
                raise err from e
            # Re-raise other Playwright errors
            raise
    
    return wrapper

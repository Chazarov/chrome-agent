"""
Raised when tool execution fails due to Playwright operations.
Covers timeouts, element not found, navigation errors, and other Playwright exceptions.
Provides agent with specific context about what went wrong and how to fix it.
"""

from .domain_error import DomainError

class ToolExecutionError(DomainError):
    def __init__(self, error_reason: str, proposed_fix: str):
        super().__init__(error_reason, proposed_fix)

class ElementNotFoundError(ToolExecutionError):
    def __init__(self, selector: str, timeout: int = 10):
        super().__init__(
            error_reason=f"Element with selector '{selector}' not found within {timeout} seconds",
            proposed_fix="Use get_page_info tool to find correct selector on current page"
        )

class NavigationTimeoutError(ToolExecutionError):
    def __init__(self, url: str, timeout: int = 30):
        super().__init__(
            error_reason=f"Navigation to '{url}' timed out after {timeout} seconds",
            proposed_fix="Try navigating to a different URL or check if the page is accessible"
        )

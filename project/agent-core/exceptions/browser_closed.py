"""
Raised when browser window was closed manually by user or not started.
This error indicates that the browser is not available for automation operations.
Resolves Bug #1 (handle_browser_closing_error).
"""

from .domain_error import DomainError

class BrowserClosedError(DomainError):
    def __init__(self, context: str = "Browser operation"):
        super().__init__(
            error_reason=f"{context}: Browser window is not available (closed or not started)",
            proposed_fix="Ask user to keep browser window open during task execution"
        )

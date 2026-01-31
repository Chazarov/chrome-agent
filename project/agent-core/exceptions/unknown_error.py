"""
Wraps unexpected exceptions that don't fit into other domain error categories.
Ensures all errors are caught and categorized for proper handling.
Acts as a safety net for unanticipated scenarios.
"""

from .domain_error import DomainError

class UnknownError(DomainError):
    def __init__(self, original_error: Exception):
        error_type = type(original_error).__name__
        error_message = str(original_error)
        
        super().__init__(
            error_reason=f"Unexpected {error_type}: {error_message}",
            proposed_fix="Report this error to developers or retry the operation"
        )
        
        self.original_error = original_error

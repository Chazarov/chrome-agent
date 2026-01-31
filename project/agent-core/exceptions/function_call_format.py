"""
Raised when LLM generates invalid function call format.
This typically occurs when Groq API returns 400 error for malformed tool calls.
Resolves Bug #4 (function_call_format_error).
"""

from .domain_error import DomainError

class FunctionCallFormatError(DomainError):
    def __init__(self, details: str = ""):
        error_msg = "LLM generated invalid function call format"
        if details:
            error_msg += f": {details}"
        
        super().__init__(
            error_reason=error_msg,
            proposed_fix="Check that all tool definitions have proper args_schema with Pydantic models. Update langchain-groq to latest version."
        )

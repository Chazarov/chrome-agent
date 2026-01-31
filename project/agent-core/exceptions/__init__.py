"""
Domain exceptions package for Chrome Agent.
Provides structured error handling with agent-friendly descriptions and proposed fixes.
"""

from .domain_error import DomainError
from .browser_closed import BrowserClosedError
from .function_call_format import FunctionCallFormatError
from .tool_execution import ToolExecutionError
from .unknown_error import UnknownError

__all__ = [
    "DomainError",
    "BrowserClosedError",
    "FunctionCallFormatError",
    "ToolExecutionError",
    "UnknownError",
]

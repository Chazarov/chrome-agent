"""
Base domain error class for all custom exceptions in the system.
Provides structured error information with agent-friendly descriptions and proposed fixes.
All domain errors inherit from this class and must provide error_reason and proposed_fix.
"""

class DomainError(Exception):
    def __init__(self, error_reason: str, proposed_fix: str):
        self.error_reason = error_reason
        self.proposed_fix = proposed_fix
        super().__init__(error_reason)

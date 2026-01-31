"""
Debug tools for agent development.
Contains utilities for logging and debugging LLM responses.
"""

import sys
from typing import Any
from pathlib import Path
from loguru import logger

from config import config

# Configure loguru format for Windows-style paths
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file.path}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True
)


def print_llm_response(response: Any) -> None:
    print("\n" + "="*80)
    print("LLM RESPONSE")
    print("="*80)
    
    if hasattr(response, 'content') and response.content:
        print("\nCONTENT:")
        print(response.content)
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print("\nTOOL CALLS:")
        for i, tool_call in enumerate(response.tool_calls, 1):
            print(f"\n  [{i}] {tool_call.get('name', 'unknown')}")
            if 'args' in tool_call:
                for key, value in tool_call['args'].items():
                    print(f"      {key}: {value}")
            if 'id' in tool_call:
                print(f"      id: {tool_call['id']}")
    
    if hasattr(response, 'additional_kwargs') and 'tool_calls' in response.additional_kwargs:
        print("\nADDITIONAL TOOL CALLS:")
        for i, tc in enumerate(response.additional_kwargs['tool_calls'], 1):
            print(f"\n  [{i}] {tc}")
    
    if hasattr(response, 'response_metadata') and response.response_metadata:
        print("\nRESPONSE METADATA:")
        for key, value in response.response_metadata.items():
            print(f"  {key}: {value}")
    
    print("\n" + "="*80 + "\n")


def log_error(error: Exception) -> None:
    """
    Log domain error if debug mode is enabled.
    Shows the actual location where the error was raised (one level up in call stack).
    
    Args:
        error: Exception instance to log
    """
    if config.is_debug():
        logger.opt(depth=1).error(f"{error.__class__.__name__}: {error}")

"""
Debug tools for agent development.
Contains utilities for logging and debugging LLM responses.
"""

import sys
import functools
from typing import Any, Optional, Callable
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
    
    # Check for reasoning in both possible locations
    reasoning_content = None
    if hasattr(response, 'reasoning') and response.reasoning:
        reasoning_content = response.reasoning
    elif hasattr(response, 'additional_kwargs') and 'reasoning_content' in response.additional_kwargs:
        reasoning_content = response.additional_kwargs['reasoning_content']
    
    if reasoning_content:
        print("\nREASONING:")
        print(reasoning_content)
    
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


def extract_reasoning(response: Any) -> Optional[str]:
    """
    Extract reasoning content from LLM response.
    Checks multiple possible locations where reasoning might be stored.
    
    Args:
        response: LLM response object
        
    Returns:
        Reasoning text if found, None otherwise
    """
    if hasattr(response, 'reasoning') and response.reasoning:
        return response.reasoning
    elif hasattr(response, 'additional_kwargs') and 'reasoning_content' in response.additional_kwargs:
        return response.additional_kwargs['reasoning_content']
    return None


def collect_tool_result(tool_name: str):
    """
    Decorator for automatic collection of tool execution results.
    Collects tool results when save_debug_info is enabled.
    
    Args:
        tool_name: Name of the tool for identification in debug log
        
    Returns:
        Decorated async function
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute function
            result = await func(*args, **kwargs)
            
            # Collect result if debug mode enabled
            if config.is_save_debug_info_enabled():
                from agent.debug_collector import DebugCollector
                collector = DebugCollector.get_instance()
                collector.add_tool_result(tool_name, result)
            
            return result
        return wrapper
    return decorator

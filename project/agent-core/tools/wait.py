import asyncio
from typing import Dict, Any

from config import config


async def wait() -> Dict[str, Any]:
    """
    Wait for page to finish loading/verification.
    Used when browser shows verification pages or loading screens.
    
    Returns:
        Dict with success status and message
    """
    await asyncio.sleep(config.wait_delay / 1000)
    return {
        "success": True,
        "message": f"Waited {config.wait_delay}ms"
    }

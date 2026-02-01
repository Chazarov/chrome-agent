from typing import Dict, Any, TYPE_CHECKING
from playwright.async_api import TimeoutError as PlaywrightTimeout

from agent.debug_tools import log_error
from exceptions.unknown_error import UnknownError
from .utils import handle_browser_closed

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


# Mapping of common key names to Playwright key codes
KEY_MAPPING = {
    "enter": "Enter",
    "tab": "Tab",
    "escape": "Escape",
    "esc": "Escape",
    "backspace": "Backspace",
    "delete": "Delete",
    "arrowup": "ArrowUp",
    "arrowdown": "ArrowDown",
    "arrowleft": "ArrowLeft",
    "arrowright": "ArrowRight",
    "up": "ArrowUp",
    "down": "ArrowDown",
    "left": "ArrowLeft",
    "right": "ArrowRight",
    "space": " ",
    "home": "Home",
    "end": "End",
    "pageup": "PageUp",
    "pagedown": "PageDown",
}


@handle_browser_closed
async def press_key(browser_manager: "BrowserManager", key: str) -> Dict[str, Any]:
    """
    Press a keyboard key
    
    Args:
        browser_manager: BrowserManager instance
        key: Key to press (e.g., "Enter", "Tab", "Escape", "ArrowDown")
        
    Returns:
        Dict with success status and message
    """
    try:
        page = browser_manager.page
        
        # Normalize key name
        normalized_key = KEY_MAPPING.get(key.lower(), key)
        
        # Press the key
        await page.keyboard.press(normalized_key)
        
        # Wait a bit for potential page changes
        try:
            await page.wait_for_load_state('networkidle', timeout=2000)
        except PlaywrightTimeout:
            pass  # Page might not change, that's okay
        
        return {
            "success": True,
            "message": f"Successfully pressed key: {normalized_key}"
        }
        
    except Exception as e:
        err = UnknownError(e)
        log_error(err)
        raise err from e

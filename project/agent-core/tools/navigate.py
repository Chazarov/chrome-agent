from typing import Dict, Any
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout


async def navigate(page: Page, url: str) -> Dict[str, Any]:
    """
    Navigate to a URL
    
    Args:
        page: Playwright page instance
        url: Target URL to navigate to
        
    Returns:
        Dict with success status and message
    """
    try:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Navigate to URL
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for page to be ready
        try:
            await page.wait_for_load_state('networkidle', timeout=10000)
        except PlaywrightTimeout:
            pass  # Page might still be loading resources, that's okay
        
        return {
            "success": True,
            "message": f"Successfully navigated to: {url}",
            "current_url": page.url
        }
        
    except PlaywrightTimeout:
        return {
            "success": False,
            "message": f"Timeout: Could not load page: {url}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error navigating to {url}: {str(e)}"
        }


async def go_back(page: Page) -> Dict[str, Any]:
    """
    Navigate back in browser history
    
    Args:
        page: Playwright page instance
        
    Returns:
        Dict with success status and message
    """
    try:
        await page.go_back(wait_until='domcontentloaded', timeout=10000)
        
        return {
            "success": True,
            "message": "Successfully navigated back",
            "current_url": page.url
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error going back: {str(e)}"
        }

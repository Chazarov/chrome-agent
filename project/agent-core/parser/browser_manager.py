from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright

from config import config
from agent.debug_tools import log_error
from exceptions.browser_closed import BrowserClosedError


class BrowserManager:
    """Manages browser lifecycle using Playwright"""
    
    def __init__(self):
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        
    async def start(self):
        """Start browser instance (always visible)"""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=False  # Always visible window
        )
        self._context = await self._browser.new_context(
            viewport={
                'width': config.browser_viewport_width,
                'height': config.browser_viewport_height
            }
        )
        self._page = await self._context.new_page()
        self._page.set_default_timeout(config.browser_timeout)
        
    async def stop(self):
        """Stop browser and cleanup resources"""
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
            
    async def navigate(self, url: str) -> None:
        """Navigate to URL"""
        if not self._page:
            err = BrowserClosedError("Navigate")
            log_error(err)
            raise err
        await self._page.goto(url, wait_until='domcontentloaded')
        await self._page.wait_for_load_state('networkidle', timeout=10000)
        
    async def go_back(self) -> None:
        """Navigate back in history"""
        if not self._page:
            err = BrowserClosedError("Go back")
            log_error(err)
            raise err
        await self._page.go_back()
        
    async def go_forward(self) -> None:
        """Navigate forward in history"""
        if not self._page:
            err = BrowserClosedError("Go forward")
            log_error(err)
            raise err
        await self._page.go_forward()
        
    @property
    def page(self) -> Page:
        """Get current page instance"""
        if not self._page:
            err = BrowserClosedError("Get page")
            log_error(err)
            raise err
        return self._page
    
    @property
    def current_url(self) -> str:
        """Get current page URL"""
        if not self._page:
            err = BrowserClosedError("Get URL")
            log_error(err)
            raise err
        return self._page.url

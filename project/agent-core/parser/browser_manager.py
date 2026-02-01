from typing import Optional, Dict, List, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright, TimeoutError as PlaywrightTimeout
from playwright_stealth import Stealth

from loguru import logger

from config import config
from agent.debug_tools import log_error
from exceptions.browser_closed import BrowserClosedError
from models.button import ButtonInternal
from models.input_field import InputInternal
from models.page import PageTextItem, PageButtonsItem, PageLinksItem


class BrowserManager:
    """Manages browser lifecycle using Playwright and page element storage"""
    
    def __init__(self):
        self._stealth: Optional[Stealth] = None
        self._stealth_context: Optional[Any] = None
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        
        # Text items state
        self._text_items: List[PageTextItem] = []
        self._current_text_index: int = 0
        self._last_text_parsed_url: Optional[str] = None
        
        # Buttons items state
        self._buttons_items: List[PageButtonsItem] = []
        self._current_buttons_index: int = 0
        self._last_buttons_parsed_url: Optional[str] = None
        
        # Links items state
        self._links_items: List[PageLinksItem] = []
        self._current_links_index: int = 0
        self._last_links_parsed_url: Optional[str] = None
        
        # Playwright element storage
        self._buttons_internal: Dict[int, ButtonInternal] = {}
        self._inputs_internal: Dict[int, InputInternal] = {}
        
    async def start(self):
        """Start browser instance with stealth mode (always visible)"""
        self._stealth = Stealth()
        self._stealth_context = self._stealth.use_async(async_playwright())
        self._playwright = await self._stealth_context.__aenter__()
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
        if self._stealth_context:
            await self._stealth_context.__aexit__(None, None, None)
            
    async def navigate(self, url: str) -> None:
        """Navigate to URL"""
        if not self._page:
            err = BrowserClosedError("Navigate")
            log_error(err)
            raise err
        await self._page.goto(url, wait_until='domcontentloaded')
        try:
            await self._page.wait_for_load_state('networkidle', timeout=10000)
        except PlaywrightTimeout:
            if config.is_debug():
                logger.debug(f"networkidle timeout for {url}, continuing anyway")
        
        # Reset all page items after navigation
        self.reset_text_items()
        self.reset_buttons_items()
        self.reset_links_items()
        
    async def go_back(self) -> None:
        """Navigate back in history"""
        if not self._page:
            err = BrowserClosedError("Go back")
            log_error(err)
            raise err
        await self._page.go_back()
        
        # Reset all page items after navigation
        self.reset_text_items()
        self.reset_buttons_items()
        self.reset_links_items()
        
    async def go_forward(self) -> None:
        """Navigate forward in history"""
        if not self._page:
            err = BrowserClosedError("Go forward")
            log_error(err)
            raise err
        await self._page.go_forward()
        
        # Reset all page items after navigation
        self.reset_text_items()
        self.reset_buttons_items()
        self.reset_links_items()
        
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
    
    # Text items methods
    
    async def get_next_page_text_item(self) -> Optional[PageTextItem]:
        """Get next portion of page text"""
        if not self._page:
            raise BrowserClosedError("Browser page is not available")
        
        current_url = self._page.url
        
        if current_url != self._last_text_parsed_url or not self._text_items:
            from parser.page_parser import PageParser
            parser = PageParser(self._page)
            self._text_items = await parser.parse_page_text_items()
            self._current_text_index = 0
            self._last_text_parsed_url = current_url
        
        if self._current_text_index < len(self._text_items):
            item = self._text_items[self._current_text_index]
            self._current_text_index += 1
            return item
        
        return None
    
    def reset_text_items(self):
        """Reset text items state"""
        self._text_items = []
        self._current_text_index = 0
        self._last_text_parsed_url = None
    
    # Buttons items methods
    
    async def get_next_page_buttons_item(self) -> Optional[PageButtonsItem]:
        """Get next portion of buttons and input fields"""
        if not self._page:
            raise BrowserClosedError("Browser page is not available")
        
        current_url = self._page.url
        
        if current_url != self._last_buttons_parsed_url or not self._buttons_items:
            from parser.page_parser import PageParser
            parser = PageParser(self._page)
            buttons_internal, inputs_internal, buttons_items = await parser.parse_page_buttons_items()
            
            # Store internal elements by ID
            self._buttons_internal = {btn.id: btn for btn in buttons_internal}
            self._inputs_internal = {inp.id: inp for inp in inputs_internal}
            
            self._buttons_items = buttons_items
            self._current_buttons_index = 0
            self._last_buttons_parsed_url = current_url
        
        if self._current_buttons_index < len(self._buttons_items):
            item = self._buttons_items[self._current_buttons_index]
            self._current_buttons_index += 1
            return item
        
        return None
    
    def reset_buttons_items(self):
        """Reset buttons items state"""
        self._buttons_items = []
        self._current_buttons_index = 0
        self._last_buttons_parsed_url = None
        self._buttons_internal = {}
        self._inputs_internal = {}
    
    def get_button_by_id(self, button_id: int) -> Optional[ButtonInternal]:
        """Get internal button object by ID"""
        return self._buttons_internal.get(button_id)
    
    def get_input_by_id(self, input_id: int) -> Optional[InputInternal]:
        """Get internal input object by ID"""
        return self._inputs_internal.get(input_id)
    
    # Links items methods
    
    async def get_next_page_links_item(self) -> Optional[PageLinksItem]:
        """Get next portion of links"""
        if not self._page:
            raise BrowserClosedError("Browser page is not available")
        
        current_url = self._page.url
        
        if current_url != self._last_links_parsed_url or not self._links_items:
            from parser.page_parser import PageParser
            parser = PageParser(self._page)
            self._links_items = await parser.parse_page_links_items()
            self._current_links_index = 0
            self._last_links_parsed_url = current_url
        
        if self._current_links_index < len(self._links_items):
            item = self._links_items[self._current_links_index]
            self._current_links_index += 1
            return item
        
        return None
    
    def reset_links_items(self):
        """Reset links items state"""
        self._links_items = []
        self._current_links_index = 0
        self._last_links_parsed_url = None

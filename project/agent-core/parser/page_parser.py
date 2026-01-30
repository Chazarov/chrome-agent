from typing import List, Optional
from playwright.async_api import Page, Locator

from models.button import Button
from models.link import Link
from models.page import Page as PageModel


class PageParser:
    """Parses webpage and extracts structured information"""
    
    def __init__(self, page: Page):
        self.page = page
        
    async def parse_page(self) -> PageModel:
        """Main method to extract all page information"""
        url = self.page.url
        title = await self.page.title()
        visible_text = await self.get_visible_text()
        buttons = await self.extract_buttons()
        links = await self.extract_links()
        
        return PageModel(
            url=url,
            title=title,
            visible_text=visible_text,
            buttons=buttons,
            links=links
        )
    
    async def get_visible_text(self) -> str:
        """Extract all visible text from the page"""
        try:
            text = await self.page.evaluate("""
                () => {
                    const body = document.body;
                    return body.innerText || body.textContent || '';
                }
            """)
            return text.strip()[:5000]  # Limit to first 5000 chars
        except Exception:
            return ""
    
    async def extract_buttons(self) -> List[Button]:
        """Extract all clickable button elements"""
        buttons = []
        
        # Query for all button-like elements
        selectors = [
            'button',
            '[role="button"]',
            'input[type="submit"]',
            'input[type="button"]'
        ]
        
        for selector in selectors:
            elements = await self.page.query_selector_all(selector)
            
            for idx, element in enumerate(elements):
                try:
                    # Check if element is visible
                    is_visible = await element.is_visible()
                    if not is_visible:
                        continue
                    
                    # Get text content
                    text = await element.text_content()
                    if not text:
                        text = await element.get_attribute('value') or ''
                    text = text.strip()[:100]
                    
                    # Get position
                    box = await element.bounding_box()
                    if not box:
                        continue
                    position = (box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                    
                    # Get parent text for context
                    parent_text = await self._get_parent_text(element)
                    
                    # Generate unique selector
                    css_selector = f"{selector}:nth-of-type({idx + 1})"
                    
                    buttons.append(Button(
                        text=text,
                        position=position,
                        parent_text=parent_text,
                        selector=css_selector
                    ))
                    
                except Exception:
                    continue
                    
        return buttons
    
    async def extract_links(self) -> List[Link]:
        """Extract all hyperlinks from the page"""
        links = []
        
        elements = await self.page.query_selector_all('a[href]')
        
        for idx, element in enumerate(elements):
            try:
                # Check if element is visible
                is_visible = await element.is_visible()
                if not is_visible:
                    continue
                
                # Get text content
                text = await element.text_content()
                if not text:
                    text = await element.get_attribute('aria-label') or ''
                text = text.strip()[:100]
                
                # Get URL
                href = await element.get_attribute('href')
                if not href:
                    continue
                    
                # Make absolute URL
                url = await self.page.evaluate(f"() => new URL('{href}', window.location.href).href")
                
                # Get position
                box = await element.bounding_box()
                if not box:
                    continue
                position = (box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                
                # Get parent text for context
                parent_text = await self._get_parent_text(element)
                
                # Generate selector
                css_selector = f"a:nth-of-type({idx + 1})"
                
                links.append(Link(
                    text=text,
                    position=position,
                    url=url,
                    parent_text=parent_text,
                    selector=css_selector
                ))
                
            except Exception:
                continue
                
        return links
    
    async def _get_parent_text(self, element: Locator) -> Optional[str]:
        """Get text content from parent container(s)"""
        try:
            parent = await element.evaluate_handle("el => el.parentElement")
            if parent:
                text = await parent.evaluate("el => el.textContent")
                return text.strip()[:200] if text else None
        except Exception:
            pass
        return None

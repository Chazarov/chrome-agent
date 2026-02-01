from typing import List, Optional, Tuple
from playwright.async_api import Page, Locator

from models.button import Button, ButtonInternal
from models.link import Link
from models.input_field import Input, InputInternal
from models.page import PageTextItem, PageButtonsItem, PageLinksItem


class PageParser:
    """Parses webpage and extracts structured information with pagination support"""
    
    def __init__(self, page: Page):
        self.page = page
        self._element_id_counter = 0
    
    def _generate_element_id(self) -> int:
        """Generate unique element ID"""
        element_id = self._element_id_counter
        self._element_id_counter += 1
        return element_id
    
    async def get_visible_text(self) -> str:
        """Extract all visible text from the page"""
        try:
            text = await self.page.evaluate("""
                () => {
                    const body = document.body;
                    return body.innerText || body.textContent || '';
                }
            """)
            return text.strip()
        except Exception:
            return ""
    
    async def extract_buttons(self) -> Tuple[List[ButtonInternal], List[Button]]:
        """Extract buttons: internal (with Playwright elements) and external (for agent)"""
        buttons_internal = []
        buttons_external = []
        
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
                    is_visible = await element.is_visible()
                    if not is_visible:
                        continue
                    
                    text = await element.text_content()
                    if not text:
                        text = await element.get_attribute('value') or ''
                    text = text.strip()[:100]
                    
                    box = await element.bounding_box()
                    if not box:
                        continue
                    position = (box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                    
                    parent_text = await self._get_parent_text(element)
                    
                    element_id = self._generate_element_id()
                    
                    # Create locator for element
                    locator = self.page.locator(f"{selector}").nth(idx)
                    
                    buttons_internal.append(ButtonInternal(
                        element_id=element_id,
                        element=locator,
                        text=text,
                        position=position,
                        parent_text=parent_text
                    ))
                    
                    buttons_external.append(Button(
                        id=element_id,
                        text=text,
                        position=position,
                        parent_text=parent_text
                    ))
                    
                except Exception:
                    continue
        
        return buttons_internal, buttons_external
    
    async def extract_links(self) -> List[Link]:
        """Extract links (information for agent only, no Playwright elements needed)"""
        links = []
        elements = await self.page.query_selector_all('a[href]')
        
        for element in elements:
            try:
                is_visible = await element.is_visible()
                if not is_visible:
                    continue
                
                text = await element.text_content()
                if not text:
                    text = await element.get_attribute('aria-label') or ''
                text = text.strip()[:100]
                
                href = await element.get_attribute('href')
                if not href:
                    continue
                
                # Make absolute URL
                try:
                    url = await self.page.evaluate(
                        "(href) => new URL(href, window.location.href).href",
                        href
                    )
                except Exception:
                    url = href
                
                parent_text = await self._get_parent_text(element)
                
                links.append(Link(
                    text=text,
                    url=url,
                    parent_text=parent_text
                ))
                
            except Exception:
                continue
        
        return links
    
    async def extract_inputs(self) -> Tuple[List[InputInternal], List[Input]]:
        """Extract input fields: internal (with Playwright elements) and external (for agent)"""
        inputs_internal = []
        inputs_external = []
        
        selectors = [
            'input[type="text"]',
            'input[type="email"]',
            'input[type="password"]',
            'input[type="search"]',
            'input[type="tel"]',
            'input[type="url"]',
            'input:not([type])',
            'textarea'
        ]
        
        for selector in selectors:
            elements = await self.page.query_selector_all(selector)
            
            for idx, element in enumerate(elements):
                try:
                    is_visible = await element.is_visible()
                    if not is_visible:
                        continue
                    
                    input_type = await element.get_attribute('type') or 'text'
                    if selector == 'textarea':
                        input_type = 'textarea'
                    
                    name = await element.get_attribute('name') or ''
                    placeholder = await element.get_attribute('placeholder') or ''
                    
                    box = await element.bounding_box()
                    if not box:
                        continue
                    position = (box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                    
                    parent_text = await self._get_parent_text(element)
                    
                    element_id = self._generate_element_id()
                    
                    locator = self.page.locator(f"{selector}").nth(idx)
                    
                    inputs_internal.append(InputInternal(
                        element_id=element_id,
                        element=locator,
                        input_type=input_type,
                        name=name,
                        placeholder=placeholder,
                        position=position,
                        parent_text=parent_text
                    ))
                    
                    inputs_external.append(Input(
                        id=element_id,
                        input_type=input_type,
                        name=name,
                        placeholder=placeholder,
                        position=position,
                        parent_text=parent_text
                    ))
                    
                except Exception:
                    continue
        
        return inputs_internal, inputs_external
    
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
    
    # Helper methods for pagination
    
    def _get_max_y_coordinate(self, buttons: List[Button], inputs: List[Input]) -> float:
        """Get maximum Y coordinate from buttons and inputs"""
        max_y = 0.0
        
        for btn in buttons:
            if btn.position[1] > max_y:
                max_y = btn.position[1]
        
        for inp in inputs:
            if inp.position[1] > max_y:
                max_y = inp.position[1]
        
        return max_y
    
    def _filter_buttons_by_y_range(
        self,
        buttons_internal: List[ButtonInternal],
        buttons_external: List[Button],
        y_start: float,
        y_end: float
    ) -> Tuple[List[ButtonInternal], List[Button]]:
        """Filter buttons by Y-coordinate range"""
        buttons_int_filtered = [
            btn for btn in buttons_internal
            if y_start <= btn.position[1] < y_end
        ]
        
        buttons_ext_filtered = [
            btn for btn in buttons_external
            if y_start <= btn.position[1] < y_end
        ]
        
        return buttons_int_filtered, buttons_ext_filtered
    
    def _filter_inputs_by_y_range(
        self,
        inputs_internal: List[InputInternal],
        inputs_external: List[Input],
        y_start: float,
        y_end: float
    ) -> Tuple[List[InputInternal], List[Input]]:
        """Filter inputs by Y-coordinate range"""
        inputs_int_filtered = [
            inp for inp in inputs_internal
            if y_start <= inp.position[1] < y_end
        ]
        
        inputs_ext_filtered = [
            inp for inp in inputs_external
            if y_start <= inp.position[1] < y_end
        ]
        
        return inputs_int_filtered, inputs_ext_filtered
    
    # Pagination methods
    
    async def parse_page_text_items(self) -> List[PageTextItem]:
        """Parse page text and split into chunks"""
        from config import config
        
        url = self.page.url
        title = await self.page.title()
        full_text = await self.get_visible_text()
        
        chunk_size = config.text_chunk_size
        items = []
        
        for i in range(0, len(full_text), chunk_size):
            text_chunk = full_text[i:i + chunk_size]
            items.append(PageTextItem(
                item_id=len(items),
                total_items=-1,
                url=url,
                title=title,
                text_chunk=text_chunk
            ))
        
        if not items:
            items = [PageTextItem(
                item_id=0,
                total_items=1,
                url=url,
                title=title,
                text_chunk=""
            )]
        
        # Update total_items
        total = len(items)
        items = [
            PageTextItem(
                item_id=item.item_id,
                total_items=total,
                url=item.url,
                title=item.title,
                text_chunk=item.text_chunk
            )
            for item in items
        ]
        
        return items
    
    async def parse_page_buttons_items(self) -> Tuple[List[ButtonInternal], List[InputInternal], List[PageButtonsItem]]:
        """Parse buttons and inputs, split by Y-coordinate ranges
        
        Returns:
            Tuple of (all_buttons_internal, all_inputs_internal, buttons_items_for_agent)
        """
        from config import config
        
        url = self.page.url
        title = await self.page.title()
        
        # Extract all elements
        buttons_internal, buttons_external = await self.extract_buttons()
        inputs_internal, inputs_external = await self.extract_inputs()
        
        # Determine max_y
        max_y = self._get_max_y_coordinate(buttons_external, inputs_external)
        
        if max_y == 0:
            max_y = await self.page.evaluate("() => document.body.scrollHeight")
        
        section_height = config.parse_item_size
        
        items = []
        y_start = 0.0
        
        while y_start < max_y:
            y_end = y_start + section_height
            
            _, buttons_ext_filtered = self._filter_buttons_by_y_range(
                buttons_internal, buttons_external,
                y_start, y_end
            )
            
            _, inputs_ext_filtered = self._filter_inputs_by_y_range(
                inputs_internal, inputs_external,
                y_start, y_end
            )
            
            items.append(PageButtonsItem(
                item_id=len(items),
                total_items=-1,
                url=url,
                title=title,
                buttons=buttons_ext_filtered,
                inputs=inputs_ext_filtered
            ))
            
            y_start = y_end
        
        if not items:
            items = [PageButtonsItem(
                item_id=0,
                total_items=1,
                url=url,
                title=title,
                buttons=[],
                inputs=[]
            )]
        
        # Update total_items
        total = len(items)
        items = [
            PageButtonsItem(
                item_id=item.item_id,
                total_items=total,
                url=item.url,
                title=item.title,
                buttons=item.buttons,
                inputs=item.inputs
            )
            for item in items
        ]
        
        return buttons_internal, inputs_internal, items
    
    async def parse_page_links_items(self) -> List[PageLinksItem]:
        """Parse links and split into chunks by count
        
        Returns:
            List of PageLinksItem for agent
        """
        from config import config
        
        url = self.page.url
        title = await self.page.title()
        
        all_links = await self.extract_links()
        
        chunk_size = config.links_chunk_size
        items = []
        
        for i in range(0, len(all_links), chunk_size):
            links_chunk = all_links[i:i + chunk_size]
            items.append(PageLinksItem(
                item_id=len(items),
                total_items=-1,
                url=url,
                title=title,
                links=links_chunk
            ))
        
        if not items:
            items = [PageLinksItem(
                item_id=0,
                total_items=1,
                url=url,
                title=title,
                links=[]
            )]
        
        # Update total_items
        total = len(items)
        items = [
            PageLinksItem(
                item_id=item.item_id,
                total_items=total,
                url=item.url,
                title=item.title,
                links=item.links
            )
            for item in items
        ]
        
        return items

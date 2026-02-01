"""Tests for buttons/inputs pagination functionality"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


def create_mock_element(text, x, y, visible=True, value=None):
    """Helper to create mock Playwright element"""
    element = MagicMock()
    element.is_visible = AsyncMock(return_value=visible)
    element.text_content = AsyncMock(return_value=text)
    element.get_attribute = AsyncMock(side_effect=lambda attr: {
        'value': value,
        'type': 'text',
        'name': 'test_name',
        'placeholder': 'test_placeholder'
    }.get(attr, ''))
    element.bounding_box = AsyncMock(return_value={
        'x': x, 'y': y, 'width': 100, 'height': 30
    })
    element.evaluate_handle = AsyncMock(return_value=MagicMock(
        evaluate=AsyncMock(return_value="Parent text")
    ))
    return element


@pytest.fixture
def mock_page_with_buttons():
    """Create a mock page with buttons and inputs at different Y positions"""
    page = MagicMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Test Page")
    page.evaluate = AsyncMock(return_value=2500)  # scrollHeight
    
    # Create buttons at different Y positions
    buttons = [
        create_mock_element("Button 1", 100, 200),   # Y=200, should be in first chunk
        create_mock_element("Button 2", 100, 800),   # Y=800, should be in first chunk
        create_mock_element("Button 3", 100, 1200),  # Y=1200, should be in second chunk
        create_mock_element("Button 4", 100, 1800),  # Y=1800, should be in second chunk
        create_mock_element("Button 5", 100, 2200),  # Y=2200, should be in third chunk
    ]
    
    inputs = [
        create_mock_element("", 100, 300),  # Y=300, first chunk
        create_mock_element("", 100, 1500), # Y=1500, second chunk
    ]
    
    def mock_query_selector_all(selector):
        if selector == 'button':
            return AsyncMock(return_value=buttons)()
        elif selector.startswith('input[type="text"]'):
            return AsyncMock(return_value=inputs)()
        else:
            return AsyncMock(return_value=[])()
    
    page.query_selector_all = mock_query_selector_all
    page.locator = MagicMock(return_value=MagicMock(nth=MagicMock(return_value=MagicMock())))
    
    return page


@pytest.mark.asyncio
async def test_parse_page_buttons_items_creates_sections(mock_page_with_buttons):
    """Test that buttons/inputs are properly split by Y-coordinates"""
    from parser.page_parser import PageParser
    
    parser = PageParser(mock_page_with_buttons)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.parse_item_size = 1000  # 1000px sections
        
        buttons_internal, inputs_internal, items = await parser.parse_page_buttons_items()
    
    # Should have internal elements stored
    assert len(buttons_internal) == 5  # All buttons
    assert len(inputs_internal) == 2   # All inputs
    
    # Should create 3 sections (0-1000, 1000-2000, 2000-3000)
    assert len(items) == 3
    
    # Check first section (0-1000)
    assert items[0].item_id == 0
    assert items[0].total_items == 3
    # Buttons at Y=200, Y=800 should be in first chunk
    # Input at Y=300 should be in first chunk


@pytest.mark.asyncio
async def test_buttons_have_unique_ids(mock_page_with_buttons):
    """Test that all buttons have unique IDs"""
    from parser.page_parser import PageParser
    
    parser = PageParser(mock_page_with_buttons)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.parse_item_size = 1000
        
        buttons_internal, _, items = await parser.parse_page_buttons_items()
    
    # Collect all IDs
    ids = [btn.id for btn in buttons_internal]
    
    # All IDs should be unique
    assert len(ids) == len(set(ids))


@pytest.mark.asyncio
async def test_empty_page_returns_one_item():
    """Test that empty page returns single empty item"""
    from parser.page_parser import PageParser
    
    page = MagicMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Empty Page")
    page.evaluate = AsyncMock(return_value=0)  # No scrollHeight
    page.query_selector_all = AsyncMock(return_value=[])
    
    parser = PageParser(page)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.parse_item_size = 1000
        
        buttons_internal, inputs_internal, items = await parser.parse_page_buttons_items()
    
    assert len(items) == 1
    assert items[0].buttons == []
    assert items[0].inputs == []
    assert items[0].total_items == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""Tests for links pagination functionality"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


def create_mock_link(text, url):
    """Helper to create mock link element"""
    element = MagicMock()
    element.is_visible = AsyncMock(return_value=True)
    element.text_content = AsyncMock(return_value=text)
    element.get_attribute = AsyncMock(side_effect=lambda attr: {
        'href': url,
        'aria-label': ''
    }.get(attr, ''))
    element.bounding_box = AsyncMock(return_value={
        'x': 100, 'y': 100, 'width': 100, 'height': 20
    })
    element.evaluate_handle = AsyncMock(return_value=MagicMock(
        evaluate=AsyncMock(return_value="Parent text")
    ))
    return element


@pytest.fixture
def mock_page_with_links():
    """Create a mock page with many links"""
    page = MagicMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Test Page")
    
    # Create 50 links
    links = [
        create_mock_link(f"Link {i}", f"https://example.com/page{i}")
        for i in range(50)
    ]
    
    page.query_selector_all = AsyncMock(return_value=links)
    
    # Mock evaluate for URL resolution
    async def mock_evaluate(script, arg=None):
        if arg:
            return arg  # Return the href as-is
        return 1000  # Default for other evaluations
    
    page.evaluate = mock_evaluate
    
    return page


@pytest.mark.asyncio
async def test_parse_page_links_items_creates_chunks(mock_page_with_links):
    """Test that links are properly split into chunks"""
    from parser.page_parser import PageParser
    
    parser = PageParser(mock_page_with_links)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.links_chunk_size = 20
        
        items = await parser.parse_page_links_items()
    
    # Should create 3 chunks (50 / 20 = 2.5, rounded up = 3)
    assert len(items) == 3
    
    # Check item structure
    assert items[0].item_id == 0
    assert items[0].total_items == 3
    assert items[0].url == "https://example.com"
    assert items[0].title == "Test Page"
    assert len(items[0].links) == 20
    
    # Second chunk
    assert items[1].item_id == 1
    assert len(items[1].links) == 20
    
    # Last chunk (remainder)
    assert items[2].item_id == 2
    assert len(items[2].links) == 10


@pytest.mark.asyncio
async def test_links_have_no_id_or_position():
    """Test that Link model doesn't have id or position fields"""
    from models.link import Link
    
    link = Link(
        text="Test Link",
        url="https://example.com",
        parent_text="Parent"
    )
    
    # Verify structure
    assert link.text == "Test Link"
    assert link.url == "https://example.com"
    assert link.parent_text == "Parent"
    
    # Verify no id or position fields
    assert not hasattr(link, 'id') or 'id' not in link.model_fields
    assert not hasattr(link, 'position') or 'position' not in link.model_fields
    assert not hasattr(link, 'selector') or 'selector' not in link.model_fields


@pytest.mark.asyncio
async def test_empty_page_returns_one_item():
    """Test that page with no links returns single empty item"""
    from parser.page_parser import PageParser
    
    page = MagicMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Empty Page")
    page.query_selector_all = AsyncMock(return_value=[])
    
    parser = PageParser(page)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.links_chunk_size = 20
        
        items = await parser.parse_page_links_items()
    
    assert len(items) == 1
    assert items[0].links == []
    assert items[0].total_items == 1


@pytest.mark.asyncio
async def test_links_small_page():
    """Test page with fewer links than chunk size"""
    from parser.page_parser import PageParser
    
    page = MagicMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Small Page")
    
    # Create 5 links
    links = [
        create_mock_link(f"Link {i}", f"https://example.com/page{i}")
        for i in range(5)
    ]
    page.query_selector_all = AsyncMock(return_value=links)
    
    async def mock_evaluate(script, arg=None):
        if arg:
            return arg
        return 500
    page.evaluate = mock_evaluate
    
    parser = PageParser(page)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.links_chunk_size = 20
        
        items = await parser.parse_page_links_items()
    
    assert len(items) == 1
    assert len(items[0].links) == 5
    assert items[0].total_items == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

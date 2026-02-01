"""Tests for text pagination functionality"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_page():
    """Create a mock Playwright page"""
    page = MagicMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Test Page")
    
    # Create a long text for testing chunking
    long_text = "A" * 2100  # This should create 3 chunks with 700 char size
    page.evaluate = AsyncMock(return_value=long_text)
    
    return page


@pytest.mark.asyncio
async def test_parse_page_text_items_creates_chunks(mock_page):
    """Test that text is properly split into chunks"""
    from parser.page_parser import PageParser
    
    parser = PageParser(mock_page)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.text_chunk_size = 700
        
        items = await parser.parse_page_text_items()
    
    # Should create 3 chunks (2100 / 700 = 3)
    assert len(items) == 3
    
    # Check item structure
    assert items[0].item_id == 0
    assert items[0].total_items == 3
    assert items[0].url == "https://example.com"
    assert items[0].title == "Test Page"
    assert len(items[0].text_chunk) == 700
    
    # Last item
    assert items[2].item_id == 2
    assert items[2].total_items == 3


@pytest.mark.asyncio
async def test_parse_page_text_items_empty_text(mock_page):
    """Test handling of empty page text"""
    from parser.page_parser import PageParser
    
    mock_page.evaluate = AsyncMock(return_value="")
    parser = PageParser(mock_page)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.text_chunk_size = 700
        
        items = await parser.parse_page_text_items()
    
    # Should create 1 empty item
    assert len(items) == 1
    assert items[0].text_chunk == ""
    assert items[0].total_items == 1


@pytest.mark.asyncio
async def test_parse_page_text_items_small_text(mock_page):
    """Test handling of text smaller than chunk size"""
    from parser.page_parser import PageParser
    
    mock_page.evaluate = AsyncMock(return_value="Small text")
    parser = PageParser(mock_page)
    
    with patch('parser.page_parser.config') as mock_config:
        mock_config.text_chunk_size = 700
        
        items = await parser.parse_page_text_items()
    
    # Should create 1 item
    assert len(items) == 1
    assert items[0].text_chunk == "Small text"
    assert items[0].total_items == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

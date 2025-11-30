#!/usr/bin/env python3
"""Tests for pagination helpers."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from zerion_mcp_server.pagination import (
    fetch_all_pages,
    extract_cursor_from_url,
    fetch_page
)
from zerion_mcp_server.errors import ValidationError


@pytest.mark.asyncio
class TestFetchAllPages:
    """Tests for fetch_all_pages function."""

    async def test_single_page_no_next(self):
        """Test fetching when there's only one page."""
        mock_api_call = AsyncMock(return_value={
            "data": [{"id": 1}, {"id": 2}],
            "links": {}  # No next link
        })

        result = await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=10,
            page_size=100
        )

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2
        assert mock_api_call.call_count == 1

    async def test_multiple_pages(self):
        """Test fetching multiple pages."""
        # Simulate 3 pages of data
        responses = [
            {
                "data": [{"id": 1}, {"id": 2}],
                "links": {"next": "https://api.test.com/endpoint?page[after]=cursor1"}
            },
            {
                "data": [{"id": 3}, {"id": 4}],
                "links": {"next": "https://api.test.com/endpoint?page[after]=cursor2"}
            },
            {
                "data": [{"id": 5}],
                "links": {}  # Last page
            }
        ]

        mock_api_call = AsyncMock(side_effect=responses)

        result = await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=10,
            page_size=100
        )

        assert len(result) == 5
        assert result[0]["id"] == 1
        assert result[4]["id"] == 5
        assert mock_api_call.call_count == 3

    async def test_max_pages_limit(self):
        """Test that max_pages limit is respected."""
        # Simulate infinite pagination
        def create_response(page_num):
            return {
                "data": [{"id": page_num}],
                "links": {"next": f"https://api.test.com/endpoint?page[after]=cursor{page_num}"}
            }

        mock_api_call = AsyncMock(side_effect=[create_response(i) for i in range(10)])

        result = await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=3,  # Limit to 3 pages
            page_size=100
        )

        assert len(result) == 3
        assert mock_api_call.call_count == 3

    async def test_empty_result_set(self):
        """Test fetching when result set is empty."""
        mock_api_call = AsyncMock(return_value={
            "data": [],
            "links": {}
        })

        result = await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=10,
            page_size=100
        )

        assert len(result) == 0
        assert mock_api_call.call_count == 1

    async def test_default_max_pages(self):
        """Test that default max_pages is applied."""
        # Create many pages to exceed default limit
        def create_response(page_num):
            if page_num < 60:  # More than default max (50)
                return {
                    "data": [{"id": page_num}],
                    "links": {"next": f"https://api.test.com/endpoint?page[after]=cursor{page_num}"}
                }
            return {
                "data": [{"id": page_num}],
                "links": {}
            }

        mock_api_call = AsyncMock(side_effect=[create_response(i) for i in range(60)])

        result = await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=None,  # Use default
            page_size=100
        )

        # Should stop at default max_pages (50)
        assert len(result) == 50
        assert mock_api_call.call_count == 50

    async def test_invalid_response_no_data_field(self):
        """Test error handling when response missing 'data' field."""
        mock_api_call = AsyncMock(return_value={
            "items": [{"id": 1}],  # Wrong field name
            "links": {}
        })

        with pytest.raises(ValidationError) as exc_info:
            await fetch_all_pages(
                api_call=mock_api_call,
                max_pages=10,
                page_size=100
            )

        assert "missing 'data' field" in str(exc_info.value)

    async def test_invalid_response_not_dict(self):
        """Test error handling when response is not a dict."""
        mock_api_call = AsyncMock(return_value=["item1", "item2"])  # List instead of dict

        with pytest.raises(ValidationError) as exc_info:
            await fetch_all_pages(
                api_call=mock_api_call,
                max_pages=10,
                page_size=100
            )

        assert "expected dict" in str(exc_info.value)

    async def test_invalid_data_not_list(self):
        """Test error handling when data field is not a list."""
        mock_api_call = AsyncMock(return_value={
            "data": {"id": 1},  # Dict instead of list
            "links": {}
        })

        with pytest.raises(ValidationError) as exc_info:
            await fetch_all_pages(
                api_call=mock_api_call,
                max_pages=10,
                page_size=100
            )

        assert "expected list" in str(exc_info.value)

    async def test_additional_params_passed_through(self):
        """Test that additional parameters are passed to api_call."""
        mock_api_call = AsyncMock(return_value={
            "data": [{"id": 1}],
            "links": {}
        })

        await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=10,
            page_size=100,
            address="0x123",
            filter_chain_ids="ethereum"
        )

        # Check that params were passed
        call_kwargs = mock_api_call.call_args[1]
        assert call_kwargs["address"] == "0x123"
        assert call_kwargs["filter_chain_ids"] == "ethereum"
        assert call_kwargs["page[size]"] == 100


class TestExtractCursorFromUrl:
    """Tests for extract_cursor_from_url function."""

    def test_extract_cursor_success(self):
        """Test extracting cursor from valid URL."""
        url = "https://api.zerion.io/v1/wallets/0x123/transactions?page[after]=abc123xyz"
        cursor = extract_cursor_from_url(url)
        assert cursor == "abc123xyz"

    def test_extract_cursor_with_multiple_params(self):
        """Test extracting cursor from URL with multiple params."""
        url = "https://api.zerion.io/v1/wallets/0x123/transactions?page[size]=100&page[after]=cursor123&filter[trash]=only_non_trash"
        cursor = extract_cursor_from_url(url)
        assert cursor == "cursor123"

    def test_extract_cursor_no_cursor_param(self):
        """Test extracting cursor when page[after] is missing."""
        url = "https://api.zerion.io/v1/wallets/0x123/transactions?page[size]=100"
        cursor = extract_cursor_from_url(url)
        assert cursor is None

    def test_extract_cursor_empty_url(self):
        """Test extracting cursor from empty URL."""
        cursor = extract_cursor_from_url("")
        assert cursor is None

    def test_extract_cursor_malformed_url(self):
        """Test extracting cursor from malformed URL."""
        url = "not-a-valid-url"
        cursor = extract_cursor_from_url(url)
        assert cursor is None

    def test_extract_cursor_url_encoded(self):
        """Test extracting URL-encoded cursor."""
        url = "https://api.test.com/endpoint?page[after]=abc%20123"
        cursor = extract_cursor_from_url(url)
        assert cursor == "abc 123"


@pytest.mark.asyncio
class TestFetchPage:
    """Tests for fetch_page function."""

    async def test_fetch_first_page(self):
        """Test fetching first page without cursor."""
        mock_api_call = AsyncMock(return_value={
            "data": [{"id": 1}, {"id": 2}],
            "links": {"next": "https://api.test.com/endpoint?page[after]=cursor1"}
        })

        result = await fetch_page(
            api_call=mock_api_call,
            page_size=50
        )

        assert len(result["data"]) == 2
        assert "next" in result["links"]

        # Check params
        call_kwargs = mock_api_call.call_args[1]
        assert call_kwargs["page[size]"] == 50
        assert "page[after]" not in call_kwargs

    async def test_fetch_page_with_cursor(self):
        """Test fetching page with cursor."""
        mock_api_call = AsyncMock(return_value={
            "data": [{"id": 3}, {"id": 4}],
            "links": {"next": "https://api.test.com/endpoint?page[after]=cursor2"}
        })

        result = await fetch_page(
            api_call=mock_api_call,
            page_size=50,
            page_after="cursor1"
        )

        assert len(result["data"]) == 2

        # Check params
        call_kwargs = mock_api_call.call_args[1]
        assert call_kwargs["page[size]"] == 50
        assert call_kwargs["page[after]"] == "cursor1"

    async def test_fetch_last_page(self):
        """Test fetching last page (no next link)."""
        mock_api_call = AsyncMock(return_value={
            "data": [{"id": 5}],
            "links": {}  # No next
        })

        result = await fetch_page(
            api_call=mock_api_call,
            page_size=50,
            page_after="cursor2"
        )

        assert len(result["data"]) == 1
        assert "next" not in result["links"]

    async def test_fetch_page_with_additional_params(self):
        """Test that additional params are passed through."""
        mock_api_call = AsyncMock(return_value={
            "data": [],
            "links": {}
        })

        await fetch_page(
            api_call=mock_api_call,
            page_size=100,
            address="0xabc",
            filter_trash="only_non_trash"
        )

        call_kwargs = mock_api_call.call_args[1]
        assert call_kwargs["address"] == "0xabc"
        assert call_kwargs["filter_trash"] == "only_non_trash"


@pytest.mark.asyncio
class TestPaginationIntegration:
    """Integration tests for pagination helpers."""

    async def test_real_world_pagination_scenario(self):
        """Test realistic pagination scenario with filters."""
        # Simulate fetching transactions for an active wallet
        page1 = {
            "data": [{"hash": f"0x{i}"} for i in range(100)],
            "links": {"next": "https://api.test.com/transactions?page[after]=cursor1"}
        }
        page2 = {
            "data": [{"hash": f"0x{i}"} for i in range(100, 200)],
            "links": {"next": "https://api.test.com/transactions?page[after]=cursor2"}
        }
        page3 = {
            "data": [{"hash": f"0x{i}"} for i in range(200, 250)],
            "links": {}  # Last page
        }

        mock_api_call = AsyncMock(side_effect=[page1, page2, page3])

        result = await fetch_all_pages(
            api_call=mock_api_call,
            max_pages=10,
            page_size=100,
            address="0xActiveWallet",
            filter_trash="only_non_trash",
            filter_chain_ids="ethereum"
        )

        # Should have all 250 transactions
        assert len(result) == 250
        assert result[0]["hash"] == "0x0"
        assert result[249]["hash"] == "0x249"

        # Verify params were passed correctly
        for call in mock_api_call.call_args_list:
            kwargs = call[1]
            assert kwargs["address"] == "0xActiveWallet"
            assert kwargs["filter_trash"] == "only_non_trash"
            assert kwargs["filter_chain_ids"] == "ethereum"

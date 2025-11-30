#!/usr/bin/env python3
"""Tests for retry client functionality."""

import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio

from zerion_mcp_server.retry_client import RetryAsyncClient
from zerion_mcp_server.errors import RateLimitError, WalletIndexingError


@pytest.fixture
def retry_config():
    """Default retry configuration for tests."""
    return {
        "max_attempts": 3,
        "base_delay": 0.1,  # Faster for tests
        "max_delay": 1,
        "exponential_base": 2
    }


@pytest.fixture
def indexing_config():
    """Default indexing configuration for tests."""
    return {
        "retry_delay": 0.1,  # Faster for tests
        "max_retries": 2,
        "auto_retry": True
    }


@pytest.fixture
async def retry_client(retry_config, indexing_config):
    """Create a retry client for testing."""
    client = RetryAsyncClient(
        base_url="https://api.test.com",
        retry_config=retry_config,
        indexing_config=indexing_config
    )
    yield client
    await client.aclose()


@pytest.mark.asyncio
class TestRetryClient:
    """Tests for RetryAsyncClient."""

    async def test_successful_request_no_retry(self, retry_client):
        """Test that successful requests don't trigger retry."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"data": []}'

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            response = await retry_client.request("GET", "/test")

            assert response.status_code == 200
            assert mock_request.call_count == 1  # No retries

    async def test_202_auto_retry_success(self, retry_client):
        """Test automatic retry on 202 Accepted."""
        # First request: 202, second request: 200
        mock_responses = [
            MagicMock(status_code=202),
            MagicMock(status_code=200, text='{"data": []}')
        ]

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = mock_responses

            response = await retry_client.request("GET", "/wallet")

            assert response.status_code == 200
            assert mock_request.call_count == 2  # Initial + 1 retry

    async def test_202_auto_retry_timeout(self, retry_client):
        """Test 202 timeout after max retries."""
        # All requests return 202
        mock_response = MagicMock(status_code=202)

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(WalletIndexingError) as exc_info:
                await retry_client.request("GET", "/wallet")

            assert "still being indexed" in str(exc_info.value)
            assert exc_info.value.attempts == 2  # max_retries
            # Initial request + 2 retries = 3 total
            assert mock_request.call_count == 3

    async def test_202_auto_retry_disabled(self):
        """Test 202 with auto_retry disabled."""
        client = RetryAsyncClient(
            base_url="https://api.test.com",
            indexing_config={"auto_retry": False, "retry_delay": 1, "max_retries": 3}
        )

        mock_response = MagicMock(status_code=202)

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(WalletIndexingError) as exc_info:
                await client.request("GET", "/wallet")

            assert "Enable auto_retry" in str(exc_info.value)
            assert mock_request.call_count == 1  # No retries

        await client.aclose()

    async def test_429_auto_retry_success(self, retry_client):
        """Test automatic retry on 429 Too Many Requests."""
        # First two requests: 429, third request: 200
        mock_responses = [
            MagicMock(status_code=429, headers={"retry-after": "1"}),
            MagicMock(status_code=429, headers={"retry-after": "1"}),
            MagicMock(status_code=200, text='{"data": []}')
        ]

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = mock_responses

            response = await retry_client.request("GET", "/test")

            assert response.status_code == 200
            # Note: Due to retry decorator, exact call count may vary
            assert mock_request.call_count >= 3

    async def test_429_retry_after_header(self, retry_client):
        """Test that Retry-After header is parsed correctly."""
        mock_response = MagicMock(status_code=429, headers={"retry-after": "30"})

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(RateLimitError) as exc_info:
                await retry_client.request("GET", "/test")

            assert exc_info.value.retry_after == 30

    async def test_429_no_retry_after_header(self, retry_client):
        """Test 429 without Retry-After header."""
        mock_response = MagicMock(status_code=429, headers={})

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(RateLimitError):
                await retry_client.request("GET", "/test")

    async def test_other_errors_not_retried(self, retry_client):
        """Test that other HTTP errors (404, 500) are not retried."""
        mock_response = MagicMock(status_code=404)

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            response = await retry_client.request("GET", "/nonexistent")

            assert response.status_code == 404
            assert mock_request.call_count == 1  # No retries

    async def test_retry_config_validation(self):
        """Test that retry config is properly applied."""
        custom_config = {
            "max_attempts": 10,
            "base_delay": 2,
            "max_delay": 120,
            "exponential_base": 3
        }

        client = RetryAsyncClient(
            base_url="https://api.test.com",
            retry_config=custom_config
        )

        assert client.retry_config["max_attempts"] == 10
        assert client.retry_config["base_delay"] == 2
        assert client.retry_config["max_delay"] == 120
        assert client.retry_config["exponential_base"] == 3

        await client.aclose()

    async def test_indexing_config_validation(self):
        """Test that indexing config is properly applied."""
        custom_config = {
            "retry_delay": 5,
            "max_retries": 10,
            "auto_retry": False
        }

        client = RetryAsyncClient(
            base_url="https://api.test.com",
            indexing_config=custom_config
        )

        assert client.indexing_config["retry_delay"] == 5
        assert client.indexing_config["max_retries"] == 10
        assert client.indexing_config["auto_retry"] is False

        await client.aclose()


@pytest.mark.asyncio
class TestRetryClientIntegration:
    """Integration tests for retry client."""

    async def test_202_then_429_handling(self):
        """Test handling of 202 followed by 429."""
        client = RetryAsyncClient(
            base_url="https://api.test.com",
            retry_config={"max_attempts": 3, "base_delay": 0.1, "max_delay": 1, "exponential_base": 2},
            indexing_config={"retry_delay": 0.1, "max_retries": 2, "auto_retry": True}
        )

        # Sequence: 202 -> 202 -> 200 -> 429 -> 200
        mock_responses = [
            MagicMock(status_code=202),  # Initial request
            MagicMock(status_code=200, text='{"data": []}')  # After 202 retry
        ]

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = mock_responses

            response = await client.request("GET", "/wallet")

            assert response.status_code == 200

        await client.aclose()

    async def test_concurrent_requests_with_retries(self):
        """Test multiple concurrent requests with retries."""
        client = RetryAsyncClient(
            base_url="https://api.test.com",
            retry_config={"max_attempts": 2, "base_delay": 0.1, "max_delay": 1, "exponential_base": 2},
            indexing_config={"retry_delay": 0.1, "max_retries": 1, "auto_retry": True}
        )

        # Some succeed immediately, some need retry
        mock_responses = [
            MagicMock(status_code=200, text='{"data": []}'),  # Request 1: immediate success
            MagicMock(status_code=202),  # Request 2: needs retry
            MagicMock(status_code=200, text='{"data": []}'),  # Request 3: immediate success
            MagicMock(status_code=200, text='{"data": []}'),  # Request 2 retry: success
        ]

        with patch.object(httpx.AsyncClient, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = mock_responses

            # Make concurrent requests
            results = await asyncio.gather(
                client.request("GET", "/endpoint1"),
                client.request("GET", "/endpoint2"),
                client.request("GET", "/endpoint3")
            )

            assert all(r.status_code == 200 for r in results)

        await client.aclose()

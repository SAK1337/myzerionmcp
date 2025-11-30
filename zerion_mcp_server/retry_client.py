#!/usr/bin/env python3
"""HTTP client with automatic retry logic for rate limiting and wallet indexing."""

import asyncio
from typing import Optional, Any
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryCallState
)

from .errors import RateLimitError, WalletIndexingError, APIError
from .logger import get_logger

logger = get_logger(__name__)


class RetryAsyncClient(httpx.AsyncClient):
    """AsyncClient with automatic retry logic for 429 and 202 responses.

    This client wraps httpx.AsyncClient and adds transparent retry handling for:
    - 429 Too Many Requests (rate limiting) - exponential backoff
    - 202 Accepted (wallet indexing) - fixed delay retry

    Attributes:
        retry_config: Configuration for retry behavior
        indexing_config: Configuration for 202 handling
    """

    def __init__(
        self,
        *args,
        retry_config: Optional[dict] = None,
        indexing_config: Optional[dict] = None,
        **kwargs
    ):
        """Initialize retry client.

        Args:
            retry_config: Retry policy configuration with keys:
                - max_attempts: Maximum retry attempts (default: 5)
                - base_delay: Base delay in seconds (default: 1)
                - max_delay: Maximum delay in seconds (default: 60)
                - exponential_base: Backoff multiplier (default: 2)
            indexing_config: Wallet indexing configuration with keys:
                - retry_delay: Delay between retries in seconds (default: 3)
                - max_retries: Maximum retry attempts (default: 3)
                - auto_retry: Enable automatic retry (default: True)
        """
        super().__init__(*args, **kwargs)

        # Default retry configuration
        self.retry_config = retry_config or {
            "max_attempts": 5,
            "base_delay": 1,
            "max_delay": 60,
            "exponential_base": 2
        }

        # Default indexing configuration
        self.indexing_config = indexing_config or {
            "retry_delay": 3,
            "max_retries": 3,
            "auto_retry": True
        }

        logger.debug("RetryAsyncClient initialized", extra={
            "retry_max_attempts": self.retry_config["max_attempts"],
            "indexing_auto_retry": self.indexing_config["auto_retry"]
        })

    async def request(
        self,
        method: str,
        url: httpx.URL | str,
        *,
        content: Any = None,
        data: Any = None,
        files: Any = None,
        json: Any = None,
        params: Any = None,
        headers: Any = None,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with automatic retry logic.

        This method wraps the parent request() and adds:
        - Rate limit detection and exponential backoff retry
        - Wallet indexing detection and fixed delay retry

        Args:
            method: HTTP method
            url: Request URL
            content: Request content
            data: Form data
            files: Files to upload
            json: JSON data
            params: Query parameters
            headers: Request headers
            **kwargs: Additional arguments

        Returns:
            httpx.Response object

        Raises:
            RateLimitError: If rate limit exceeded after max retries
            WalletIndexingError: If wallet indexing timeout after max retries
            APIError: For other API errors
        """
        # Make initial request
        response = await super().request(
            method, url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            **kwargs
        )

        # Handle 202 Accepted (wallet indexing)
        if response.status_code == 202:
            response = await self._handle_202_accepted(
                method, url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                **kwargs
            )

        # Handle 429 Too Many Requests (rate limiting)
        elif response.status_code == 429:
            response = await self._handle_429_rate_limit(
                method, url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                **kwargs
            )

        return response

    async def _handle_202_accepted(
        self,
        method: str,
        url: httpx.URL | str,
        **request_kwargs
    ) -> httpx.Response:
        """Handle 202 Accepted response with fixed delay retry.

        Args:
            method: HTTP method
            url: Request URL
            **request_kwargs: Request arguments

        Returns:
            httpx.Response with status 200 (success)

        Raises:
            WalletIndexingError: If indexing timeout after max retries
        """
        if not self.indexing_config["auto_retry"]:
            # Auto-retry disabled, raise error immediately
            raise WalletIndexingError(
                "Wallet indexing in progress. This is a new wallet address for Zerion. "
                "Enable auto_retry in configuration or wait and retry manually.",
                retry_delay=self.indexing_config["retry_delay"],
                max_retries=0,
                attempts=0
            )

        retry_delay = self.indexing_config["retry_delay"]
        max_retries = self.indexing_config["max_retries"]

        logger.info(
            "Wallet indexing in progress, will retry",
            extra={
                "url": str(url),
                "retry_delay_sec": retry_delay,
                "max_retries": max_retries
            }
        )

        # Retry with fixed delay
        for attempt in range(1, max_retries + 1):
            await asyncio.sleep(retry_delay)

            logger.info(
                f"Retrying wallet indexing request",
                extra={
                    "attempt": f"{attempt}/{max_retries}",
                    "url": str(url)
                }
            )

            response = await super().request(method, url, **request_kwargs)

            if response.status_code == 200:
                logger.info(
                    "Wallet indexing completed successfully",
                    extra={
                        "attempts": attempt,
                        "total_wait_sec": attempt * retry_delay,
                        "url": str(url)
                    }
                )
                return response
            elif response.status_code != 202:
                # Different error, return it
                return response

        # Max retries exhausted
        total_wait = max_retries * retry_delay
        logger.warning(
            "Wallet indexing timeout",
            extra={
                "url": str(url),
                "attempts": max_retries,
                "total_wait_sec": total_wait
            }
        )

        raise WalletIndexingError(
            f"Wallet is still being indexed by Zerion. "
            f"Tried {max_retries} times over {total_wait} seconds. "
            f"Please retry in 30-60 seconds.",
            retry_delay=retry_delay,
            max_retries=max_retries,
            attempts=max_retries
        )

    async def _handle_429_rate_limit(
        self,
        method: str,
        url: httpx.URL | str,
        **request_kwargs
    ) -> httpx.Response:
        """Handle 429 Too Many Requests with exponential backoff retry.

        Uses tenacity library for retry logic with exponential backoff.

        Args:
            method: HTTP method
            url: Request URL
            **request_kwargs: Request arguments

        Returns:
            httpx.Response with status 200 (success)

        Raises:
            RateLimitError: If rate limit still exceeded after max retries
        """
        # Get retry-after header if present
        retry_after = None
        response = await super().request(method, url, **request_kwargs)

        if "retry-after" in response.headers:
            try:
                retry_after = int(response.headers["retry-after"])
            except ValueError:
                logger.warning(
                    "Invalid Retry-After header value",
                    extra={"value": response.headers["retry-after"]}
                )

        logger.warning(
            "Rate limit exceeded",
            extra={
                "url": str(url),
                "retry_after_sec": retry_after,
                "status_code": 429
            }
        )

        # Create retry decorator dynamically with config
        retry_decorator = retry(
            retry=retry_if_exception_type(RateLimitError),
            wait=wait_exponential(
                multiplier=self.retry_config["base_delay"],
                min=self.retry_config["base_delay"],
                max=self.retry_config["max_delay"]
            ),
            stop=stop_after_attempt(self.retry_config["max_attempts"]),
            reraise=True,
            before_sleep=self._log_retry_attempt
        )

        @retry_decorator
        async def _retry_request():
            """Inner function to retry with exponential backoff."""
            resp = await super(RetryAsyncClient, self).request(method, url, **request_kwargs)

            if resp.status_code == 429:
                # Still rate limited, raise error to trigger retry
                attempts = getattr(_retry_request.retry, 'statistics', {}).get('attempt_number', 0)
                raise RateLimitError(
                    f"Rate limit exceeded. Retry after {retry_after or 'unknown'} seconds.",
                    retry_after=retry_after,
                    attempts=attempts
                )

            return resp

        try:
            return await _retry_request()
        except RateLimitError as e:
            # Max retries exhausted
            logger.error(
                "Rate limit exhausted after max retries",
                extra={
                    "url": str(url),
                    "attempts": e.attempts,
                    "retry_after_sec": retry_after
                }
            )

            # Enhance error message with guidance
            guidance = (
                f"Rate limit exceeded after {e.attempts} retry attempts. "
            )
            if retry_after:
                guidance += f"Retry after {retry_after} seconds. "
            guidance += (
                "Consider upgrading tier or reducing request frequency. "
                "See: https://zerion.io/pricing"
            )

            raise RateLimitError(
                guidance,
                retry_after=retry_after,
                attempts=e.attempts
            )

    def _log_retry_attempt(self, retry_state: RetryCallState) -> None:
        """Log retry attempt information.

        Args:
            retry_state: Tenacity retry state
        """
        attempt_number = retry_state.attempt_number
        if retry_state.outcome and retry_state.outcome.failed:
            exception = retry_state.outcome.exception()
            logger.info(
                f"Retrying request after rate limit",
                extra={
                    "attempt": attempt_number,
                    "exception": str(exception)
                }
            )

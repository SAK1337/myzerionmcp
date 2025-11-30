#!/usr/bin/env python3
"""Pagination helpers for Zerion API responses."""

from typing import Any, Dict, List, Optional, Callable, Awaitable
import asyncio

from .logger import get_logger
from .errors import ValidationError

logger = get_logger(__name__)


async def fetch_all_pages(
    api_call: Callable[..., Awaitable[Dict[str, Any]]],
    max_pages: Optional[int] = None,
    page_size: int = 100,
    **params: Any
) -> List[Dict[str, Any]]:
    """Fetch all pages from a paginated endpoint automatically.

    This helper function fetches all pages from a Zerion API endpoint that supports
    cursor-based pagination. It follows the `links.next` URL in responses until
    no more pages exist or the safety limit is reached.

    Args:
        api_call: Async function that makes the API call. Should accept `page_size`
            and `page_after` parameters and return a dict response.
        max_pages: Maximum number of pages to fetch (safety limit). If None, uses
            default from configuration or 50.
        page_size: Number of items per page (default: 100).
        **params: Additional parameters to pass to api_call.

    Returns:
        List of all data items from all pages combined.

    Raises:
        ValidationError: If response format is invalid or missing expected fields.

    Example:
        ```python
        from zerion_mcp_server.pagination import fetch_all_pages

        # Define your API call function
        async def get_transactions(address, **kwargs):
            return await client.get(f"/wallets/{address}/transactions", params=kwargs)

        # Fetch all transactions
        all_transactions = await fetch_all_pages(
            api_call=lambda **kw: get_transactions("0x123...", **kw),
            max_pages=50,
            page_size=100
        )
        ```
    """
    # Default max pages if not specified
    if max_pages is None:
        max_pages = 50

    all_data: List[Dict[str, Any]] = []
    current_page = 1
    page_after: Optional[str] = None

    logger.info(
        "Starting auto-pagination",
        extra={
            "max_pages": max_pages,
            "page_size": page_size
        }
    )

    while current_page <= max_pages:
        # Build request parameters
        request_params = {
            **params,
            "page[size]": page_size
        }
        if page_after:
            request_params["page[after]"] = page_after

        logger.debug(
            f"Fetching page {current_page}",
            extra={
                "page": current_page,
                "has_cursor": page_after is not None
            }
        )

        # Make API call
        try:
            response = await api_call(**request_params)
        except Exception as e:
            logger.error(
                f"Error fetching page {current_page}",
                extra={"error": str(e), "page": current_page},
                exc_info=True
            )
            raise

        # Validate response structure
        if not isinstance(response, dict):
            raise ValidationError(
                f"Invalid response type: expected dict, got {type(response).__name__}",
                context={"page": current_page}
            )

        # Extract data array
        if "data" not in response:
            raise ValidationError(
                "Response missing 'data' field",
                field="data",
                context={"page": current_page}
            )

        page_data = response.get("data", [])
        if not isinstance(page_data, list):
            raise ValidationError(
                f"Invalid data type: expected list, got {type(page_data).__name__}",
                field="data",
                expected="list",
                actual=type(page_data).__name__,
                context={"page": current_page}
            )

        # Add page data to results
        items_count = len(page_data)
        all_data.extend(page_data)

        logger.debug(
            f"Fetched page {current_page}",
            extra={
                "page": current_page,
                "items_in_page": items_count,
                "total_items": len(all_data)
            }
        )

        # Check for next page
        links = response.get("links", {})
        next_url = links.get("next")

        if not next_url:
            # No more pages
            logger.info(
                "Pagination complete - no more pages",
                extra={
                    "pages_fetched": current_page,
                    "total_items": len(all_data)
                }
            )
            break

        # Extract cursor from next URL
        page_after = extract_cursor_from_url(next_url)

        # Warn at thresholds
        if current_page == 10:
            logger.warning(
                "Fetched 10 pages - quota impact may be significant",
                extra={"pages": 10, "total_items": len(all_data)}
            )
        elif current_page == 25:
            logger.warning(
                "Fetched 25 pages - high quota usage",
                extra={"pages": 25, "total_items": len(all_data)}
            )
        elif current_page == max_pages:
            logger.warning(
                "Reached max page limit - results may be incomplete",
                extra={
                    "max_pages": max_pages,
                    "total_items": len(all_data),
                    "has_more_pages": True
                }
            )
            break

        current_page += 1

    logger.info(
        "Auto-pagination finished",
        extra={
            "pages_fetched": current_page,
            "total_items": len(all_data),
            "reached_limit": current_page >= max_pages
        }
    )

    return all_data


def extract_cursor_from_url(url: str) -> Optional[str]:
    """Extract the page[after] cursor value from a pagination URL.

    Args:
        url: Pagination URL containing page[after] parameter.

    Returns:
        Cursor value or None if not found.

    Example:
        >>> extract_cursor_from_url("https://api.zerion.io/v1/wallets/.../transactions?page[after]=abc123")
        'abc123'
    """
    try:
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        # Check for page[after] parameter
        cursor = query_params.get("page[after]", [None])[0]

        if cursor:
            logger.debug(f"Extracted cursor from URL", extra={"cursor": cursor[:20] + "..."})

        return cursor

    except Exception as e:
        logger.warning(
            f"Failed to extract cursor from URL",
            extra={"url": url, "error": str(e)}
        )
        return None


async def fetch_page(
    api_call: Callable[..., Awaitable[Dict[str, Any]]],
    page_size: int = 100,
    page_after: Optional[str] = None,
    **params: Any
) -> Dict[str, Any]:
    """Fetch a single page from a paginated endpoint.

    This is a convenience wrapper that adds pagination parameters to an API call.

    Args:
        api_call: Async function that makes the API call.
        page_size: Number of items per page (default: 100).
        page_after: Cursor for next page (from previous response's links.next).
        **params: Additional parameters to pass to api_call.

    Returns:
        Response dict with data and links fields.

    Example:
        ```python
        # Fetch first page
        response = await fetch_page(
            api_call=lambda **kw: client.get("/wallets/.../transactions", params=kw),
            page_size=50
        )

        # Fetch next page using cursor
        next_cursor = extract_cursor_from_url(response["links"]["next"])
        next_response = await fetch_page(
            api_call=lambda **kw: client.get("/wallets/.../transactions", params=kw),
            page_size=50,
            page_after=next_cursor
        )
        ```
    """
    request_params = {
        **params,
        "page[size]": page_size
    }

    if page_after:
        request_params["page[after]"] = page_after

    logger.debug(
        "Fetching single page",
        extra={
            "page_size": page_size,
            "has_cursor": page_after is not None
        }
    )

    response = await api_call(**request_params)

    # Log page info
    data_count = len(response.get("data", []))
    has_next = bool(response.get("links", {}).get("next"))

    logger.debug(
        "Page fetched",
        extra={
            "items": data_count,
            "has_next_page": has_next
        }
    )

    return response

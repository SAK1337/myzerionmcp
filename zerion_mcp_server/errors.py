#!/usr/bin/env python3
"""Custom exception classes for Zerion MCP Server."""

from typing import Optional, Dict, Any


class ZerionMCPError(Exception):
    """Base exception for all Zerion MCP Server errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Initialize error with message and optional context.
        
        Args:
            message: Error message.
            context: Additional context about the error.
        """
        super().__init__(message)
        self.context = context or {}


class ConfigError(ZerionMCPError):
    """Raised when configuration is invalid or missing.
    
    Examples:
        - Missing required configuration field
        - Invalid configuration value
        - Config file not found
        - Invalid YAML syntax
    """
    pass


class NetworkError(ZerionMCPError):
    """Raised when network operations fail.
    
    Examples:
        - Connection timeout
        - DNS resolution failure
        - Connection refused
        - Network unreachable
    """
    
    def __init__(
        self,
        message: str,
        url: Optional[str] = None,
        timeout: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize network error.
        
        Args:
            message: Error message.
            url: URL that failed.
            timeout: Timeout value if applicable.
            context: Additional context.
        """
        context = context or {}
        if url:
            context["url"] = url
        if timeout:
            context["timeout_sec"] = timeout
        
        super().__init__(message, context)
        self.url = url
        self.timeout = timeout


class APIError(ZerionMCPError):
    """Raised when Zerion API returns an error.
    
    Examples:
        - 401 Unauthorized
        - 429 Rate limit exceeded
        - 500 Internal server error
        - Invalid response format
    """
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
        retry_after: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize API error.
        
        Args:
            message: Error message.
            status_code: HTTP status code.
            response_body: Response body text.
            retry_after: Retry-After header value in seconds.
            context: Additional context.
        """
        context = context or {}
        if status_code:
            context["status_code"] = status_code
        if retry_after:
            context["retry_after_sec"] = retry_after
        
        super().__init__(message, context)
        self.status_code = status_code
        self.response_body = response_body
        self.retry_after = retry_after
    
    @classmethod
    def from_response(cls, response, message: Optional[str] = None):
        """Create APIError from HTTP response.
        
        Args:
            response: httpx.Response object.
            message: Optional custom message.
            
        Returns:
            APIError instance.
        """
        status_code = response.status_code
        response_body = response.text
        
        # Try to get retry-after header
        retry_after = None
        if "retry-after" in response.headers:
            try:
                retry_after = int(response.headers["retry-after"])
            except ValueError:
                pass
        
        # Generate message based on status code
        if not message:
            if status_code == 401:
                message = (
                    "Unauthorized: Invalid or missing API key. "
                    "Check your ZERION_API_KEY environment variable."
                )
            elif status_code == 429:
                retry_msg = f" Retry after {retry_after} seconds." if retry_after else ""
                message = f"Rate limit exceeded.{retry_msg}"
            elif 500 <= status_code < 600:
                message = (
                    f"Zerion API server error (HTTP {status_code}). "
                    "This is a temporary issue. Please try again later."
                )
            else:
                message = f"API request failed with HTTP {status_code}"
        
        return cls(
            message=message,
            status_code=status_code,
            response_body=response_body,
            retry_after=retry_after
        )


class ValidationError(ZerionMCPError):
    """Raised when data validation fails.
    
    Examples:
        - Invalid JSON in response
        - Missing required field in data
        - Data type mismatch
        - Invalid OpenAPI schema
    """
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize validation error.
        
        Args:
            message: Error message.
            field: Field that failed validation.
            expected: Expected value or type.
            actual: Actual value or type.
            context: Additional context.
        """
        context = context or {}
        if field:
            context["field"] = field
        if expected:
            context["expected"] = expected
        if actual:
            context["actual"] = actual
        
        super().__init__(message, context)
        self.field = field
        self.expected = expected
        self.actual = actual

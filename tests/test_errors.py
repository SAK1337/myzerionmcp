#!/usr/bin/env python3
"""Tests for custom exception classes."""

import pytest
from unittest.mock import Mock
from zerion_mcp_server.errors import (
    ZerionMCPError,
    ConfigError,
    NetworkError,
    APIError,
    ValidationError
)


class TestZerionMCPError:
    """Test base exception class."""
    
    def test_basic_error(self):
        """Test basic error creation."""
        error = ZerionMCPError("Test error")
        
        assert str(error) == "Test error"
        assert error.context == {}
    
    def test_error_with_context(self):
        """Test error with context."""
        context = {"key": "value", "count": 42}
        error = ZerionMCPError("Test error", context=context)
        
        assert error.context == context
        assert error.context["key"] == "value"
        assert error.context["count"] == 42


class TestConfigError:
    """Test configuration error."""
    
    def test_config_error(self):
        """Test ConfigError creation."""
        error = ConfigError("Missing required field: api_key")
        
        assert "api_key" in str(error)
        assert isinstance(error, ZerionMCPError)


class TestNetworkError:
    """Test network error."""
    
    def test_basic_network_error(self):
        """Test basic NetworkError."""
        error = NetworkError("Connection failed")
        
        assert "Connection failed" in str(error)
        assert error.url is None
        assert error.timeout is None
    
    def test_network_error_with_url(self):
        """Test NetworkError with URL."""
        url = "https://api.example.com"
        error = NetworkError("Connection failed", url=url)
        
        assert error.url == url
        assert error.context["url"] == url
    
    def test_network_error_with_timeout(self):
        """Test NetworkError with timeout."""
        error = NetworkError("Timeout", url="https://example.com", timeout=30.0)
        
        assert error.timeout == 30.0
        assert error.context["timeout_sec"] == 30.0
    
    def test_network_error_with_context(self):
        """Test NetworkError with additional context."""
        context = {"suggestion": "Check your connection"}
        error = NetworkError("Failed", context=context)
        
        assert error.context["suggestion"] == "Check your connection"


class TestAPIError:
    """Test API error."""
    
    def test_basic_api_error(self):
        """Test basic APIError."""
        error = APIError("API request failed")
        
        assert "API request failed" in str(error)
        assert error.status_code is None
        assert error.response_body is None
    
    def test_api_error_with_status(self):
        """Test APIError with status code."""
        error = APIError("Request failed", status_code=404)
        
        assert error.status_code == 404
        assert error.context["status_code"] == 404
    
    def test_api_error_with_retry_after(self):
        """Test APIError with retry_after."""
        error = APIError("Rate limited", status_code=429, retry_after=60)
        
        assert error.retry_after == 60
        assert error.context["retry_after_sec"] == 60
    
    def test_from_response_401(self):
        """Test APIError.from_response for 401."""
        response = Mock()
        response.status_code = 401
        response.text = '{"error": "Unauthorized"}'
        response.headers = {}
        
        error = APIError.from_response(response)
        
        assert error.status_code == 401
        assert "api key" in str(error).lower()
    
    def test_from_response_429(self):
        """Test APIError.from_response for 429."""
        response = Mock()
        response.status_code = 429
        response.text = '{"error": "Rate limit exceeded"}'
        response.headers = {"retry-after": "120"}
        
        error = APIError.from_response(response)
        
        assert error.status_code == 429
        assert error.retry_after == 120
        assert "rate limit" in str(error).lower()
    
    def test_from_response_500(self):
        """Test APIError.from_response for 500."""
        response = Mock()
        response.status_code = 500
        response.text = '{"error": "Internal server error"}'
        response.headers = {}
        
        error = APIError.from_response(response)
        
        assert error.status_code == 500
        assert "server error" in str(error).lower()
        assert "temporary" in str(error).lower()
    
    def test_from_response_custom_message(self):
        """Test APIError.from_response with custom message."""
        response = Mock()
        response.status_code = 400
        response.text = '{"error": "Bad request"}'
        response.headers = {}
        
        custom_msg = "Custom error message"
        error = APIError.from_response(response, message=custom_msg)
        
        assert str(error) == custom_msg


class TestValidationError:
    """Test validation error."""
    
    def test_basic_validation_error(self):
        """Test basic ValidationError."""
        error = ValidationError("Invalid data")
        
        assert "Invalid data" in str(error)
        assert error.field is None
    
    def test_validation_error_with_field(self):
        """Test ValidationError with field."""
        error = ValidationError("Invalid value", field="email")
        
        assert error.field == "email"
        assert error.context["field"] == "email"
    
    def test_validation_error_with_expected_actual(self):
        """Test ValidationError with expected and actual values."""
        error = ValidationError(
            "Type mismatch",
            field="age",
            expected="integer",
            actual="string"
        )
        
        assert error.expected == "integer"
        assert error.actual == "string"
        assert error.context["expected"] == "integer"
        assert error.context["actual"] == "string"
    
    def test_validation_error_context(self):
        """Test ValidationError with additional context."""
        context = {"suggestion": "Check data format"}
        error = ValidationError("Invalid format", context=context)
        
        assert error.context["suggestion"] == "Check data format"

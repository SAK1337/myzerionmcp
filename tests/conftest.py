#!/usr/bin/env python3
"""Shared pytest fixtures for Zerion MCP Server tests."""

import pytest
import yaml
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Sample configuration for testing.
    
    Returns:
        Configuration dictionary.
    """
    return {
        "name": "Test Zerion API",
        "base_url": "https://api.zerion.io",
        "oas_url": "https://example.com/openapi.yaml",
        "api_key": "Bearer test-api-key-123",
        "logging": {
            "level": "DEBUG",
            "format": "text"
        }
    }


@pytest.fixture
def config_file(tmp_path: Path, sample_config: Dict[str, Any]) -> Path:
    """Create a temporary config file.
    
    Args:
        tmp_path: pytest temporary path fixture.
        sample_config: Sample configuration dictionary.
        
    Returns:
        Path to temporary config file.
    """
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(sample_config, f)
    return config_path


@pytest.fixture
def sample_openapi_spec() -> Dict[str, Any]:
    """Minimal OpenAPI spec for testing.
    
    Returns:
        OpenAPI specification dictionary.
    """
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Test API",
            "version": "1.0.0"
        },
        "servers": [
            {"url": "https://api.zerion.io"}
        ],
        "paths": {
            "/v1/test": {
                "get": {
                    "operationId": "getTest",
                    "summary": "Test endpoint",
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            },
            "/v1/wallets/{address}": {
                "get": {
                    "operationId": "getWallet",
                    "summary": "Get wallet",
                    "parameters": [
                        {
                            "name": "address",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            }
        }
    }


@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """Sample API response data.
    
    Returns:
        Mock API response dictionary.
    """
    return {
        "data": {
            "id": "0x1234567890abcdef",
            "type": "wallet",
            "attributes": {
                "balance": "1000.50",
                "currency": "USD"
            }
        }
    }


@pytest.fixture
def clear_env_vars(monkeypatch):
    """Clear environment variables that might interfere with tests.
    
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    env_vars = [
        "ZERION_API_KEY",
        "ZERION_BASE_URL",
        "ZERION_OAS_URL",
        "CONFIG_PATH",
        "LOG_LEVEL",
        "LOG_FORMAT"
    ]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)

#!/usr/bin/env python3
"""Integration tests for Zerion MCP Server."""

import pytest
import httpx
import respx
from unittest.mock import Mock, patch
from zerion_mcp_server.config import ConfigManager
from zerion_mcp_server.errors import NetworkError, APIError, ValidationError
import asyncio
import yaml
import uvicorn
from fastmcp import FastMCP, McpAsyncClient
from fastmcp.server.openapi import RouteMap, MCPType


@pytest.fixture
def mock_openapi_spec_yaml():
    """YAML string of mock OpenAPI spec."""
    return """
openapi: 3.0.3
info:
  title: Test API
  version: 1.0.0
servers:
  - url: https://api.zerion.io
paths:
  /v1/test:
    get:
      operationId: getTest
      summary: Test endpoint
      responses:
        '200':
          description: Success
"""


class TestServerInitialization:
    """Test server initialization flow."""
    
    @respx.mock
    def test_successful_initialization(self, monkeypatch, clear_env_vars, mock_openapi_spec_yaml):
        """Test successful server initialization."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test-key")
        
        # Mock OpenAPI spec download
        spec_url = "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"
        respx.get(spec_url).mock(return_value=httpx.Response(200, text=mock_openapi_spec_yaml))
        
        # Mock FastMCP.from_openapi to avoid actual server creation
        with patch('zerion_mcp_server.FastMCP.from_openapi') as mock_fastmcp:
            mock_server = Mock()
            mock_fastmcp.return_value = mock_server
            
            # Import and run main (will be mocked)
            from zerion_mcp_server import main
            
            # Mock the run() method to prevent blocking
            mock_server.run = Mock()
            
            # Run main function
            main()
            
            # Verify FastMCP was called
            assert mock_fastmcp.called
    
    @respx.mock
    def test_openapi_spec_timeout(self, monkeypatch, clear_env_vars, capsys):
        """Test timeout when loading OpenAPI spec."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test-key")
        
        # Mock timeout
        spec_url = "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"
        respx.get(spec_url).mock(side_effect=httpx.TimeoutException("Connection timeout"))
        
        from zerion_mcp_server import main
        
        main()
        
        captured = capsys.readouterr()
        assert "timeout" in captured.out.lower() or "error" in captured.out.lower()
    
    @respx.mock
    def test_openapi_spec_404(self, monkeypatch, clear_env_vars, capsys):
        """Test 404 when loading OpenAPI spec."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test-key")
        
        # Mock 404 response
        spec_url = "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"
        respx.get(spec_url).mock(return_value=httpx.Response(404, text="Not found"))
        
        from zerion_mcp_server import main
        
        main()
        
        captured = capsys.readouterr()
        assert "404" in captured.out or "error" in captured.out.lower()
    
    @respx.mock
    def test_invalid_yaml_spec(self, monkeypatch, clear_env_vars, capsys):
        """Test invalid YAML in OpenAPI spec."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test-key")
        
        # Mock invalid YAML
        spec_url = "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"
        respx.get(spec_url).mock(return_value=httpx.Response(200, text="invalid: yaml: [bad"))
        
        from zerion_mcp_server import main
        
        main()
        
        captured = capsys.readouterr()
        assert "yaml" in captured.out.lower() or "error" in captured.out.lower()
    
    def test_missing_api_key(self, clear_env_vars, capsys):
        """Test error when API key is missing."""
        from zerion_mcp_server import main
        
        main()
        
        captured = capsys.readouterr()
        assert "api_key" in captured.out.lower() or "configuration" in captured.out.lower()


class TestConfigurationIntegration:
    """Test configuration integration."""
    
    def test_config_from_env_vars(self, monkeypatch, clear_env_vars):
        """Test configuration loaded from environment variables."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer env-key")
        monkeypatch.setenv("ZERION_BASE_URL", "https://custom.api.com")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        
        config = ConfigManager()
        
        assert config.api_key == "Bearer env-key"
        assert config.base_url == "https://custom.api.com"
        assert config.log_level == "DEBUG"
    
    def test_config_with_file_and_env_override(self, tmp_path, monkeypatch, clear_env_vars, sample_config):
        """Test config file with environment variable override."""
        import yaml
        
        # Create config file
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(sample_config, f)
        
        # Override with env var
        monkeypatch.setenv("ZERION_API_KEY", "Bearer overridden-key")
        
        config = ConfigManager(str(config_path))
        
        # File values used
        assert config.base_url == sample_config["base_url"]
        # Env var overrides
        assert config.api_key == "Bearer overridden-key"


class TestLoggingIntegration:
    """Test logging integration."""
    
    def test_logging_setup_text_format(self, monkeypatch, clear_env_vars):
        """Test logging with text format."""
        from zerion_mcp_server.logger import setup_logging, get_logger
        
        setup_logging(level="INFO", format_type="text")
        logger = get_logger("test")
        
        # Should not raise
        logger.info("Test message")
        logger.debug("Debug message")
        logger.error("Error message")
    
    def test_logging_setup_json_format(self, monkeypatch, clear_env_vars):
        """Test logging with JSON format."""
        from zerion_mcp_server.logger import setup_logging, get_logger
        
        setup_logging(level="DEBUG", format_type="json")
        logger = get_logger("test")
        
        # Should not raise
        logger.info("Test message")
        logger.debug("Debug message")
    
    def test_sensitive_data_redaction(self, monkeypatch, clear_env_vars, capsys):
        """Test that sensitive data is redacted in logs."""
        from zerion_mcp_server.logger import setup_logging, get_logger
        
        setup_logging(level="INFO", format_type="text")
        logger = get_logger("test")
        
        # Log message with bearer token
        logger.info("Authorization: Bearer sk_test_123456789")
        
        captured = capsys.readouterr()
        # Should be redacted
        assert "REDACTED" in captured.out or "sk_test_123456789" not in captured.out


class TestErrorHandlingIntegration:
    """Test error handling integration."""
    
    def test_network_error_context(self):
        """Test NetworkError with context."""
        error = NetworkError(
            "Connection failed",
            url="https://api.example.com",
            timeout=30.0,
            context={"suggestion": "Check network"}
        )
        
        assert error.url == "https://api.example.com"
        assert error.timeout == 30.0
        assert error.context["suggestion"] == "Check network"
    
    def test_api_error_from_response(self):
        """Test APIError.from_response."""
        response = Mock()
        response.status_code = 401
        response.text = '{"error": "Unauthorized"}'
        response.headers = {}
        
        error = APIError.from_response(response)
        
        assert error.status_code == 401
        assert "api key" in str(error).lower()
    
    def test_validation_error_with_details(self):
        """Test ValidationError with field details."""
        error = ValidationError(
            "Type mismatch",
            field="age",
            expected="int",
            actual="str"
        )
        
        assert error.field == "age"
        assert error.expected == "int"
        assert error.actual == "str"


@pytest.mark.asyncio
class TestMCPTools:
    """Test MCP tool functionality."""

    @respx.mock
    async def test_list_chains_tool(self, monkeypatch, unused_tcp_port):
        """Test the listChains tool via an MCP client."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test-key")
        base_url = "https://api.zerion.io"
        port = unused_tcp_port

        # Mock the API response for listChains
        mock_chains_response = {
            "data": [
                {
                    "id": "ethereum",
                    "type": "chains",
                    "attributes": {"name": "Ethereum"}
                }
            ]
        }
        respx.get(f"{base_url}/v1/chains/").mock(return_value=httpx.Response(200, json=mock_chains_response))

        # Load the real OpenAPI spec
        with open("zerion_mcp_server/openapi_zerion.yaml", "r") as f:
            openapi_spec = yaml.safe_load(f)

        # Create a real FastMCP server
        client = httpx.AsyncClient(base_url=base_url, headers={"Authorization": "Bearer test-key"})
        mcp_server = FastMCP.from_openapi(
            openapi_spec=openapi_spec,
            client=client,
            name="TestZerionServer",
            route_maps=[RouteMap(mcp_type=MCPType.TOOL)]
        )

        # Run the server in the background
        server_config = uvicorn.Config(mcp_server, host="127.0.0.1", port=port, log_level="info")
        server = uvicorn.Server(server_config)
        server_task = asyncio.create_task(server.serve())
        await asyncio.sleep(1)  # Give server time to start

        try:
            # Connect with an MCP client
            async with McpAsyncClient.create(f"ws://127.0.0.1:{port}") as mcp_client:
                # Call the listChains tool
                response = await mcp_client.request("listChains")

                # Verify the response
                assert response["status"] == "success"
                assert len(response["data"]) == 1
                assert response["data"][0]["id"] == "ethereum"

        finally:
            # Stop the server
            server.should_exit = True
            await server_task

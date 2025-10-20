#!/usr/bin/env python3
"""Universal MCP Server for OpenAPI specifications."""

import time
import yaml
import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

from .config import ConfigManager
from .errors import ConfigError, NetworkError, APIError, ValidationError
from .logger import setup_logging, get_logger


def main():
    """Main entry point."""
    # Load configuration
    try:
        config = ConfigManager()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return
    
    # Setup logging
    setup_logging(level=config.log_level, format_type=config.log_format)
    logger = get_logger(__name__)
    
    logger.info("Starting Zerion MCP Server")
    logger.info(f"Configuration loaded", extra={
        "config_source": "config.yaml" if config.get("_config_loaded_from_file") else "defaults",
        "base_url": config.base_url,
        "log_level": config.log_level,
        "log_format": config.log_format
    })
    
    # Download OpenAPI spec (YAML format)
    logger.info(f"Loading OpenAPI specification from {config.oas_url}")
    start_time = time.time()
    
    try:
        response = httpx.get(config.oas_url, timeout=30.0)
        response.raise_for_status()
        
        spec_size = len(response.text)
        openapi_spec = yaml.safe_load(response.text)
        
        load_duration = time.time() - start_time
        logger.info("OpenAPI specification loaded successfully", extra={
            "duration_sec": round(load_duration, 2),
            "spec_size_bytes": spec_size,
            "endpoints": len(openapi_spec.get("paths", {}))
        })
        
    except httpx.TimeoutException as e:
        error = NetworkError(
            f"Timeout loading OpenAPI specification",
            url=config.oas_url,
            timeout=30.0,
            context={"suggestion": "Check your internet connection"}
        )
        logger.error(str(error), extra=error.context)
        print(f"Error: {error}")
        return
    except httpx.HTTPStatusError as e:
        error = APIError.from_response(
            e.response,
            message=f"Failed to download OpenAPI spec from {config.oas_url}"
        )
        logger.error(str(error), extra=error.context)
        print(f"Error: {error}")
        return
    except yaml.YAMLError as e:
        error = ValidationError(
            f"Invalid YAML in OpenAPI specification: {e}",
            context={"suggestion": "Check the OpenAPI spec file format"}
        )
        logger.error(str(error), extra=error.context)
        print(f"Error: {error}")
        return
    except Exception as e:
        logger.error(f"Unexpected error loading OpenAPI spec", extra={"error": str(e)}, exc_info=True)
        print(f"Error loading OpenAPI spec from {config.oas_url}: {e}")
        return
    
    # Setup headers (API key from config)
    headers = {"Authorization": config.api_key}
    logger.debug("HTTP client configured", extra={"base_url": config.base_url})
    
    # Create HTTP client
    client = httpx.AsyncClient(
        base_url=config.base_url,
        headers=headers,
        timeout=30.0
    )
    
    # Create MCP server
    try:
        logger.info("Creating MCP server from OpenAPI spec")
        mcp = FastMCP.from_openapi(
            openapi_spec=openapi_spec,
            client=client,
            name=config.name,
            route_maps=[RouteMap(mcp_type=MCPType.TOOL)]
        )
        
        # Count tools
        tool_count = len([r for r in (openapi_spec.get("paths", {}) or [])])
        logger.info("MCP server created successfully", extra={
            "server_name": config.name,
            "tools_available": tool_count
        })
        
    except Exception as e:
        logger.error("Failed to create MCP server", extra={"error": str(e)}, exc_info=True)
        print(f"Error creating MCP server: {e}")
        return
    
    # Start server
    logger.info("Server started and ready to accept requests")
    mcp.run()


if __name__ == "__main__":
    main()

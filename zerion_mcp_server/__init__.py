#!/usr/bin/env python3
"""Universal MCP Server for OpenAPI specifications."""

import os
import yaml
import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType


def main():
    """Main entry point."""
    # Zerion configuration
    config = {
        "name": "Zerion API",
        "base_url": "https://api.zerion.io",
        "oas_url": "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"
    }
    
    # Download OpenAPI spec (YAML format)
    response = httpx.get(config["oas_url"])
    openapi_spec = yaml.safe_load(response.text)
    
    # Setup headers (API key required)
    headers = {}
    api_key = os.getenv("ZERION_API_KEY")
    if not api_key:
        print("Error: ZERION_API_KEY environment variable is required")
        print("Set it as: export ZERION_API_KEY='Bearer your-api-key-here'")
        return
    
    headers["Authorization"] = api_key
    
    # Create HTTP client
    client = httpx.AsyncClient(
        base_url=config["base_url"],
        headers=headers
    )
    
    # Create MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name=config["name"],
        route_maps=[RouteMap(mcp_type=MCPType.TOOL)]
    )
    
    mcp.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the MCP server in HTTP mode for testing."""

from zerion_mcp_server import main

if __name__ == "__main__":
    print("Starting MCP server in HTTP mode on http://127.0.0.1:8000")
    print("Press Ctrl+C to stop")
    main(transport="http")
